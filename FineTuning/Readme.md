- Fine Tuning - to change the model as per our requirements

- Base Model ---FineTuing---> Fine-tuned Model

- Base Model are the pre-trained transformers that just try to predict the next tokens 

- Base Model has enitire internet Context and also has knowledge cut-off and they are updated only by the large companies after a period of time 

- Base Model -- GPT4 , GPT3.5 etc 
- Fine tuning Model -- ChatGPT , Gemini etc


---------------------------------------------------------------------------------------------------------------------

<b>Note: Base Model are the transformers that try to predict the next tokens where as fine-tuned model are who try to gave the answer of our questions </b>


---------------------------------------------------------------------------------------------------------------------


```
- Domain Specific fine Tuning Model :
When we write the system prompt then we write like things like that [You are Specialise in Maths ... etc] things so that makes the model domain-specific
```


```
-Task-level fine Tuning Model :
When our model fine tuned for a task on a label data
```




-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


1. <i>Full parameter Fine tuning </i> - In this type of fine tuning , the actual weight of base model changes 

- Note - As A developer , we do fine tuning using the fine-tuing services like Replicate etc


2. <i>LoRA- Low Rank Adapter</i> is a parameter efficient  fine tuning  techinique for LLMs 



------------------------------------------------------------------------------------------------------------------------------------------

- <i>FineTunings vs SystemPrompt</i> -- both are d/f becuse system prompt changes the behaviour of model but Finetuning try to change the weight of base model

- <i>FineTuning vs RAGs</i> -- they depends on useCase and reuirement and moreover intution of choosing choice like if data is chnaging very frequenltly on each query then try to go with RAG , if not and very large data that don't fit in system prompts and not change that much frequently try to use the Fine-tuning 


- FineTuing is simple but RAG is Complex 






-------------------------------------------------------------------------------------------------------------------------------------



<b> Interesting Things </b>

- Don't change your format of writing code :

```
from openai import OpenAI
client = OpenAi()

response = client.chat.completions.create(
    model:"",
    messages:[{
        "role":"user",
        "content":"How are you ?"
    }]
)
````

- Use the same format with the compatable OpenAI SDK with Gemini , groq , etc 








