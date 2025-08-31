# A2A Protocol Topics

## 1. What is A2A?

The Agent2Agent (A2A) Protocol is an open standard designed to solve a fundamental challenge in the rapidly evolving landscape of artificial intelligence: **how do AI agents, built by different teams, using different technologies, and owned by different organizations, communicate and collaborate effectively?**

As AI agents become more specialized and capable, the need for them to work together on complex tasks increases. Imagine a user asking their primary AI assistant to plan an international trip. This single request might involve coordinating the capabilities of several specialized agents:

1. An agent for flight bookings.
2. Another agent for hotel reservations.
3. A third for local tour recommendations and bookings.
4. A fourth to handle currency conversion and travel advisories.

Without a common communication protocol, integrating these diverse agents into a cohesive user experience is a significant engineering hurdle. Each integration would likely be a custom, point-to-point solution, making the system difficult to scale, maintain, and extend.

### The A2A Solution

A2A provides a standardized way for these independent, often "opaque" (black-box) agentic systems to interact. It defines:

- **A common transport and format:** JSON-RPC 2.0 over HTTP(S) for how messages are structured and transmitted.
- **Discovery mechanisms (Agent Cards):** How agents can advertise their capabilities and be found by other agents.
- **Task management workflows:** How collaborative tasks are initiated, progressed, and completed. This includes support for tasks that may be long-running or require multiple turns of interaction.
- **Support for various data modalities:** How agents exchange not just text, but also files, structured data (like forms), and potentially other rich media.
- **Core principles for security and asynchronicity:** Guidelines for secure communication and handling tasks that might take significant time or involve human-in-the-loop processes.

### Key Design Principles of A2A

The development of A2A is guided by several core principles:

- **Simplicity:** Leverage existing, well-understood standards like HTTP, JSON-RPC, and Server-Sent Events (SSE) where possible, rather than reinventing the wheel.
- **Enterprise Readiness:** Address critical enterprise needs such as authentication, authorization, security, privacy, tracing, and monitoring from the outset by aligning with standard web practices.
- **Asynchronous First:** Natively support long-running tasks and scenarios where agents or users might not be continuously connected, through mechanisms like streaming and push notifications.
- **Modality Agnostic:** Allow agents to communicate using a variety of content types, enabling rich and flexible interactions beyond plain text.
- **Opaque Execution:** Enable collaboration without requiring agents to expose their internal logic, memory, or proprietary tools. Agents interact based on declared capabilities and exchanged context, preserving intellectual property and enhancing security.

### Benefits of Using A2A

Adopting A2A can lead to significant advantages:

- **Increased Interoperability:** Break down silos between different AI agent ecosystems, allowing agents from various vendors and frameworks to work together.
- **Enhanced Agent Capabilities:** Allow developers to create more sophisticated applications by composing the strengths of multiple specialized agents.
- **Reduced Integration Complexity:** Standardize the "how" of agent communication, allowing teams to focus on the "what" – the value their agents provide.
- **Fostering Innovation:** Encourage the development of a richer ecosystem of specialized agents that can readily plug into larger collaborative workflows.
- **Future-Proofing:** Provide a flexible framework that can adapt as agent technologies continue to evolve.

By establishing common ground for agent-to-agent communication, A2A aims to accelerate the adoption and utility of AI agents across diverse industries and applications, paving the way for more powerful and collaborative AI systems.

## 2. Key Concepts in A2A

The Agent2Agent (A2A) protocol is built around a set of core concepts that define how agents interact. Understanding these concepts is crucial for developing or integrating with A2A-compliant systems.

