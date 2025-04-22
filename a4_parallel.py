from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain_openai import ChatOpenAI

load_dotenv()

systemMessageTuple = ("system", "Você é um analisador profissional de produtos.")
model = ChatOpenAI(model="gpt-3.5-turbo")

prompt_template = ChatPromptTemplate.from_messages(
    [
        systemMessageTuple,
        ("human", "Liste as principais funcionalidades do produto: {product_name}"),
    ]
)

def analyze_pros(features):
    pros_template = ChatPromptTemplate.from_messages(
        [
            systemMessageTuple,
            ("human", "Dadas essas funcionalidades: {features}, liste os prós dessas funcionalidades"),
        ]
    )
    return pros_template.format_prompt(features=features)

def analyze_cons(features):
    cons_template = ChatPromptTemplate.from_messages(
        [
            systemMessageTuple,
            ("human", "Dadas essas funcionalidades: {features}, liste os contras dessas funcionalidades"),
        ]
    )
    return cons_template.format_prompt(features=features)

def combine_pros_cons(pros, cons):
    return f"Prós:\n{pros}\n\nContras:\n{cons}"

pros_branch = (RunnableLambda(lambda x: analyze_pros(x)) | model | StrOutputParser())

cons_branch = (RunnableLambda(lambda x: analyze_cons(x)) | model | StrOutputParser())

chain = (
    prompt_template
    | model
    | StrOutputParser()
    | RunnableParallel(branches={"pros": pros_branch, "cons": cons_branch})
    | RunnableLambda(lambda x: combine_pros_cons(x["branches"]["pros"], x["branches"]["cons"])))

result = chain.invoke({"product_name": "Samsung Galaxy S25"})

print(result)