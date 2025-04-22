from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from datasets import load_dataset
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Sumário
# Iteração 1: Carregar o modelo e fazer uma pergunta simples
# Iteração 2: Adicionar contexto e fazer uma pergunta mais complexa
# Iteração 3: Adicionar mais contexto e fazer uma pergunta mais complexa
# Iteração 4: Adicionar um banco de dados vetorial e fazer uma pergunta mais complexa

chat = ChatOpenAI(model='gpt-3.5-turbo')

messages = [
    SystemMessage(content="Você é um assistente útil que responde perguntas."),
    HumanMessage(content="Olá Bot, como você está hoje?"),
    AIMessage(content="Estou bem, obrigado. Como posso ajudar?"),
    HumanMessage(content="Gostaria de entender o que é machine learning.")
]

# Interação 1
res = chat.invoke(messages)
messages.append(res)

# Interação 2
prompt = HumanMessage(content="Qual é a diferença entre supervisionado e não supervisionado?")
messages.append(prompt)
res = chat.invoke(messages)
messages.append(res)

# Interação 3
llmchain_information = [
    "A LLMChain is the most common type of chain. It consists of a PromptTemplate, a model (either an LLM or a ChatModel), and an optional output parser. This chain takes multiple input variables, uses the PromptTemplate to format them into a prompt. It then passes that to the model. Finally, it uses the OutputParser (if provided) to parse the output of the LLM into a final format.",
    "Chains is an incredibly generic concept which returns to a sequence of modular components (or other chains) combined in a particular way to accomplish a common use case.",
    "LangChain is a framework for developing applications powered by language models. We believe that the most powerful and differentiated applications will not only call out to a language model via an api, but will also: (1) Be data-aware: connect a language model to other sources of data, (2) Be agentic: Allow a language model to interact with its environment. As such, the LangChain framework is designed with the objective in mind to enable those types of applications."
]

source_knowledge = "\n".join(llmchain_information)

query = "Você pode me falar sobre o LLMChain no LangChain?"

augmented_prompt = f"""
    Use o contexto abaixo para responder à pergunta.

    Contexto:
    {source_knowledge}

    Pergunta: {query}
"""

prompt = HumanMessage(
    content=augmented_prompt
)

messages.append(prompt)
res = chat.invoke(messages)

# Interação 4

dataset = load_dataset("infoslack/mistral-7b-arxiv-paper-chunked", split="train") # base de informações para servir de Contexto
data = dataset.to_pandas()
docs = data[['chunk', 'source']]

# Converte o DataFrame em uma lista de documentos do LangChain
loader = DataFrameLoader(docs, page_content_column="chunk")
documents = loader.load()

embed_model = OpenAIEmbeddings(model="text-embedding-3-small")
qdrant = Qdrant.from_documents(
    documents=documents,
    embedding=embed_model,
    location=":memory:", # banco vetorial Qdrant em memória (não persistente)
    collection_name="chatbot"
)

query = "O que tem de tão especial no Mistral 7B?"
qdrant.similarity_search(query, k=3) # Busca os 3 documentos mais similares ao query

def custom_prompt(query: str):
    results = qdrant.similarity_search(query, k=3)
    source_knowledge = "\n".join([x.page_content for x in results])
    augment_prompt = f"""
        Use o contexto abaixo para responder à pergunta.

        Contexto:
        {source_knowledge}

        Pergunta: {query}
    """

    return augment_prompt

print(custom_prompt(query))

prompt = HumanMessage(
    content=custom_prompt(query)
)

messages.append(prompt)

res = chat.invoke(messages)

print(res.content)

# Trecho de código para usar o Groq como LLM
# Promete ser mais rápido e mais barato que o OpenAI

# from langchain_groq import ChatGroq

# chat = ChatGroq(temperature=0, model_name="llama-3.1-70b-versatile")
# prompt = HumanMessage(
#     content=custom_prompt(query)
# )

# messages.append(prompt)
# res = chat.invoke(messages)
# print(res.content)