from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import httpx
import os

app = FastAPI()

# Request & Response Models
class EvalRequest(BaseModel):
    input: str
    output: str
    criteria: str

class EvalResponse(BaseModel):
    success: bool
    explanation: str
    confidence: Optional[float] = None  # Optional as per spec

# LLM Config 
API_KEY = "" #Set your openrouter API key over here or use it as env vars - os.getenv("OPENROUTER_API_KEY")
#MODEL = "deepseek/deepseek-chat-v3-0324:free"
MODEL = "deepseek/deepseek-r1:free" # Use any model of your choice
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# LLM Evaluation Logic
async def call_judge_llm(data: EvalRequest) -> EvalResponse:
    prompt = f"""
    Evaluate if the output is correct based on the input and the given criteria.

    Input: {data.input}
    Output: {data.output}
    Criteria: {data.criteria}

    Reply with: PASS: <explanation> or FAIL: <explanation>
    """

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                API_URL,
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )

        print("[DEBUG] Status code:", response.status_code)
        print("[DEBUG] Response text:", response.text)

        if response.status_code == 402:
            raise HTTPException(status_code=502, detail="Insufficient credits for LLM usage.")
        if response.status_code == 429:
            raise HTTPException(status_code=502, detail="LLM rate-limited. Try again later.")
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail="LLM returned an error.")

        data_json = response.json()

        if "choices" not in data_json:
            raise HTTPException(status_code=500, detail="Invalid LLM response format.")

        content = data_json["choices"][0]["message"]["content"]

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LLM timed out.")
    except httpx.RequestError as e:
        print("[ERROR] Network error:", e)
        raise HTTPException(status_code=502, detail="LLM request failed.")
    except Exception as e:
        print("[ERROR] Unexpected error:", e)
        raise HTTPException(status_code=500, detail="Unexpected error calling LLM.")

    # Parse result
    if content.startswith("PASS:"):
        return EvalResponse(success=True, explanation=content[5:].strip())
    elif content.startswith("FAIL:"):
        return EvalResponse(success=False, explanation=content[5:].strip())
    else:
        return EvalResponse(success=False, explanation="Could not interpret LLM response.")

# API Endpoint
@app.post("/evaluate", response_model=EvalResponse)
async def evaluate(request: Request, body: EvalRequest):
    # Check content length
    content_length = int(request.headers.get("content-length", 0))
    if content_length > 1_000_000:
        raise HTTPException(status_code=413, detail="Payload too large (1MB max).")
    if content_length < 1024:
        raise HTTPException(status_code=411, detail="Payload too small (min 1KB).")

    return await call_judge_llm(body)
