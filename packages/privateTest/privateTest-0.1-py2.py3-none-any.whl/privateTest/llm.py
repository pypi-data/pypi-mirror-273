import json
import re
from openai import AzureOpenAI

class llmConnect:
    def __init__(self,azure_endpoint,api_key,api_version):
            self.client = AzureOpenAI(
                        azure_endpoint = azure_endpoint, 
                        api_key=api_key,  
                        api_version=api_version
                        )        

    def generate(self,content,model,type="string"):
        chat_completion = self.client.chat.completions.create(
            messages=content,
            model=model,
        )
        if type=="json":
            chat_completion=self.jsonEdit(chat_completion)
        elif type=="list":
            chat_completion=self.listEdit(chat_completion)
        else:
            chat_completion=self.stringEdit(chat_completion)
        return chat_completion

    def jsonEdit(self,response):
        response=response.choices[0].message.content
        try:        
            response=json.loads(response)
        except Exception as e:
            response=self.extract_json_structure(response)
        return response

    def stringEdit(response):
        response=response.choices[0].message.content
        response=str(response)
        return response

    def listEdit(response):
        response=response.choices[0].message.content
        pass

    def extract_json_structure(self,input_string):
            # text = input_string        
            if "```json" in input_string:
                # Use regular expression to extract the JSON-formatted substring
                match = re.search(r"```json\n(.*?)\n```", input_string, re.DOTALL)

                if match:
                    json_str = match.group(1)
                    # Load the JSON string into a dictionary
                    json_data = json.loads(json_str)
                    # Print the extracted JSON object
                    body = json_data
                    return body
                
                    # print("JSON data not found.")
            else:
                # Extract the JSON object directly
                start_index = input_string.find("{")
                end_index = input_string.rfind("}")

                if start_index != -1 and end_index != -1:
                    json_str = input_string[start_index : end_index + 1]               
                    json_data = json.loads(json_str)                
                    body = json_data
                    return body

                

