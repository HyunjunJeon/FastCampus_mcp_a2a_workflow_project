
# a2a package [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html\#a2a-package "Link to this heading")

## Subpackages [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html\#subpackages "Link to this heading")

- [a2a.auth package](https://a2a-protocol.org/latest/sdk/python/api/a2a.auth.html)
  - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.auth.html#submodules)
  - [a2a.auth.user module](https://a2a-protocol.org/latest/sdk/python/api/a2a.auth.html#module-a2a.auth.user)
    - [`UnauthenticatedUser`](https://a2a-protocol.org/latest/sdk/python/api/a2a.auth.html#a2a.auth.user.UnauthenticatedUser)
      - [`UnauthenticatedUser.is_authenticated`](https://a2a-protocol.org/latest/sdk/python/api/a2a.auth.html#a2a.auth.user.UnauthenticatedUser.is_authenticated)
      - [`UnauthenticatedUser.user_name`](https://a2a-protocol.org/latest/sdk/python/api/a2a.auth.html#a2a.auth.user.UnauthenticatedUser.user_name)
    - [`User`](https://a2a-protocol.org/latest/sdk/python/api/a2a.auth.html#a2a.auth.user.User)
      - [`User.is_authenticated`](https://a2a-protocol.org/latest/sdk/python/api/a2a.auth.html#a2a.auth.user.User.is_authenticated)
      - [`User.user_name`](https://a2a-protocol.org/latest/sdk/python/api/a2a.auth.html#a2a.auth.user.User.user_name)
  - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.auth.html#module-a2a.auth)
- [a2a.client package](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html)
  - [Subpackages](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#subpackages)
    - [a2a.client.auth package](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.auth.html)
      - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.auth.html#submodules)
      - [a2a.client.auth.credentials module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.auth.html#module-a2a.client.auth.credentials)
      - [a2a.client.auth.interceptor module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.auth.html#module-a2a.client.auth.interceptor)
      - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.auth.html#module-a2a.client.auth)
    - [a2a.client.transports package](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.transports.html)
      - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.transports.html#submodules)
      - [a2a.client.transports.base module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.transports.html#module-a2a.client.transports.base)
      - [a2a.client.transports.grpc module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.transports.html#a2a-client-transports-grpc-module)
      - [a2a.client.transports.jsonrpc module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.transports.html#module-a2a.client.transports.jsonrpc)
      - [a2a.client.transports.rest module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.transports.html#module-a2a.client.transports.rest)
      - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.transports.html#module-a2a.client.transports)
  - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#submodules)
  - [a2a.client.base\_client module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client.base_client)
    - [`BaseClient`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.base_client.BaseClient)
      - [`BaseClient.cancel_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.base_client.BaseClient.cancel_task)
      - [`BaseClient.close()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.base_client.BaseClient.close)
      - [`BaseClient.get_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.base_client.BaseClient.get_card)
      - [`BaseClient.get_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.base_client.BaseClient.get_task)
      - [`BaseClient.get_task_callback()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.base_client.BaseClient.get_task_callback)
      - [`BaseClient.resubscribe()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.base_client.BaseClient.resubscribe)
      - [`BaseClient.send_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.base_client.BaseClient.send_message)
      - [`BaseClient.set_task_callback()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.base_client.BaseClient.set_task_callback)
  - [a2a.client.card\_resolver module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client.card_resolver)
    - [`A2ACardResolver`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.card_resolver.A2ACardResolver)
      - [`A2ACardResolver.get_agent_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.card_resolver.A2ACardResolver.get_agent_card)
  - [a2a.client.client module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client.client)
    - [`Client`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client)
      - [`Client.add_event_consumer()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client.add_event_consumer)
      - [`Client.add_request_middleware()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client.add_request_middleware)
      - [`Client.cancel_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client.cancel_task)
      - [`Client.consume()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client.consume)
      - [`Client.get_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client.get_card)
      - [`Client.get_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client.get_task)
      - [`Client.get_task_callback()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client.get_task_callback)
      - [`Client.resubscribe()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client.resubscribe)
      - [`Client.send_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client.send_message)
      - [`Client.set_task_callback()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.Client.set_task_callback)
    - [`ClientConfig`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.ClientConfig)
      - [`ClientConfig.accepted_output_modes`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.ClientConfig.accepted_output_modes)
      - [`ClientConfig.grpc_channel_factory`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.ClientConfig.grpc_channel_factory)
      - [`ClientConfig.httpx_client`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.ClientConfig.httpx_client)
      - [`ClientConfig.polling`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.ClientConfig.polling)
      - [`ClientConfig.push_notification_configs`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.ClientConfig.push_notification_configs)
      - [`ClientConfig.streaming`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.ClientConfig.streaming)
      - [`ClientConfig.supported_transports`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.ClientConfig.supported_transports)
      - [`ClientConfig.use_client_preference`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client.ClientConfig.use_client_preference)
  - [a2a.client.client\_factory module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client.client_factory)
    - [`ClientFactory`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client_factory.ClientFactory)
      - [`ClientFactory.create()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client_factory.ClientFactory.create)
      - [`ClientFactory.register()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client_factory.ClientFactory.register)
    - [`minimal_agent_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client_factory.minimal_agent_card)
  - [a2a.client.client\_task\_manager module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client.client_task_manager)
    - [`ClientTaskManager`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client_task_manager.ClientTaskManager)
      - [`ClientTaskManager.get_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client_task_manager.ClientTaskManager.get_task)
      - [`ClientTaskManager.get_task_or_raise()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client_task_manager.ClientTaskManager.get_task_or_raise)
      - [`ClientTaskManager.process()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client_task_manager.ClientTaskManager.process)
      - [`ClientTaskManager.save_task_event()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client_task_manager.ClientTaskManager.save_task_event)
      - [`ClientTaskManager.update_with_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.client_task_manager.ClientTaskManager.update_with_message)
  - [a2a.client.errors module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client.errors)
    - [`A2AClientError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.errors.A2AClientError)
    - [`A2AClientHTTPError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.errors.A2AClientHTTPError)
    - [`A2AClientInvalidArgsError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.errors.A2AClientInvalidArgsError)
    - [`A2AClientInvalidStateError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.errors.A2AClientInvalidStateError)
    - [`A2AClientJSONError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.errors.A2AClientJSONError)
    - [`A2AClientJSONRPCError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.errors.A2AClientJSONRPCError)
    - [`A2AClientTimeoutError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.errors.A2AClientTimeoutError)
  - [a2a.client.helpers module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client.helpers)
    - [`create_text_message_object()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.helpers.create_text_message_object)
  - [a2a.client.legacy module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client.legacy)
    - [`A2AClient`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.legacy.A2AClient)
      - [`A2AClient.cancel_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.legacy.A2AClient.cancel_task)
      - [`A2AClient.get_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.legacy.A2AClient.get_card)
      - [`A2AClient.get_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.legacy.A2AClient.get_task)
      - [`A2AClient.get_task_callback()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.legacy.A2AClient.get_task_callback)
      - [`A2AClient.resubscribe()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.legacy.A2AClient.resubscribe)
      - [`A2AClient.send_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.legacy.A2AClient.send_message)
      - [`A2AClient.send_message_streaming()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.legacy.A2AClient.send_message_streaming)
      - [`A2AClient.set_task_callback()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.legacy.A2AClient.set_task_callback)
  - [a2a.client.legacy\_grpc module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a-client-legacy-grpc-module)
  - [a2a.client.middleware module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client.middleware)
    - [`ClientCallContext`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.middleware.ClientCallContext)
      - [`ClientCallContext.model_config`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.middleware.ClientCallContext.model_config)
      - [`ClientCallContext.state`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.middleware.ClientCallContext.state)
    - [`ClientCallInterceptor`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.middleware.ClientCallInterceptor)
      - [`ClientCallInterceptor.intercept()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.middleware.ClientCallInterceptor.intercept)
  - [a2a.client.optionals module](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client.optionals)
  - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#module-a2a.client)
    - [`A2ACardResolver`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2ACardResolver)
      - [`A2ACardResolver.get_agent_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2ACardResolver.get_agent_card)
    - [`A2AClient`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClient)
      - [`A2AClient.cancel_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClient.cancel_task)
      - [`A2AClient.get_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClient.get_card)
      - [`A2AClient.get_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClient.get_task)
      - [`A2AClient.get_task_callback()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClient.get_task_callback)
      - [`A2AClient.resubscribe()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClient.resubscribe)
      - [`A2AClient.send_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClient.send_message)
      - [`A2AClient.send_message_streaming()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClient.send_message_streaming)
      - [`A2AClient.set_task_callback()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClient.set_task_callback)
    - [`A2AClientError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClientError)
    - [`A2AClientHTTPError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClientHTTPError)
    - [`A2AClientJSONError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClientJSONError)
    - [`A2AClientTimeoutError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AClientTimeoutError)
    - [`A2AGrpcClient`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.A2AGrpcClient)
    - [`AuthInterceptor`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.AuthInterceptor)
      - [`AuthInterceptor.intercept()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.AuthInterceptor.intercept)
    - [`Client`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client)
      - [`Client.add_event_consumer()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client.add_event_consumer)
      - [`Client.add_request_middleware()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client.add_request_middleware)
      - [`Client.cancel_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client.cancel_task)
      - [`Client.consume()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client.consume)
      - [`Client.get_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client.get_card)
      - [`Client.get_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client.get_task)
      - [`Client.get_task_callback()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client.get_task_callback)
      - [`Client.resubscribe()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client.resubscribe)
      - [`Client.send_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client.send_message)
      - [`Client.set_task_callback()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.Client.set_task_callback)
    - [`ClientCallContext`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientCallContext)
      - [`ClientCallContext.model_config`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientCallContext.model_config)
      - [`ClientCallContext.state`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientCallContext.state)
    - [`ClientCallInterceptor`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientCallInterceptor)
      - [`ClientCallInterceptor.intercept()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientCallInterceptor.intercept)
    - [`ClientConfig`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientConfig)
      - [`ClientConfig.accepted_output_modes`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientConfig.accepted_output_modes)
      - [`ClientConfig.grpc_channel_factory`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientConfig.grpc_channel_factory)
      - [`ClientConfig.httpx_client`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientConfig.httpx_client)
      - [`ClientConfig.polling`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientConfig.polling)
      - [`ClientConfig.push_notification_configs`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientConfig.push_notification_configs)
      - [`ClientConfig.streaming`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientConfig.streaming)
      - [`ClientConfig.supported_transports`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientConfig.supported_transports)
      - [`ClientConfig.use_client_preference`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientConfig.use_client_preference)
    - [`ClientFactory`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientFactory)
      - [`ClientFactory.create()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientFactory.create)
      - [`ClientFactory.register()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.ClientFactory.register)
    - [`CredentialService`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.CredentialService)
      - [`CredentialService.get_credentials()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.CredentialService.get_credentials)
    - [`InMemoryContextCredentialStore`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.InMemoryContextCredentialStore)
      - [`InMemoryContextCredentialStore.get_credentials()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.InMemoryContextCredentialStore.get_credentials)
      - [`InMemoryContextCredentialStore.set_credentials()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.InMemoryContextCredentialStore.set_credentials)
    - [`create_text_message_object()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.create_text_message_object)
    - [`minimal_agent_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.client.html#a2a.client.minimal_agent_card)
- [a2a.extensions package](https://a2a-protocol.org/latest/sdk/python/api/a2a.extensions.html)
  - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.extensions.html#submodules)
  - [a2a.extensions.common module](https://a2a-protocol.org/latest/sdk/python/api/a2a.extensions.html#module-a2a.extensions.common)
    - [`find_extension_by_uri()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.extensions.html#a2a.extensions.common.find_extension_by_uri)
    - [`get_requested_extensions()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.extensions.html#a2a.extensions.common.get_requested_extensions)
  - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.extensions.html#module-a2a.extensions)
- [a2a.grpc package](https://a2a-protocol.org/latest/sdk/python/api/a2a.grpc.html)
  - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.grpc.html#submodules)
  - [a2a.grpc.a2a\_pb2 module](https://a2a-protocol.org/latest/sdk/python/api/a2a.grpc.html#module-a2a.grpc.a2a_pb2)
  - [a2a.grpc.a2a\_pb2\_grpc module](https://a2a-protocol.org/latest/sdk/python/api/a2a.grpc.html#a2a-grpc-a2a-pb2-grpc-module)
  - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.grpc.html#module-a2a.grpc)
- [a2a.server package](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html)
  - [Subpackages](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#subpackages)
    - [a2a.server.agent\_execution package](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.agent_execution.html)
      - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.agent_execution.html#submodules)
      - [a2a.server.agent\_execution.agent\_executor module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.agent_execution.html#module-a2a.server.agent_execution.agent_executor)
      - [a2a.server.agent\_execution.context module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.agent_execution.html#module-a2a.server.agent_execution.context)
      - [a2a.server.agent\_execution.request\_context\_builder module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.agent_execution.html#module-a2a.server.agent_execution.request_context_builder)
      - [a2a.server.agent\_execution.simple\_request\_context\_builder module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.agent_execution.html#module-a2a.server.agent_execution.simple_request_context_builder)
      - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.agent_execution.html#module-a2a.server.agent_execution)
    - [a2a.server.apps package](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.apps.html)
      - [Subpackages](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.apps.html#subpackages)
      - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.apps.html#module-a2a.server.apps)
    - [a2a.server.events package](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.events.html)
      - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.events.html#submodules)
      - [a2a.server.events.event\_consumer module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.events.html#module-a2a.server.events.event_consumer)
      - [a2a.server.events.event\_queue module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.events.html#module-a2a.server.events.event_queue)
      - [a2a.server.events.in\_memory\_queue\_manager module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.events.html#module-a2a.server.events.in_memory_queue_manager)
      - [a2a.server.events.queue\_manager module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.events.html#module-a2a.server.events.queue_manager)
      - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.events.html#module-a2a.server.events)
    - [a2a.server.request\_handlers package](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.request_handlers.html)
      - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.request_handlers.html#submodules)
      - [a2a.server.request\_handlers.default\_request\_handler module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.request_handlers.html#module-a2a.server.request_handlers.default_request_handler)
      - [a2a.server.request\_handlers.grpc\_handler module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.request_handlers.html#a2a-server-request-handlers-grpc-handler-module)
      - [a2a.server.request\_handlers.jsonrpc\_handler module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.request_handlers.html#module-a2a.server.request_handlers.jsonrpc_handler)
      - [a2a.server.request\_handlers.request\_handler module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.request_handlers.html#module-a2a.server.request_handlers.request_handler)
      - [a2a.server.request\_handlers.response\_helpers module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.request_handlers.html#module-a2a.server.request_handlers.response_helpers)
      - [a2a.server.request\_handlers.rest\_handler module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.request_handlers.html#module-a2a.server.request_handlers.rest_handler)
      - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.request_handlers.html#module-a2a.server.request_handlers)
    - [a2a.server.tasks package](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html)
      - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#submodules)
      - [a2a.server.tasks.base\_push\_notification\_sender module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#module-a2a.server.tasks.base_push_notification_sender)
      - [a2a.server.tasks.database\_push\_notification\_config\_store module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#a2a-server-tasks-database-push-notification-config-store-module)
      - [a2a.server.tasks.database\_task\_store module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#a2a-server-tasks-database-task-store-module)
      - [a2a.server.tasks.inmemory\_push\_notification\_config\_store module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#module-a2a.server.tasks.inmemory_push_notification_config_store)
      - [a2a.server.tasks.inmemory\_task\_store module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#module-a2a.server.tasks.inmemory_task_store)
      - [a2a.server.tasks.push\_notification\_config\_store module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#module-a2a.server.tasks.push_notification_config_store)
      - [a2a.server.tasks.push\_notification\_sender module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#module-a2a.server.tasks.push_notification_sender)
      - [a2a.server.tasks.result\_aggregator module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#module-a2a.server.tasks.result_aggregator)
      - [a2a.server.tasks.task\_manager module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#module-a2a.server.tasks.task_manager)
      - [a2a.server.tasks.task\_store module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#module-a2a.server.tasks.task_store)
      - [a2a.server.tasks.task\_updater module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#module-a2a.server.tasks.task_updater)
      - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.tasks.html#module-a2a.server.tasks)
  - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#submodules)
  - [a2a.server.context module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#module-a2a.server.context)
    - [`ServerCallContext`](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#a2a.server.context.ServerCallContext)
      - [`ServerCallContext.activated_extensions`](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#a2a.server.context.ServerCallContext.activated_extensions)
      - [`ServerCallContext.model_config`](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#a2a.server.context.ServerCallContext.model_config)
      - [`ServerCallContext.requested_extensions`](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#a2a.server.context.ServerCallContext.requested_extensions)
      - [`ServerCallContext.state`](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#a2a.server.context.ServerCallContext.state)
      - [`ServerCallContext.user`](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#a2a.server.context.ServerCallContext.user)
  - [a2a.server.models module](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#a2a-server-models-module)
  - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.server.html#module-a2a.server)
- [a2a.utils package](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html)
  - [Submodules](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#submodules)
  - [a2a.utils.artifact module](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#module-a2a.utils.artifact)
    - [`new_artifact()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.artifact.new_artifact)
    - [`new_data_artifact()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.artifact.new_data_artifact)
    - [`new_text_artifact()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.artifact.new_text_artifact)
  - [a2a.utils.constants module](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#module-a2a.utils.constants)
  - [a2a.utils.error\_handlers module](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#module-a2a.utils.error_handlers)
    - [`rest_error_handler()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.error_handlers.rest_error_handler)
    - [`rest_stream_error_handler()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.error_handlers.rest_stream_error_handler)
  - [a2a.utils.errors module](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#module-a2a.utils.errors)
    - [`A2AServerError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.errors.A2AServerError)
    - [`MethodNotImplementedError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.errors.MethodNotImplementedError)
    - [`ServerError`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.errors.ServerError)
  - [a2a.utils.helpers module](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#module-a2a.utils.helpers)
    - [`append_artifact_to_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.helpers.append_artifact_to_task)
    - [`are_modalities_compatible()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.helpers.are_modalities_compatible)
    - [`build_text_artifact()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.helpers.build_text_artifact)
    - [`create_task_obj()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.helpers.create_task_obj)
    - [`validate()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.helpers.validate)
    - [`validate_async_generator()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.helpers.validate_async_generator)
  - [a2a.utils.message module](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#module-a2a.utils.message)
    - [`get_data_parts()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.message.get_data_parts)
    - [`get_file_parts()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.message.get_file_parts)
    - [`get_message_text()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.message.get_message_text)
    - [`get_text_parts()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.message.get_text_parts)
    - [`new_agent_parts_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.message.new_agent_parts_message)
    - [`new_agent_text_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.message.new_agent_text_message)
  - [a2a.utils.proto\_utils module](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#module-a2a.utils.proto_utils)
    - [`FromProto`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto)
      - [`FromProto.agent_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.agent_card)
      - [`FromProto.agent_interface()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.agent_interface)
      - [`FromProto.artifact()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.artifact)
      - [`FromProto.authentication_info()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.authentication_info)
      - [`FromProto.capabilities()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.capabilities)
      - [`FromProto.data()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.data)
      - [`FromProto.file()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.file)
      - [`FromProto.message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.message)
      - [`FromProto.message_send_configuration()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.message_send_configuration)
      - [`FromProto.message_send_params()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.message_send_params)
      - [`FromProto.metadata()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.metadata)
      - [`FromProto.oauth2_flows()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.oauth2_flows)
      - [`FromProto.part()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.part)
      - [`FromProto.provider()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.provider)
      - [`FromProto.push_notification_config()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.push_notification_config)
      - [`FromProto.role()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.role)
      - [`FromProto.security()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.security)
      - [`FromProto.security_scheme()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.security_scheme)
      - [`FromProto.security_schemes()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.security_schemes)
      - [`FromProto.skill()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.skill)
      - [`FromProto.stream_response()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.stream_response)
      - [`FromProto.task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.task)
      - [`FromProto.task_artifact_update_event()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.task_artifact_update_event)
      - [`FromProto.task_id_params()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.task_id_params)
      - [`FromProto.task_or_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.task_or_message)
      - [`FromProto.task_push_notification_config()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.task_push_notification_config)
      - [`FromProto.task_push_notification_config_request()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.task_push_notification_config_request)
      - [`FromProto.task_query_params()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.task_query_params)
      - [`FromProto.task_state()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.task_state)
      - [`FromProto.task_status()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.task_status)
      - [`FromProto.task_status_update_event()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.FromProto.task_status_update_event)
    - [`ToProto`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto)
      - [`ToProto.agent_card()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.agent_card)
      - [`ToProto.agent_interface()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.agent_interface)
      - [`ToProto.artifact()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.artifact)
      - [`ToProto.authentication_info()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.authentication_info)
      - [`ToProto.capabilities()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.capabilities)
      - [`ToProto.data()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.data)
      - [`ToProto.file()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.file)
      - [`ToProto.message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.message)
      - [`ToProto.message_send_configuration()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.message_send_configuration)
      - [`ToProto.metadata()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.metadata)
      - [`ToProto.oauth2_flows()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.oauth2_flows)
      - [`ToProto.part()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.part)
      - [`ToProto.provider()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.provider)
      - [`ToProto.push_notification_config()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.push_notification_config)
      - [`ToProto.role()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.role)
      - [`ToProto.security()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.security)
      - [`ToProto.security_scheme()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.security_scheme)
      - [`ToProto.security_schemes()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.security_schemes)
      - [`ToProto.skill()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.skill)
      - [`ToProto.stream_response()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.stream_response)
      - [`ToProto.task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.task)
      - [`ToProto.task_artifact_update_event()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.task_artifact_update_event)
      - [`ToProto.task_or_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.task_or_message)
      - [`ToProto.task_push_notification_config()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.task_push_notification_config)
      - [`ToProto.task_state()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.task_state)
      - [`ToProto.task_status()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.task_status)
      - [`ToProto.task_status_update_event()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.task_status_update_event)
      - [`ToProto.update_event()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.proto_utils.ToProto.update_event)
  - [a2a.utils.task module](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#module-a2a.utils.task)
    - [`completed_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.task.completed_task)
    - [`new_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.task.new_task)
  - [a2a.utils.telemetry module](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#module-a2a.utils.telemetry)
  - [Module contents](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#module-a2a.utils)
    - [`append_artifact_to_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.append_artifact_to_task)
    - [`are_modalities_compatible()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.are_modalities_compatible)
    - [`build_text_artifact()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.build_text_artifact)
    - [`completed_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.completed_task)
    - [`create_task_obj()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.create_task_obj)
    - [`get_data_parts()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.get_data_parts)
    - [`get_file_parts()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.get_file_parts)
    - [`get_message_text()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.get_message_text)
    - [`get_text_parts()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.get_text_parts)
    - [`new_agent_parts_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.new_agent_parts_message)
    - [`new_agent_text_message()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.new_agent_text_message)
    - [`new_artifact()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.new_artifact)
    - [`new_data_artifact()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.new_data_artifact)
    - [`new_task()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.new_task)
    - [`new_text_artifact()`](https://a2a-protocol.org/latest/sdk/python/api/a2a.utils.html#a2a.utils.new_text_artifact)

## Submodules [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html\#submodules "Link to this heading")

## a2a.types module [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html\#module-a2a.types "Link to this heading")

_class_ a2a.types.A2A( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.A2A "Link to this definition")

Bases: `RootModel[Any]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.A2A.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _:Any_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.A2A.root "Link to this definition")_class_ a2a.types.A2AError( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.A2AError "Link to this definition")

Bases: `RootModel[Union[JSONParseError, InvalidRequestError, MethodNotFoundError, InvalidParamsError, InternalError, TaskNotFoundError, TaskNotCancelableError, PushNotificationNotSupportedError, UnsupportedOperationError, ContentTypeNotSupportedError, InvalidAgentResponseError, AuthenticatedExtendedCardNotConfiguredError]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.A2AError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONParseError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONParseError "a2a.types.JSONParseError") \| [InvalidRequestError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidRequestError "a2a.types.InvalidRequestError") \| [MethodNotFoundError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MethodNotFoundError "a2a.types.MethodNotFoundError") \| [InvalidParamsError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidParamsError "a2a.types.InvalidParamsError") \| [InternalError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InternalError "a2a.types.InternalError") \| [TaskNotFoundError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotFoundError "a2a.types.TaskNotFoundError") \| [TaskNotCancelableError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotCancelableError "a2a.types.TaskNotCancelableError") \| [PushNotificationNotSupportedError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationNotSupportedError "a2a.types.PushNotificationNotSupportedError") \| [UnsupportedOperationError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.UnsupportedOperationError "a2a.types.UnsupportedOperationError") \| [ContentTypeNotSupportedError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ContentTypeNotSupportedError "a2a.types.ContentTypeNotSupportedError") \| [InvalidAgentResponseError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidAgentResponseError "a2a.types.InvalidAgentResponseError") \| [AuthenticatedExtendedCardNotConfiguredError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthenticatedExtendedCardNotConfiguredError "a2a.types.AuthenticatedExtendedCardNotConfiguredError")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.A2AError.root "Link to this definition")

A discriminated union of all standard JSON-RPC and A2A-specific error types.

_class_ a2a.types.A2ARequest( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.A2ARequest "Link to this definition")

Bases: `RootModel[Union[SendMessageRequest, SendStreamingMessageRequest, GetTaskRequest, CancelTaskRequest, SetTaskPushNotificationConfigRequest, GetTaskPushNotificationConfigRequest, TaskResubscriptionRequest, ListTaskPushNotificationConfigRequest, DeleteTaskPushNotificationConfigRequest, GetAuthenticatedExtendedCardRequest]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.A2ARequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [SendMessageRequest](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageRequest "a2a.types.SendMessageRequest") \| [SendStreamingMessageRequest](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageRequest "a2a.types.SendStreamingMessageRequest") \| [GetTaskRequest](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskRequest "a2a.types.GetTaskRequest") \| [CancelTaskRequest](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskRequest "a2a.types.CancelTaskRequest") \| [SetTaskPushNotificationConfigRequest](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigRequest "a2a.types.SetTaskPushNotificationConfigRequest") \| [GetTaskPushNotificationConfigRequest](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigRequest "a2a.types.GetTaskPushNotificationConfigRequest") \| [TaskResubscriptionRequest](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskResubscriptionRequest "a2a.types.TaskResubscriptionRequest") \| [ListTaskPushNotificationConfigRequest](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigRequest "a2a.types.ListTaskPushNotificationConfigRequest") \| [DeleteTaskPushNotificationConfigRequest](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigRequest "a2a.types.DeleteTaskPushNotificationConfigRequest") \| [GetAuthenticatedExtendedCardRequest](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardRequest "a2a.types.GetAuthenticatedExtendedCardRequest")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.A2ARequest.root "Link to this definition")

A discriminated union representing all possible JSON-RPC 2.0 requests supported by the A2A specification.

_class_ a2a.types.APIKeySecurityScheme( _\*_, _description:str\|None=None_, _in\_:[In](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.In "a2a.types.In")_, _name:str_, _type:Literal\['apiKey'\]='apiKey'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.APIKeySecurityScheme "Link to this definition")

Bases: `A2ABaseModel`

Defines a security scheme using an API key.

description _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.APIKeySecurityScheme.description "Link to this definition")

An optional description for the security scheme.

in\_ _: [In](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.In "a2a.types.In")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.APIKeySecurityScheme.in_ "Link to this definition")

The location of the API key.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.APIKeySecurityScheme.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

name _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.APIKeySecurityScheme.name "Link to this definition")

The name of the header, query, or cookie parameter to be used.

type _:Literal\['apiKey'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.APIKeySecurityScheme.type "Link to this definition")

The type of the security scheme. Must be ‘apiKey’.

_class_ a2a.types.AgentCapabilities( _\*_, _extensions:list\[ [AgentExtension](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentExtension "a2a.types.AgentExtension")\]\|None=None_, _pushNotifications:bool\|None=None_, _stateTransitionHistory:bool\|None=None_, _streaming:bool\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCapabilities "Link to this definition")

Bases: `A2ABaseModel`

Defines optional capabilities supported by an agent.

extensions _:list\[ [AgentExtension](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentExtension "a2a.types.AgentExtension")\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCapabilities.extensions "Link to this definition")

A list of protocol extensions supported by the agent.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCapabilities.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

push\_notifications _:bool\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCapabilities.push_notifications "Link to this definition")

Indicates if the agent supports sending push notifications for asynchronous task updates.

state\_transition\_history _:bool\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCapabilities.state_transition_history "Link to this definition")

Indicates if the agent provides a history of state transitions for a task.

streaming _:bool\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCapabilities.streaming "Link to this definition")

Indicates if the agent supports Server-Sent Events (SSE) for streaming responses.

_class_ a2a.types.AgentCard( _\*_, _additionalInterfaces:list\[ [AgentInterface](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentInterface "a2a.types.AgentInterface")\]\|None=None_, _capabilities:[AgentCapabilities](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCapabilities "a2a.types.AgentCapabilities")_, _defaultInputModes:list\[str\]_, _defaultOutputModes:list\[str\]_, _description:str_, _documentationUrl:str\|None=None_, _iconUrl:str\|None=None_, _name:str_, _preferredTransport:str\|None='JSONRPC'_, _protocolVersion:str\|None='0.3.0'_, _provider:[AgentProvider](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentProvider "a2a.types.AgentProvider") \|None=None_, _security:list\[dict\[str,list\[str\]\]\]\|None=None_, _securitySchemes:dict\[str, [SecurityScheme](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SecurityScheme "a2a.types.SecurityScheme")\]\|None=None_, _signatures:list\[ [AgentCardSignature](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCardSignature "a2a.types.AgentCardSignature")\]\|None=None_, _skills:list\[ [AgentSkill](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill "a2a.types.AgentSkill")\]_, _supportsAuthenticatedExtendedCard:bool\|None=None_, _url:str_, _version:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard "Link to this definition")

Bases: `A2ABaseModel`

The AgentCard is a self-describing manifest for an agent. It provides essential
metadata including the agent’s identity, capabilities, skills, supported
communication methods, and security requirements.

additional\_interfaces _:list\[ [AgentInterface](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentInterface "a2a.types.AgentInterface")\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.additional_interfaces "Link to this definition")

A list of additional supported interfaces (transport and URL combinations).
This allows agents to expose multiple transports, potentially at different URLs.

Best practices:
\- SHOULD include all supported transports for completeness
\- SHOULD include an entry matching the main ‘url’ and ‘preferredTransport’
\- MAY reuse URLs if multiple transports are available at the same endpoint
\- MUST accurately declare the transport available at each URL

Clients can select any interface from this list based on their transport capabilities
and preferences. This enables transport negotiation and fallback scenarios.

capabilities _: [AgentCapabilities](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCapabilities "a2a.types.AgentCapabilities")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.capabilities "Link to this definition")

A declaration of optional capabilities supported by the agent.

default\_input\_modes _:list\[str\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.default_input_modes "Link to this definition")

Default set of supported input MIME types for all skills, which can be
overridden on a per-skill basis.

default\_output\_modes _:list\[str\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.default_output_modes "Link to this definition")

Default set of supported output MIME types for all skills, which can be
overridden on a per-skill basis.

description _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.description "Link to this definition")

A human-readable description of the agent, assisting users and other agents
in understanding its purpose.

documentation\_url _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.documentation_url "Link to this definition")

An optional URL to the agent’s documentation.

icon\_url _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.icon_url "Link to this definition")

An optional URL to an icon for the agent.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

name _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.name "Link to this definition")

A human-readable name for the agent.

preferred\_transport _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.preferred_transport "Link to this definition")

The transport protocol for the preferred endpoint (the main ‘url’ field).
If not specified, defaults to ‘JSONRPC’.

IMPORTANT: The transport specified here MUST be available at the main ‘url’.
This creates a binding between the main URL and its supported transport protocol.
Clients should prefer this transport and URL combination when both are supported.

protocol\_version _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.protocol_version "Link to this definition")

The version of the A2A protocol this agent supports.

provider _: [AgentProvider](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentProvider "a2a.types.AgentProvider") \|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.provider "Link to this definition")

Information about the agent’s service provider.

security _:list\[dict\[str,list\[str\]\]\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.security "Link to this definition")

A list of security requirement objects that apply to all agent interactions. Each object
lists security schemes that can be used. Follows the OpenAPI 3.0 Security Requirement Object.
This list can be seen as an OR of ANDs. Each object in the list describes one possible
set of security requirements that must be present on a request. This allows specifying,
for example, “callers must either use OAuth OR an API Key AND mTLS.”

security\_schemes _:dict\[str, [SecurityScheme](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SecurityScheme "a2a.types.SecurityScheme")\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.security_schemes "Link to this definition")

A declaration of the security schemes available to authorize requests. The key is the
scheme name. Follows the OpenAPI 3.0 Security Scheme Object.

signatures _:list\[ [AgentCardSignature](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCardSignature "a2a.types.AgentCardSignature")\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.signatures "Link to this definition")

JSON Web Signatures computed for this AgentCard.

skills _:list\[ [AgentSkill](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill "a2a.types.AgentSkill")\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.skills "Link to this definition")

The set of skills, or distinct capabilities, that the agent can perform.

supports\_authenticated\_extended\_card _:bool\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.supports_authenticated_extended_card "Link to this definition")

If true, the agent can provide an extended agent card with additional details
to authenticated users. Defaults to false.

url _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.url "Link to this definition")

The preferred endpoint URL for interacting with the agent.
This URL MUST support the transport specified by ‘preferredTransport’.

version _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard.version "Link to this definition")

The agent’s own version number. The format is defined by the provider.

_class_ a2a.types.AgentCardSignature( _\*_, _header:dict\[str,Any\]\|None=None_, _protected:str_, _signature:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCardSignature "Link to this definition")

Bases: `A2ABaseModel`

AgentCardSignature represents a JWS signature of an AgentCard.
This follows the JSON format of an RFC 7515 JSON Web Signature (JWS).

header _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCardSignature.header "Link to this definition")

The unprotected JWS header values.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCardSignature.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

protected _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCardSignature.protected "Link to this definition")

The protected JWS header for the signature. This is a Base64url-encoded
JSON object, as per RFC 7515.

signature _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCardSignature.signature "Link to this definition")

The computed signature, Base64url-encoded.

_class_ a2a.types.AgentExtension( _\*_, _description:str\|None=None_, _params:dict\[str,Any\]\|None=None_, _required:bool\|None=None_, _uri:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentExtension "Link to this definition")

Bases: `A2ABaseModel`

A declaration of a protocol extension supported by an Agent.

description _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentExtension.description "Link to this definition")

A human-readable description of how this agent uses the extension.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentExtension.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentExtension.params "Link to this definition")

Optional, extension-specific configuration parameters.

required _:bool\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentExtension.required "Link to this definition")

If true, the client must understand and comply with the extension’s requirements
to interact with the agent.

uri _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentExtension.uri "Link to this definition")

The unique URI identifying the extension.

_class_ a2a.types.AgentInterface( _\*_, _transport:str_, _url:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentInterface "Link to this definition")

Bases: `A2ABaseModel`

Declares a combination of a target URL and a transport protocol for interacting with the agent.
This allows agents to expose the same functionality over multiple transport mechanisms.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentInterface.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

transport _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentInterface.transport "Link to this definition")

The transport protocol supported at this URL.

url _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentInterface.url "Link to this definition")

The URL where this interface is available. Must be a valid absolute HTTPS URL in production.

_class_ a2a.types.AgentProvider( _\*_, _organization:str_, _url:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentProvider "Link to this definition")

Bases: `A2ABaseModel`

Represents the service provider of an agent.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentProvider.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

organization _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentProvider.organization "Link to this definition")

The name of the agent provider’s organization.

url _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentProvider.url "Link to this definition")

A URL for the agent provider’s website or relevant documentation.

_class_ a2a.types.AgentSkill( _\*_, _description:str_, _examples:list\[str\]\|None=None_, _id:str_, _inputModes:list\[str\]\|None=None_, _name:str_, _outputModes:list\[str\]\|None=None_, _security:list\[dict\[str,list\[str\]\]\]\|None=None_, _tags:list\[str\]_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill "Link to this definition")

Bases: `A2ABaseModel`

Represents a distinct capability or function that an agent can perform.

description _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill.description "Link to this definition")

A detailed description of the skill, intended to help clients or users
understand its purpose and functionality.

examples _:list\[str\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill.examples "Link to this definition")

Example prompts or scenarios that this skill can handle. Provides a hint to
the client on how to use the skill.

id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill.id "Link to this definition")

A unique identifier for the agent’s skill.

input\_modes _:list\[str\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill.input_modes "Link to this definition")

The set of supported input MIME types for this skill, overriding the agent’s defaults.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

name _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill.name "Link to this definition")

A human-readable name for the skill.

output\_modes _:list\[str\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill.output_modes "Link to this definition")

The set of supported output MIME types for this skill, overriding the agent’s defaults.

security _:list\[dict\[str,list\[str\]\]\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill.security "Link to this definition")

Security schemes necessary for the agent to leverage this skill.
As in the overall AgentCard.security, this list represents a logical OR of security
requirement objects. Each object is a set of security schemes that must be used together
(a logical AND).

tags _:list\[str\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentSkill.tags "Link to this definition")

A set of keywords describing the skill’s capabilities.

_class_ a2a.types.Artifact( _\*_, _artifactId:str_, _description:str\|None=None_, _extensions:list\[str\]\|None=None_, _metadata:dict\[str,Any\]\|None=None_, _name:str\|None=None_, _parts:list\[ [Part](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Part "a2a.types.Part")\]_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact "Link to this definition")

Bases: `A2ABaseModel`

Represents a file, data structure, or other resource generated by an agent during a task.

artifact\_id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact.artifact_id "Link to this definition")

A unique identifier for the artifact within the scope of the task.

description _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact.description "Link to this definition")

An optional, human-readable description of the artifact.

extensions _:list\[str\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact.extensions "Link to this definition")

The URIs of extensions that are relevant to this artifact.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact.metadata "Link to this definition")

Optional metadata for extensions. The key is an extension-specific identifier.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

name _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact.name "Link to this definition")

An optional, human-readable name for the artifact.

parts _:list\[ [Part](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Part "a2a.types.Part")\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact.parts "Link to this definition")

An array of content parts that make up the artifact.

_class_ a2a.types.AuthenticatedExtendedCardNotConfiguredError( _\*_, _code:Literal\[-32007\]=-32007_, _data:Any\|None=None_, _message:str\|None='AuthenticatedExtendedCardisnotconfigured'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthenticatedExtendedCardNotConfiguredError "Link to this definition")

Bases: `A2ABaseModel`

An A2A-specific error indicating that the agent does not have an Authenticated Extended Card configured

code _:Literal\[-32007\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthenticatedExtendedCardNotConfiguredError.code "Link to this definition")

The error code for when an authenticated extended card is not configured.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthenticatedExtendedCardNotConfiguredError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthenticatedExtendedCardNotConfiguredError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthenticatedExtendedCardNotConfiguredError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.AuthorizationCodeOAuthFlow( _\*_, _authorizationUrl:str_, _refreshUrl:str\|None=None_, _scopes:dict\[str,str\]_, _tokenUrl:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthorizationCodeOAuthFlow "Link to this definition")

Bases: `A2ABaseModel`

Defines configuration details for the OAuth 2.0 Authorization Code flow.

authorization\_url _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthorizationCodeOAuthFlow.authorization_url "Link to this definition")

The authorization URL to be used for this flow.
This MUST be a URL and use TLS.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthorizationCodeOAuthFlow.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

refresh\_url _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthorizationCodeOAuthFlow.refresh_url "Link to this definition")

The URL to be used for obtaining refresh tokens.
This MUST be a URL and use TLS.

scopes _:dict\[str,str\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthorizationCodeOAuthFlow.scopes "Link to this definition")

The available scopes for the OAuth2 security scheme. A map between the scope
name and a short description for it.

token\_url _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthorizationCodeOAuthFlow.token_url "Link to this definition")

The token URL to be used for this flow.
This MUST be a URL and use TLS.

_class_ a2a.types.CancelTaskRequest( _\*_, _id:str\|int_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:Literal\['tasks/cancel'\]='tasks/cancel'_, _params:[TaskIdParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskIdParams "a2a.types.TaskIdParams")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC request for the tasks/cancel method.

id _:str\|int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskRequest.id "Link to this definition")

The identifier for this request.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:Literal\['tasks/cancel'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskRequest.method "Link to this definition")

The method name. Must be ‘tasks/cancel’.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _: [TaskIdParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskIdParams "a2a.types.TaskIdParams")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskRequest.params "Link to this definition")

The parameters identifying the task to cancel.

_class_ a2a.types.CancelTaskResponse( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskResponse "Link to this definition")

Bases: `RootModel[Union[JSONRPCErrorResponse, CancelTaskSuccessResponse]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONRPCErrorResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "a2a.types.JSONRPCErrorResponse") \| [CancelTaskSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskSuccessResponse "a2a.types.CancelTaskSuccessResponse")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskResponse.root "Link to this definition")

Represents a JSON-RPC response for the tasks/cancel method.

_class_ a2a.types.CancelTaskSuccessResponse( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _result:[Task](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task "a2a.types.Task")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskSuccessResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a successful JSON-RPC response for the tasks/cancel method.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskSuccessResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskSuccessResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskSuccessResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

result _: [Task](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task "a2a.types.Task")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskSuccessResponse.result "Link to this definition")

The result, containing the final state of the canceled Task object.

_class_ a2a.types.ClientCredentialsOAuthFlow( _\*_, _refreshUrl:str\|None=None_, _scopes:dict\[str,str\]_, _tokenUrl:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ClientCredentialsOAuthFlow "Link to this definition")

Bases: `A2ABaseModel`

Defines configuration details for the OAuth 2.0 Client Credentials flow.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ClientCredentialsOAuthFlow.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

refresh\_url _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ClientCredentialsOAuthFlow.refresh_url "Link to this definition")

The URL to be used for obtaining refresh tokens. This MUST be a URL.

scopes _:dict\[str,str\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ClientCredentialsOAuthFlow.scopes "Link to this definition")

The available scopes for the OAuth2 security scheme. A map between the scope
name and a short description for it.

token\_url _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ClientCredentialsOAuthFlow.token_url "Link to this definition")

The token URL to be used for this flow. This MUST be a URL.

_class_ a2a.types.ContentTypeNotSupportedError( _\*_, _code:Literal\[-32005\]=-32005_, _data:Any\|None=None_, _message:str\|None='Incompatiblecontenttypes'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ContentTypeNotSupportedError "Link to this definition")

Bases: `A2ABaseModel`

An A2A-specific error indicating an incompatibility between the requested
content types and the agent’s capabilities.

code _:Literal\[-32005\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ContentTypeNotSupportedError.code "Link to this definition")

The error code for an unsupported content type.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ContentTypeNotSupportedError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ContentTypeNotSupportedError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ContentTypeNotSupportedError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.DataPart( _\*_, _data:dict\[str,Any\]_, _kind:Literal\['data'\]='data'_, _metadata:dict\[str,Any\]\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DataPart "Link to this definition")

Bases: `A2ABaseModel`

Represents a structured data segment (e.g., JSON) within a message or artifact.

data _:dict\[str,Any\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DataPart.data "Link to this definition")

The structured data content.

kind _:Literal\['data'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DataPart.kind "Link to this definition")

The type of this part, used as a discriminator. Always ‘data’.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DataPart.metadata "Link to this definition")

Optional metadata associated with this part.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DataPart.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.DeleteTaskPushNotificationConfigParams( _\*_, _id:str_, _metadata:dict\[str,Any\]\|None=None_, _pushNotificationConfigId:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigParams "Link to this definition")

Bases: `A2ABaseModel`

Defines parameters for deleting a specific push notification configuration for a task.

id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigParams.id "Link to this definition")

The unique identifier of the task.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigParams.metadata "Link to this definition")

Optional metadata associated with the request.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigParams.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

push\_notification\_config\_id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigParams.push_notification_config_id "Link to this definition")

The ID of the push notification configuration to delete.

_class_ a2a.types.DeleteTaskPushNotificationConfigRequest( _\*_, _id:str\|int_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:Literal\['tasks/pushNotificationConfig/delete'\]='tasks/pushNotificationConfig/delete'_, _params:[DeleteTaskPushNotificationConfigParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigParams "a2a.types.DeleteTaskPushNotificationConfigParams")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC request for the tasks/pushNotificationConfig/delete method.

id _:str\|int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigRequest.id "Link to this definition")

The identifier for this request.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:Literal\['tasks/pushNotificationConfig/delete'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigRequest.method "Link to this definition")

The method name. Must be ‘tasks/pushNotificationConfig/delete’.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _: [DeleteTaskPushNotificationConfigParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigParams "a2a.types.DeleteTaskPushNotificationConfigParams")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigRequest.params "Link to this definition")

The parameters identifying the push notification configuration to delete.

_class_ a2a.types.DeleteTaskPushNotificationConfigResponse( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigResponse "Link to this definition")

Bases: `RootModel[Union[JSONRPCErrorResponse, DeleteTaskPushNotificationConfigSuccessResponse]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONRPCErrorResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "a2a.types.JSONRPCErrorResponse") \| [DeleteTaskPushNotificationConfigSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse "a2a.types.DeleteTaskPushNotificationConfigSuccessResponse")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigResponse.root "Link to this definition")

Represents a JSON-RPC response for the tasks/pushNotificationConfig/delete method.

_class_ a2a.types.DeleteTaskPushNotificationConfigSuccessResponse( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _result:None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a successful JSON-RPC response for the tasks/pushNotificationConfig/delete method.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

result _:None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse.result "Link to this definition")

The result is null on successful deletion.

_class_ a2a.types.FileBase( _\*_, _mimeType:str\|None=None_, _name:str\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileBase "Link to this definition")

Bases: `A2ABaseModel`

Defines base properties for a file.

mime\_type _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileBase.mime_type "Link to this definition")

The MIME type of the file (e.g., “application/pdf”).

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileBase.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

name _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileBase.name "Link to this definition")

An optional name for the file (e.g., “document.pdf”).

_class_ a2a.types.FilePart( _\*_, _file:[FileWithBytes](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithBytes "a2a.types.FileWithBytes") \| [FileWithUri](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithUri "a2a.types.FileWithUri")_, _kind:Literal\['file'\]='file'_, _metadata:dict\[str,Any\]\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FilePart "Link to this definition")

Bases: `A2ABaseModel`

Represents a file segment within a message or artifact. The file content can be
provided either directly as bytes or as a URI.

file _: [FileWithBytes](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithBytes "a2a.types.FileWithBytes") \| [FileWithUri](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithUri "a2a.types.FileWithUri")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FilePart.file "Link to this definition")

The file content, represented as either a URI or as base64-encoded bytes.

kind _:Literal\['file'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FilePart.kind "Link to this definition")

The type of this part, used as a discriminator. Always ‘file’.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FilePart.metadata "Link to this definition")

Optional metadata associated with this part.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FilePart.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.FileWithBytes( _\*_, _bytes:str_, _mimeType:str\|None=None_, _name:str\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithBytes "Link to this definition")

Bases: `A2ABaseModel`

Represents a file with its content provided directly as a base64-encoded string.

bytes _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithBytes.bytes "Link to this definition")

The base64-encoded content of the file.

mime\_type _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithBytes.mime_type "Link to this definition")

The MIME type of the file (e.g., “application/pdf”).

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithBytes.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

name _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithBytes.name "Link to this definition")

An optional name for the file (e.g., “document.pdf”).

_class_ a2a.types.FileWithUri( _\*_, _mimeType:str\|None=None_, _name:str\|None=None_, _uri:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithUri "Link to this definition")

Bases: `A2ABaseModel`

Represents a file with its content located at a specific URI.

mime\_type _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithUri.mime_type "Link to this definition")

The MIME type of the file (e.g., “application/pdf”).

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithUri.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

name _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithUri.name "Link to this definition")

An optional name for the file (e.g., “document.pdf”).

uri _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FileWithUri.uri "Link to this definition")

A URL pointing to the file’s content.

_class_ a2a.types.GetAuthenticatedExtendedCardRequest( _\*_, _id:str\|int_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:Literal\['agent/getAuthenticatedExtendedCard'\]='agent/getAuthenticatedExtendedCard'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC request for the agent/getAuthenticatedExtendedCard method.

id _:str\|int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardRequest.id "Link to this definition")

The identifier for this request.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:Literal\['agent/getAuthenticatedExtendedCard'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardRequest.method "Link to this definition")

The method name. Must be ‘agent/getAuthenticatedExtendedCard’.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.GetAuthenticatedExtendedCardResponse( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardResponse "Link to this definition")

Bases: `RootModel[Union[JSONRPCErrorResponse, GetAuthenticatedExtendedCardSuccessResponse]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONRPCErrorResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "a2a.types.JSONRPCErrorResponse") \| [GetAuthenticatedExtendedCardSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardSuccessResponse "a2a.types.GetAuthenticatedExtendedCardSuccessResponse")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardResponse.root "Link to this definition")

Represents a JSON-RPC response for the agent/getAuthenticatedExtendedCard method.

_class_ a2a.types.GetAuthenticatedExtendedCardSuccessResponse( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _result:[AgentCard](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard "a2a.types.AgentCard")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardSuccessResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a successful JSON-RPC response for the agent/getAuthenticatedExtendedCard method.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardSuccessResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardSuccessResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardSuccessResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

result _: [AgentCard](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AgentCard "a2a.types.AgentCard")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardSuccessResponse.result "Link to this definition")

The result is an Agent Card object.

_class_ a2a.types.GetTaskPushNotificationConfigParams( _\*_, _id:str_, _metadata:dict\[str,Any\]\|None=None_, _pushNotificationConfigId:str\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigParams "Link to this definition")

Bases: `A2ABaseModel`

Defines parameters for fetching a specific push notification configuration for a task.

id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigParams.id "Link to this definition")

The unique identifier of the task.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigParams.metadata "Link to this definition")

Optional metadata associated with the request.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigParams.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

push\_notification\_config\_id _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigParams.push_notification_config_id "Link to this definition")

The ID of the push notification configuration to retrieve.

_class_ a2a.types.GetTaskPushNotificationConfigRequest( _\*_, _id:str\|int_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:Literal\['tasks/pushNotificationConfig/get'\]='tasks/pushNotificationConfig/get'_, _params:[TaskIdParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskIdParams "a2a.types.TaskIdParams") \| [GetTaskPushNotificationConfigParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigParams "a2a.types.GetTaskPushNotificationConfigParams")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC request for the tasks/pushNotificationConfig/get method.

id _:str\|int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigRequest.id "Link to this definition")

The identifier for this request.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:Literal\['tasks/pushNotificationConfig/get'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigRequest.method "Link to this definition")

The method name. Must be ‘tasks/pushNotificationConfig/get’.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _: [TaskIdParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskIdParams "a2a.types.TaskIdParams") \| [GetTaskPushNotificationConfigParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigParams "a2a.types.GetTaskPushNotificationConfigParams")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigRequest.params "Link to this definition")

The parameters for getting a push notification configuration.

_class_ a2a.types.GetTaskPushNotificationConfigResponse( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigResponse "Link to this definition")

Bases: `RootModel[Union[JSONRPCErrorResponse, GetTaskPushNotificationConfigSuccessResponse]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONRPCErrorResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "a2a.types.JSONRPCErrorResponse") \| [GetTaskPushNotificationConfigSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigSuccessResponse "a2a.types.GetTaskPushNotificationConfigSuccessResponse")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigResponse.root "Link to this definition")

Represents a JSON-RPC response for the tasks/pushNotificationConfig/get method.

_class_ a2a.types.GetTaskPushNotificationConfigSuccessResponse( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _result:[TaskPushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig "a2a.types.TaskPushNotificationConfig")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigSuccessResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a successful JSON-RPC response for the tasks/pushNotificationConfig/get method.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigSuccessResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigSuccessResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigSuccessResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

result _: [TaskPushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig "a2a.types.TaskPushNotificationConfig")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigSuccessResponse.result "Link to this definition")

The result, containing the requested push notification configuration.

_class_ a2a.types.GetTaskRequest( _\*_, _id:str\|int_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:Literal\['tasks/get'\]='tasks/get'_, _params:[TaskQueryParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskQueryParams "a2a.types.TaskQueryParams")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC request for the tasks/get method.

id _:str\|int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskRequest.id "Link to this definition")

The identifier for this request.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:Literal\['tasks/get'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskRequest.method "Link to this definition")

The method name. Must be ‘tasks/get’.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _: [TaskQueryParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskQueryParams "a2a.types.TaskQueryParams")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskRequest.params "Link to this definition")

The parameters for querying a task.

_class_ a2a.types.GetTaskResponse( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskResponse "Link to this definition")

Bases: `RootModel[Union[JSONRPCErrorResponse, GetTaskSuccessResponse]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONRPCErrorResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "a2a.types.JSONRPCErrorResponse") \| [GetTaskSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskSuccessResponse "a2a.types.GetTaskSuccessResponse")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskResponse.root "Link to this definition")

Represents a JSON-RPC response for the tasks/get method.

_class_ a2a.types.GetTaskSuccessResponse( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _result:[Task](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task "a2a.types.Task")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskSuccessResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a successful JSON-RPC response for the tasks/get method.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskSuccessResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskSuccessResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskSuccessResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

result _: [Task](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task "a2a.types.Task")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskSuccessResponse.result "Link to this definition")

The result, containing the requested Task object.

_class_ a2a.types.HTTPAuthSecurityScheme( _\*_, _bearerFormat:str\|None=None_, _description:str\|None=None_, _scheme:str_, _type:Literal\['http'\]='http'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.HTTPAuthSecurityScheme "Link to this definition")

Bases: `A2ABaseModel`

Defines a security scheme using HTTP authentication.

bearer\_format _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.HTTPAuthSecurityScheme.bearer_format "Link to this definition")

A hint to the client to identify how the bearer token is formatted (e.g., “JWT”).
This is primarily for documentation purposes.

description _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.HTTPAuthSecurityScheme.description "Link to this definition")

An optional description for the security scheme.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.HTTPAuthSecurityScheme.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

scheme _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.HTTPAuthSecurityScheme.scheme "Link to this definition")

The name of the HTTP Authentication scheme to be used in the Authorization header,
as defined in RFC7235 (e.g., “Bearer”).
This value should be registered in the IANA Authentication Scheme registry.

type _:Literal\['http'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.HTTPAuthSecurityScheme.type "Link to this definition")

The type of the security scheme. Must be ‘http’.

_class_ a2a.types.ImplicitOAuthFlow( _\*_, _authorizationUrl:str_, _refreshUrl:str\|None=None_, _scopes:dict\[str,str\]_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ImplicitOAuthFlow "Link to this definition")

Bases: `A2ABaseModel`

Defines configuration details for the OAuth 2.0 Implicit flow.

authorization\_url _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ImplicitOAuthFlow.authorization_url "Link to this definition")

The authorization URL to be used for this flow. This MUST be a URL.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ImplicitOAuthFlow.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

refresh\_url _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ImplicitOAuthFlow.refresh_url "Link to this definition")

The URL to be used for obtaining refresh tokens. This MUST be a URL.

scopes _:dict\[str,str\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ImplicitOAuthFlow.scopes "Link to this definition")

The available scopes for the OAuth2 security scheme. A map between the scope
name and a short description for it.

_class_ a2a.types.In( _\*values_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.In "Link to this definition")

Bases: `str`, `Enum`

The location of the API key.

cookie _='cookie'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.In.cookie "Link to this definition")header _='header'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.In.header "Link to this definition")query _='query'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.In.query "Link to this definition")_class_ a2a.types.InternalError( _\*_, _code:Literal\[-32603\]=-32603_, _data:Any\|None=None_, _message:str\|None='Internalerror'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InternalError "Link to this definition")

Bases: `A2ABaseModel`

An error indicating an internal error on the server.

code _:Literal\[-32603\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InternalError.code "Link to this definition")

The error code for an internal server error.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InternalError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InternalError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InternalError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.InvalidAgentResponseError( _\*_, _code:Literal\[-32006\]=-32006_, _data:Any\|None=None_, _message:str\|None='Invalidagentresponse'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidAgentResponseError "Link to this definition")

Bases: `A2ABaseModel`

An A2A-specific error indicating that the agent returned a response that
does not conform to the specification for the current method.

code _:Literal\[-32006\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidAgentResponseError.code "Link to this definition")

The error code for an invalid agent response.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidAgentResponseError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidAgentResponseError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidAgentResponseError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.InvalidParamsError( _\*_, _code:Literal\[-32602\]=-32602_, _data:Any\|None=None_, _message:str\|None='Invalidparameters'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidParamsError "Link to this definition")

Bases: `A2ABaseModel`

An error indicating that the method parameters are invalid.

code _:Literal\[-32602\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidParamsError.code "Link to this definition")

The error code for an invalid parameters error.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidParamsError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidParamsError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidParamsError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.InvalidRequestError( _\*_, _code:Literal\[-32600\]=-32600_, _data:Any\|None=None_, _message:str\|None='Requestpayloadvalidationerror'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidRequestError "Link to this definition")

Bases: `A2ABaseModel`

An error indicating that the JSON sent is not a valid Request object.

code _:Literal\[-32600\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidRequestError.code "Link to this definition")

The error code for an invalid request.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidRequestError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidRequestError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidRequestError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.JSONParseError( _\*_, _code:Literal\[-32700\]=-32700_, _data:Any\|None=None_, _message:str\|None='InvalidJSONpayload'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONParseError "Link to this definition")

Bases: `A2ABaseModel`

An error indicating that the server received invalid JSON.

code _:Literal\[-32700\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONParseError.code "Link to this definition")

The error code for a JSON parse error.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONParseError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONParseError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONParseError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.JSONRPCError( _\*_, _code:int_, _data:Any\|None=None_, _message:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCError "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC 2.0 Error object, included in an error response.

code _:int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCError.code "Link to this definition")

A number that indicates the error type that occurred.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCError.message "Link to this definition")

A string providing a short description of the error.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.JSONRPCErrorResponse( _\*_, _error:[JSONRPCError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCError "a2a.types.JSONRPCError") \| [JSONParseError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONParseError "a2a.types.JSONParseError") \| [InvalidRequestError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidRequestError "a2a.types.InvalidRequestError") \| [MethodNotFoundError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MethodNotFoundError "a2a.types.MethodNotFoundError") \| [InvalidParamsError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidParamsError "a2a.types.InvalidParamsError") \| [InternalError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InternalError "a2a.types.InternalError") \| [TaskNotFoundError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotFoundError "a2a.types.TaskNotFoundError") \| [TaskNotCancelableError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotCancelableError "a2a.types.TaskNotCancelableError") \| [PushNotificationNotSupportedError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationNotSupportedError "a2a.types.PushNotificationNotSupportedError") \| [UnsupportedOperationError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.UnsupportedOperationError "a2a.types.UnsupportedOperationError") \| [ContentTypeNotSupportedError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ContentTypeNotSupportedError "a2a.types.ContentTypeNotSupportedError") \| [InvalidAgentResponseError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidAgentResponseError "a2a.types.InvalidAgentResponseError") \| [AuthenticatedExtendedCardNotConfiguredError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthenticatedExtendedCardNotConfiguredError "a2a.types.AuthenticatedExtendedCardNotConfiguredError")_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC 2.0 Error Response object.

error _: [JSONRPCError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCError "a2a.types.JSONRPCError") \| [JSONParseError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONParseError "a2a.types.JSONParseError") \| [InvalidRequestError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidRequestError "a2a.types.InvalidRequestError") \| [MethodNotFoundError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MethodNotFoundError "a2a.types.MethodNotFoundError") \| [InvalidParamsError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidParamsError "a2a.types.InvalidParamsError") \| [InternalError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InternalError "a2a.types.InternalError") \| [TaskNotFoundError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotFoundError "a2a.types.TaskNotFoundError") \| [TaskNotCancelableError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotCancelableError "a2a.types.TaskNotCancelableError") \| [PushNotificationNotSupportedError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationNotSupportedError "a2a.types.PushNotificationNotSupportedError") \| [UnsupportedOperationError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.UnsupportedOperationError "a2a.types.UnsupportedOperationError") \| [ContentTypeNotSupportedError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ContentTypeNotSupportedError "a2a.types.ContentTypeNotSupportedError") \| [InvalidAgentResponseError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.InvalidAgentResponseError "a2a.types.InvalidAgentResponseError") \| [AuthenticatedExtendedCardNotConfiguredError](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthenticatedExtendedCardNotConfiguredError "a2a.types.AuthenticatedExtendedCardNotConfiguredError")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse.error "Link to this definition")

An object describing the error that occurred.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.JSONRPCMessage( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCMessage "Link to this definition")

Bases: `A2ABaseModel`

Defines the base structure for any JSON-RPC 2.0 request, response, or notification.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCMessage.id "Link to this definition")

A unique identifier established by the client. It must be a String, a Number, or null.
The server must reply with the same value in the response. This property is omitted for notifications.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCMessage.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCMessage.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.JSONRPCRequest( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:str_, _params:dict\[str,Any\]\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC 2.0 Request object.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCRequest.id "Link to this definition")

A unique identifier established by the client. It must be a String, a Number, or null.
The server must reply with the same value in the response. This property is omitted for notifications.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCRequest.method "Link to this definition")

A string containing the name of the method to be invoked.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCRequest.params "Link to this definition")

A structured value holding the parameter values to be used during the method invocation.

_class_ a2a.types.JSONRPCResponse( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCResponse "Link to this definition")

Bases: `RootModel[Union[JSONRPCErrorResponse, SendMessageSuccessResponse, SendStreamingMessageSuccessResponse, GetTaskSuccessResponse, CancelTaskSuccessResponse, SetTaskPushNotificationConfigSuccessResponse, GetTaskPushNotificationConfigSuccessResponse, ListTaskPushNotificationConfigSuccessResponse, DeleteTaskPushNotificationConfigSuccessResponse, GetAuthenticatedExtendedCardSuccessResponse]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONRPCErrorResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "a2a.types.JSONRPCErrorResponse") \| [SendMessageSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageSuccessResponse "a2a.types.SendMessageSuccessResponse") \| [SendStreamingMessageSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageSuccessResponse "a2a.types.SendStreamingMessageSuccessResponse") \| [GetTaskSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskSuccessResponse "a2a.types.GetTaskSuccessResponse") \| [CancelTaskSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.CancelTaskSuccessResponse "a2a.types.CancelTaskSuccessResponse") \| [SetTaskPushNotificationConfigSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigSuccessResponse "a2a.types.SetTaskPushNotificationConfigSuccessResponse") \| [GetTaskPushNotificationConfigSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetTaskPushNotificationConfigSuccessResponse "a2a.types.GetTaskPushNotificationConfigSuccessResponse") \| [ListTaskPushNotificationConfigSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigSuccessResponse "a2a.types.ListTaskPushNotificationConfigSuccessResponse") \| [DeleteTaskPushNotificationConfigSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse "a2a.types.DeleteTaskPushNotificationConfigSuccessResponse") \| [GetAuthenticatedExtendedCardSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.GetAuthenticatedExtendedCardSuccessResponse "a2a.types.GetAuthenticatedExtendedCardSuccessResponse")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCResponse.root "Link to this definition")

A discriminated union representing all possible JSON-RPC 2.0 responses
for the A2A specification methods.

_class_ a2a.types.JSONRPCSuccessResponse( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _result:Any_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCSuccessResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a successful JSON-RPC 2.0 Response object.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCSuccessResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCSuccessResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCSuccessResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

result _:Any_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCSuccessResponse.result "Link to this definition")

The value of this member is determined by the method invoked on the Server.

_class_ a2a.types.ListTaskPushNotificationConfigParams( _\*_, _id:str_, _metadata:dict\[str,Any\]\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigParams "Link to this definition")

Bases: `A2ABaseModel`

Defines parameters for listing all push notification configurations associated with a task.

id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigParams.id "Link to this definition")

The unique identifier of the task.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigParams.metadata "Link to this definition")

Optional metadata associated with the request.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigParams.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.ListTaskPushNotificationConfigRequest( _\*_, _id:str\|int_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:Literal\['tasks/pushNotificationConfig/list'\]='tasks/pushNotificationConfig/list'_, _params:[ListTaskPushNotificationConfigParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigParams "a2a.types.ListTaskPushNotificationConfigParams")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC request for the tasks/pushNotificationConfig/list method.

id _:str\|int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigRequest.id "Link to this definition")

The identifier for this request.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:Literal\['tasks/pushNotificationConfig/list'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigRequest.method "Link to this definition")

The method name. Must be ‘tasks/pushNotificationConfig/list’.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _: [ListTaskPushNotificationConfigParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigParams "a2a.types.ListTaskPushNotificationConfigParams")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigRequest.params "Link to this definition")

The parameters identifying the task whose configurations are to be listed.

_class_ a2a.types.ListTaskPushNotificationConfigResponse( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigResponse "Link to this definition")

Bases: `RootModel[Union[JSONRPCErrorResponse, ListTaskPushNotificationConfigSuccessResponse]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONRPCErrorResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "a2a.types.JSONRPCErrorResponse") \| [ListTaskPushNotificationConfigSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigSuccessResponse "a2a.types.ListTaskPushNotificationConfigSuccessResponse")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigResponse.root "Link to this definition")

Represents a JSON-RPC response for the tasks/pushNotificationConfig/list method.

_class_ a2a.types.ListTaskPushNotificationConfigSuccessResponse( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _result:list\[ [TaskPushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig "a2a.types.TaskPushNotificationConfig")\]_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigSuccessResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a successful JSON-RPC response for the tasks/pushNotificationConfig/list method.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigSuccessResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigSuccessResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigSuccessResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

result _:list\[ [TaskPushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig "a2a.types.TaskPushNotificationConfig")\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ListTaskPushNotificationConfigSuccessResponse.result "Link to this definition")

The result, containing an array of all push notification configurations for the task.

_class_ a2a.types.Message( _\*_, _contextId:str\|None=None_, _extensions:list\[str\]\|None=None_, _kind:Literal\['message'\]='message'_, _messageId:str_, _metadata:dict\[str,Any\]\|None=None_, _parts:list\[ [Part](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Part "a2a.types.Part")\]_, _referenceTaskIds:list\[str\]\|None=None_, _role:[Role](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Role "a2a.types.Role")_, _taskId:str\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "Link to this definition")

Bases: `A2ABaseModel`

Represents a single message in the conversation between a user and an agent.

context\_id _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message.context_id "Link to this definition")

The context identifier for this message, used to group related interactions.

extensions _:list\[str\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message.extensions "Link to this definition")

The URIs of extensions that are relevant to this message.

kind _:Literal\['message'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message.kind "Link to this definition")

The type of this object, used as a discriminator. Always ‘message’ for a Message.

message\_id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message.message_id "Link to this definition")

A unique identifier for the message, typically a UUID, generated by the sender.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message.metadata "Link to this definition")

Optional metadata for extensions. The key is an extension-specific identifier.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

parts _:list\[ [Part](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Part "a2a.types.Part")\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message.parts "Link to this definition")

An array of content parts that form the message body. A message can be
composed of multiple parts of different types (e.g., text and files).

reference\_task\_ids _:list\[str\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message.reference_task_ids "Link to this definition")

A list of other task IDs that this message references for additional context.

role _: [Role](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Role "a2a.types.Role")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message.role "Link to this definition")

Identifies the sender of the message. user for the client, agent for the service.

task\_id _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message.task_id "Link to this definition")

The identifier of the task this message is part of. Can be omitted for the first message of a new task.

_class_ a2a.types.MessageSendConfiguration( _\*_, _acceptedOutputModes:list\[str\]\|None=None_, _blocking:bool\|None=None_, _historyLength:int\|None=None_, _pushNotificationConfig:[PushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationConfig "a2a.types.PushNotificationConfig") \|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendConfiguration "Link to this definition")

Bases: `A2ABaseModel`

Defines configuration options for a message/send or message/stream request.

accepted\_output\_modes _:list\[str\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendConfiguration.accepted_output_modes "Link to this definition")

A list of output MIME types the client is prepared to accept in the response.

blocking _:bool\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendConfiguration.blocking "Link to this definition")

If true, the client will wait for the task to complete. The server may reject this if the task is long-running.

history\_length _:int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendConfiguration.history_length "Link to this definition")

The number of most recent messages from the task’s history to retrieve in the response.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendConfiguration.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

push\_notification\_config _: [PushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationConfig "a2a.types.PushNotificationConfig") \|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendConfiguration.push_notification_config "Link to this definition")

Configuration for the agent to send push notifications for updates after the initial response.

_class_ a2a.types.MessageSendParams( _\*_, _configuration:[MessageSendConfiguration](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendConfiguration "a2a.types.MessageSendConfiguration") \|None=None_, _message:[Message](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "a2a.types.Message")_, _metadata:dict\[str,Any\]\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendParams "Link to this definition")

Bases: `A2ABaseModel`

Defines the parameters for a request to send a message to an agent. This can be used
to create a new task, continue an existing one, or restart a task.

configuration _: [MessageSendConfiguration](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendConfiguration "a2a.types.MessageSendConfiguration") \|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendParams.configuration "Link to this definition")

Optional configuration for the send request.

message _: [Message](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "a2a.types.Message")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendParams.message "Link to this definition")

The message object being sent to the agent.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendParams.metadata "Link to this definition")

Optional metadata for extensions.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendParams.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.MethodNotFoundError( _\*_, _code:Literal\[-32601\]=-32601_, _data:Any\|None=None_, _message:str\|None='Methodnotfound'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MethodNotFoundError "Link to this definition")

Bases: `A2ABaseModel`

An error indicating that the requested method does not exist or is not available.

code _:Literal\[-32601\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MethodNotFoundError.code "Link to this definition")

The error code for a method not found error.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MethodNotFoundError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MethodNotFoundError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MethodNotFoundError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.MutualTLSSecurityScheme( _\*_, _description:str\|None=None_, _type:Literal\['mutualTLS'\]='mutualTLS'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MutualTLSSecurityScheme "Link to this definition")

Bases: `A2ABaseModel`

Defines a security scheme using mTLS authentication.

description _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MutualTLSSecurityScheme.description "Link to this definition")

An optional description for the security scheme.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MutualTLSSecurityScheme.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

type _:Literal\['mutualTLS'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MutualTLSSecurityScheme.type "Link to this definition")

The type of the security scheme. Must be ‘mutualTLS’.

_class_ a2a.types.OAuth2SecurityScheme( _\*_, _description:str\|None=None_, _flows:[OAuthFlows](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuthFlows "a2a.types.OAuthFlows")_, _oauth2MetadataUrl:str\|None=None_, _type:Literal\['oauth2'\]='oauth2'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuth2SecurityScheme "Link to this definition")

Bases: `A2ABaseModel`

Defines a security scheme using OAuth 2.0.

description _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuth2SecurityScheme.description "Link to this definition")

An optional description for the security scheme.

flows _: [OAuthFlows](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuthFlows "a2a.types.OAuthFlows")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuth2SecurityScheme.flows "Link to this definition")

An object containing configuration information for the supported OAuth 2.0 flows.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuth2SecurityScheme.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

oauth2\_metadata\_url _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuth2SecurityScheme.oauth2_metadata_url "Link to this definition")

URL to the oauth2 authorization server metadata
\[RFC8414\]( [https://datatracker.ietf.org/doc/html/rfc8414](https://datatracker.ietf.org/doc/html/rfc8414)). TLS is required.

type _:Literal\['oauth2'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuth2SecurityScheme.type "Link to this definition")

The type of the security scheme. Must be ‘oauth2’.

_class_ a2a.types.OAuthFlows( _\*_, _authorizationCode:[AuthorizationCodeOAuthFlow](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthorizationCodeOAuthFlow "a2a.types.AuthorizationCodeOAuthFlow") \|None=None_, _clientCredentials:[ClientCredentialsOAuthFlow](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ClientCredentialsOAuthFlow "a2a.types.ClientCredentialsOAuthFlow") \|None=None_, _implicit:[ImplicitOAuthFlow](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ImplicitOAuthFlow "a2a.types.ImplicitOAuthFlow") \|None=None_, _password:[PasswordOAuthFlow](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PasswordOAuthFlow "a2a.types.PasswordOAuthFlow") \|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuthFlows "Link to this definition")

Bases: `A2ABaseModel`

Defines the configuration for the supported OAuth 2.0 flows.

authorization\_code _: [AuthorizationCodeOAuthFlow](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.AuthorizationCodeOAuthFlow "a2a.types.AuthorizationCodeOAuthFlow") \|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuthFlows.authorization_code "Link to this definition")

Configuration for the OAuth Authorization Code flow. Previously called accessCode in OpenAPI 2.0.

client\_credentials _: [ClientCredentialsOAuthFlow](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ClientCredentialsOAuthFlow "a2a.types.ClientCredentialsOAuthFlow") \|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuthFlows.client_credentials "Link to this definition")

Configuration for the OAuth Client Credentials flow. Previously called application in OpenAPI 2.0.

implicit _: [ImplicitOAuthFlow](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.ImplicitOAuthFlow "a2a.types.ImplicitOAuthFlow") \|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuthFlows.implicit "Link to this definition")

Configuration for the OAuth Implicit flow.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuthFlows.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

password _: [PasswordOAuthFlow](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PasswordOAuthFlow "a2a.types.PasswordOAuthFlow") \|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuthFlows.password "Link to this definition")

Configuration for the OAuth Resource Owner Password flow.

_class_ a2a.types.OpenIdConnectSecurityScheme( _\*_, _description:str\|None=None_, _openIdConnectUrl:str_, _type:Literal\['openIdConnect'\]='openIdConnect'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OpenIdConnectSecurityScheme "Link to this definition")

Bases: `A2ABaseModel`

Defines a security scheme using OpenID Connect.

description _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OpenIdConnectSecurityScheme.description "Link to this definition")

An optional description for the security scheme.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OpenIdConnectSecurityScheme.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

open\_id\_connect\_url _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OpenIdConnectSecurityScheme.open_id_connect_url "Link to this definition")

The OpenID Connect Discovery URL for the OIDC provider’s metadata.

type _:Literal\['openIdConnect'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OpenIdConnectSecurityScheme.type "Link to this definition")

The type of the security scheme. Must be ‘openIdConnect’.

_class_ a2a.types.Part( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Part "Link to this definition")

Bases: `RootModel[Union[TextPart, FilePart, DataPart]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Part.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [TextPart](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TextPart "a2a.types.TextPart") \| [FilePart](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.FilePart "a2a.types.FilePart") \| [DataPart](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.DataPart "a2a.types.DataPart")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Part.root "Link to this definition")

A discriminated union representing a part of a message or artifact, which can
be text, a file, or structured data.

_class_ a2a.types.PartBase( _\*_, _metadata:dict\[str,Any\]\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PartBase "Link to this definition")

Bases: `A2ABaseModel`

Defines base properties common to all message or artifact parts.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PartBase.metadata "Link to this definition")

Optional metadata associated with this part.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PartBase.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.PasswordOAuthFlow( _\*_, _refreshUrl:str\|None=None_, _scopes:dict\[str,str\]_, _tokenUrl:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PasswordOAuthFlow "Link to this definition")

Bases: `A2ABaseModel`

Defines configuration details for the OAuth 2.0 Resource Owner Password flow.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PasswordOAuthFlow.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

refresh\_url _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PasswordOAuthFlow.refresh_url "Link to this definition")

The URL to be used for obtaining refresh tokens. This MUST be a URL.

scopes _:dict\[str,str\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PasswordOAuthFlow.scopes "Link to this definition")

The available scopes for the OAuth2 security scheme. A map between the scope
name and a short description for it.

token\_url _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PasswordOAuthFlow.token_url "Link to this definition")

The token URL to be used for this flow. This MUST be a URL.

_class_ a2a.types.PushNotificationAuthenticationInfo( _\*_, _credentials:str\|None=None_, _schemes:list\[str\]_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationAuthenticationInfo "Link to this definition")

Bases: `A2ABaseModel`

Defines authentication details for a push notification endpoint.

credentials _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationAuthenticationInfo.credentials "Link to this definition")

Optional credentials required by the push notification endpoint.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationAuthenticationInfo.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

schemes _:list\[str\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationAuthenticationInfo.schemes "Link to this definition")

A list of supported authentication schemes (e.g., ‘Basic’, ‘Bearer’).

_class_ a2a.types.PushNotificationConfig( _\*_, _authentication:[PushNotificationAuthenticationInfo](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationAuthenticationInfo "a2a.types.PushNotificationAuthenticationInfo") \|None=None_, _id:str\|None=None_, _token:str\|None=None_, _url:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationConfig "Link to this definition")

Bases: `A2ABaseModel`

Defines the configuration for setting up push notifications for task updates.

authentication _: [PushNotificationAuthenticationInfo](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationAuthenticationInfo "a2a.types.PushNotificationAuthenticationInfo") \|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationConfig.authentication "Link to this definition")

Optional authentication details for the agent to use when calling the notification URL.

id _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationConfig.id "Link to this definition")

A unique ID for the push notification configuration, set by the client
to support multiple notification callbacks.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationConfig.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

token _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationConfig.token "Link to this definition")

A unique token for this task or session to validate incoming push notifications.

url _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationConfig.url "Link to this definition")

The callback URL where the agent should send push notifications.

_class_ a2a.types.PushNotificationNotSupportedError( _\*_, _code:Literal\[-32003\]=-32003_, _data:Any\|None=None_, _message:str\|None='PushNotificationisnotsupported'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationNotSupportedError "Link to this definition")

Bases: `A2ABaseModel`

An A2A-specific error indicating that the agent does not support push notifications.

code _:Literal\[-32003\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationNotSupportedError.code "Link to this definition")

The error code for when push notifications are not supported.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationNotSupportedError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationNotSupportedError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationNotSupportedError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.Role( _\*values_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Role "Link to this definition")

Bases: `str`, `Enum`

Identifies the sender of the message. user for the client, agent for the service.

agent _='agent'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Role.agent "Link to this definition")user _='user'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Role.user "Link to this definition")_class_ a2a.types.SecurityScheme( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SecurityScheme "Link to this definition")

Bases: `RootModel[Union[APIKeySecurityScheme, HTTPAuthSecurityScheme, OAuth2SecurityScheme, OpenIdConnectSecurityScheme, MutualTLSSecurityScheme]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SecurityScheme.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [APIKeySecurityScheme](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.APIKeySecurityScheme "a2a.types.APIKeySecurityScheme") \| [HTTPAuthSecurityScheme](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.HTTPAuthSecurityScheme "a2a.types.HTTPAuthSecurityScheme") \| [OAuth2SecurityScheme](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OAuth2SecurityScheme "a2a.types.OAuth2SecurityScheme") \| [OpenIdConnectSecurityScheme](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.OpenIdConnectSecurityScheme "a2a.types.OpenIdConnectSecurityScheme") \| [MutualTLSSecurityScheme](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MutualTLSSecurityScheme "a2a.types.MutualTLSSecurityScheme")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SecurityScheme.root "Link to this definition")

Defines a security scheme that can be used to secure an agent’s endpoints.
This is a discriminated union type based on the OpenAPI 3.0 Security Scheme Object.

_class_ a2a.types.SecuritySchemeBase( _\*_, _description:str\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SecuritySchemeBase "Link to this definition")

Bases: `A2ABaseModel`

Defines base properties shared by all security scheme objects.

description _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SecuritySchemeBase.description "Link to this definition")

An optional description for the security scheme.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SecuritySchemeBase.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.SendMessageRequest( _\*_, _id:str\|int_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:Literal\['message/send'\]='message/send'_, _params:[MessageSendParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendParams "a2a.types.MessageSendParams")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC request for the message/send method.

id _:str\|int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageRequest.id "Link to this definition")

The identifier for this request.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:Literal\['message/send'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageRequest.method "Link to this definition")

The method name. Must be ‘message/send’.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _: [MessageSendParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendParams "a2a.types.MessageSendParams")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageRequest.params "Link to this definition")

The parameters for sending a message.

_class_ a2a.types.SendMessageResponse( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageResponse "Link to this definition")

Bases: `RootModel[Union[JSONRPCErrorResponse, SendMessageSuccessResponse]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONRPCErrorResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "a2a.types.JSONRPCErrorResponse") \| [SendMessageSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageSuccessResponse "a2a.types.SendMessageSuccessResponse")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageResponse.root "Link to this definition")

Represents a JSON-RPC response for the message/send method.

_class_ a2a.types.SendMessageSuccessResponse( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _result:[Task](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task "a2a.types.Task") \| [Message](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "a2a.types.Message")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageSuccessResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a successful JSON-RPC response for the message/send method.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageSuccessResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageSuccessResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageSuccessResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

result _: [Task](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task "a2a.types.Task") \| [Message](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "a2a.types.Message")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendMessageSuccessResponse.result "Link to this definition")

The result, which can be a direct reply Message or the initial Task object.

_class_ a2a.types.SendStreamingMessageRequest( _\*_, _id:str\|int_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:Literal\['message/stream'\]='message/stream'_, _params:[MessageSendParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendParams "a2a.types.MessageSendParams")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC request for the message/stream method.

id _:str\|int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageRequest.id "Link to this definition")

The identifier for this request.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:Literal\['message/stream'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageRequest.method "Link to this definition")

The method name. Must be ‘message/stream’.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _: [MessageSendParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.MessageSendParams "a2a.types.MessageSendParams")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageRequest.params "Link to this definition")

The parameters for sending a message.

_class_ a2a.types.SendStreamingMessageResponse( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageResponse "Link to this definition")

Bases: `RootModel[Union[JSONRPCErrorResponse, SendStreamingMessageSuccessResponse]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONRPCErrorResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "a2a.types.JSONRPCErrorResponse") \| [SendStreamingMessageSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageSuccessResponse "a2a.types.SendStreamingMessageSuccessResponse")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageResponse.root "Link to this definition")

Represents a JSON-RPC response for the message/stream method.

_class_ a2a.types.SendStreamingMessageSuccessResponse( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _result:[Task](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task "a2a.types.Task") \| [Message](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "a2a.types.Message") \| [TaskStatusUpdateEvent](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatusUpdateEvent "a2a.types.TaskStatusUpdateEvent") \| [TaskArtifactUpdateEvent](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent "a2a.types.TaskArtifactUpdateEvent")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageSuccessResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a successful JSON-RPC response for the message/stream method.
The server may send multiple response objects for a single request.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageSuccessResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageSuccessResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageSuccessResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

result _: [Task](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task "a2a.types.Task") \| [Message](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "a2a.types.Message") \| [TaskStatusUpdateEvent](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatusUpdateEvent "a2a.types.TaskStatusUpdateEvent") \| [TaskArtifactUpdateEvent](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent "a2a.types.TaskArtifactUpdateEvent")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SendStreamingMessageSuccessResponse.result "Link to this definition")

The result, which can be a Message, Task, or a streaming update event.

_class_ a2a.types.SetTaskPushNotificationConfigRequest( _\*_, _id:str\|int_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:Literal\['tasks/pushNotificationConfig/set'\]='tasks/pushNotificationConfig/set'_, _params:[TaskPushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig "a2a.types.TaskPushNotificationConfig")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC request for the tasks/pushNotificationConfig/set method.

id _:str\|int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigRequest.id "Link to this definition")

The identifier for this request.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:Literal\['tasks/pushNotificationConfig/set'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigRequest.method "Link to this definition")

The method name. Must be ‘tasks/pushNotificationConfig/set’.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _: [TaskPushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig "a2a.types.TaskPushNotificationConfig")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigRequest.params "Link to this definition")

The parameters for setting the push notification configuration.

_class_ a2a.types.SetTaskPushNotificationConfigResponse( _root:RootModelRootType=PydanticUndefined_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigResponse "Link to this definition")

Bases: `RootModel[Union[JSONRPCErrorResponse, SetTaskPushNotificationConfigSuccessResponse]]`

model\_config _:ClassVar\[ConfigDict\]_ _={}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

root _: [JSONRPCErrorResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.JSONRPCErrorResponse "a2a.types.JSONRPCErrorResponse") \| [SetTaskPushNotificationConfigSuccessResponse](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigSuccessResponse "a2a.types.SetTaskPushNotificationConfigSuccessResponse")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigResponse.root "Link to this definition")

Represents a JSON-RPC response for the tasks/pushNotificationConfig/set method.

_class_ a2a.types.SetTaskPushNotificationConfigSuccessResponse( _\*_, _id:str\|int\|None=None_, _jsonrpc:Literal\['2.0'\]='2.0'_, _result:[TaskPushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig "a2a.types.TaskPushNotificationConfig")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigSuccessResponse "Link to this definition")

Bases: `A2ABaseModel`

Represents a successful JSON-RPC response for the tasks/pushNotificationConfig/set method.

id _:str\|int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigSuccessResponse.id "Link to this definition")

The identifier established by the client.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigSuccessResponse.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigSuccessResponse.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

result _: [TaskPushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig "a2a.types.TaskPushNotificationConfig")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.SetTaskPushNotificationConfigSuccessResponse.result "Link to this definition")

The result, containing the configured push notification settings.

_class_ a2a.types.Task( _\*_, _artifacts:list\[ [Artifact](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact "a2a.types.Artifact")\]\|None=None_, _contextId:str_, _history:list\[ [Message](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "a2a.types.Message")\]\|None=None_, _id:str_, _kind:Literal\['task'\]='task'_, _metadata:dict\[str,Any\]\|None=None_, _status:[TaskStatus](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatus "a2a.types.TaskStatus")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task "Link to this definition")

Bases: `A2ABaseModel`

Represents a single, stateful operation or conversation between a client and an agent.

artifacts _:list\[ [Artifact](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact "a2a.types.Artifact")\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task.artifacts "Link to this definition")

A collection of artifacts generated by the agent during the execution of the task.

context\_id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task.context_id "Link to this definition")

A server-generated identifier for maintaining context across multiple related tasks or interactions.

history _:list\[ [Message](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "a2a.types.Message")\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task.history "Link to this definition")

An array of messages exchanged during the task, representing the conversation history.

id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task.id "Link to this definition")

A unique identifier for the task, generated by the server for a new task.

kind _:Literal\['task'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task.kind "Link to this definition")

The type of this object, used as a discriminator. Always ‘task’ for a Task.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task.metadata "Link to this definition")

Optional metadata for extensions. The key is an extension-specific identifier.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

status _: [TaskStatus](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatus "a2a.types.TaskStatus")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Task.status "Link to this definition")

The current status of the task, including its state and a descriptive message.

_class_ a2a.types.TaskArtifactUpdateEvent( _\*_, _append:bool\|None=None_, _artifact:[Artifact](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact "a2a.types.Artifact")_, _contextId:str_, _kind:Literal\['artifact-update'\]='artifact-update'_, _lastChunk:bool\|None=None_, _metadata:dict\[str,Any\]\|None=None_, _taskId:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent "Link to this definition")

Bases: `A2ABaseModel`

An event sent by the agent to notify the client that an artifact has been
generated or updated. This is typically used in streaming models.

append _:bool\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent.append "Link to this definition")

If true, the content of this artifact should be appended to a previously sent artifact with the same ID.

artifact _: [Artifact](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Artifact "a2a.types.Artifact")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent.artifact "Link to this definition")

The artifact that was generated or updated.

context\_id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent.context_id "Link to this definition")

The context ID associated with the task.

kind _:Literal\['artifact-update'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent.kind "Link to this definition")

The type of this event, used as a discriminator. Always ‘artifact-update’.

last\_chunk _:bool\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent.last_chunk "Link to this definition")

If true, this is the final chunk of the artifact.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent.metadata "Link to this definition")

Optional metadata for extensions.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

task\_id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskArtifactUpdateEvent.task_id "Link to this definition")

