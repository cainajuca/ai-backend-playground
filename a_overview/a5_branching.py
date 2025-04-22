from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableBranch
from langchain_openai import ChatOpenAI

load_dotenv()

systemMessageTuple = ("system", "Você é um assistente útil que responde feedbacks.")
model = ChatOpenAI(model="gpt-3.5-turbo")

positive_feedback_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente útil que responde feedbacks."),
        ("user", "Gere uma resposta em agradecimento por este feedback positivo: {feedback}"),
    ]
)

negative_feedback_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente útil que responde feedbacks."),
        ("user", "Gere uma resposta para este feedback negativo: {feedback}"),
    ]
)

neutral_feedback_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente útil que responde feedbacks."),
        ("user", "Gere uma resposta perguntando por mais detalhes para este feedback: {feedback}"),
    ]
)

escalate_feedback_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente útil que responde feedbacks."),
        ("user", "Gere uma mensagem para encaminhar esse feedback a um atendente humano: {feedback}"),
    ]
)

classification_template = ChatPromptTemplate.from_messages(
    [
        systemMessageTuple,
        ("user", "Classifique o feedback a seguir como positivo, negativo, neutro ou escalate: {feedback}"),
    ]
)

branches = RunnableBranch(
    (
        lambda x: "positivo" in x,
        positive_feedback_template | model | StrOutputParser()
    ),
    (
        lambda x: "negativo" in x,
        negative_feedback_template | model | StrOutputParser()
    ),
    (
        lambda x: "neutro" in x,
        neutral_feedback_template | model | StrOutputParser()
    ),
    escalate_feedback_template | model | StrOutputParser()
)

classification_chain = classification_template | model | StrOutputParser()

chain = classification_chain | branches

# Exemplos:
# Bom: "O produto é incrível!"
# Ruim: "O produto não funcionou como esperado."
# Neutro: "O produto é bom, mas poderia ser melhor."
# Escalar: "Preciso de ajuda com o produto, não consigo resolver o problema."

review = "Preciso de ajuda com o produto, não consigo resolver o problema."
response = chain.invoke({"feedback": review})

# Output
print(f"Feedback: {review}")
print(f"Resposta: {response}")