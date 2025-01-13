from services.llm_service import LLMService
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path = sys.path + ["./app"]


app = FastAPI()
llm_service = LLMService()


class TextData(BaseModel):
    text: str
    lang: str


@app.post("/summarize")
async def summarize(data: TextData):
    """
    Endpoint para resumir texto com base no idioma especificado.

    Args:
        data (TextData): Objeto contendo o texto a ser resumido e o idioma (lang).

    Returns:
        dict: Um dicionário com o resumo do texto.

    Raises:
        HTTPException: Se o idioma não for suportado ou se ocorrer um erro ao gerar o resumo.
    """
    text = data.text
    lang = data.lang

    # Idiomas suportados
    supported_languages = ["pt", "en", "es"]
    if lang not in supported_languages:
        raise HTTPException(status_code=400, detail="Language not supported")

    try:
        # Gerar o resumo com base no texto e idioma
        summary = llm_service.summarize_text(text, lang)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating summary: {str(e)}")


@app.get("/")
async def root():
    """
    Endpoint principal para verificar o status da API.

    Returns:
        dict: Mensagem indicando que a API está funcionando.
    """
    return {"message": "API is running"}