The ID of the task this artifact belongs to.

_class_ a2a.types.TaskIdParams( _\*_, _id:str_, _metadata:dict\[str,Any\]\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskIdParams "Link to this definition")

Bases: `A2ABaseModel`

Defines parameters containing a task ID, used for simple task operations.

id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskIdParams.id "Link to this definition")

The unique identifier of the task.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskIdParams.metadata "Link to this definition")

Optional metadata associated with the request.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskIdParams.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.TaskNotCancelableError( _\*_, _code:Literal\[-32002\]=-32002_, _data:Any\|None=None_, _message:str\|None='Taskcannotbecanceled'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotCancelableError "Link to this definition")

Bases: `A2ABaseModel`

An A2A-specific error indicating that the task is in a state where it cannot be canceled.

code _:Literal\[-32002\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotCancelableError.code "Link to this definition")

The error code for a task that cannot be canceled.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotCancelableError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotCancelableError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotCancelableError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.TaskNotFoundError( _\*_, _code:Literal\[-32001\]=-32001_, _data:Any\|None=None_, _message:str\|None='Tasknotfound'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotFoundError "Link to this definition")

Bases: `A2ABaseModel`

An A2A-specific error indicating that the requested task ID was not found.

code _:Literal\[-32001\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotFoundError.code "Link to this definition")

