
import httpx
from fastapi import HTTPException


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"


async def generate_response(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    timeout = httpx.Timeout(
        connect=10.0,
        read=300.0,
        write=10.0,
        pool=10.0
    )

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OLLAMA_URL,
                json=payload
            )

            response.raise_for_status()

        data = response.json()
        generated_text = data.get("response")

        if not isinstance(generated_text, str) or not generated_text.strip():
            raise HTTPException(
                status_code=502,
                detail="The AI service returned an empty or invalid response."
            )

        return generated_text

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="The AI service took too long to respond. Please try again."
        )

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="The AI service is unavailable. Please ensure Ollama is running."
        )

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="The AI service returned an HTTP error."
        )

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=502,
            detail="The AI service returned an invalid response."
        )
