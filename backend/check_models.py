import google.generativeai as genai
import os

# Paste your API key here directly for this test
genai.configure(api_key="AIzaSyCRpLKi0upCAa966o_3tPwM02wvfr_nGzI")

print("Listing available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)