The error code for a task not found error.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotFoundError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotFoundError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskNotFoundError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.TaskPushNotificationConfig( _\*_, _pushNotificationConfig:[PushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationConfig "a2a.types.PushNotificationConfig")_, _taskId:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig "Link to this definition")

Bases: `A2ABaseModel`

A container associating a push notification configuration with a specific task.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

push\_notification\_config _: [PushNotificationConfig](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.PushNotificationConfig "a2a.types.PushNotificationConfig")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig.push_notification_config "Link to this definition")

The push notification configuration for this task.

task\_id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskPushNotificationConfig.task_id "Link to this definition")

The ID of the task.

_class_ a2a.types.TaskQueryParams( _\*_, _historyLength:int\|None=None_, _id:str_, _metadata:dict\[str,Any\]\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskQueryParams "Link to this definition")

Bases: `A2ABaseModel`

Defines parameters for querying a task, with an option to limit history length.

history\_length _:int\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskQueryParams.history_length "Link to this definition")

The number of most recent messages from the task’s history to retrieve.

id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskQueryParams.id "Link to this definition")

The unique identifier of the task.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskQueryParams.metadata "Link to this definition")

Optional metadata associated with the request.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskQueryParams.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

_class_ a2a.types.TaskResubscriptionRequest( _\*_, _id:str\|int_, _jsonrpc:Literal\['2.0'\]='2.0'_, _method:Literal\['tasks/resubscribe'\]='tasks/resubscribe'_, _params:[TaskIdParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskIdParams "a2a.types.TaskIdParams")_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskResubscriptionRequest "Link to this definition")

