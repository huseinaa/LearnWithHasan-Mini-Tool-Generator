import os
from dotenv import load_dotenv
from SimplerLLM.language.llm import LLM, LLMProvider
from prompts import backend_generator_prompt, frontend_generator_prompt

# Load environment variables from .env file
load_dotenv()

#Inputs
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-4o-mini")
tool_description = "AI X Bio Generator tool which takes 3 inputs which are the users achievements what skills they have and the target audience and generates a x bio for them"
tool_title = "AI X Bio Generator"
openai_api_key = os.getenv('OPENAI_API_KEY')

#Frontend
final_frontend_generator_prompt = frontend_generator_prompt.format(title = tool_title, tool_info = tool_description)
frontend_code = llm_instance.generate_response(prompt = final_frontend_generator_prompt, max_tokens= 5000)

with open("frontend_code.html", "w") as w:
    frontend_code = frontend_code.replace("result.innerHTML = marked.parse(data.data.choices.map(choice => choice.message.content).join('\n'));", "result.innerHTML = marked.parse(data.data.choices.map(choice => choice.message.content).join('\\n'));")
    w.write(frontend_code) 

#Backend
final_backend_generator_prompt = backend_generator_prompt.format(title = tool_title, tool_info = tool_description, api_key = openai_api_key)
backend_code = llm_instance.generate_response(prompt = final_backend_generator_prompt, max_tokens= 5000)

with open("backend_code.php", "w") as w:
    w.write(backend_code)

"""
#SEO
final_SEO_optimizer = SEO_optimizer.format(title = tool_title, description = tool_description)
tool_SEO = llm_instance.generate_response(prompt = final_SEO_optimizer)

with open("SEO.txt", "w") as w:
    w.write(tool_SEO)  
"""
