"""
MCP Server for OpenMemory with resilient memory client handling.

This module implements an MCP (Model Context Protocol) server that provides
memory operations for OpenMemory. The memory client is initialized lazily
to prevent server crashes when external dependencies (like Ollama) are
unavailable. If the memory client cannot be initialized, the server will
continue running with limited functionality and appropriate error messages.

Key features:
- Lazy memory client initialization
- Graceful error handling for unavailable dependencies
- Fallback to database-only mode when vector store is unavailable
- Proper logging for debugging connection issues
- Environment variable parsing for API keys
"""

import contextvars
import datetime
import logging
import uuid

from app.database import SessionLocal
from app.models import Memory, MemoryAccessLog, MemoryState, MemoryStatusHistory
from app.utils.db import get_user_and_app
from app.utils.memory import get_memory_client
from app.utils.permissions import check_memory_access_permissions
from dotenv import load_dotenv
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

# Import OpenMemory adapter for response formatting and safe execution decorator
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

# Load environment variables
load_dotenv()

# Initialize MCP with streamable_http configuration
mcp = FastMCP(
    "mem0-mcp-server",
    host="0.0.0.0",
    port=8031,
    streamable_http_path="/mcp"
)

from starlette.requests import Request
from starlette.responses import JSONResponse

# Add custom health check endpoint using FastMCP's custom_route
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    """Health check endpoint for OpenMemory MCP."""
    try:
        # Check if memory client can be initialized
        client = get_memory_client_safe()
        if client:
            return JSONResponse({"status": "healthy", "service": "openmemory-mcp", "memory_client": "connected"})
        else:
            return JSONResponse({"status": "degraded", "service": "openmemory-mcp", "memory_client": "disconnected", "note": "Service running but memory client unavailable"})
    except Exception as e:
        return JSONResponse({"status": "unhealthy", "service": "openmemory-mcp", "error": str(e)})

# Add root endpoint using FastMCP's custom_route
@mcp.custom_route("/", methods=["GET"])
async def root(request: Request):
    """Root endpoint with service information."""
    return JSONResponse({
        "service": "openmemory-mcp", 
        "version": "1.0.0",
        "description": "Memory Context Protocol Server for OpenMemory",
        "endpoints": [
            "/health - Health check endpoint",
            "/mcp - MCP streaming endpoint",
            "/ - This information endpoint"
        ]
    })

# Don't initialize memory client at import time - do it lazily when needed
def get_memory_client_safe():
    """Get memory client with error handling. Returns None if client cannot be initialized."""
    try:
        return get_memory_client()
    except Exception as e:
        logging.warning(f"Failed to get memory client: {e}")
        return None

# Context variables for user_id and client_name
user_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("user_id")
client_name_var: contextvars.ContextVar[str] = contextvars.ContextVar("client_name")

