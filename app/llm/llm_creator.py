from app.llm.openai import  AzureOpenAILLM



class LLMCreator:
    def __init__(self):
        pass

    
    llms = {
        "azure": AzureOpenAILLM
    }
    
    @classmethod
    def create_llm(cls, type, api_key, user_api_key, *args, **kwargs):
        llm_class = cls.llms.get(type.lower())
        if not llm_class:
            raise ValueError(f"No LLM class found for type {type}")
        return llm_class(api_key, user_api_key, *args, **kwargs)
