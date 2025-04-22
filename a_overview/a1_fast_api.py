from a1_simplest_gpt_call import chain
from fastapi import FastAPI
from langserve import add_routes

app = FastAPI(title="Meu app de IA", description="Traduza o texto que você quiser para qualquer idioma!")

add_routes(app, chain, path="/tradutor")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

# access through a Post in localhost:8000/tradutor/invoke
# with body {"idioma": "frances", "texto": "Olá, mundo! Como você está?"}

# test in localhost:8000/tradutor/playground