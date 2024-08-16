from SimplerLLM.language.llm import LLM, LLMProvider
from prompts import backend_generator, frontend_generator, SEO_optimizer

#Inputs
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-4o-mini")
tool_description = "AI X Bio Generator tool which takes 3 inputs which are the users achievements what skills they have and the target audience and generates a x bio for them"
tool_title = "AI X Bio Generator"
openai_api_key = "sk-proj-LgZbOzpHTPvCdPiabzJQT3BlbkFJeGinsKp3j5WfX7TgpWw8"

#Frontend
final_frontend_generator = frontend_generator.format(title = tool_title, tool_info = tool_description)
frontend_code = llm_instance.generate_response(prompt = final_frontend_generator, max_tokens= 5000)

with open("frontend_code.html", "w") as w:
    frontend_code = frontend_code.replace("result.innerHTML = marked.parse(data.data.choices.map(choice => choice.message.content).join('\n'));", "result.innerHTML = marked.parse(data.data.choices.map(choice => choice.message.content).join('\\n'));")
    w.write(frontend_code) 

#Backend
final_backend_generator = backend_generator.format(title = tool_title, tool_info = tool_description, api_key = openai_api_key)
backend_code = llm_instance.generate_response(prompt = final_backend_generator, max_tokens= 5000)

with open("backend_code.php", "w") as w:
    w.write(backend_code)
"""
#SEO
final_SEO_optimizer = SEO_optimizer.format(title = tool_title, description = tool_description)
tool_SEO = llm_instance.generate_response(prompt = final_SEO_optimizer)

with open("SEO.txt", "w") as w:
    w.write(tool_SEO)  
"""
