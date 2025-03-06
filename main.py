import asyncio
import os
from typing import AsyncGenerator, List, Optional, Union, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel
from starlette.responses import JSONResponse

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[dict] = None
    user: Optional[str] = None


async def proxy_openai_stream(request: ChatRequest) -> AsyncGenerator[str, None]:
    try:
        response = client.chat.completions.create(**request.model_dump(exclude={"stream": True}), stream=True)
        if request.stream:
            for chunk in response:
                yield f"data: {chunk.model_dump_json()}\n\n"
                await asyncio.sleep(0)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def proxy_openai(request: ChatRequest) -> JSONResponse:
    response = client.chat.completions.create(**request.model_dump(exclude={"stream": True}), stream=False)
    return JSONResponse(content=response.to_dict())


@app.post("/chat/completions")
async def chat(request: ChatRequest):
    if request.stream:
        return StreamingResponse(proxy_openai_stream(request), media_type="text/event-stream")
    return proxy_openai(request)


@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})
