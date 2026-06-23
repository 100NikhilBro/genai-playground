from typing_extensions import TypedDict

from typing import Literal

from langgraph.graph import StateGraph , START, END

from langsmith.wrappers import wrap_openai
# from langsmith.wrappers import wrap_gemini

from openai import OpenAI
# from google import genai

from pydantic import BaseModel   # This is the Zod of python - so we made the Schema here 



class DetectCallResponse(BaseModel):
    is_question_ai:bool


class CodingAiResponse(BaseModel):
    ans:str
        


from dotenv import load_dotenv

load_dotenv()


client = wrap_openai(OpenAI())

# client = wrap_gemini(
#     genai.Client()
# )

class State(TypedDict):
    user_msg:str
    ai_msg:str
    is_coding_qn:bool



def detect_query(state:State):

    user_msg = state.get("user_msg")


    SYSTEM_PROMPT = """
     You are an AI assistant. Your job is to detect if the user's query is related to coding question or not.
     Return the response in specified JSON boolean only.        
"""

    result = client.beta.chat.completions.parse( # When we use `beta` - then we also pass Schema as well 
        model='gpt-5-mini',
        response_format=DetectCallResponse,
        messages=[
            {"role":"system" , "content":SYSTEM_PROMPT },
            {"role":"user","content":user_msg}
        ]
    )

    print(result.choices[0].message.parsed)  # Output : is_question_ai:True/False

    state["is_coding_qn"] = result.choices[0].message.parsed.is_question_ai
    return state 


# LangGraph - bug
def route_edge(state:State) -> Literal["solve_coding_question","solve_simple_question"]:
    is_coding_qn = state.get('is_coding_qn')

    if is_coding_qn:
        return "solve_coding_question"
    else :
        return "solve_simple_question"



def solve_coding_question(state:State):
    user_msg = state.get("user_msg")


    SYSTEM_PROMPT = """
     You are an AI assistant. Your Job to resolve the user query based on coding he/she is facing.       
"""

    result = client.beta.chat.completions.parse( # When we use `beta` - then we also pass Schema as well 
        model='gpt-4.1',
        response_format=CodingAiResponse,
        messages=[
            {"role":"system" , "content":SYSTEM_PROMPT },
            {"role":"user","content":user_msg}
        ]
    )

    print(result.choices[0].message.parsed)  # Output : ans:""

   

    state["ai_msg"] = result.choices[0].message.parsed.ans

    return state



def solve_simple_question(state:State):
   
    user_msg = state.get("user_msg")

   
    SYSTEM_PROMPT = """
     You are an AI assistant. Your Job to chat with the user .       
"""

    result = client.beta.chat.completions.parse( # When we use `beta` - then we also pass Schema as well 
        model='gpt-4.1',
        response_format=CodingAiResponse,
        messages=[
            {"role":"system" , "content":SYSTEM_PROMPT },
            {"role":"user","content":user_msg}
        ]
    )

    print(result.choices[0].message.parsed)  # Output : ans:""

   

    state["ai_msg"] = result.choices[0].message.parsed.ans

    return state



graph_builder =  StateGraph(State)

graph_builder.add_node("detect_query",detect_query)
graph_builder.add_node("solve_coding_question",solve_coding_question)
graph_builder.add_node("solve_simple_question",solve_simple_question)
graph_builder.add_node("route_edge",route_edge)

graph_builder.add_edge(START,"detect_query")
graph_builder.add_conditional_edges("detect_query",route_edge)

graph_builder.add_edge("solve_coding_question",END)
graph_builder.add_edge("solve_simple_question",END)


graph = graph_builder.compile()




def call_graph():
    state = {
        "user_msg":"Hey! Can u explain pydantic ?",
        "ai_msg":"",
        "is_coding_qn":False
    }

    result = graph.invoke(state)


    print("Result",result)




call_graph()

