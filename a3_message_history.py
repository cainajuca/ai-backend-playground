from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

load_dotenv()

chat = ChatOpenAI(model='gpt-3.5-turbo')

chat_history = []

system_message = SystemMessage(content="Você é um assistente útil que responde perguntas.")
chat_history.append(system_message)

while True:
    query = input("Digite sua pergunta (ou 'sair' para encerrar): ")
    if query.lower() == 'sair':
        break

    chat_history.append(HumanMessage(content=query))

    result = chat.invoke(chat_history)
    response = result.content

    chat_history.append(AIMessage(content=response))
    print(f"Resposta: {response}")

print("---- Histórico de Mensagens ----")
print(chat_history)