Bases: `A2ABaseModel`

Represents a JSON-RPC request for the tasks/resubscribe method, used to resume a streaming connection.

id _:str\|int_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskResubscriptionRequest.id "Link to this definition")

The identifier for this request.

jsonrpc _:Literal\['2.0'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskResubscriptionRequest.jsonrpc "Link to this definition")

The version of the JSON-RPC protocol. MUST be exactly “2.0”.

method _:Literal\['tasks/resubscribe'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskResubscriptionRequest.method "Link to this definition")

The method name. Must be ‘tasks/resubscribe’.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskResubscriptionRequest.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

params _: [TaskIdParams](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskIdParams "a2a.types.TaskIdParams")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskResubscriptionRequest.params "Link to this definition")

The parameters identifying the task to resubscribe to.

_class_ a2a.types.TaskState( _\*values_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState "Link to this definition")

Bases: `str`, `Enum`

Defines the lifecycle states of a Task.

auth\_required _='auth-required'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState.auth_required "Link to this definition")canceled _='canceled'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState.canceled "Link to this definition")completed _='completed'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState.completed "Link to this definition")failed _='failed'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState.failed "Link to this definition")input\_required _='input-required'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState.input_required "Link to this definition")rejected _='rejected'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState.rejected "Link to this definition")submitted _='submitted'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState.submitted "Link to this definition")unknown _='unknown'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState.unknown "Link to this definition")working _='working'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState.working "Link to this definition")_class_ a2a.types.TaskStatus( _\*_, _message:[Message](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "a2a.types.Message") \|None=None_, _state:[TaskState](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState "a2a.types.TaskState")_, _timestamp:str\|None=None_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatus "Link to this definition")