![A2A Actors showing a User, A2A Client (Client Agent), and A2A Server (Remote Agent)](https://a2a-protocol.org/latest/assets/a2a-actors.png)

### Core Actors

- **User:** The end user (human or automated service) who initiates a request or goal that requires agent assistance.
- **A2A Client (Client Agent):** An application, service, or another AI agent that acts on behalf of the user to request actions or information from a remote agent. The client initiates communication using the A2A protocol.
- **A2A Server (Remote Agent):** An AI agent or agentic system that exposes an HTTP endpoint implementing the A2A protocol. It receives requests from clients, processes tasks, and returns results or status updates. The remote agent operates as an "opaque" system from the client's perspective, meaning the client doesn't need to know its internal workings, memory, or tools.

### Fundamental Communication Elements

- **Agent Card:**
  - A JSON metadata document, typically discoverable at a well-known URL (e.g., `/.well-known/agent-card.json`), that describes an A2A Server.
  - It details the agent's identity (name, description), service endpoint URL, version, supported A2A capabilities (like streaming or push notifications), specific skills it offers, default input/output modalities, and authentication requirements.
  - Clients use the Agent Card to discover agents and understand how to interact with them securely and effectively.
  - See details in the [Protocol Specification: Agent Card](https://a2a-protocol.org/latest/specification/#5-agent-discovery-the-agent-card).
- **Task:**
  - When a client sends a message to an agent, the agent might determine that fulfilling the request requires a stateful task to be completed (e.g., "generate a report," "book a flight," "answer a question").
  - Each task has a unique ID defined by the agent and progresses through a defined lifecycle (e.g., `submitted`, `working`, `input-required`, `completed`, `failed`).
  - Tasks are stateful and can involve multiple exchanges (messages) between the client and the server.
  - See details in the [Life of a Task](https://a2a-protocol.org/latest/topics/life-of-a-task/).
  - Protocol specification: [Task Object](https://a2a-protocol.org/latest/specification/#61-task-object).
- **Message:**
  - Represents a single turn or unit of communication between a client and an agent.
  - Messages have a `role` (either `"user"` for client-sent messages or `"agent"` for server-sent messages) and contain one or more `Part` objects that carry the actual content. `messageId` part of the Message object is a unique identifier for each message set by the sender of the message.
  - Used for conveying instructions, context, questions, answers, or status updates that are not necessarily formal `Artifacts` that are part of a `Task`.
  - See details in the [Protocol Specification: Message Object](https://a2a-protocol.org/latest/specification/#64-message-object).
- **Part:**
  - The fundamental unit of content within a `Message` or an `Artifact`. Each part has a specific `type` and can carry different kinds of data:
    - `TextPart`: Contains plain textual content.
    - `FilePart`: Represents a file, which can be transmitted as inline base64-encoded bytes or referenced via a URI. Includes metadata like filename and Media Type.
    - `DataPart`: Carries structured JSON data, useful for forms, parameters, or any machine-readable information.
  - See details in the [Protocol Specification: Part Union Type](https://a2a-protocol.org/latest/specification/#65-part-union-type).
- **Artifact:**
  - Represents a tangible output or result generated by the remote agent during the processing of a task.
  - Examples include generated documents, images, spreadsheets, structured data results, or any other self-contained piece of information that is a direct result of the task.
  - Tasks in completed state SHOULD use artifact objects for returning the generated output to the clients.
  - Artifacts are composed of one or more `Part` objects and can be streamed incrementally.
  - See details in the [Protocol Specification: Artifact Object](https://a2a-protocol.org/latest/specification/#67-artifact-object).

### Interaction Mechanisms

- **Request/Response (Polling):**
  - The client sends a request (e.g., using the `message/send` RPC method) and receives a response from the server.
  - If the interaction requires a stateful long-running task, the server might initially respond with a `working` status. The client would then periodically call `tasks/get` to poll for updates until the task reaches a terminal state (e.g., `completed`, `failed`).
- **Streaming (Server-Sent Events - SSE):**
  - For tasks that produce incremental results (like generating a long document or streaming media) or provide real-time progress updates.
  - The client initiates an interaction with the server using `message/stream`.
  - The server responds with an HTTP connection that remains open, over which it sends a stream of Server-Sent Events (SSE).
  - These events can be `Task`, `Message`, or `TaskStatusUpdateEvent` (for status changes) or `TaskArtifactUpdateEvent` (for new or updated artifact chunks).
  - This requires the server to advertise the `streaming` capability in its Agent Card.
  - Learn more about [Streaming & Asynchronous Operations](https://a2a-protocol.org/latest/topics/streaming-and-async/).
- **Push Notifications:**
  - For very long-running tasks or scenarios where maintaining a persistent connection (like SSE) is impractical.
  - The client can provide a webhook URL when initiating a task (or by calling `tasks/pushNotificationConfig/set`).
  - When the task status changes significantly (e.g., completes, fails, or requires input), the server can send an asynchronous notification (an HTTP POST request) to this client-provided webhook.
  - This requires the server to advertise the `pushNotifications` capability in its Agent Card.
  - Learn more about [Streaming & Asynchronous Operations](https://a2a-protocol.org/latest/topics/streaming-and-async/).

### Agent Response: Task or Message

See details in the [Life of a Task](https://a2a-protocol.org/latest/topics/life-of-a-task/).

### Other Important Concepts

- **Context ( `contextId`):** A server-generated identifier that can be used to logically group multiple related `Task` objects, providing context across a series of interactions.
- **Transport and Format:** A2A communication occurs over HTTP(S). JSON-RPC 2.0 is used as the payload format for all requests and responses.
- **Authentication & Authorization:** A2A relies on standard web security practices. Authentication requirements are declared in the Agent Card, and credentials (e.g., OAuth tokens, API keys) are typically passed via HTTP headers, separate from the A2A protocol messages themselves.
  - Learn more about [Enterprise-Ready Features](https://a2a-protocol.org/latest/topics/enterprise-ready/).
- **Agent Discovery:** The process by which clients find Agent Cards to learn about available A2A Servers and their capabilities.
  - Learn more about [Agent Discovery](https://a2a-protocol.org/latest/topics/agent-discovery/).
- **Extensions:** A2A allows agents to declare custom protocol extensions as part of their AgentCard.
  - More documentation coming soon.

By understanding these core components and mechanisms, developers can effectively design, implement, and utilize A2A for building interoperable and collaborative AI agent systems.

## 3. Life of a Task

When a message is sent to an agent, it can choose to reply with either:

- A stateless `Message`.
- A stateful `Task` followed by zero or more `TaskStatusUpdateEvent` or `TaskArtifactUpdateEvent`.

If the response is a `Message`, the interaction is completed. On the other hand, if the response is a `Task`, then the task will be processed by the agent, until it is in a interrupted state ( `input-required` or `auth-required`) or a terminal state ( `completed`, `cancelled`, `rejected` or `failed`).

### Context

A `contextId` logically composes many `Task` objects and independent `Message` objects. If the A2A agent uses an LLM internally, it can utilize the `contextId` to manage the LLM context.

For the first message, the agent responds with a server-generated `contextId`. If the agent creates a task, it will also include a server-generated `taskId`. Subsequent client messages can include the same `contextId` to continue the interaction, and optionally the `taskId` to continue a specific task.

`contextId` allows collaboration over a goal or share a single contextual session across multiple tasks.

### Agent: Message or a Task

Messages can be used for trivial interactions which do not require long-running processing or collaboration. An agent can use messages to negotiate the acceptance of a task. Once an agent maps the intent of an incoming message to a supported capability, it can reply back with a `Task`.

So conceptually there can be three levels of agents:

1. An agent which always responds with `Message` objects only. Doesn't do complex state management, no long running execution and uses contextID to tie messages together. Agent most probably directly wraps around an LLM invocation and simple tools.
2. Generates a `Task`, does more substantial work that can be tracked and runs over extended life time.
3. Generates both `Message` and `Task` objects. Uses messages to negotiate agent capability and scope of work for a task. Then sends `Task` object to track its execution and collaborate over task states like more input-needed, error handling, etc.

An agent can choose to always reply back with `Task` objects and model simple responses as tasks in `completed` state.

### Task Refinements & Follow-ups

Clients may want to follow up with new asks based on the results of a task, and/or refine upon the task results. This can be modeled by starting another interaction using the same `contextId` as the original task. Clients can further hint the agent by providing the reference to the original task using `referenceTaskIds` in `Message` object. Agent would then respond with either a new `Task` or a `Message`.

Once a task has reached a terminal state ( `completed`, `cancelled`, `rejected` or `failed`), it can't be restarted. There are some benefits to this:

- **Task Immutability**: Clients can reliably reference tasks and their associated state, artifacts, and messages.
  - This provides a clean mapping of inputs to outputs.
  - Useful for mapping client orchestrator to task execution.
- **Clear Unit of Work**: Every new request, refinement, or a follow-up becomes a distinct task, simplifying bookkeeping and allowing for granular tracking of an agent's work.
  - Each artifact can be traced to a unit task.
  - This unit of work can be referenced much more granularly by parent agents or other systems like agent optimizers. In case of restartable tasks, all the subsequent refinements are combined, and any reference to an interaction would need to resort to some kind of message index range.
- **Easier Implementation**: No ambiguity for agent developers, whether to create a new task or restart an existing task. Once a task is in terminal state, any related subsequent interaction would need to be within a new task.

### Parallel Follow-ups

Parallel work is supported by having agents create distinct, parallel tasks for each follow-up message sent within the same contextId. This allows clients to track individual tasks and create new dependent tasks as soon as a prerequisite task is complete.

For example:

```md-code__content
Task 1: Book a flight to Helsinki.
(After Task 1 finishes)
Task 2: Based on Task 1, book a hotel.
Task 3: Based on Task 1, book a snowmobile activity.
(After Task 2 finishes, while Task 3 is still in progress)
Task 4: Based on Task 2, add a spa reservation to the hotel booking.

```

### Referencing Previous Artifacts

The serving agent is responsible for inferring the relevant artifact from the referenced task or from the `contextId`. The serving agent, as the domain expert, is best suited to resolve ambiguity or identify missing information because they are the ones who generated the artifacts.

If there is ambiguity (e.g., multiple artifacts could fit the request), the agent will ask the client for clarification by returning an input-required state. The client can then specify the artifact in its response. Client can optionally populate artifact reference {artifactId, taskId} in part metadata. This allows for linkage between inputs for follow-up tasks and previously generated artifacts.

This approach allows for the client implementation to be simple.

### Tracking Artifact Mutation

A follow up or refinement can result in an older artifact being modified and newer artifacts being generated. It would be good to know this linkage and maybe track all mutations of the artifact to make sure only the latest copy is used for future context. Something like a linked list, with the head as the latest version of the task result.

But the client is best suited, as well as is the real judge of what it considers as an acceptable result. And in fact can reject the mutation as well. Hence, the serving agent should not own this linkage and hence this linkage does not need to be part of A2A protocol spec. Clients can maintain the linkage on their end and show the latest version to the user.

To help with the tracking, the serving agent should maintain the same artifact-name when generating a refinement on the original artifact.

For follow-up or refinement tasks, the client is best suited to refer to the "latest" or what it considers to be the intended artifact to be refined upon. If the artifact reference is not explicitly specified, the serving agent can:

- Use context to figure out the latest artifact.
- Or in case of ambiguity or context not supported, agent can use `input-required` task state.

### Example Follow-up

#### Client sends message to agent

```md-code__content
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [\
        {\
          "kind": "text",\
          "text": "Generate an image of a sailboat on the ocean."\
        }\
      ],
      "messageId": "msg-user-001"
    }
  }
}

```

#### Agent responds with boat image

```md-code__content
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "result": {
    "id": "task-boat-gen-123",
    "contextId": "ctx-conversation-abc",
    "status": {
      "state": "completed",
    },
    "artifacts": [\
      {\
        "artifactId": "artifact-boat-v1-xyz",\
        "name": "sailboat_image.png",\
        "description": "A generated image of a sailboat on the ocean.",\
        "parts": [\
          {\
            "kind": "file",\
            "file": {\
              "name": "sailboat_image.png",\
              "mimeType": "image/png",\
              "bytes": "<base64_encoded_png_data_of_a_sailboat>"\
            }\
          }\
        ]\
      }\
    ],
    "kind": "task"
  }
}

```

#### Client asks for coloring the boat red

Refers to previous taskID and uses same contextId.

```md-code__content
{
  "jsonrpc": "2.0",
  "id": "req-002",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "messageId": "msg-user-002",
      "contextId": "ctx-conversation-abc", // Same contextId
      "referenceTaskIds": ["task-boat-gen-123"] // Optional: Referencing the previous task
      "parts": [\
        {\
          "kind": "text",\
          "text": "That's great! Can you make the sailboat red?"\
          // Optional: In case the agent asked for actual relevant artifact.\
          // Client could provide the artifact data in parts.\
          // Also it could add metadata to the part to\
          // reference the specific artifact.\
          // "metadata": {\
          //   "referenceArtifacts: [\
          //      {\
          //        "artifactId": "artifact-boat-v1-xyz",\
          //        "taskId": "task-boat-gen-123"\
          //      }\
          //   ]\
          // }\
        }\
      ],
    }
  }
}

```

#### Agent responds with new image artifact

- Creates new task in same contextId.
- Boat image artifact has same name. but a new artifactId.

```md-code__content
{
  "jsonrpc": "2.0",
  "id": "req-002",
  "result": {
    "id": "task-boat-color-456", // New task ID
    "contextId": "ctx-conversation-abc", // Same contextId
    "status": {
      "state": "completed",
    },
    "artifacts": [\
      {\
        "artifactId": "artifact-boat-v2-red-pqr", // New artifactId\
        "name": "sailboat_image.png", // Same name as the original artifact\
        "description": "A generated image of a red sailboat on the ocean.",\
        "parts": [\
          {\
            "kind": "file",\
            "file": {\
              "name": "sailboat_image.png",\
              "mimeType": "image/png",\
              "bytes": "<base64_encoded_png_data_of_a_RED_sailboat>"\
            }\
          }\
        ]\
      }\
    ],
    "kind": "task"
  }
}

```

## 4. Agent Discovery in A2A

For AI agents to collaborate using the Agent2Agent (A2A) protocol, they first need to find each other and understand what capabilities the other agents offer. A2A standardizes the format of an agent's self-description through the **[Agent Card](https://a2a-protocol.org/latest/specification/#5-agent-discovery-the-agent-card)**. However, the methods for discovering these Agent Cards can vary depending on the environment and requirements.

### The Role of the Agent Card

The Agent Card is a JSON document that serves as a digital "business card" for an A2A Server (the remote agent). It is crucial for discovery and initiating interaction. Key information typically included in an Agent Card:

- **Identity:** `name`, `description`, `provider` information.
- **Service Endpoint:** The `url` where the A2A service can be reached.
- **A2A Capabilities:** Supported protocol features like `streaming` or `pushNotifications`.
- **Authentication:** Required authentication `schemes` (e.g., "Bearer", "OAuth2") to interact with the agent.
- **Skills:** A list of specific tasks or functions the agent can perform ( `AgentSkill` objects), including their `id`, `name`, `description`, `inputModes`, `outputModes`, and `examples`.

Client agents parse the Agent Card to determine if a remote agent is suitable for a given task, how to structure requests for its skills, and how to communicate with it securely.

### Discovery Strategies

Here are common strategies for how a client agent might discover the Agent Card of a remote agent:

#### 1\. Well-Known URI

This is a recommended approach for public agents or agents intended for broad discoverability within a specific domain.

- **Mechanism:** A2A Servers host their Agent Card at a standardized, "well-known" path on their domain.
- **Standard Path:** `https://{agent-server-domain}/.well-known/agent-card.json` (following the principles of [RFC 8615](https://www.ietf.org/rfc/rfc8615.txt) for well-known URIs).
- **Process:**
1. A client agent knows or programmatically discovers the domain of a potential A2A Server (e.g., `smart-thermostat.example.com`).
2. The client performs an HTTP `GET` request to `https://smart-thermostat.example.com/.well-known/agent-card.json`.
3. If the Agent Card exists and is accessible, the server returns it as a JSON response.
- **Advantages:** Simple, standardized, and enables automated discovery by crawlers or systems that can resolve domains. Effectively reduces the discovery problem to "find the agent's domain."
- **Considerations:** Best suited for agents intended for open discovery or discovery within an organization that controls the domain. The endpoint serving the Agent Card may itself require authentication if the card contains sensitive information.

#### 2\. Curated Registries (Catalog-Based Discovery)

For enterprise environments, marketplaces, or specialized ecosystems, Agent Cards can be published to and discovered via a central registry or catalog.

- **Mechanism:** An intermediary service (the registry) maintains a collection of Agent Cards. Clients query this registry's API to find agents based on various criteria (e.g., skills offered, tags, provider name, desired capabilities).
- **Process:**
1. A2A Servers (or their administrators) register their Agent Cards with the registry service. The mechanism for this registration is outside the scope of the A2A protocol itself.
2. Client agents query the registry's API (e.g., "find agents with 'image-generation' skill that support streaming").
3. The registry returns a list of matching Agent Cards or references to them.
- **Advantages:**
  - Centralized management, curation, and governance of available agents.
  - Facilitates discovery based on functional capabilities rather than just domain names.
  - Enables scenarios like company-specific or team-specific agent catalogs, or public marketplaces of A2A-compliant agents.
  - Can implement access controls, policies, and trust mechanisms at the registry level.
- **Considerations:** Requires an additional registry service. The A2A protocol does not currently define a standard API for such registries, though this is an area of potential future exploration and community standardization.

#### 3\. Direct Configuration / Private Discovery

In many scenarios, especially within tightly coupled systems, for private agents, or during development and testing, clients might be directly configured with Agent Card information or a URL to fetch it.

- **Mechanism:** The client application has hardcoded Agent Card details, reads them from a local configuration file, receives them through an environment variable, or fetches them from a private, proprietary API endpoint known to the client.
- **Process:** This is highly specific to the application's deployment and configuration strategy.
- **Advantages:** Simple and effective for known, static relationships between agents or when dynamic discovery is not a requirement.
- **Considerations:** Less flexible for discovering new or updated agents dynamically. Changes to the remote agent's card might require re-configuration of the client. Proprietary API-based discovery is not standardized by A2A.

### Securing Agent Cards

Agent Cards themselves can sometimes contain information that should be protected, such as:

- The `url` of an internal-only or restricted-access agent.
- Details in the `authentication.credentials` field if it's used for scheme-specific, non-secret information (e.g., an OAuth token URL). Storing actual plaintext secrets in an Agent Card is **strongly discouraged**.
- Descriptions of sensitive or internal skills.

**Protection Mechanisms:**

- **Access Control on the Endpoint:** The HTTP endpoint serving the Agent Card (whether it's the `/.well-known/agent-card.json` path, a registry API, or a custom URL) should be secured using standard web practices if the card is not intended for public, unauthenticated access.
  - **mTLS:** Require mutual TLS for client authentication if appropriate for the trust model.
  - **Network Restrictions:** Limit access to specific IP ranges, VPCs, or private networks.
  - **Authentication:** Require standard HTTP authentication (e.g., OAuth 2.0 Bearer token, API Key) to access the Agent Card itself.
- **Selective Disclosure by Registries:** Agent registries can implement logic to return different Agent Cards or varying levels of detail based on the authenticated client's identity and permissions. For example, a public query might return a limited card, while an authenticated partner query might receive a card with more details.

It's crucial to remember that if an Agent Card were to contain sensitive data (again, **not recommended** for secrets), the card itself **must never** be available without strong authentication and authorization. The A2A protocol encourages authentication schemes where the client obtains dynamic credentials out-of-band, rather than relying on static secrets embedded in the Agent Card.

### Future Considerations

The A2A community may explore standardizing aspects of registry interactions or more advanced, semantic discovery protocols in the future. Feedback and contributions in this area are welcome to enhance the discoverability and interoperability of A2A agents.

## 5. A2A and MCP: Complementary Protocols for Agentic Systems

### A2A ❤️ MCP

In the landscape of AI agent development, two key types of protocols are emerging to facilitate interoperability: those for connecting agents to **tools and resources**, and those for enabling **agent-to-agent collaboration**. The Agent2Agent (A2A) Protocol and the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) address these distinct but related needs.

**TL;DR;** Agentic applications need both A2A and MCP. We recommend MCP for tools and A2A for agents.

### Why Different Protocols?

The distinction arises from the nature of what an agent interacts with:

- **Tools & Resources:**
  - These are typically primitives with well-defined, structured inputs and outputs. They perform specific, often stateless, functions (e.g., a calculator, a database query API, a weather lookup service).
  - Their behavior is generally predictable and transactional.
  - Interaction is often a single request-response cycle.
- **Agents:**
  - These are more autonomous systems. They can reason, plan, use multiple tools, maintain state over longer interactions, and engage in complex, often multi-turn dialogues to achieve novel or evolving tasks.
  - Their behavior can be emergent and less predictable than a simple tool.
  - Interaction often involves ongoing tasks, context sharing, and negotiation.

Agentic applications need to leverage both: agents use tools to gather information and perform actions, and agents collaborate with other agents to tackle broader, more complex goals.

### Model Context Protocol (MCP)

- **Focus:** MCP standardizes how AI models and agents connect to and interact with **tools, APIs, data sources, and other external resources.**
- **Mechanism:** It defines a structured way to describe tool capabilities (akin to function calling in Large Language Models), pass inputs to them, and receive structured outputs.
- **Use Cases:**
  - Enabling an LLM to call an external API (e.g., fetch current stock prices).
  - Allowing an agent to query a database with specific parameters.
  - Connecting an agent to a set of predefined functions or services.
- **Ecosystem:** MCP aims to create an ecosystem where tool providers can easily expose their services to various AI models and agent frameworks, and agent developers can easily consume these tools in a standardized way.

### Agent2Agent Protocol (A2A)

- **Focus:** A2A standardizes how independent, often opaque, **AI agents communicate and collaborate with each other as peers.**
- **Mechanism:** It provides an application-level protocol for agents to:
  - Discover each other's high-level skills and capabilities (via Agent Cards).
  - Negotiate interaction modalities (text, files, structured data).
  - Manage shared, stateful, and potentially long-running tasks.
  - Exchange conversational context, instructions, and complex, multi-part results.
- **Use Cases:**
  - A customer service agent delegating a complex billing inquiry to a specialized billing agent, maintaining context of the customer interaction.
  - A travel planning agent coordinating with separate flight, hotel, and activity booking agents, managing a multi-stage booking process.
  - Agents exchanging information and status updates for a collaborative project that evolves over time.
- **Key Difference from Tool Interaction:** A2A allows for more dynamic, stateful, and potentially multi-modal interactions than typically seen with simple tool calls. Agents using A2A communicate _as agents_ (or on behalf of users) rather than just invoking a discrete function.

### How A2A and MCP Complement Each Other

A2A and MCP are not mutually exclusive; they are highly complementary and address different layers of an agentic system's interaction needs.

![Diagram showing A2A and MCP working together. A User interacts with Agent A via A2A. Agent A interacts with Agent B via A2A. Agent B uses MCP to interact with Tool 1 and Tool 2.](https://a2a-protocol.org/latest/assets/a2a-mcp.png)

_An agentic application might use A2A to communicate with other agents, while each agent internally uses MCP to interact with its specific tools and resources._

#### Example Scenario: The Auto Repair Shop

> Consider an auto repair shop staffed by autonomous AI agent "mechanics" who use special-purpose tools (such as vehicle jacks, multimeters, and socket wrenches) to diagnose and repair problems. The workers often have to diagnose and repair problems they have not seen before. The repair process can involve extensive conversations with a customer, research, and working with part suppliers.

1. **Customer Interaction (User-to-Agent via A2A):**
   - A customer (or their primary assistant agent) uses A2A to communicate with the "Shop Manager" agent: _"My car is making a rattling noise."_
   - The Shop Manager agent uses A2A for a multi-turn diagnostic conversation: _"Can you send a video of the noise?"_, _"I see some fluid leaking. How long has this been happening?"_
2. **Internal Tool Usage (Agent-to-Tool via MCP):**
   - The Mechanic agent, assigned the task by the Shop Manager, needs to diagnose the issue. It uses MCP to interact with its specialized tools:
     - MCP call to a "Vehicle Diagnostic Scanner" tool: `scan_vehicle_for_error_codes(vehicle_id='XYZ123')`.
     - MCP call to a "Repair Manual Database" tool: `get_repair_procedure(error_code='P0300', vehicle_make='Toyota', vehicle_model='Camry')`.
     - MCP call to a "Platform Lift" tool: `raise_platform(height_meters=2)`.
3. **Supplier Interaction (Agent-to-Agent via A2A):**
   - The Mechanic agent determines a specific part is needed. It uses A2A to communicate with a "Parts Supplier" agent: _"Do you have part #12345 in stock for a Toyota Camry 2018?"_
   - The Parts Supplier agent, also an A2A-compliant system, responds, potentially leading to an order.

In this example:

- **A2A** facilitates the higher-level, conversational, and task-oriented interactions between the customer and the shop, and between the shop's agents and external supplier agents.
- **MCP** enables the mechanic agent to use its specific, structured tools to perform its diagnostic and repair functions.

### Representing A2A Agents as MCP Resources

It's conceivable that an A2A Server (a remote agent) could also expose some of its skills as MCP-compatible resources, especially if those skills are well-defined and can be invoked in a more tool-like, stateless manner. In such a case, another agent might "discover" this A2A agent's specific skill via an MCP-style tool description (perhaps derived from its Agent Card).

However, the primary strength of A2A lies in its support for more flexible, stateful, and collaborative interactions that go beyond typical tool invocation. A2A is about agents _partnering_ on tasks, while MCP is more about agents _using_ capabilities.

By leveraging both A2A for inter-agent collaboration and MCP for tool integration, developers can build more powerful, flexible, and interoperable AI systems.

## 6. Streaming & Asynchronous Operations in A2A

The Agent2Agent (A2A) protocol is designed to handle tasks that may not complete immediately. Many AI-driven operations can be long-running, involve multiple steps, produce incremental results, or require human intervention. A2A provides robust mechanisms for managing such asynchronous interactions, ensuring that clients can receive updates effectively, whether they remain continuously connected or operate in a more disconnected fashion.

### 1\. Streaming with Server-Sent Events (SSE)

For tasks that produce incremental results (like generating a long document or streaming media) or provide ongoing status updates, A2A supports real-time communication using Server-Sent Events (SSE). This is ideal when the client can maintain an active HTTP connection with the A2A Server.

**Key Characteristics:**

- **Initiation:** The client uses the `message/stream` RPC method to send an initial message (e.g., a prompt or command) and simultaneously subscribe to updates for that task.
- **Server Capability:** The A2A Server must indicate its support for streaming by setting `capabilities.streaming: true` in its [Agent Card](https://a2a-protocol.org/latest/specification/#552-agentcapabilities-object).
- **Server Response (Connection):** If the subscription is successful, the server responds with an HTTP `200 OK` status and a `Content-Type: text/event-stream`. This HTTP connection remains open for the server to push events.
- **Event Structure:** The server sends events over this stream. Each event's `data` field contains a JSON-RPC 2.0 Response object, specifically a [`SendStreamingMessageResponse`](https://a2a-protocol.org/latest/specification/#721-sendstreamingmessageresponse-object). The `id` in this JSON-RPC response matches the `id` from the client's original `message/stream` request.
- **Event Types (within `SendStreamingMessageResponse.result`):**
  - [`Task`](https://a2a-protocol.org/latest/specification/#61-task-object): Represents the stateful unit of work being processed by the A2A Server for an A2A Client.
  - [`TaskStatusUpdateEvent`](https://a2a-protocol.org/latest/specification/#722-taskstatusupdateevent-object): Communicates changes in the task's lifecycle state (e.g., from `working` to `input-required` or `completed`). It can also provide intermediate messages from the agent (e.g., "I'm currently analyzing the data...").
  - [`TaskArtifactUpdateEvent`](https://a2a-protocol.org/latest/specification/#723-taskartifactupdateevent-object): Delivers new or updated [Artifacts](https://a2a-protocol.org/latest/specification/#67-artifact-object) generated by the task. This is used to stream large files or data structures in chunks. This object itself contains fields like `append`, and `lastChunk` to help the client reassemble the complete artifact.
- **Stream Termination:** The server signals the end of updates for a particular interaction cycle (i.e., for the current `message/stream` request) by setting `final: true` in a `TaskStatusUpdateEvent`. This typically occurs when the task reaches a terminal state ( `completed`, `failed`, `canceled`) or an `input-required` state (where the server expects further input from the client). After sending a `final: true` event, the server usually closes the SSE connection for that specific request.
- **Resubscription:** If a client's SSE connection breaks prematurely while a task is still active (and the server hasn't sent a `final: true` event for that phase), the client can attempt to reconnect to the stream using the `tasks/resubscribe` RPC method. The server's behavior regarding missed events during the disconnection period (e.g., whether it backfills or only sends new updates) is implementation-dependent.

**When to Use Streaming:**

- Real-time progress monitoring of long-running tasks.
- Receiving large results (artifacts) incrementally, allowing processing to begin before the entire result is available.
- Interactive, conversational exchanges where immediate feedback or partial responses are beneficial.
- Applications requiring low-latency updates from the agent.

Refer to the Protocol Specification for detailed structures:

- [`message/stream`](https://a2a-protocol.org/latest/specification/#72-messagestream)
- [`tasks/resubscribe`](https://a2a-protocol.org/latest/specification/#79-tasksresubscribe)

### 2\. Push Notifications for Disconnected Scenarios

For very long-running tasks (e.g., lasting minutes, hours, or even days) or when clients cannot or prefer not to maintain persistent connections (like mobile clients or serverless functions), A2A supports asynchronous updates via push notifications. This mechanism allows the A2A Server to actively notify a client-provided webhook when a significant task update occurs.

**Key Characteristics:**

- **Server Capability:** The A2A Server must indicate its support for this feature by setting `capabilities.pushNotifications: true` in its [Agent Card](https://a2a-protocol.org/latest/specification/#552-agentcapabilities-object).
- **Configuration:** The client provides a [`PushNotificationConfig`](https://a2a-protocol.org/latest/specification/#68-pushnotificationconfig-object) to the server.
  - This configuration can be supplied:
    - Within the initial `message/send` or `message/stream` request (via the optional `pushNotification` parameter in `TaskSendParams`).
    - Separately, using the `tasks/pushNotificationConfig/set` RPC method for an existing task.
  - The `PushNotificationConfig` includes:
    - `url`: The absolute HTTPS webhook URL where the A2A Server should send (POST) task update notifications.
    - `token` (optional): A client-generated opaque string (e.g., a secret or task-specific identifier). The server SHOULD include this token in the notification request (e.g., in a custom header like `X-A2A-Notification-Token`) for validation by the client's webhook receiver.
    - `authentication` (optional): An [`AuthenticationInfo`](https://a2a-protocol.org/latest/specification/#69-pushnotificationauthenticationinfo-object) object specifying how the A2A Server should authenticate itself _to the client's webhook URL_. The client (receiver of the webhook) defines these authentication requirements.
- **Notification Trigger:** The A2A Server decides when to send a push notification. Typically, this happens when a task reaches a significant state change, such as transitioning to a terminal state ( `completed`, `failed`, `canceled`, `rejected`) or an `input-required` or `auth-required` state, particularly after its associated message and artifacts are fully generated and stable.

- **Notification Payload:** The A2A protocol itself does **not** strictly define the HTTP body payload of the push notification sent by the server to the client's webhook. However, the notification **SHOULD** contain sufficient information for the client to identify the `Task ID` and understand the general nature of the update (e.g., the new `TaskState`). Servers might send a minimal payload (just `Task ID` and new state) or a more comprehensive one (e.g., a summary or even the full [`Task`](https://a2a-protocol.org/latest/specification/#61-task-object) object).
- **Client Action:** Upon receiving a push notification (and successfully verifying its authenticity and relevance), the client typically uses the `tasks/get` RPC method with the `task ID` from the notification to retrieve the complete, updated `Task` object, including any new artifacts or detailed messages.

**The Push Notification Service (Client-Side Webhook Infrastructure):**

- The target `url` specified in `PushNotificationConfig.url` points to a **Push Notification Service**. This service is a component on the client's side (or a service the client subscribes to) responsible for receiving the HTTP POST notification from the A2A Server.
- Its responsibilities include:
  - Authenticating the incoming notification (i.e., verifying it's from the legitimate A2A Server).
  - Validating the notification's relevance (e.g., checking the `token`).
  - Relaying the notification or its content to the appropriate client application logic or system.
- In simple scenarios (e.g., local development), the client application itself might directly expose the webhook endpoint.
- In enterprise or production settings, this is often a robust, secure service that handles incoming webhooks, authenticates callers, and routes messages (e.g., to a message queue, an internal API, a mobile push notification gateway, or another event-driven system).

### Security Considerations for Push Notifications

Security is paramount for push notifications due to their asynchronous and server-initiated outbound nature. Both the A2A Server (sending the notification) and the client's webhook receiver have responsibilities.

#### A2A Server Security (When Sending Notifications to Client Webhook)

1. **Webhook URL Validation:**
   - Servers **SHOULD NOT** blindly trust and send POST requests to any `url` provided by a client in `PushNotificationConfig`. Malicious clients could provide URLs pointing to internal services or unrelated third-party systems to cause harm (Server-Side Request Forgery - SSRF attacks) or act as Distributed Denial of Service (DDoS) amplifiers.
   - **Mitigation Strategies:**
     - **Allowlisting:** Maintain an allowlist of trusted domains or IP ranges for webhook URLs, if feasible.
     - **Ownership Verification / Challenge-Response:** Before sending actual notifications, the server can (and SHOULD ideally) perform a verification step. For example, it could issue an HTTP `GET` or `OPTIONS` request to the proposed webhook URL with a unique `validationToken` (as a query parameter or header). The webhook service must respond appropriately (e.g., echo back the token or confirm readiness) to prove ownership and reachability. The [A2A Python samples](https://github.com/a2aproject/a2a-samples) demonstrate a simple validation token check mechanism.
     - **Network Controls:** Use egress firewalls or network policies to restrict where the A2A Server can send outbound HTTP requests.
2. **Authenticating to the Client's Webhook:**
   - The A2A Server **MUST** authenticate itself to the client's webhook URL according to the scheme(s) specified in `PushNotificationConfig.authentication`.
   - Common authentication schemes for server-to-server webhooks include:
     - **Bearer Tokens (OAuth 2.0):** The A2A Server obtains an access token (e.g., using the OAuth 2.0 client credentials grant flow if the webhook provider supports it) for an audience/scope representing the client's webhook, and includes it in the `Authorization: Bearer <token>` header of the notification POST request.
     - **API Keys:** A pre-shared API key that the A2A Server includes in a specific HTTP header (e.g., `X-Api-Key`).
     - **HMAC Signatures:** The A2A Server signs the request payload (or parts of the request) with a shared secret key using HMAC, and includes the signature in a header (e.g., `X-Hub-Signature`). The webhook receiver then verifies this signature.
     - **Mutual TLS (mTLS):** If supported by the client's webhook infrastructure, the A2A Server can present a client TLS certificate.

#### Client Webhook Receiver Security (When Receiving Notifications from A2A Server)

1. **Authenticating the A2A Server:**
   - The webhook endpoint **MUST** rigorously verify the authenticity of incoming notification requests to ensure they originate from the legitimate A2A Server and not an imposter.
   - **Verify Signatures/Tokens:**
     - If using JWTs (e.g., as Bearer tokens), validate the JWT's signature against the A2A Server's trusted public keys (e.g., fetched from a JWKS endpoint provided by the A2A Server, if applicable). Also, validate claims like `iss` (issuer), `aud` (audience - should identify your webhook), `iat` (issued at), and `exp` (expiration time).
     - If using HMAC signatures, recalculate the signature on the received payload using the shared secret and compare it to the signature in the request header.
     - If using API keys, ensure the key is valid and known.
   - **Validate `PushNotificationConfig.token`:** If the client provided an opaque `token` in its `PushNotificationConfig` when setting up notifications for the task, the webhook should check that the incoming notification includes this exact token (e.g., in a custom header like `X-A2A-Notification-Token`). This helps ensure the notification is intended for this specific client context and task, adding a layer of authorization.
2. **Preventing Replay Attacks:**
   - **Timestamps:** Notifications should ideally include a timestamp (e.g., `iat` \- issued at - claim in a JWT, or a custom timestamp header). The webhook should reject notifications that are too old (e.g., older than a few minutes) to prevent attackers from replaying old, captured notifications. The timestamp should be part of the signed payload (if using signatures) to ensure its integrity.
   - **Nonces/Unique IDs:** For critical notifications, consider using unique, single-use identifiers (nonces or event IDs) for each notification. The webhook should track received IDs (for a reasonable window) to prevent processing duplicate notifications. A JWT's `jti` (JWT ID) claim can serve this purpose.
3. **Secure Key Management and Rotation:**
   - If using cryptographic keys (symmetric secrets for HMAC, or asymmetric key pairs for JWT signing/mTLS), implement secure key management practices, including regular key rotation.
   - For asymmetric keys where the A2A Server signs and the client webhook verifies, protocols like JWKS (JSON Web Key Set) allow the server to publish its public keys (including new ones during rotation) at a well-known endpoint. Client webhooks can then dynamically fetch the correct public key for signature verification, facilitating smoother key rotation.

##### Example Asymmetric Key Flow (JWT + JWKS)

1. Client sets `PushNotificationConfig` specifying `authentication.schemes: ["Bearer"]` and possibly an expected `issuer` or `audience` for the JWT.
2. A2A Server, when sending a notification:
   - Generates a JWT, signing it with its private key. The JWT includes claims like `iss` (issuer), `aud` (audience - the webhook), `iat` (issued at), `exp` (expires), `jti` (JWT ID), and `taskId`.
   - The JWT header ( `alg` and `kid`) indicates the signing algorithm and key ID.
   - The A2A Server makes its public keys available via a JWKS endpoint (URL for this endpoint might be known to the webhook provider or discovered).
3. Client Webhook, upon receiving the notification:
   - Extracts the JWT from the `Authorization` header.
   - Inspects the `kid` in the JWT header.
   - Fetches the corresponding public key from the A2A Server's JWKS endpoint (caching keys is recommended).
   - Verifies the JWT signature using the public key.
   - Validates claims ( `iss`, `aud`, `iat`, `exp`, `jti`).
   - Checks the `PushNotificationConfig.token` if provided.

This comprehensive, layered approach to security for push notifications ensures that messages are authentic, integral, and timely, protecting both the sending A2A Server and the receiving client webhook infrastructure.

## 7. Enterprise-Ready Features for A2A Agents

The Agent2Agent (A2A) protocol is designed with enterprise requirements at its core. Instead of inventing new, proprietary standards for security and operations, A2A aims to integrate seamlessly with existing enterprise infrastructure and widely adopted best practices. A2A treats remote agents as standard, HTTP-based enterprise applications. This approach allows organizations to leverage their existing investments and expertise in security, monitoring, governance, and identity management.

A key principle of A2A is that agents are typically "opaque" – they do not share internal memory, tools, or direct resource access with each other. This opacity naturally aligns with standard client/server security paradigms.

### 1\. Transport Level Security (TLS)

Ensuring the confidentiality and integrity of data in transit is fundamental.

- **HTTPS Mandate:** All A2A communication in production environments **MUST** occur over HTTPS.
- **Modern TLS Standards:** Implementations **SHOULD** use modern TLS versions (TLS 1.2 or higher is recommended) with strong, industry-standard cipher suites to protect data from eavesdropping and tampering.
- **Server Identity Verification:** A2A Clients **SHOULD** verify the A2A Server's identity by validating its TLS certificate against trusted certificate authorities (CAs) during the TLS handshake. This prevents man-in-the-middle attacks.

### 2\. Authentication

A2A delegates authentication to standard web mechanisms, primarily relying on HTTP headers and established standards like OAuth2 and OpenID Connect. Authentication requirements are advertised by the A2A Server in its [Agent Card](https://a2a-protocol.org/latest/specification/#5-agent-discovery-the-agent-card).

- **No In-Payload Identity:** A2A protocol payloads (JSON-RPC messages) do **not** carry user or client identity information. Identity is established at the transport/HTTP layer.
- **Agent Card Declaration:** The A2A Server's `AgentCard` describes the authentication `schemes` it supports in its `security` field. Each named scheme in this field is an identifier specific to the card. The details for each named scheme, including the scheme type, can be provided in the `securitySchemes` field of the Agent Card. The supported names of the scheme types ("apiKey", "http", "oauth2", "openIdConnect") align with those defined in the [OpenAPI Specification for authentication](https://swagger.io/docs/specification/authentication/).
- **Out-of-Band Credential Acquisition:** The A2A Client is responsible for obtaining the necessary credential materials (e.g., OAuth 2.0 tokens, either in JWT format or some other format; API keys; or other) through processes external to the A2A protocol itself. This could involve OAuth flows (authorization code, client credentials), secure key distribution, etc.
- **HTTP Header Transmission:** Credentials **MUST** be transmitted in standard HTTP headers as per the requirements of the chosen authentication scheme (e.g., `Authorization: Bearer <token>`, `API-Key: <key_value>`).
- **Server-Side Validation:** The A2A Server **MUST** authenticate **every** incoming request based on the credentials provided in the HTTP headers and its declared requirements.
  - If authentication fails or is missing, the server **SHOULD** respond with standard HTTP status codes such as `401 Unauthorized` or `403 Forbidden`.
  - A `401 Unauthorized` response **SHOULD** include a `WWW-Authenticate` header indicating the required scheme(s), guiding the client on how to authenticate correctly.
- **In-Task Authentication (Secondary Credentials):** If an agent, during a task, requires additional credentials for a _different_ system (e.g., to access a specific tool on behalf of the user), A2A recommends:
1. The A2A Server transitions the A2A task to the `input-required` state.
2. The `TaskStatus.message` (often using a `DataPart`) should provide details about the required authentication for the secondary system, potentially using an `AuthenticationInfo`-like structure.
3. The A2A Client then obtains these new credentials out-of-band for the secondary system. These credentials might be provided back to the A2A Server (if it's proxying the request) or used by the client to interact directly with the secondary system.

### 3\. Authorization

Once a client is authenticated, the A2A Server is responsible for authorizing the request. Authorization logic is specific to the agent's implementation, the data it handles, and applicable enterprise policies.

- **Granular Control:** Authorization **SHOULD** be applied based on the authenticated identity (which could represent an end user, a client application, or both).
- **Skill-Based Authorization:** Access can be controlled on a per-skill basis, as advertised in the Agent Card. For example, specific OAuth scopes might grant an authenticated client access to invoke certain skills but not others.
- **Data and Action-Level Authorization:** Agents that interact with backend systems, databases, or tools **MUST** enforce appropriate authorization before performing sensitive actions or accessing sensitive data through those underlying resources. The agent acts as a gatekeeper.
- **Principle of Least Privilege:** Grant only the necessary permissions required for a client or user to perform their intended operations via the A2A interface.

### 4\. Data Privacy and Confidentiality

- **Sensitivity Awareness:** Implementers must be acutely aware of the sensitivity of data exchanged in `Message` and `Artifact` parts of A2A interactions.
- **Compliance:** Ensure compliance with relevant data privacy regulations (e.g., GDPR, CCPA, HIPAA, depending on the domain and data).
- **Data Minimization:** Avoid including or requesting unnecessarily sensitive information in A2A exchanges.
- **Secure Handling:** Protect data both in transit (via TLS, as mandated) and at rest (if persisted by agents) according to enterprise data security policies and regulatory requirements.

### 5\. Tracing, Observability, and Monitoring

A2A's reliance on HTTP allows for straightforward integration with standard enterprise tracing, logging, and monitoring tools.

- **Distributed Tracing:**
  - A2A Clients and Servers **SHOULD** participate in distributed tracing systems (e.g., OpenTelemetry, Jaeger, Zipkin).
  - Trace context (trace IDs, span IDs) **SHOULD** be propagated via standard HTTP headers (e.g., W3C Trace Context headers like `traceparent` and `tracestate`).
  - This enables end-to-end visibility of requests as they flow across multiple agents and underlying services, which is invaluable for debugging and performance analysis.
- **Comprehensive Logging:** Implement detailed logging on both client and server sides. Logs should include relevant identifiers such as `taskId`, `sessionId`, correlation IDs, and trace context to facilitate troubleshooting and auditing.
- **Metrics:** A2A Servers should expose key operational metrics (e.g., request rates, error rates, task processing latency, resource utilization) to enable performance monitoring, alerting, and capacity planning. These can be integrated with systems like Prometheus or Google Cloud Monitoring.
- **Auditing:** Maintain audit trails for significant events, such as task creation, critical state changes, and actions performed by agents, especially those involving sensitive data access, modifications, or high-impact operations.

### 6\. API Management and Governance

For A2A Servers exposed externally, across organizational boundaries, or even within large enterprises, integration with API Management solutions is highly recommended. This can provide:

- **Centralized Policy Enforcement:** Consistent application of security policies (authentication, authorization), rate limiting, and quotas.
- **Traffic Management:** Load balancing, routing, and mediation.
- **Analytics and Reporting:** Insights into agent usage, performance, and trends.
- **Developer Portals:** Facilitate discovery of A2A-enabled agents, provide documentation (including Agent Cards), and streamline onboarding for client developers.

By adhering to these enterprise-grade practices, A2A implementations can be deployed securely, reliably, and manageably within complex organizational environments, fostering trust and enabling scalable inter-agent collaboration.

## 8. Extensions

### Abstract

Extensions are a means of extending the Agent2Agent (A2A) protocol with new data, requirements, methods, and state machines. Agents declare their support for extensions in their [`AgentCard`](https://a2a-protocol.org/specification/#5-agent-discovery-the-agent-card), and clients can then opt-in to the behavior offered by the extension as part of requests they make to the agent. Extensions are identified by a URI and defined by their extension specification. Anyone is able to define, publish, and implement an extension.

### Introduction

The core A2A protocol is a solid basis for enabling communication between agents. However, it's clear that some domains require additional structure than what is offered by the generic methods in the protocol. Extensions were added to the protocol to help support these cases: with extensions, agents and clients can negotiate additional, custom logic to be layered on top of the core protocol.

#### Scope of Extensions

The exact set of possible ways to use extensions is intentionally not defined. This is to facilitate the ability to use extensions to expand A2A beyond currently known use cases. However, some use cases are clearly foreseeable, such as:

- Exposing new information in the `AgentCard`. An extension may not impact the request/response flow at all -- it can be simply used as a way to convey additional structured information to clients via the `AgentCard`. We refer to these as _data-only extensions_. For example, an extension could add structured data about an agent's GDPR compliance to its `AgentCard`.

- Overlaying additional structure and state change requirements on the core request/response messages. An extension could, for example, require that all messages use `DataPart` s that adhere to a specific schema. This type of extension effectively acts as a profile on the core A2A protocol, narrowing the space of allowed values. We refer to these as _profile extensions_. For example, a healthcare extension could mandate that all `Message` parts containing patient information must be encrypted and placed within a `DataPart` that conforms to a FHIR standard.

- Adding new RPC methods entirely. Extensions may define that the agent implements more than the core set of protocol methods. We refer to these as _method extensions_. For example, a ['task-history' extension](https://github.com/a2aproject/A2A/issues/585#:~:text=Details%20with%20an%20example) might add a `tasks/search` RPC method to retrieve a list of previous tasks.

There are some changes to the protocol that extensions _do not_ allow. These are:

- Changing the definition of core data structures. Adding new fields or removing required fields to protocol-defined data structures is not supported. Extensions are expected to place custom attributes in the `metadata` map that is present on core data structures.
- Adding new values to enum types. Instead, extensions should use existing enum values and annotate additional semantic meaning in the `metadata` field.

These limitations exist to prevent extensions from breaking core type validations that clients and agents perform.

### Extension Declaration

Agents declare their support for extensions in their `AgentCard` by including `AgentExtension` objects in their `AgentCapabilities` object.

| Field Name | Type | Required | Description |
| --- | --- | --- | --- |
| `uri` | `string` | Yes | The URI of the extension. This is an arbitrary identifier that the extension specification defines. Implementations of an extension use this URI to identify when to activate, and clients use this to determine extension compatibility. extension. |
| `required` | `boolean` | No | Whether the agent requires clients to use this extension. |
| `description` | `string` | No | A description of how the agent uses the declared extension. Full details of a extension are intended to be in an extension specification. This field is useful to explain the connection between the agent and the extension. |
| `params` | `object` | No | Extension-specific configuration. The expected values to be placed in this field, if any, are defined by the extension specification. This field can be used for specifying parameters of the extension or declaring additional agent-specific data. |

An example `AgentCard` showing extensions:

```md-code__content
{
    "name": "Magic 8-ball",
    "description": "An agent that can tell your future... maybe.",
    "version": "0.1.0",
    "url": "https://example.com/agents/eightball",
    "capabilities": {
        "streaming": true,
        "extensions": [\
            {\
                "uri": "https://example.com/ext/konami-code/v1",\
                "description": "Provide cheat codes to unlock new fortunes",\
                "required": false,\
                "params": {\
                    "hints": [\
                        "When your sims need extra cash fast",\
                        "You might deny it, but we've seen the evidence of those cows."\
                    ]\
                }\
            }\
        ]
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [\
        {\
            "id": "fortune",\
            "name": "Fortune teller",\
            "description": "Seek advice from the mystical magic 8-ball",\
            "tags": ["mystical", "untrustworthy"]\
        }\
    ]
}

```

#### Required Extensions

While extensions are a means of enabling additional functionality, we anticipate that some agents will have stricter requirements than those expressible by the core A2A protocol. For example, an agent may require that all incoming messages are cryptographically signed by their author. Extensions that are declared `required` are intended to support this use case.

When an `AgentCard` declares a required extension, this is a signal to clients that some aspect of the extension impacts how requests are structured. Agents should not mark data-only extensions as required, since there is no direct impact on how requests are made to the agent.

If an `AgentCard` declares a required extension, and the client does not request activation of that required extension, Agents should return reject the incoming request and return an appropriate error code.

If a client requests extension activation, but does not follow an extension-defined protocol, the Agent should reject the request and return an appropriate validation failure message.

### Extension Specification

The details of an extension are defined by a specification. The exact format of this document is not specified, however it should contain at least:

- The specific URI(s) that extension implementations should identify and respond to. Multiple URIs may identify the same extension to account for versioning or changes in location of the specification document. Extension authors are encouraged to use a permanent identifier service, such as [w3id](https://w3id.org/), to avoid a proliferation of URLs.

- The schema and meaning of objects specified in the `params` field of the `AgentExtension` object exposed in the `AgentCard`.

- The schemas of any additional data structures communicated between client and agent.

- Details of request/response flows, additional endpoints, or any other logic required to implement the extension.

### Extension Dependencies

Extensions may depend on other extensions. This dependency may be required, where the core functionality of the extension is unable to run without the presence of the dependent, or optional, where some additional functionality is enabled when another extension is present. Extension specifications should document the dependency and its type.

Dependencies are declared within the extension's specification, not in the `AgentExtension` object. It is the responsibility of the client to activate an extension _and_ all of its required dependencies as listed in the extension's specification.

## Extension Activation

Extensions should default to being inactive. This provides a "default to baseline" experience, where extension-unaware clients are not burdened by the details and data provided by an extension. Instead, clients and agents perform negotiation to determine which extensions are active for a request. This negotiation is initiated by the client including the `X-A2A-Extensions` header in the HTTP request to the agent. The value of this header should be a list of extension URIs that the client is intending to activate.

Clients may request activation of any extension. Agents are responsible for identifying supported extensions in the request and performing the activation. Any requested extensions that are not supported by the agent can be ignored.

Not all extensions are activatable: data-only extensions exist solely to provide additional information via an AgentCard. Clients may still request activation of these extensions. Since the extension does not perform any additional logic upon activation, this should have no impact on the request.

Some extensions may have additional pre-requisites for activation. For example, some sensitive extensions may have a corresponding access-control list dictating who is allowed to activate the extension. It is up to the agent to determine which of the requested extensions are activated.

If a client requests activation of an extension with a required dependency, that client must also request activation of, and adhere to requirements of, that dependent extension. If the client does not request all required dependencies for a requested extension, the server may fail the request with an appropriate error.

Once the agent has identified all activated extensions, the response should include the `X-A2A-Extensions` header identifying all extensions that were activated.

An example request showing extension activation:

```md-code__content
POST /agents/eightball HTTP/1.1
Host: example.com
Content-Type: application/json
X-A2A-Extensions: https://example.com/ext/konami-code/v1
Content-Length: 519

{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "1",
  "params": {
    "message": {
        "kind": "message",
        "messageId": "1",
        "role": "user",
        "parts": [{"kind": "text", "text": "Oh magic 8-ball, will it rain today?"}]
    },
    "metadata": {
        "https://example.com/ext/konami-code/v1/code": "motherlode",
    }
  }
}

```

And corresponding response echoing the activated extensions:

```md-code__content
HTTP/1.1 200 OK
Content-Type: application/json
X-A2A-Extensions: https://example.com/ext/konami-code/v1
Content-Length: 338

{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "type": "message",
    "role": "agent",
    "parts": [{"type": "text", "text": "That's a bingo!"}],
  }
}

```

### Implementation Considerations

While the A2A protocol defines the "what" of extensions, this section provides guidance on the "how"—best practices for authoring, versioning, and distributing extension implementations.

#### Versioning

Extension specifications will inevitably evolve. It is crucial to have a clear versioning strategy to ensure that clients and agents can negotiate compatible implementations.

- **Recommendation**: Use the extension's URI as the primary version identifier. We recommend including a version number directly in the URI path, such as `https://example.com/ext/my-extension/v1` or `https://example.com/ext/my-extension/v2`.
- **Breaking Changes**: A new URI **MUST** be used when introducing a breaking change to an extension's logic, data structures, or required parameters. This prevents ambiguity and ensures that an agent supporting `/v1` does not incorrectly process a `/v2` request.
- **Handling Mismatches**: If a client requests a version of an extension that the agent does not support (e.g., client requests `/v2` but the agent only supports `/v1`), the agent **SHOULD** ignore the activation request for that extension. The agent **MUST NOT** attempt to "fall back" to a different version, as the client's logic is explicitly tied to the requested version.

#### Discoverability and Publication

For an extension to be useful, other developers need to be able to find its specification and understand how to use it.

- **Specification Hosting**: The extension specification document **SHOULD** be hosted at the extension's URI. This allows developers to easily access the documentation by simply resolving the identifier.
- **Permanent Identifiers**: To prevent issues with broken links or changing domains, authors are encouraged to use a permanent identifier service, such as [w3id.org](https://w3id.org/), for their extension URIs.
- **Community Registry (Future)**: In the future, the A2A community may establish a central registry for discovering and Browse available extensions.

#### Packaging and Reusability

To promote adoption, extension logic should be packaged into reusable libraries that can be easily integrated into existing A2A client and server applications.

- **Distribution**: An extension implementation should be distributed as a standard package for its language ecosystem (e.g., a PyPI package for Python, an npm package for TypeScript/JavaScript).

- **Simplified Integration**: The goal should be a near "plug-and-play" experience for developers. A well-designed extension package should allow a developer to add it to their server with minimal code, for example:

```md-code__content
# Hypothetical Python Server Integration
from konami_code_extension import CheatCodeHandler
from a2a.server import A2AServer, DefaultRequestHandler

# The extension hooks into the request handler to process its logic
extension = CheatCodeHandler(description="")
extension.add_cheat(
      code="motherlode",
      hint="When your sims need extra cash fast",
)
extension.add_cheat(
      code="thereisnocowlevel",
      hint="You might deny it, but we've seen the evidence of those cows.",
)
request_handler = DefaultRequestHandler(
      agent_executor=MyAgentExecutor(extension),
      task_store=InMemoryTaskStore(),
      extensions=[extension]
)

server = A2AStarletteApplication(
    agent_card, request_handler
)
server.run()

```

### Security

Extensions modify the core behavior of the A2A protocol and therefore introduce new security considerations.

- **Input Validation**: Any new data fields, parameters, or methods introduced by an extension **MUST** be rigorously validated by the implementation. Treat all extension-related data from an external party as untrusted input, unless there are protocol-defined means for establishing trust.
- **Scope of `required` extensions**: Be mindful when marking an extension as `required: true` in an `AgentCard`. This creates a hard dependency for all clients. Only use this for extensions that are fundamental to the agent's core function and security posture (e.g., a message signing extension).
- **Authentication and Authorization**: If an extension adds new methods, the implementation **MUST** ensure that these methods are subject to the same authentication and authorization checks as the core A2A methods. An extension **MUST NOT** provide a way to bypass the agent's primary security controls.
