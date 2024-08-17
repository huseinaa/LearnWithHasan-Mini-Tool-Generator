frontend_generator_prompt = """
As an expert in HTML, CSS, and JavaScript Programming, your task is to create a UI for a tool whose functionality and number of inputs will be provided in the inputs section delimited between triple backticks.
The UI should have a simple and clean design, following the code structure for a tool that takes 2 inputs in the Sample Output section delimited between triple backticks.
The most important thing is that the output code should only focus on editing the base code to make it compatible with the new number and type of inputs the user wants. 

But when fetching the rest api make sure to edit the fetch link so that its like this: /wp-json/my-api/v1/{{Tool Title}}. But ofcourse write them in lower case and the words are separated by _ for it to work.

DONT CHANGE any links or anything that has to do with the way we're sending the form data like input_1 input_2 and so on. So only use input_1 input_2 input_3 ... when dealing with inputs.

##Input
Tool Title: ```{title}```
Tool Information: ```{tool_info}```

##Sample Output
```
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <title>Document</title>
    <style>
    
        .flex input {{
            font-size: 17px;
            width: 98%; 
            margin: 10px 1%; 
            padding: 12px; 
            border: 1px solid #d1d1d1; 
        }}
        
        #result-container {{
            box-shadow: 2px 2px 20px 2px rgba(0, 0, 0, 0.1);
            background-color: #fff;
            border-radius: 8px;
            margin: 2rem auto;
        }}
    
        .result-content {{
            word-spacing: normal;  
            padding: 0;
            margin: 0;   
        }}
        
        .result-content h1, 
        .result-content h2, 
        .result-content h3{{
            white-space: pre-wrap; 
            margin-top: 20px; 
        }}

        .copy-button-container {{
            margin-top: 10px;
            text-align: right;
            position: relative;
        }}

        #generate-button {{
            font-size: 20px;
            color: white;
            background-color: #0d2451;
            cursor: pointer;
            border: none;
            width: 200px;
            border-radius: 0px;
            padding: 10px 10px;
            margin: 10px 1%;
        }}

        #generate-button:hover {{
            background-color: #005999;
        }}
        
        #copy-button {{
            font-size: 20px;
            color: white;
            background-color: #0d2451;
            cursor: pointer;
            border: none;
            width: 200px;
            border-radius: 0px;
            padding: 10px 10px;
            margin: 10px 1%;
        }}

        #copy-button:hover {{
            background-color: #005999;
        }}

        .copy-message {{
            position: absolute;
            top: -30px;
            right: 10px;
            font-size: 14px;
            color: green;
            display: flex;
            align-items: center;
        }}

        .copy-message i {{
            margin-right: 5px;
        }}

        #loading {{
            width: 70px; 
            height: 70px;
            margin-top: 150px;
            margin: 0 auto;
        }}

        .flex {{
            display: flex;
            flex-direction: column;
        }}
                
        .spinner {{
            border: 15px solid rgba(0, 0, 0, 0.1); 
            border-top: 15px solid #0d2451;      
            border-radius: 50%;              
            animation: spin 1s linear infinite;  
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}    
            100% {{ transform: rotate(360deg); }}   
        }}

    </style>
</head>
    <body>
            <div class="tool-container">
                <form onsubmit="return false;">
                    <div class="flex">
                        <input type="text" id="topic1" oninput="handleInputChange(event)" placeholder='Enter topic 1'>
                        <input type="text" id="topic2" oninput="handleInputChange(event)" placeholder='Enter topic 2'>
                        <button id="generate-button" type="button"> Generate </button>
                    </div>
                </form>
            </div>
            
            <div id="result-container" class="tool-container" style="display: none; padding: 1rem;">
                <div id="result" class="result-content"></div>
                <div class="copy-button-container">
                    <button id="copy-button">Copy</button>
                    <div id="copy-message" class="copy-message" style="display: none;">
                        <i class="fa fa-check-circle"></i> Copied
                    </div>
                </div>
            </div>
            <div id="loading" class="spinner" style="display: none;"></div>
    <script>
    document.getElementById("generate-button").addEventListener("click", function(e) {{
    e.preventDefault();
    var generateButton = document.getElementById("generate-button");
    if (generateButton.disabled) return;

    generateButton.disabled = true;
    var topic1 = document.getElementById('topic1').value;
    var topic2 = document.getElementById('topic2').value;
    var loading = document.getElementById('loading');
    var result = document.getElementById('result');
    var resultC = document.getElementById('result-container');

    loading.style.display = 'block'; 
    result.style.display = 'none';
    resultC.style.display = 'none';

    var formData = new FormData();
    formData.append('input_1', topic1);
    formData.append('input_2', topic2);

    fetch('/wp-json/my-api/v1/mini_tool', {{
        method: 'POST',
        body: formData  
    }})
    .then(response => response.json())
    .then(data => {{
        loading.style.display = 'none'; 
        if (data.success) {{
            result.innerHTML = marked.parse(data.data.choices.map(choice => choice.message.content).join('\n'));
            result.style.display = 'block';
            resultC.style.display = 'block';
        }} else {{
            result.textContent = data.data;
            result.style.display = 'block';
            resultC.style.display = 'block';
        }}
        generateButton.disabled = false;
    }})
    .catch(error => {{
        loading.style.display = 'none'; 
        result.textContent = 'OOPS! An error has occurred, please try again!';
        result.style.display = 'block';
        resultC.style.display = 'block';
        generateButton.disabled = false;
    }});
}});

    document.getElementById('copy-button').addEventListener('click', function() {{
        var text = document.getElementById('result').textContent;
        var copyMessage = document.getElementById('copy-message');

        if (navigator.clipboard) {{
            navigator.clipboard.writeText(text).then(function() {{
                copyMessage.style.display = 'flex';
                setTimeout(function() {{
                    copyMessage.style.display = 'none';
                }}, 2000);
            }}, function(err) {{
                alert('Error in copying text: ' + err);
            }});
        }} else {{
            var textarea = document.createElement('textarea');
            textarea.textContent = text;
            textarea.style.position = 'fixed';  
            document.body.appendChild(textarea);
            textarea.select();
            try {{
                document.execCommand('copy');  
                copyMessage.style.display = 'flex';
                setTimeout(function() {{
                    copyMessage.style.display = 'none';
                }}, 2000);
            }} catch (ex) {{
                console.warn('Copy to clipboard failed.', ex);
                alert('Copy not successful, please try manually.');
            }} finally {{
                document.body.removeChild(textarea);
            }}
        }}
    }});
</script>
</body>
</html>
```

##Output
The output should be the code but in normal text form dont use triple backticks to make it in code form and only that.
"""

