from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from PIL import Image
import io
import os

app = FastAPI()

# Allow React to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
# TIP: Best practice is to use os.getenv, but for now hardcoding is fine for testing
genai.configure(api_key="AIzaSyCRpLKi0upCAa966o_3tPwM02wvfr_nGzI") 
model = genai.GenerativeModel('gemini-2.5-flash')

@app.post("/solve")
async def solve_equation(file: UploadFile = File(...)):
    try:
        print("Receiving image...")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        prompt = (
            "You are a math tutor. "
            "I have drawn a math problem in GREEN ink on a digital canvas. "
            "1. Identify the equation or problem exactly. "
            "2. Solve it step-by-step. "
            "3. Use LaTeX formatting for all math expressions (enclose them in $ signs). "
            "4. Be concise and clear."
        )
        response = model.generate_content([prompt, image])
        
        print("Solved!")
        return {"solution": response.text}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))