import ollama
import re
import os 


def generate(query, model_name):
    query_with_instruction = f"{query}"
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": query_with_instruction}])
    model_reply = response.message.content
    model_reply_no_formatting = re.sub(r'[\*\_]{1,2}(.*?)\1', r'\1', model_reply)
    return model_reply_no_formatting

def generateLLAVA(query, model_name, fullPath):
    query_with_instruction = f"look at the image and respond to this query: {query}"
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": query_with_instruction, "images": [f"{fullPath}"]}])
    model_reply = response.message.content
    model_reply_no_formatting = re.sub(r'[\*\_]{1,2}(.*?)\1', r'\1', model_reply)
    return model_reply_no_formatting
