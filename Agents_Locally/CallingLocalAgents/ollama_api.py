from fastapi import FastAPI
from ollama import Client

# This is for taking message from the Body 
from fastapi import Body 

app = FastAPI()

client = Client(
    host='http://localhost:11434'
)

client.pull('gemma3:1b')

@app.post("/chat")

# This one has no body

# def chat():
#     response = client.chat(model='gemma3:1b',messages=[{
#         "role":"user",
#         "content":"hey there "
#     }])

#     return response['message']['content']


# This one has no body
def chat(msg:str = Body(...,description="Chat Message")):
    response = client.chat(model='gemma3:1b',messages=[
        {
            "role":"user",
            "content":msg
        }
    ])

    return response['message']['content']