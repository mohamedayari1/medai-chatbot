from app.llm.base import BaseLLM
from app.core.settings import settings


class AzureOpenAILLM(BaseLLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        from openai import AzureOpenAI

        self.client = AzureOpenAI(
            api_version=settings.OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY
        )
        # import openai
        # # Set up the OpenAI client with your Azure endpoint and API key
        # openai.api_type = "azure"
        # openai.api_key = settings.AZURE_OPENAI_API_KEY
        # openai.api_base = settings.AZURE_OPENAI_ENDPOINT
        # openai.api_version = settings.OPENAI_API_VERSION

        # self.client = openai  # Use the configured openai client


    def _raw_gen(
        self,
        model,
        messages,
        stream=False,
        **kwargs
    ):          

 
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream,
            **kwargs
        )
        return response.choices[0].message.content