Bases: `A2ABaseModel`

Represents the status of a task at a specific point in time.

message _: [Message](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.Message "a2a.types.Message") \|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatus.message "Link to this definition")

An optional, human-readable message providing more details about the current status.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatus.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

state _: [TaskState](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskState "a2a.types.TaskState")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatus.state "Link to this definition")

The current state of the task’s lifecycle.

timestamp _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatus.timestamp "Link to this definition")

An ISO 8601 datetime string indicating when this status was recorded.

_class_ a2a.types.TaskStatusUpdateEvent( _\*_, _contextId:str_, _final:bool_, _kind:Literal\['status-update'\]='status-update'_, _metadata:dict\[str,Any\]\|None=None_, _status:[TaskStatus](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatus "a2a.types.TaskStatus")_, _taskId:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatusUpdateEvent "Link to this definition")

Bases: `A2ABaseModel`

An event sent by the agent to notify the client of a change in a task’s status.
This is typically used in streaming or subscription models.

context\_id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatusUpdateEvent.context_id "Link to this definition")

The context ID associated with the task.

final _:bool_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatusUpdateEvent.final "Link to this definition")

If true, this is the final event in the stream for this interaction.

kind _:Literal\['status-update'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatusUpdateEvent.kind "Link to this definition")

The type of this event, used as a discriminator. Always ‘status-update’.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatusUpdateEvent.metadata "Link to this definition")

