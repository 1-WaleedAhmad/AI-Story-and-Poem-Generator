from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "https://your-google-cloud-llm-service-url.com/generate")

class GenerateRequest(BaseModel):
    prompt: str
    type: str = "story"
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9

class GenerateResponse(BaseModel):
    result: str

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    Forward the generation request to the external LLM service.
    """
    try:
        # Prepare the payload for the LLM service
        # Adjust the payload structure based on what your Colab/Cloud service expects
        payload = {
            "prompt": request.prompt,
            "max_length": 500,  # You might want to make this configurable too
            "temperature": request.temperature,
            "top_k": request.top_k,
            "top_p": request.top_p,
            "do_sample": True
        }
        
        # Add specific instructions based on type
        if request.type == "poem":
            payload["prompt"] = f"Write a poem about: {request.prompt}"
        
        async with httpx.AsyncClient() as client:
            # This assumes the LLM service accepts a POST request with JSON
            # You might need to adjust headers or authentication if needed
            response = await client.post(
                LLM_SERVICE_URL, 
                json=payload, 
                timeout=60.0  # LLMs can take time
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"LLM Service Error: {response.text}")
            
            data = response.json()
            
            # Adjust this based on the actual response structure from your LLM service
            # For example, if it returns {"generated_text": "..."}
            generated_text = data.get("generated_text", "") or data.get("result", "") or str(data)
            
            return GenerateResponse(result=generated_text)

    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Error communicating with LLM service: {exc}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
