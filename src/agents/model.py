from langchain.chat_models import init_chat_model


# Azure OpenAI 모델 설정
configurable_azure_model = init_chat_model(
    model_provider='azure_openai',
    configurable_fields=(
        'model',
        'azure_endpoint',
        'azure_deployment',
        'temperature',
        'api_version',
        'api_key',
    ),
    temperature=0.0,
)

# 기존 configurable_model (다른 provider와 함께 사용)
configurable_model = init_chat_model(
    configurable_fields=('model', 'max_tokens', 'api_key', 'temperature'),
)


"""example
model_config = {
    "model": configurable.research_model,
    "max_tokens": configurable.research_model_max_tokens,
    "api_key": get_api_key_for_model(configurable.research_model, config),
    "tags": ["langsmith:nostream"]
}

# Configure model with structured output and retry logic
clarification_model = (
    configurable_model
    .with_structured_output(ClarifyWithUser)
    .with_retry(stop_after_attempt=configurable.max_structured_output_retries)
    .with_config(model_config)
)
"""
