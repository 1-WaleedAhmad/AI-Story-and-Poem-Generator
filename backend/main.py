from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline, set_seed
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the model
# We use distilgpt2 for faster local inference on CPU, or gpt2
print("Loading model...")
generator = pipeline('text-generation', model='gpt2')
print("Model loaded!")

class GenerateRequest(BaseModel):
    prompt: str
    type: str = "story"
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9
    max_new_tokens: int = 150

class GenerateResponse(BaseModel):
    result: str

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    Generate text locally using Hugging Face Transformers.
    """
    try:
        # Construct a prompt based on the type
        input_prompt = request.prompt
        if request.type == "poem":
            input_prompt = f"Write a poem about {request.prompt}:\n"
        elif request.type == "story":
            input_prompt = f"Story about {request.prompt}:\n"

        # Generate text
        # set_seed(42) # Optional: for reproducibility
        
        output = generator(
            input_prompt, 
            max_length=len(input_prompt) + request.max_new_tokens, 
            num_return_sequences=1,
            temperature=request.temperature,
            top_k=request.top_k,
            top_p=request.top_p,
            do_sample=True,
            truncation=True
        )
        
        generated_text = output[0]['generated_text']
        
        # Clean up the prompt from the result if desired, or keep it
        # For now we return the whole thing or just the new part. 
        # Usually users like to see the continuation.
        
        # If we want to strip the prompt prefix we added:
        if request.type == "poem" and generated_text.startswith(input_prompt):
            generated_text = generated_text[len(input_prompt):].strip()
        elif request.type == "story" and generated_text.startswith(input_prompt):
             generated_text = generated_text[len(input_prompt):].strip()

        return GenerateResponse(result=generated_text)

    except Exception as e:
        print(f"Error generating text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "gpt2"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