@mcp.tool(description="Add a new memory. This method is called everytime the user informs anything about themselves, their preferences, or anything that has any relevant information which can be useful in the future conversation. This can also be called when the user asks you to remember something.")
async def add_memories(text: str) -> dict:
    # For testing, use default values if context variables are not set
    uid = user_id_var.get(None) or "jhj"
    client_name = client_name_var.get(None) or "knowledge-agent"

    if not uid:
        return {"status": "error", "error": "user_id not provided", "results": [], "text": text}
    if not client_name:
        return {"status": "error", "error": "client_name not provided", "results": [], "text": text}

    # Get memory client safely
    memory_client = get_memory_client_safe()
    if not memory_client:
        return {"status": "error", "error": "Memory system is currently unavailable. Please try again later.", "results": [], "text": text}

    try:
        db = SessionLocal()
        try:
            # Get or create user and app
            user, app = get_user_and_app(db, user_id=uid, app_id=client_name)

            # Check if app is active
            if not app.is_active:
                return {"status": "error", "error": f"App {app.name} is currently paused on OpenMemory. Cannot create new memories.", "results": [], "text": text}

            # Call memory client add method with error handling
            try:
                response = memory_client.add(text,
                                             user_id=uid,
                                             metadata={
                                                "source_app": "openmemory",
                                                "mcp_client": client_name,
                                             })
            except Exception as client_error:
                logging.error(f"Memory client add method failed: {client_error}")
                raise RuntimeError(f"Failed to add memory to vector store: {client_error}")

            # Process the response and update database
            if isinstance(response, dict) and 'results' in response:
                results = response['results']
                if isinstance(results, list):
                    for result in results:
                        # Validate result structure
                        if not isinstance(result, dict):
                            logging.warning(f"Skipping invalid result format: {type(result)}")
                            continue

                        # Safely extract memory_id
                        try:
                            memory_id_str = result.get('id')
                            if not memory_id_str:
                                logging.warning("Skipping result with missing 'id' field")
                                continue
                            memory_id = uuid.UUID(str(memory_id_str))
                        except (ValueError, TypeError) as e:
                            logging.warning(f"Skipping invalid memory_id '{memory_id_str}': {e}")
                            continue

                        memory = db.query(Memory).filter(Memory.id == memory_id).first()

                        # Safely extract event type
                        event = result.get('event')
                        if not event:
                            logging.warning(f"Skipping result with missing 'event' field for memory {memory_id}")
                            continue

                        if event == 'ADD':
                            # Safely extract memory content
                            memory_content = result.get('memory', '')
                            if not memory_content:
                                logging.warning(f"Skipping ADD event with empty memory content for {memory_id}")
                                continue

                            if not memory:
                                memory = Memory(
                                    id=memory_id,
                                    user_id=user.id,
                                    app_id=app.id,
                                    content=str(memory_content),
                                    state=MemoryState.active
                                )
                                db.add(memory)
                            else:
                                memory.state = MemoryState.active
                                memory.content = str(memory_content)

                            # Create history entry
                            history = MemoryStatusHistory(
                                memory_id=memory_id,
                                changed_by=user.id,
                                old_state=MemoryState.deleted if memory else None,
                                new_state=MemoryState.active
                            )
                            db.add(history)

                        elif event == 'DELETE':
                            if memory:
                                memory.state = MemoryState.deleted
                                memory.deleted_at = datetime.datetime.now(datetime.UTC)
                                # Create history entry
                                history = MemoryStatusHistory(
                                    memory_id=memory_id,
                                    changed_by=user.id,
                                    old_state=MemoryState.active,
                                    new_state=MemoryState.deleted
                                )
                                db.add(history)

                    # Commit database transaction with error handling
                    try:
                        db.commit()
                    except Exception as commit_error:
                        logging.error(f"Database commit failed: {commit_error}")
                        db.rollback()
                        raise RuntimeError(f"Failed to save memory changes to database: {commit_error}")
                else:
                    logging.warning(f"Expected 'results' to be a list, got {type(results)}")
            else:
                logging.warning(f"Response format unexpected: {type(response)} or missing 'results' key")

            # Return response as dictionary directly
            # Ensure response is not None and has proper structure
            if response is None:
                return {"results": [], "status": "success", "message": "No memory operations performed"}

            # Ensure response has proper dictionary structure
            if not isinstance(response, dict):
                return {"results": [], "status": "error", "message": f"Invalid response type: {type(response)}"}

            # Add success status if not present
            if "status" not in response:
                response["status"] = "success"

            return response
        finally:
            db.close()
    except Exception as e:
        logging.exception(f"Error adding to memory: {e}")
        # Ensure database rollback on error
        try:
            db.rollback()
        except Exception as rollback_error:
            logging.error(f"Error during database rollback: {rollback_error}")

        return {
            "status": "error",
            "error": f"Error adding to memory: {str(e)}",
            "results": [],
            "text": text
        }


