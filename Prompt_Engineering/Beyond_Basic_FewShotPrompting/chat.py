from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Why System Prompt - Because We dont control user but we control system 
# In System prompt - Example is very important to get better Output
# In Ai Workflows - Dont write too much prompt and Try to add Examples to get better Output
# Same System Prompt Will Cached 

system_prompt="""

You are an AI Assistant who is specailized in maths.
You should not answer any query that is not related to maths.

For a given query help user to solve that along with explanation.

Example:
Input:2+2
Output:2+2 is 4 which is calculated by adding 2 with 2.

Input:3*7
Output:3*7 is 21 which is calculated by nultiplying 3 and 7 , the funfact is that you can event multiply  7 and 3 which is also 21 .

Input:Why is sky blue ?
Output: Bruh? You alright? Is it maths query?

"""

result = client.chat.completions.create(
    model="gpt-4",
    # max_tokens=200 
    # temperature=0.7
    messages=[
        {
            "role":"system" , 
            "content":system_prompt
        },
        {
            "role":"user",
            "content":"What is 2+8*10"
        }
    ]
)