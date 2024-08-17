import os
import requests
from dotenv import load_dotenv
from SimplerLLM.language.llm import LLM, LLMProvider
from prompts import backend_generator_prompt, frontend_generator_prompt

# Load environment variables from .env file
load_dotenv()

# Setup
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-4o-mini")
openai_api_key = os.getenv('OPENAI_API_KEY')
tool_title = "YOUR_TOOL_TITLE"
tool_description = "YOUR_TOOL_DESCRIPTION"
wordpress_url = "YOUR_WEBSITE_LINK"  
wordpress_username = "YOUR_WORDPRESS_USERNAME"  
application_password = "YOUR_WORDPRESS_APP_PASSWORD"

#Frontend Code Generation
final_frontend_generator_prompt = frontend_generator_prompt.format(title = tool_title, tool_info = tool_description)
frontend_code = llm_instance.generate_response(prompt = final_frontend_generator_prompt, max_tokens= 5000)

with open("frontend_code.html", "w") as w:
    frontend_code = frontend_code.replace("result.innerHTML = marked.parse(data.data.choices.map(choice => choice.message.content).join('\n'));", "result.innerHTML = marked.parse(data.data.choices.map(choice => choice.message.content).join('\\n'));")
    w.write(frontend_code)

#Backend Code Generation
final_backend_generator_prompt = backend_generator_prompt.format(title = tool_title, tool_info = tool_description, api_key = openai_api_key)
backend_code = llm_instance.generate_response(prompt = final_backend_generator_prompt, max_tokens= 5000)

with open("backend_code.php", "w") as w:
    w.write(backend_code)

def create_wordpress_page(title, html_content, url, username, app_password):
    headers = {
        'Authorization': f'Basic {username}:{app_password}'
    }

    # Formatting HTML content within WordPress HTML block syntax
    formatted_html = f'<!-- wp:html -->\n{html_content}\n<!-- /wp:html -->'
    data = {
        'title': title,
        'content': formatted_html,
        'status': 'draft'  # Change to 'publish' if you want to publish immediately
    }
    response = requests.post(f'{url}/wp-json/wp/v2/pages', headers=headers, json=data, auth=(username, app_password))
    
    if response.status_code == 200 | response.status_code == 201:
        print("Page Create Successfully.")
    else:
        print("Failed to create pafe. Status code:", response.status_code, "Response:", response.text)

def create_code_snippet(url, username, app_password, snippet_details):
    # Headers for application password authentication
    headers = {
        'Authorization': f'Basic {username}:{app_password}'
    }
    
    # Make the POST request to the custom REST API endpoint
    response = requests.post(url, json=snippet_details, headers=headers, auth=(username, app_password))
    
    if response.status_code == 200:
        print("Snippet inserted successfully.")
    else:
        print("Failed to insert snippet. Status code:", response.status_code, "Response:", response.text)

# Create Frontend of the Tool
create_wordpress_page(tool_title, frontend_code, wordpress_url, wordpress_username, application_password)

# Create Backednend of the Tool
create_code_snippet(
    url=f'{wordpress_url}/wp-json/wp/v2/insert-snippet/',
    username = wordpress_username,
    app_password = application_password,
    snippet_details = {
    'name': f'{tool_title} Code Snippet',
    'description': f'This the Code Snippet for {tool_title}',
    'code': backend_code,
    'tags': 'php, mini tool',
    'scope': 'global',
    'priority': 10,
    'active': 1,
    'revision': 1,
    'cloud_id': None
}
)