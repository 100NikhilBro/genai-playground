# We have to do the Inferencing on a model so for that we need GPUs so use the Google-Collab for that 

Steps for google colab for Inferencing , I Write below :-

1. First we have to install a library called transfformers
-Code- !pip install transformers

2. We need Hugging Face token - Login to Hugging Face and create Access token 
-Code- import os 
-Code- os.environ["HF_TOKEN"]="your_token" 

3. Search for Model in the Hugging face and get access of it and copy the id of the model 
-Code- model_name = "google/gemma-4-31B-it"

4. We need to import Auto-tokenizer from Transformers 
-Code- from transformers import AutoTokenizer

5. Now we have to Load the tokenizer fro our model  
-Code- tokenizer = AutoTokenizer.from_pretrained(model_name)

6. U can check as well how ypur tokenizer is work : 
 -Code- print(tokenizer("Hello, how are you?"))
 -Code- print(tokenizer.get_vocab())
 -Code- input_tokens = tokenizer("Hello, how are you?")["input_ids"]
 -Code- print(input_tokens) 

7. AutoModelforCausalLM - import this from Transformer  - This is used to predict the next word 
-Code- from transformers import AutoModelForCausalLM 

8. We pass our model in this  
-Code- import torch 
-Code- model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16
)

9. Now make the pipeline
-Code- from transformers import pipeline
-Code- gen_pipeline = pipeline("text-generator",model=model,tokenizer=tokenizer)


10. gave input to gen_pipeline
-Code- gen_pipeline("hey There " , max_new_token = 25)



---------------------------------------------------------------------------------------------------------------


# Go Deep In Pipeline - Step 9 

- In pipeline , first we tokenize it and by using the same tokenizer , we detokenize it as well using the Transformer 

- tokenizer ----> Transformer ---> Detokenizer

- So we can write the Fast API on as well 



-----------------------------------------------------------------------------------------------------------

# Now , Writing the same thing without using the pipeline 


1. !pip install transformers
2.  import os 
    os.environ["HF_TOKEN"]="your_token" - create on Hugging Face 
    
- PIPELINE START FROM 3RD STEP

3. from transformers import AutoTokenizer, AutoModelForCausalLM
4. model_name = "google/gemma-4-31B-it" - use Any model
5. tokenizer = AutoTokenizer.from_pretrained(model_name)
6. input_prompt = ["The capital of India is "] --  We gave the initial string , now we want CausalLM complete it 
7. tokenized = tokenizer(input_prompt,return_tensors='pt')   -- tokenizing our input 
8. tokenized["input_ids"] -- print what is in tensor or input tokens kya bane ?
9. import torch 
    model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16)
10. gen_result=model.generate(tokenized     ["input_ids"],max_new_token=25)  
11. gen_result - print it , u see the predicted tokens 
12. output = tokenizer.batch_decode(gen_result)
13. output - print it , u see the result 