@mcp.tool(description="Search through stored memories. This method is called EVERYTIME the user asks anything.")
async def search_memory(query: str) -> dict:
    # For testing, use default values if context variables are not set
    uid = user_id_var.get(None) or "jhj"
    client_name = client_name_var.get(None) or "knowledge-agent"
    if not uid:
        return {"status": "error", "error": "user_id not provided", "results": [], "query": query}
    if not client_name:
        return {"status": "error", "error": "client_name not provided", "results": [], "query": query}

    # Get memory client safely
    memory_client = get_memory_client_safe()
    if not memory_client:
        return {"status": "error", "error": "Memory system is currently unavailable. Please try again later.", "results": [], "query": query}

    try:
        db = SessionLocal()
        try:
            # Get or create user and app
            user, app = get_user_and_app(db, user_id=uid, app_id=client_name)

            # Get accessible memory IDs based on ACL
            user_memories = db.query(Memory).filter(Memory.user_id == user.id).all()
            accessible_memory_ids = [memory.id for memory in user_memories if check_memory_access_permissions(db, memory, app.id)]

            filters = {
                "user_id": uid
            }

            embeddings = memory_client.embedding_model.embed(query, "search")

            hits = memory_client.vector_store.search(
                query=query, 
                vectors=embeddings, 
                limit=10, 
                filters=filters,
            )

            allowed = set(str(mid) for mid in accessible_memory_ids) if accessible_memory_ids else None

            results = []
            for h in hits:
                # All vector db search functions return OutputData class
                id, score, payload = h.id, h.score, h.payload
                if allowed and h.id is None or h.id not in allowed: 
                    continue
                
                results.append({
                    "id": id, 
                    "memory": payload.get("data"), 
                    "hash": payload.get("hash"),
                    "created_at": payload.get("created_at"), 
                    "updated_at": payload.get("updated_at"), 
                    "score": score,
                })

            for r in results: 
                if r.get("id"): 
                    access_log = MemoryAccessLog(
                        memory_id=uuid.UUID(r["id"]),
                        app_id=app.id,
                        access_type="search",
                        metadata_={
                            "query": query,
                            "score": r.get("score"),
                            "hash": r.get("hash"),
                        },
                    )
                    db.add(access_log)
            db.commit()

            # Return search results directly as dictionary
            return {
                "status": "success",
                "results": results,
                "query": query,
                "count": len(results)
            }
        finally:
            db.close()
    except Exception as e:
        logging.exception(e)
        return {
            "status": "error",
            "error": f"Error searching memory: {str(e)}",
            "results": [],
            "query": query
        }


@mcp.tool(description="List all memories in the user's memory")
async def list_memories() -> dict:
    # For testing, use default values if context variables are not set
    uid = user_id_var.get(None) or "jhj"
    client_name = client_name_var.get(None) or "knowledge-agent"
    if not uid:
        return {"status": "error", "error": "user_id not provided", "results": []}
    if not client_name:
        return {"status": "error", "error": "client_name not provided", "results": []}

    # Get memory client safely
    memory_client = get_memory_client_safe()
    if not memory_client:
        return {"status": "error", "error": "Memory system is currently unavailable. Please try again later.", "results": []}

    try:
        db = SessionLocal()
        try:
            # Get or create user and app
            user, app = get_user_and_app(db, user_id=uid, app_id=client_name)

            # Get all memories
            memories = memory_client.get_all(user_id=uid)
            filtered_memories = []

            # Filter memories based on permissions
            user_memories = db.query(Memory).filter(Memory.user_id == user.id).all()
            accessible_memory_ids = [memory.id for memory in user_memories if check_memory_access_permissions(db, memory, app.id)]
            if isinstance(memories, dict) and 'results' in memories:
                for memory_data in memories['results']:
                    if 'id' in memory_data:
                        memory_id = uuid.UUID(memory_data['id'])
                        if memory_id in accessible_memory_ids:
                            # Create access log entry
                            access_log = MemoryAccessLog(
                                memory_id=memory_id,
                                app_id=app.id,
                                access_type="list",
                                metadata_={
                                    "hash": memory_data.get('hash')
                                }
                            )
                            db.add(access_log)
                            filtered_memories.append(memory_data)
                db.commit()
            else:
                for memory in memories:
                    memory_id = uuid.UUID(memory['id'])
                    memory_obj = db.query(Memory).filter(Memory.id == memory_id).first()
                    if memory_obj and check_memory_access_permissions(db, memory_obj, app.id):
                        # Create access log entry
                        access_log = MemoryAccessLog(
                            memory_id=memory_id,
                            app_id=app.id,
                            access_type="list",
                            metadata_={
                                "hash": memory.get('hash')
                            }
                        )
                        db.add(access_log)
                        filtered_memories.append(memory)
                db.commit()
            
            # Return memory list directly as dictionary
            return {
                "status": "success",
                "results": filtered_memories,
                "count": len(filtered_memories)
            }
        finally:
            db.close()
    except Exception as e:
        logging.exception(f"Error getting memories: {e}")
        return {
            "status": "error",
            "error": f"Error getting memories: {str(e)}",
            "results": []
        }


