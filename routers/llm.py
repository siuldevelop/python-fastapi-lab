import os

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/llm",tags=["llm"])

class Question(BaseModel):
    prompt: str = Field(min_length=1)

@router.post("/ask")
async def ask(question: Question):
    # La integración queda desactivada hasta que se configure un proveedor.
    # Esto evita llamadas accidentales y costos durante el desarrollo académico.
    llm_url = os.getenv("LLM_API_URL")
    if not llm_url:
        raise HTTPException(
            status_code=503,
            detail="LLM no configurado. Define LLM_API_URL para habilitarlo.",
        )

    headers = {}
    api_key = os.getenv("LLM_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                llm_url,
                json={"prompt": question.prompt},
                headers=headers,
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="No se pudo contactar al proveedor LLM.",
        ) from exc

    return response.json()
