from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

text = "The sky is good but not as good as water"

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text
)

embeddings = response.embeddings[0].values

print(len(embeddings))
print(embeddings[:10])

