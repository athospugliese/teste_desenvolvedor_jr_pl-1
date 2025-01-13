import os
from langchain_openai import OpenAI


class LLMService:
    """
    Serviço para interagir com um modelo de linguagem grande (LLM), permitindo a geração de resumos.
    """

    def __init__(self):
        """
        Inicializa o serviço de LLM com as configurações específicas.
        """
        self.llm = OpenAI(
            temperature=0.5,
            top_p=0.7,
            api_key=os.getenv("HF_TOKEN"),
            base_url="https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct/v1",
        )
        self.prompts = {
            "pt": "Leia o texto abaixo e resuma-o de forma clara e objetiva em português. Evite misturar palavras de outros idiomas.",
            "en": "Read the text below and summarize it clearly and concisely in English. Avoid using words from other languages.",
            "es": "Lee el texto a continuación y resúmelo de manera clara y concisa en español. Evita usar palabras de otros idiomas.",
        }

    def summarize_text(self, text: str, lang: str) -> str:
        """
        Gera um resumo do texto fornecido no idioma especificado.

        Args:
            text (str): Texto original a ser resumido.
            lang (str): Código do idioma desejado para o resumo ("pt", "en", "es").

        Returns:
            str: Resumo gerado no idioma solicitado.

        Raises:
            ValueError: Se o idioma especificado não for suportado.
            RuntimeError: Se ocorrer um erro ao invocar o modelo.
        """
        if lang not in self.prompts:
            raise ValueError(f"Unsupported language: {lang}")

        prompt = f"{self.prompts[lang]}\n\nTexto:\n{text}"
        return self._invoke_llm(prompt)

    def _invoke_llm(self, prompt: str) -> str:
        """
        Invoca o modelo de linguagem grande com o prompt fornecido.

        Args:
            prompt (str): Instruções detalhadas para o modelo.

        Returns:
            str: Resposta do modelo processada.

        Raises:
            RuntimeError: Se ocorrer um erro na chamada ao modelo.
        """
        try:
            response = self.llm.invoke(prompt)
            return response.strip()
        except Exception as e:
            raise RuntimeError(f"Error invoking LLM: {str(e)}")
