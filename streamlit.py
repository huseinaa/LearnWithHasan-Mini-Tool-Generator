import streamlit as st
from prompts import backend_generator_prompt, frontend_generator_prompt
from SimplerLLM.language.llm import LLM, LLMProvider
import requests

# Initialize the LLM instance with OpenAI's API
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-4o-mini")

# Define the functions for creating WordPress pages and inserting snippets
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
    
    if response.status_code in [200, 201]:
        st.success("Page Created Successfully.")
    else:
        st.error(f"Failed to create page. Status code: {response.status_code} Response: {response.text}")

def create_code_snippet(url, username, app_password, snippet_details):
    headers = {
        'Authorization': f'Basic {username}:{app_password}'
    }
    response = requests.post(url, json=snippet_details, headers=headers, auth=(username, app_password))
    
    if response.status_code == 200:
        st.success("Snippet inserted successfully.")
    else:
        st.error(f"Failed to insert snippet. Status code: {response.status_code} Response: {response.text}")

# Setting up the Streamlit UI
st.title("Mini Tool Generator")
st.subheader("Enter the necessary information to create your tool:")

# User inputs for configuration
tool_title = st.text_input("Enter the title of the tool:")
tool_description = st.text_area("Enter the description of the tool:")
wordpress_url = st.text_input("WordPress URL:")
wordpress_username = st.text_input("WordPress Username:")
application_password = st.text_input("Application Password:", type="password")
openai_api_key = st.text_input("OpenAI API Key:", type="password")

# Generate tool codes
if st.button('Generate Tool Codes'):
    st.session_state['generated'] = True  # Flag to check if codes were generated
    # Generate codes using the provided script
    final_frontend_generator_prompt = frontend_generator_prompt.format(title=tool_title, tool_info=tool_description)
    frontend_code = llm_instance.generate_response(prompt=final_frontend_generator_prompt, max_tokens=5000)
    frontend_code = frontend_code.replace("result.innerHTML = marked.parse(data.data.choices.map(choice => choice.message.content).join('\n'));", "result.innerHTML = marked.parse(data.data.choices.map(choice => choice.message.content).join('\\n'));")
    
    final_backend_generator_prompt = backend_generator_prompt.format(title=tool_title, tool_info=tool_description, api_key=openai_api_key)
    backend_code = llm_instance.generate_response(prompt=final_backend_generator_prompt, max_tokens=5000)
    
    st.session_state['frontend_code'] = frontend_code
    st.session_state['backend_code'] = backend_code

# Publish Tool
if 'generated' in st.session_state and st.session_state['generated']:
    st.success("Tool Codes Generated Successfully!")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Frontend Code")
        st.download_button("Download Frontend Code", st.session_state['frontend_code'], file_name="frontend_code.html")
    
    with col2:
        st.subheader("Backend Code")
        st.download_button("Download Backend Code", st.session_state['backend_code'], file_name="backend_code.php")
    
    # Checks if you want to publish the tool
    publish = st.radio("Do you want to publish this tool to your site?", ('Yes', 'No'))
    
    if publish == 'Yes' and st.button("Publish Tool to Your Site"):
        create_wordpress_page(tool_title, st.session_state['frontend_code'], wordpress_url, wordpress_username, application_password)
        create_code_snippet(f'{wordpress_url}/wp-json/wp/v2/insert-snippet/', wordpress_username, application_password, {
            'name': f'{tool_title} Code Snippet',
            'description': f'This is the Code Snippet for {tool_title}',
            'code': st.session_state['backend_code'],
            'tags': 'php, mini tool',
            'scope': 'global',
            'priority': 10,
            'active': 1,
            'revision': 1,
            'cloud_id': None
        })
    elif publish == 'No':
        st.info("You have chosen not to publish the tool. You can still download the codes.")
