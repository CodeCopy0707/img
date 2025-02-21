from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import DiffusionPipeline
from io import BytesIO
from PIL import Image
import base64
import torch

# Initialize FastAPI app
app = FastAPI()

# Load the Stable Diffusion model from Hugging Face
model_id = "stabilityai/stable-diffusion-3.5-large"
pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")  # Use GPU if available

# Pydantic model to define request structure
class PromptRequest(BaseModel):
    prompt: str

# API Endpoint: Generate image from prompt
@app.post("/generate")
async def generate_image(request: PromptRequest):
    try:
        # Generate image from prompt
        prompt = request.prompt
        image = pipe(prompt).images[0]

        # Convert the image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Return the image as base64
        return {"image": img_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")