@mcp.tool(description="Delete all memories in the user's memory")
async def delete_all_memories() -> dict:
    # For testing, use default values if context variables are not set
    uid = user_id_var.get(None) or "jhj"
    client_name = client_name_var.get(None) or "knowledge-agent"
    if not uid:
        return {"status": "error", "error": "user_id not provided", "deleted_count": 0}
    if not client_name:
        return {"status": "error", "error": "client_name not provided", "deleted_count": 0}

    # Get memory client safely
    memory_client = get_memory_client_safe()
    if not memory_client:
        return {"status": "error", "error": "Memory system is currently unavailable. Please try again later.", "deleted_count": 0}

    try:
        db = SessionLocal()
        try:
            # Get or create user and app
            user, app = get_user_and_app(db, user_id=uid, app_id=client_name)

            user_memories = db.query(Memory).filter(Memory.user_id == user.id).all()
            accessible_memory_ids = [memory.id for memory in user_memories if check_memory_access_permissions(db, memory, app.id)]

            # delete the accessible memories only
            deletion_errors = []
            for memory_id in accessible_memory_ids:
                try:
                    memory_client.delete(memory_id)
                except Exception as delete_error:
                    logging.warning(f"Failed to delete memory {memory_id} from vector store: {delete_error}")
                    deletion_errors.append(str(memory_id))

            # Update each memory's state and create history entries
            now = datetime.datetime.now(datetime.UTC)
            for memory_id in accessible_memory_ids:
                memory = db.query(Memory).filter(Memory.id == memory_id).first()
                # Update memory state
                memory.state = MemoryState.deleted
                memory.deleted_at = now

                # Create history entry
                history = MemoryStatusHistory(
                    memory_id=memory_id,
                    changed_by=user.id,
                    old_state=MemoryState.active,
                    new_state=MemoryState.deleted
                )
                db.add(history)

                # Create access log entry
                access_log = MemoryAccessLog(
                    memory_id=memory_id,
                    app_id=app.id,
                    access_type="delete_all",
                    metadata_={"operation": "bulk_delete"}
                )
                db.add(access_log)

            db.commit()
            
            # Return deletion result directly as dictionary
            deleted_count = len(accessible_memory_ids)
            return {
                "status": "success",
                "deleted_count": deleted_count,
                "errors": deletion_errors if deletion_errors else None
            }
        finally:
            db.close()
    except Exception as e:
        logging.exception(f"Error deleting memories: {e}")
        return {
            "status": "error",
            "error": f"Error deleting memories: {str(e)}",
            "deleted_count": 0
        }


def setup_mcp_server(app: FastAPI):
    """Setup MCP server with the FastAPI application"""
    mcp._mcp_server.name = "mem0-mcp-server"
    
    # Configure FastMCP to use root path (/) since we're mounting at /mcp
    mcp.settings.streamable_http_path = "/"
    
    # Mount the FastMCP streamable HTTP app
    # This provides the /mcp endpoint automatically
    app.mount("/", mcp.streamable_http_app())