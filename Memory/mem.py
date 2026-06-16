from mem0 import Memory
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()


# xai
API_KEY = os.getenv("XAI_API_KEY")
BASE_URL = "https://api.x.ai/v1"
MODEL = "grok-3-mini"

# GROQ 
# API_KEY = os.getenv("GROQ_API_KEY")
# BASE_URL = "https://api.groq.com/openai/v1"
# MODEL = "llama-3.1-8b-instant"

# GEMINI (OpenAI Compatible) 
# API_KEY = os.getenv("GEMINI_API_KEY")
# BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
# MODEL = "gemini-2.5-flash"



# Memory configs

config = {
    "version": "v1.1",

    "embedder": {
        "provider": "fastembed",
        "config": {
            "model": "BAAI/bge-small-en-v1.5"
        }
    },

    "llm": {
        "provider": "xai",
        "config": {
            "api_key": os.getenv("XAI_API_KEY"),
            "model": "grok-3-mini"
        }
    },

    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    },

    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "password"
        }
    }
}


mem_client = Memory.from_config(config)


# set as default to avoid mismatch here 
mem_client.vector_store.embedding_model_dims = 384


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


def chat(message):

# here actually the same things happens that retrival Part okk , it is just an abstarction 

    mem_result = mem_client.search(query=message,userid="ng100") 
    # print(mem_result.get("results"));

    memories = "\n".join([m["memory"] for m in mem_result.get('results')]);
    print(memories)
    
    SYSTEM_PROMPT = f"""

    You are a **Memory-Aware Fact Extraction Agent**, an advanced AI system designed to systematically analyze user input, extract structured knowledge, and maintain an optimized memory store.

Your primary objective is to identify, extract, and preserve important facts, preferences, relationships, goals, experiences, and personal details that may be useful in future interactions.

### Responsibilities

* Analyze the input content carefully.
* Extract factual information and long-term user preferences.
* Identify entities, relationships, and relevant contextual details.
* Avoid storing temporary, irrelevant, or redundant information.
* Update existing memories when new information supersedes previous knowledge.
* Preserve important contextual information for future retrieval.

### Memory Rules

* Store information only if it has long-term value.
* Do not store trivial conversational details.
* Merge duplicate memories when possible.
* Prefer concise, structured facts over verbose summaries.
* Maintain consistency with previously stored memories.

### Response Style

* Professional
* Analytical
* Precision-focused
* Context-aware
* Structured and concise

### Existing Memories

{memories}

    """    

    messages = [
        {
            "role":"system",
            "content":SYSTEM_PROMPT

        },
        {
            "role": "user",
            "content": message
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    assistant_response = response.choices[0].message.content

    messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

    # memory saving 
    mem_client.add(
        messages,
        user_id="ng100"
    )

    return assistant_response


while True:

    message = input(">> ")

    if message.lower() in ["exit", "quit"]:
        print("Goodbye")
        break

    try:
        print("BOT:", chat(message))

    except Exception as e:
        print("ERROR:", e)
