import openai

# Set up the OpenAI client with your Azure endpoint and API key
openai.api_type = "azure"
openai.api_key = "mcOZ1fI1JChD4P0fyyp84wEb6dJ0iIBWaSfOALNXXWwSfjj5mM7gJQQJ99AKACHYHv6XJ3w3AAAAACOGH5AI"
openai.api_base = "https://alach-m3n4py1o-eastus2.cognitiveservices.azure.com/"
openai.api_version = "2023-05-15"

from langchain_openai import AzureOpenAIEmbeddings

# Initialize Azure OpenAI Embeddings
embeddings = AzureOpenAIEmbeddings(
    # azure_deployment="your-deployment-name",  # The name you gave to your embeddings deployment in Azure
    openai_api_version="2023-05-15",
    azure_endpoint="https://alach-m3n4py1o-eastus2.cognitiveservices.azure.com/",
    api_key="mcOZ1fI1JChD4P0fyyp84wEb6dJ0iIBWaSfOALNXXWwSfjj5mM7gJQQJ99AKACHYHv6XJ3w3AAAAACOGH5AI"
)

# Example texts
text = "Hello, this is a test sentence."
texts = ["Hello, this is sentence 1.", "This is another sentence.", "And a third one."]

# Get embeddings for a single text
single_embedding = embeddings.embed_documents(text).tolist()
print(f"Single embedding dimension: {len(single_embedding)}")  # Should be 1536 for ada-002
print(single_embedding)
# Get embeddings for multiple texts
# multiple_embeddings = embeddings.embed_documents(texts)
# print(f"Number of embeddings: {len(multiple_embeddings)}")  # Should be 3
# print(f"Each embedding dimension: {len(multiple_embeddings[0])}")  # Should be 1536