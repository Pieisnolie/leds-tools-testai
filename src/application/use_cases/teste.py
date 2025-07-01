# filepath: [teste.py](http://_vscodecontentref_/1)
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
print("API KEY:", os.getenv("GOOGLE_API_KEY"))

response = completion(
    model="gemini-1.5-flash",
    messages=[{"role": "user", "content": "Diga oi"}],
    api_key=os.getenv("GOOGLE_API_KEY"),
    provider="google"  # <- ESSA LINHA É OBRIGATÓRIA PARA USAR API KEY
)
print(response)
