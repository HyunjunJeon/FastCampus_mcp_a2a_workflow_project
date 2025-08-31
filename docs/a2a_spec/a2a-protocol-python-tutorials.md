# A2A Protocol Python Tutorials

## 1. Introduction

Welcome to the Agent2Agent (A2A) Python Quickstart Tutorial!

In this tutorial, you will explore a simple "echo" A2A server using the Python SDK. This will introduce you to the fundamental concepts and components of an A2A server. You will then look at a more advanced example that integrates a Large Language Model (LLM).

This hands-on guide will help you understand:

- The basic concepts behind the A2A protocol.
- How to set up a Python environment for A2A development using the SDK.
- How Agent Skills and Agent Cards describe an agent.
- How an A2A server handles tasks.
- How to interact with an A2A server using a client.
- How streaming capabilities and multi-turn interactions work.
- How an LLM can be integrated into an A2A agent.

By the end of this tutorial, you will have a functional understanding of A2A agents and a solid foundation for building or integrating A2A-compliant applications.

## Tutorial Sections

The tutorial is broken down into the following steps:

1. **[Introduction (This Page)](https://a2a-protocol.org/latest/tutorials/python/1-introduction/)**
2. **[Setup](https://a2a-protocol.org/latest/tutorials/python/2-setup/)**: Prepare your Python environment and the A2A SDK.
3. **[Agent Skills & Agent Card](https://a2a-protocol.org/latest/tutorials/python/3-agent-skills-and-card/)**: Define what your agent can do and how it describes itself.
4. **[The Agent Executor](https://a2a-protocol.org/latest/tutorials/python/4-agent-executor/)**: Understand how the agent logic is implemented.
5. **[Starting the Server](https://a2a-protocol.org/latest/tutorials/python/5-start-server/)**: Run the Helloworld A2A server.
6. **[Interacting with the Server](https://a2a-protocol.org/latest/tutorials/python/6-interact-with-server/)**: Send requests to your agent.
7. **[Streaming & Multi-Turn Interactions](https://a2a-protocol.org/latest/tutorials/python/7-streaming-and-multiturn/)**: Explore advanced capabilities with the LangGraph example.
8. **[Next Steps](https://a2a-protocol.org/latest/tutorials/python/8-next-steps/)**: Explore further possibilities with A2A.

Let's get started!

## 2. Setup Your Environment

## Prerequisites

- Python 3.10 or higher.
- Access to a terminal or command prompt.
- Git, for cloning the repository.
- A code editor (e.g., Visual Studio Code) is recommended.

## Clone the Repository

If you haven't already, clone the A2A Samples repository:

```md-code__content
git clone https://github.com/a2aproject/a2a-samples.git -b main --depth 1
cd a2a-samples

```

## Python Environment & SDK Installation

We recommend using a virtual environment for Python projects. The A2A Python SDK uses `uv` for dependency management, but you can use `pip` with `venv` as well.

1. **Create and activate a virtual environment:**

Using `venv` (standard library):

[Mac/Linux](https://a2a-protocol.org/latest/tutorials/python/2-setup/#maclinux)[Windows](https://a2a-protocol.org/latest/tutorials/python/2-setup/#windows)

```md-code__content
python -m venv .venv
source .venv/bin/activate

```

```md-code__content
python -m venv .venv
.venv\Scripts\activate

```

2. **Install needed Python dependencies along with the A2A SDK and its dependencies:**

```md-code__content
pip install -r samples/python/requirements.txt

```

## Verify Installation

After installation, you should be able to import the `a2a` package in a Python interpreter:

```md-code__content
python -c "import a2a; print('A2A SDK imported successfully')"

```

If this command runs without error and prints the success message, your environment is set up correctly.

## 3. Agent Skills & Agent Card

Before an A2A agent can do anything, it needs to define what it _can_ do (its skills) and how other agents or clients can find out about these capabilities (its Agent Card).

We'll use the `helloworld` example located in [`a2a-samples/samples/python/agents/helloworld/`](https://github.com/a2aproject/a2a-samples/tree/main/samples/python/agents/helloworld).

## Agent Skills

An **Agent Skill** describes a specific capability or function the agent can perform. It's a building block that tells clients what kinds of tasks the agent is good for.

Key attributes of an `AgentSkill` (defined in `a2a.types`):

- `id`: A unique identifier for the skill.
- `name`: A human-readable name.
- `description`: A more detailed explanation of what the skill does.
- `tags`: Keywords for categorization and discovery.
- `examples`: Sample prompts or use cases.
- `inputModes` / `outputModes`: Supported Media Types for input and output (e.g., "text/plain", "application/json").

In `__main__.py`, you can see how a skill for the Helloworld agent is defined:

```md-code__content
skill = AgentSkill(
    id='hello_world',
    name='Returns hello world',
    description='just returns hello world',
    tags=['hello world'],
    examples=['hi', 'hello world'],
)

```

This skill is very simple: it's named "Returns hello world" and primarily deals with text.

## Agent Card

The **Agent Card** is a JSON document that an A2A Server makes available, typically at a `.well-known/agent-card.json` endpoint. It's like a digital business card for the agent.

Key attributes of an `AgentCard` (defined in `a2a.types`):

- `name`, `description`, `version`: Basic identity information.
- `url`: The endpoint where the A2A service can be reached.
- `capabilities`: Specifies supported A2A features like `streaming` or `pushNotifications`.
- `defaultInputModes` / `defaultOutputModes`: Default Media Types for the agent.
- `skills`: A list of `AgentSkill` objects that the agent offers.

The `helloworld` example defines its Agent Card like this:

```md-code__content
# This will be the public-facing agent card
public_agent_card = AgentCard(
    name='Hello World Agent',
    description='Just a hello world agent',
    url='http://localhost:9999/',
    version='1.0.0',
    default_input_modes=['text'],
    default_output_modes=['text'],
    capabilities=AgentCapabilities(streaming=True),
    skills=[skill],  # Only the basic skill for the public card
    supports_authenticated_extended_card=True,
)

```

This card tells us the agent is named "Hello World Agent", runs at `http://localhost:9999/`, supports text interactions, and has the `hello_world` skill. It also indicates public authentication, meaning no specific credentials are required.

Understanding the Agent Card is crucial because it's how a client discovers an agent and learns how to interact with it.

## 4. The Agent Executor

The core logic of how an A2A agent processes requests and generates responses/events is handled by an **Agent Executor**. The A2A Python SDK provides an abstract base class `a2a.server.agent_execution.AgentExecutor` that you implement.

## `AgentExecutor` Interface

The `AgentExecutor` class defines two primary methods:

- `async def execute(self, context: RequestContext, event_queue: EventQueue)`: Handles incoming requests that expect a response or a stream of events. It processes the user's input (available via `context`) and uses the `event_queue` to send back `Message`, `Task`, `TaskStatusUpdateEvent`, or `TaskArtifactUpdateEvent` objects.
- `async def cancel(self, context: RequestContext, event_queue: EventQueue)`: Handles requests to cancel an ongoing task.

The `RequestContext` provides information about the incoming request, such as the user's message and any existing task details. The `EventQueue` is used by the executor to send events back to the client.

## Helloworld Agent Executor

Let's look at `agent_executor.py`. It defines `HelloWorldAgentExecutor`.

1. **The Agent ( `HelloWorldAgent`)**:
    This is a simple helper class that encapsulates the actual "business logic".

```md-code__content
class HelloWorldAgent:
       """Hello World Agent."""

       async def invoke(self) -> str:
           return 'Hello World'

```

It has a simple `invoke` method that returns the string "Hello World".

2. **The Executor ( `HelloWorldAgentExecutor`)**:
    This class implements the `AgentExecutor` interface.
   - **`__init__`**:

     ```md-code__content
     class HelloWorldAgentExecutor(AgentExecutor):
         """Test AgentProxy Implementation."""

         def __init__(self):
             self.agent = HelloWorldAgent()

     ```

     It instantiates the `HelloWorldAgent`.

   - **`execute`**:

     ```md-code__content
     async def execute(
         self,
         context: RequestContext,
         event_queue: EventQueue,
     ) -> None:
         result = await self.agent.invoke()
         await event_queue.enqueue_event(new_agent_text_message(result))

     ```

     When a `message/send` or `message/stream` request comes in (both are handled by `execute` in this simplified executor):
     1. It calls `self.agent.invoke()` to get the "Hello World" string.
     2. It creates an A2A `Message` object using the `new_agent_text_message` utility function.
     3. It enqueues this message onto the `event_queue`. The underlying `DefaultRequestHandler` will then process this queue to send the response(s) to the client. For a single message like this, it will result in a single response for `message/send` or a single event for `message/stream` before the stream closes.
   - **`cancel`**:
      The Helloworld example's `cancel` method simply raises an exception, indicating that cancellation is not supported for this basic agent.

     ```md-code__content
     async def cancel(
         self, context: RequestContext, event_queue: EventQueue
     ) -> None:
         raise Exception('cancel not supported')

     ```

The `AgentExecutor` acts as the bridge between the A2A protocol (managed by the request handler and server application) and your agent's specific logic. It receives context about the request and uses an event queue to communicate results or updates back.

## 5. Starting the Server

Now that we have an Agent Card and an Agent Executor, we can set up and start the A2A server.

The A2A Python SDK provides an `A2AStarletteApplication` class that simplifies running an A2A-compliant HTTP server. It uses [Starlette](https://www.starlette.io/) for the web framework and is typically run with an ASGI server like [Uvicorn](https://www.uvicorn.org/).

## Server Setup in Helloworld

Let's look at `__main__.py` again to see how the server is initialized and started.

```md-code__content
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent_executor import (
    HelloWorldAgentExecutor,  # type: ignore[import-untyped]
)

if __name__ == '__main__':
    skill = AgentSkill(
        id='hello_world',
        name='Returns hello world',
        description='just returns hello world',
        tags=['hello world'],
        examples=['hi', 'hello world'],
    )

    extended_skill = AgentSkill(
        id='super_hello_world',
        name='Returns a SUPER Hello World',
        description='A more enthusiastic greeting, only for authenticated users.',
        tags=['hello world', 'super', 'extended'],
        examples=['super hi', 'give me a super hello'],
    )

    # This will be the public-facing agent card
    public_agent_card = AgentCard(
        name='Hello World Agent',
        description='Just a hello world agent',
        url='http://localhost:9999/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],  # Only the basic skill for the public card
        supports_authenticated_extended_card=True,
    )

    # This will be the authenticated extended agent card
    # It includes the additional 'extended_skill'
    specific_extended_agent_card = public_agent_card.model_copy(
        update={
            'name': 'Hello World Agent - Extended Edition',  # Different name for clarity
            'description': 'The full-featured hello world agent for authenticated users.',
            'version': '1.0.1',  # Could even be a different version
            # Capabilities and other fields like url, default_input_modes, default_output_modes,
            # supports_authenticated_extended_card are inherited from public_agent_card unless specified here.
            'skills': [\
                skill,\
                extended_skill,\
            ],  # Both skills for the extended card
        }
    )

    request_handler = DefaultRequestHandler(
        agent_executor=HelloWorldAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler,
        extended_agent_card=specific_extended_agent_card,
    )

    uvicorn.run(server.build(), host='0.0.0.0', port=9999)

```

Let's break this down:

1. **`DefaultRequestHandler`**:
   - The SDK provides `DefaultRequestHandler`. This handler takes your `AgentExecutor` implementation (here, `HelloWorldAgentExecutor`) and a `TaskStore` (here, `InMemoryTaskStore`).
   - It routes incoming A2A RPC calls to the appropriate methods on your executor (like `execute` or `cancel`).
   - The `TaskStore` is used by the `DefaultRequestHandler` to manage the lifecycle of tasks, especially for stateful interactions, streaming, and resubscription. Even if your agent executor is simple, the handler needs a task store.
2. **`A2AStarletteApplication`**:
   - The `A2AStarletteApplication` class is instantiated with the `agent_card` and the `request_handler` (referred to as `http_handler` in its constructor).
   - The `agent_card` is crucial because the server will expose it at the `/.well-known/agent-card.json` endpoint (by default).
   - The `request_handler` is responsible for processing all incoming A2A method calls by interacting with your `AgentExecutor`.
3. **`uvicorn.run(server_app_builder.build(), ...)`**:
   - The `A2AStarletteApplication` has a `build()` method that constructs the actual Starlette application.
   - This application is then run using `uvicorn.run()`, making your agent accessible over HTTP.
   - `host='0.0.0.0'` makes the server accessible on all network interfaces on your machine.
   - `port=9999` specifies the port to listen on. This matches the `url` in the `AgentCard`.

## Running the Helloworld Server

Navigate to the `a2a-samples` directory in your terminal (if you're not already there) and ensure your virtual environment is activated.

To run the Helloworld server:

```md-code__content
# from the a2a-samples directory
python samples/python/agents/helloworld/__main__.py

```

You should see output similar to this, indicating the server is running:

```md-code__content
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9999 (Press CTRL+C to quit)

```

Your A2A Helloworld agent is now live and listening for requests! In the next step, we'll interact with it.

## 6. Interacting with the Server

With the Helloworld A2A server running, let's send some requests to it. The SDK includes a client ( `A2AClient`) that simplifies these interactions.

## The Helloworld Test Client

The `test_client.py` script demonstrates how to:

1. Fetch the Agent Card from the server.
2. Create an `A2AClient` instance.
3. Send both non-streaming ( `message/send`) and streaming ( `message/stream`) requests.

Open a **new terminal window**, activate your virtual environment, and navigate to the `a2a-samples` directory.

Activate virtual environment (Be sure to do this in the same directory where you created the virtual environment):

[Mac/Linux](https://a2a-protocol.org/latest/tutorials/python/6-interact-with-server/#maclinux)[Windows](https://a2a-protocol.org/latest/tutorials/python/6-interact-with-server/#windows)

```md-code__content
source .venv/bin/activate

```

```md-code__content
.venv\Scripts\activate

```

Run the test client:

```md-code__content
# from the a2a-samples directory
python samples/python/agents/helloworld/test_client.py

```

## Understanding the Client Code

Let's look at key parts of `test_client.py`:

1. **Fetching the Agent Card & Initializing the Client**:

```md-code__content
base_url = 'http://localhost:9999'

async with httpx.AsyncClient() as httpx_client:
       # Initialize A2ACardResolver
       resolver = A2ACardResolver(
           httpx_client=httpx_client,
           base_url=base_url,
           # agent_card_path uses default, extended_agent_card_path also uses default
       )

```

The `A2ACardResolver` class is a convenience. It first fetches the `AgentCard` from the server's `/.well-known/agent-card.json` endpoint (based on the provided base URL) and then initializes the client with it.

2. **Sending a Non-Streaming Message ( `send_message`)**:

```md-code__content
client = A2AClient(
       httpx_client=httpx_client, agent_card=final_agent_card_to_use
)
logger.info('A2AClient initialized.')

send_message_payload: dict[str, Any] = {
       'message': {
           'role': 'user',
           'parts': [\
               {'kind': 'text', 'text': 'how much is 10 USD in INR?'}\
           ],
           'messageId': uuid4().hex,
       },
}
request = SendMessageRequest(
       id=str(uuid4()), params=MessageSendParams(**send_message_payload)
)

response = await client.send_message(request)
print(response.model_dump(mode='json', exclude_none=True))

```

- The `send_message_payload` constructs the data for `MessageSendParams`.
- This is wrapped in a `SendMessageRequest`.
- It includes a `message` object with the `role` set to "user" and the content in `parts`.
- The Helloworld agent's `execute` method will enqueue a single "Hello World" message. The `DefaultRequestHandler` will retrieve this and send it as the response.
- The `response` will be a `SendMessageResponse` object, which contains either a `SendMessageSuccessResponse` (with the agent's `Message` as the result) or a `JSONRPCErrorResponse`.

3. **Handling Task IDs (Illustrative Note for Helloworld)**:

The Helloworld client ( `test_client.py`) doesn't attempt `get_task` or `cancel_task` directly because the simple Helloworld agent's `execute` method, when called via `message/send`, results in the `DefaultRequestHandler` returning a direct `Message` response rather than a `Task` object. More complex agents that explicitly manage tasks (like the LangGraph example) would return a `Task` object from `message/send`, and its `id` could then be used for `get_task` or `cancel_task`.

4. **Sending a Streaming Message ( `send_message_streaming`)**:

```md-code__content
streaming_request = SendStreamingMessageRequest(
       id=str(uuid4()), params=MessageSendParams(**send_message_payload)
)

stream_response = client.send_message_streaming(streaming_request)

async for chunk in stream_response:
       print(chunk.model_dump(mode='json', exclude_none=True))

```

- This method calls the agent's `message/stream` endpoint. The `DefaultRequestHandler` will invoke the `HelloWorldAgentExecutor.execute` method.
- The `execute` method enqueues one "Hello World" message, and then the event queue is closed.
- The client will receive this single message as one `SendStreamingMessageResponse` event, and then the stream will terminate.
- The `stream_response` is an `AsyncGenerator`.

## Expected Output

When you run `test_client.py`, you'll see JSON outputs for:

- The non-streaming response (a single "Hello World" message).
- The streaming response (a single "Hello World" message as one chunk, after which the stream ends).

The `id` fields in the output will vary with each run.

```md-code__content
// Non-streaming response
{"jsonrpc":"2.0","id":"xxxxxxxx","result":{"type":"message","role":"agent","parts":[{"type":"text","text":"Hello World"}],"messageId":"yyyyyyyy"}}
// Streaming response (one chunk)
{"jsonrpc":"2.0","id":"zzzzzzzz","result":{"type":"message","role":"agent","parts":[{"type":"text","text":"Hello World"}],"messageId":"wwwwwwww","final":true}}

```

_(Actual IDs like `xxxxxxxx`, `yyyyyyyy`, `zzzzzzzz`, `wwwwwwww` will be different UUIDs/request IDs)_

This confirms your server is correctly handling basic A2A interactions with the updated SDK structure!

Now you can shut down the server by typing Ctrl+C in the terminal window where `__main__.py` is running.

## 7. Streaming & Multi-Turn Interactions (LangGraph Example)

The Helloworld example demonstrates the basic mechanics of A2A. For more advanced features like robust streaming, task state management, and multi-turn conversations powered by an LLM, we'll turn to the LangGraph example located in [`a2a-samples/samples/python/agents/langgraph/`](https://github.com/a2aproject/a2a-samples/tree/main/samples/python/agents/langgraph).

This example features a "Currency Agent" that uses the Gemini model via LangChain and LangGraph to answer currency conversion questions.

## Setting up the LangGraph Example

1. Create a [Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key), if you don't already have one.

2. **Environment Variable:**

Create a `.env` file in the `a2a-samples/samples/python/agents/langgraph/` directory:

```md-code__content
echo "GOOGLE_API_KEY=YOUR_API_KEY_HERE" > .env

```

Replace `YOUR_API_KEY_HERE` with your actual Gemini API key.

3. **Install Dependencies (if not already covered):**

The `langgraph` example has its own `pyproject.toml` which includes dependencies like `langchain-google-genai` and `langgraph`. When you installed the SDK from the `a2a-samples` root using `pip install -e .[dev]`, this should have also installed the dependencies for the workspace examples, including `langgraph-example`. If you encounter import errors, ensure your primary SDK installation from the root directory was successful.

## Running the LangGraph Server

Navigate to the `a2a-samples/samples/python/agents/langgraph/app` directory in your terminal and ensure your virtual environment (from the SDK root) is activated.

Start the LangGraph agent server:

```md-code__content
python __main__.py

```

This will start the server, usually on `http://localhost:10000`.

## Interacting with the LangGraph Agent

Open a **new terminal window**, activate your virtual environment, and navigate to `a2a-samples/samples/python/agents/langgraph/app`.

Run its test client:

```md-code__content
python test_client.py

```

Now, you can shut down the server by typing Ctrl+C in the terminal window where `__main__.py` is running.

## Key Features Demonstrated

The `langgraph` example showcases several important A2A concepts:

1. **LLM Integration**:
   - `agent.py` defines `CurrencyAgent`. It uses `ChatGoogleGenerativeAI` and LangGraph's `create_react_agent` to process user queries.
   - This demonstrates how a real LLM can power the agent's logic.
2. **Task State Management**:
   - `samples/langgraph/__main__.py` initializes a `DefaultRequestHandler` with an `InMemoryTaskStore`.

```md-code__content
httpx_client = httpx.AsyncClient()
push_config_store = InMemoryPushNotificationConfigStore()
push_sender = BasePushNotificationSender(httpx_client=httpx_client,
                    config_store=push_config_store)
request_handler = DefaultRequestHandler(
    agent_executor=CurrencyAgentExecutor(),
    task_store=InMemoryTaskStore(),
    push_config_store=push_config_store,
    push_sender= push_sender
)
server = A2AStarletteApplication(
    agent_card=agent_card, http_handler=request_handler
)

uvicorn.run(server.build(), host=host, port=port)

```

- The `CurrencyAgentExecutor` (in `samples/langgraph/agent_executor.py`), when its `execute` method is called by the `DefaultRequestHandler`, interacts with the `RequestContext` which contains the current task (if any).

- For `message/send`, the `DefaultRequestHandler` uses the `TaskStore` to persist and retrieve task state across interactions. The response to `message/send` will be a full `Task` object if the agent's execution flow involves multiple steps or results in a persistent task.
- The `test_client.py`'s `run_single_turn_test` demonstrates getting a `Task` object back and then querying it using `get_task`.

3. **Streaming with `TaskStatusUpdateEvent` and `TaskArtifactUpdateEvent`**:
   - The `execute` method in `CurrencyAgentExecutor` is responsible for handling both non-streaming and streaming requests, orchestrated by the `DefaultRequestHandler`.
   - As the LangGraph agent processes the request (which might involve calling tools like `get_exchange_rate`), the `CurrencyAgentExecutor` enqueues different types of events onto the `EventQueue`:
     - `TaskStatusUpdateEvent`: For intermediate updates (e.g., "Looking up exchange rates...", "Processing the exchange rates.."). The `final` flag on these events is `False`.
     - `TaskArtifactUpdateEvent`: When the final answer is ready, it's enqueued as an artifact. The `lastChunk` flag is `True`.
     - A final `TaskStatusUpdateEvent` with `state=TaskState.completed` and `final=True` is sent to signify the end of the task for streaming.
   - The `test_client.py`'s `run_streaming_test` function will print these individual event chunks as they are received from the server.
4. **Multi-Turn Conversation ( `TaskState.input_required`)**:
   - The `CurrencyAgent` can ask for clarification if a query is ambiguous (e.g., user asks "how much is 100 USD?").
   - When this happens, the `CurrencyAgentExecutor` will enqueue a `TaskStatusUpdateEvent` where `status.state` is `TaskState.input_required` and `status.message` contains the agent's question (e.g., "To which currency would you like to convert?"). This event will have `final=True` for the current interaction stream.
   - The `test_client.py`'s `run_multi_turn_test` function demonstrates this:
     - It sends an initial ambiguous query.
     - The agent responds (via the `DefaultRequestHandler` processing the enqueued events) with a `Task` whose status is `input_required`.
     - The client then sends a second message, including the `taskId` and `contextId` from the first turn's `Task` response, to provide the missing information ("in GBP"). This continues the same task.

## Exploring the Code

Take some time to look through these files:

- `__main__.py`: Server setup using `A2AStarletteApplication` and `DefaultRequestHandler`. Note the `AgentCard` definition includes `capabilities.streaming=True`.
- `agent.py`: The `CurrencyAgent` with LangGraph, LLM model, and tool definitions.
- `agent_executor.py`: The `CurrencyAgentExecutor` implementing the `execute` (and `cancel`) method. It uses the `RequestContext` to understand the ongoing task and the `EventQueue` to send back various events ( `TaskStatusUpdateEvent`, `TaskArtifactUpdateEvent`, new `Task` object implicitly via the first event if no task exists).
- `test_client.py`: Demonstrates various interaction patterns, including retrieving task IDs and using them for multi-turn conversations.

This example provides a much richer illustration of how A2A facilitates complex, stateful, and asynchronous interactions between agents.

## 8. Next Steps

Congratulations on completing the A2A Python SDK Tutorial! You've learned how to:

- Set up your environment for A2A development.
- Define Agent Skills and Agent Cards using the SDK's types.
- Implement a basic HelloWorld A2A server and client.
- Understand and implement streaming capabilities.
- Integrate a more complex agent using LangGraph, demonstrating task state management and tool use.

You now have a solid foundation for building and integrating your own A2A-compliant agents.

## Where to Go From Here?

Here are some ideas and resources to continue your A2A journey:

- **Explore Other Examples:**
  - Check out the other examples in the `a2a-samples/samples/` directory in the [A2A GitHub repository](https://github.com/a2aproject/a2a-samples/tree/main/samples) for more complex agent integrations and features.
  - The main A2A repository also has [samples for other languages and frameworks](https://github.com/a2aproject/A2A/tree/main/samples).
- **Deepen Your Protocol Understanding:**
  - Read the complete [A2A Protocol Documentation site](https://google.github.io/A2A/) for a comprehensive overview.
  - Review the detailed [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/) to understand the nuances of all data structures and RPC methods.
- **Review Key A2A Topics:**
  - [A2A and MCP](https://a2a-protocol.org/latest/topics/a2a-and-mcp/): Understand how A2A complements the Model Context Protocol for tool usage.
  - [Enterprise-Ready Features](https://a2a-protocol.org/latest/topics/enterprise-ready/): Learn about security, observability, and other enterprise considerations.
  - [Streaming & Asynchronous Operations](https://a2a-protocol.org/latest/topics/streaming-and-async/): Get more details on SSE and push notifications.
  - [Agent Discovery](https://a2a-protocol.org/latest/topics/agent-discovery/): Explore different ways agents can find each other.
- **Build Your Own Agent:**
  - Try creating a new A2A agent using your favorite Python agent framework (like LangChain, CrewAI, AutoGen, Semantic Kernel, or a custom solution).
  - Implement the `a2a.server.AgentExecutor` interface to bridge your agent's logic with the A2A protocol.
  - Think about what unique skills your agent could offer and how its Agent Card would represent them.
- **Experiment with Advanced Features:**
  - Implement robust task management with a persistent `TaskStore` if your agent handles long-running or multi-session tasks.
  - Explore implementing push notifications if your agent's tasks are very long-lived.
  - Consider more complex input and output modalities (e.g., handling file uploads/downloads, or structured data via `DataPart`).
- **Contribute to the A2A Community:**
  - Join the discussions on the [A2A GitHub Discussions page](https://github.com/a2aproject/A2A/discussions).
  - Report issues or suggest improvements via [GitHub Issues](https://github.com/a2aproject/A2A/issues).
  - Consider contributing code, examples, or documentation. See the [CONTRIBUTING.md](https://github.com/a2aproject/A2A/blob/main/CONTRIBUTING.md) guide.

The A2A protocol aims to foster an ecosystem of interoperable AI agents. By building and sharing A2A-compliant agents, you can be a part of this exciting development!