backend_generator_prompt = """
You are an expert in generating php code snippets for wordpress. Your task is to generate a php code snippet about the code idea that will be provided in the inputs section delimited between triple backticks.
The php code snippet should be clear following the code structure for the backend of a tool that takes 2 inputs delimited between triple backticks in the Sample Output section.
The most important thing is that the output code should only focus on editing the base code to make it compatible with the new number and type of inputs the user wants. 

MAKE SURE that you edit the function nameand make it about the tool, also edit the function name only in the callback part of the the api call at the end of the code keeping this part (( register_rest_route( 'my-api/v1', '/mini_tool', )) the same.
Plus make sure you edit the rest api endpoint so that its like the following:

add_action( 'rest_api_init', function () {{
register_rest_route( 'my-api/v1', '/{{Tool Title}}', array(
'methods' => 'POST',
'callback' => 'mini_tool_{{Tool Title}}',
'permission_callback' => '__return_true'

) );
}} );

Finally take the api key in the inputs section and add it to the php snippet in its correct place.

DONT CHANGE any links or anything that has to do with the way we're sending the form data like input_1 input_2 and so on. So only use input_1 input_2 input_3 ... when dealing with inputs.

##Input
Tool Title: ```{title}```
Idea: ```{tool_info}```
OpenAI Api Key: ```{api_key}```

##Sample Output
```
function mini_tool_openai_generate_text( WP_REST_Request $request ) {{
$input_1 = $request->get_param('input_1');
$input_2 = $request->get_param('input_2');

$prompt = "Generate for me [input_1] blog titles about this topic [input_2]";

$prompt = str_replace('input_1', $input_1, $prompt);
$prompt = str_replace('input_2', $input_2, $prompt);

// OpenAI API URL and key
$api_url = 'https://api.openai.com/v1/chat/completions';
$api_key = 'YOUR_OPENAI_API_KEY';  

// Headers for the OpenAI API
$headers = [
    'Content-Type' => 'application/json',
    'Authorization' => 'Bearer ' . $api_key
];

// Body for the OpenAI API
$body = [
    'model' => 'gpt-4o',
    'messages' => [['role' => 'user', 'content' => $prompt]],
    'temperature' => 0.7
];

$args = [
    'method' => 'POST',
    'headers' => $headers,
    'body' => json_encode($body),
    'timeout' => 120
];

// Send the request
$response = wp_remote_request($api_url, $args);
if (is_wp_error($response)) {{
wp_send_json_error("OOPS! An error has occurred, please try again!");
}} else {{
$body = wp_remote_retrieve_body($response);
$data = json_decode($body, true);

php
Copy code
if (json_last_error() !== JSON_ERROR_NONE) {{
    wp_send_json_error("OOPS! An error has occurred, please try again!");
}} elseif (!isset($data['choices'])) {{
    wp_send_json_error("OOPS! An error has occurred, please try again!");
}} else {{
    wp_send_json_success($data);
}}
}}
wp_die();
}}

add_action( 'rest_api_init', function () {{
register_rest_route( 'my-api/v1', '/mini_tool', array(
'methods' => 'POST',
'callback' => 'mini_tool_openai_generate_text',
'permission_callback' => '__return_true'

) );
}} );
```

##Output
The output should be the code but in normal text form dont use triple backticks to make it in code form and only that.
"""

SEO_optimizer = """
##Instruction
You are an expert in SEO and creating meta descriptions, titles, headings and so on for tools to make them SEO optimized. 
Im gonna give you the title name and a small description of what my tool does in the inputs section delimited between triple backticks, and your task is to generate for me: 
- A meta description that is of 130 characters without mentioning the title of the tool in it.
- A heading that is of 100 characters without mentioning the title of the tool in it, where the first letter of every word has to be capitalized. It should be straight-forward and shows the benefit of the tool.
- A well structured description paragraph explaining what the tool does.

One very important note is that everything you write should not contain any complex vocabulary, very straight forward and clear, and SEO optimized.

##Inputs
Tool Title: ```{title}```
Tool Description: ```{description}```

##Output
The output should be in json format of the following form and nothing else:
{{
    'Meta Title' : [The Title],
    'Meta Description' : [The Meta Description],
    'Heading' : [Heading],
    'Description Paragraph' : [Description Paragraph]
}}
"""
