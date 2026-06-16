import json
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

# from langsmith.wrappers import wrap_gemini
from langsmith.wrappers import wrap_openai

from langsmith import traceable


load_dotenv()

client = wrap_openai(
    OpenAI(
        api_key=os.getenv("GOOGLE_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)


@traceable
def run_command(cmd):
    result = os.system(command=cmd)
    return result

@traceable
def get_weather(city:str):
    print("tool called", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} in {response.text}."
    return "Something went wrong"


available_tools={
    "get_weather":{
        "fn":get_weather,
        "decription":"takes the city name as input and returns the current weather of city"
    },
    "run_command":{
        "fn":run_command,
        "description":"takes a command as input to execute on system and returns output"
    }
}


system_prompt = f"""

You are an helpful AI Assistant who is specialised in resolving user query.
You work on start , plan , action , observe mode
For the given user query and avaialble tools , plan the step by step execution based on planning
select the relevant tools from the available tool and based on the tool selection you perform an action to call the tool
Wait for the observation from the tool call resolve the user  query


Rules:
- Follow the Output JSON format
- Always perform one step at a time and wait for next input 
- Carefully analyse the user query 

Output JSON format:

{{
"step":"string",
"content":"string",
"function":"the name of function if step is action",
"input":"the input parameter for a function"
}}

Available_Tools:
- get_weather:Takes the city name as input and returns the current weather of city
- run_command:takes a command as input to execute on system and returns output


Example:

UserQuery: What is the weather of NewYork ?
Output:{{"step":"plan","content":"The user interested in weather of data of NewYork"}}
Output:{{"step":"plan","content":"from the available tools i should call get_weather"}}
Output:{{"step":"action",function:"get_weather","input":"NewYork"}}
Output:{{"step":"observe",output:"12 degree celcius"}}
Output:{{"step":"output","content":"The weather for NewYork seems to be 12 degree}}


"""



messages = [{
            "role":"system",
            "content":system_prompt
}]

while True:
    
    user_query = input("> ")
    messages.append({
    "role":"user",
    "content":user_query
})

    while True:
        response = client.chat.completions.create(
        # model="gpt-4o",
        model="gemini-2.5-flash",
        response_format={"type":"json_object"},
        messages=messages
    )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({
        "role":"assistant",
        "content":json.dumps(parsed_output)
    })

#  Now we have to put our if-else - most important step 

        if parsed_output.get("step") == "plan":
          print(f"Think:{parsed_output.get("content")}")
          continue

        
        if parsed_output.get("step") == "action":
          tool_name = parsed_output.get("function")
          tool_input = parsed_output.get("input")

          
          if available_tools.get(tool_name,False)!=False:
               output = available_tools[tool_name].get("fn")(tool_input)
               messages.append({
                "role":"assistant",
                "content":json.dumps({"step":"observe","output":output})
            })
               
               continue

        if parsed_output.get("step")=="output":
         print(f"Result:{parsed_output.get("content")}")    
         break





