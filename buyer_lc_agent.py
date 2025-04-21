from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

modelo = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)
parser = StrOutputParser()

template_mensagem = ChatPromptTemplate.from_messages(
    [
        ("system", "Traduza o texto a seguir para {idioma}."),
        ("user", "{texto}"),
    ]
)

chain = template_mensagem | modelo | parser

texto = chain.invoke({
    "idioma": "frances",
    "texto": "Olá, mundo! Como você está?",
})

print(texto)