Optional metadata for extensions.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatusUpdateEvent.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

status _: [TaskStatus](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatus "a2a.types.TaskStatus")_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatusUpdateEvent.status "Link to this definition")

The new status of the task.

task\_id _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TaskStatusUpdateEvent.task_id "Link to this definition")

The ID of the task that was updated.

_class_ a2a.types.TextPart( _\*_, _kind:Literal\['text'\]='text'_, _metadata:dict\[str,Any\]\|None=None_, _text:str_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TextPart "Link to this definition")

Bases: `A2ABaseModel`

Represents a text segment within a message or artifact.

kind _:Literal\['text'\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TextPart.kind "Link to this definition")

The type of this part, used as a discriminator. Always ‘text’.

metadata _:dict\[str,Any\]\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TextPart.metadata "Link to this definition")

Optional metadata associated with this part.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TextPart.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

text _:str_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TextPart.text "Link to this definition")

The string content of the text part.

_class_ a2a.types.TransportProtocol( _\*values_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TransportProtocol "Link to this definition")

Bases: `str`, `Enum`

Supported A2A transport protocols.

grpc _='GRPC'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TransportProtocol.grpc "Link to this definition")http\_json _='HTTP+JSON'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TransportProtocol.http_json "Link to this definition")jsonrpc _='JSONRPC'_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.TransportProtocol.jsonrpc "Link to this definition")_class_ a2a.types.UnsupportedOperationError( _\*_, _code:Literal\[-32004\]=-32004_, _data:Any\|None=None_, _message:str\|None='Thisoperationisnotsupported'_) [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.UnsupportedOperationError "Link to this definition")

Bases: `A2ABaseModel`

An A2A-specific error indicating that the requested operation is not supported by the agent.

code _:Literal\[-32004\]_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.UnsupportedOperationError.code "Link to this definition")

The error code for an unsupported operation.

data _:Any\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.UnsupportedOperationError.data "Link to this definition")

A primitive or structured value containing additional information about the error.
This may be omitted.

message _:str\|None_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.UnsupportedOperationError.message "Link to this definition")

The error message.

model\_config _:ClassVar\[ConfigDict\]_ _={'alias\_generator':<functionto\_camel\_custom>,'serialize\_by\_alias':True,'validate\_by\_alias':True,'validate\_by\_name':True}_ [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html#a2a.types.UnsupportedOperationError.model_config "Link to this definition")

Configuration for the model, should be a dictionary conforming to \[ConfigDict\]\[pydantic.config.ConfigDict\].

## Module contents [¶](https://a2a-protocol.org/latest/sdk/python/api/a2a.html\#module-a2a "Link to this heading")

The A2A Python SDK.