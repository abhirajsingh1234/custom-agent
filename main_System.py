import requests
import google.generativeai as genai
import dotenv
import os
import json

dotenv.load_dotenv()
# URL for the local server (adjust if needed)
SERVER_URL = "http://localhost:8000"

def fetch_available_tools():
    """Fetch the list of available tools from the local server."""
    response = requests.get(f"{SERVER_URL}/tools")
    if response.status_code == 200:
        tools = response.json().get("available_tools", {})
        print("Available tools fetched:", tools)
        return tools
    else:
        print("Error fetching available tools!")
        return {} 

def email_llm(query, chat_history):
    emails = {'rajpurohitabhirajsinghvyasch@gmail.com':'owner of this email id is Abhiraj singh rajpurohit',
    'karanshelar8775@gmail.com':'owner of this email id is Karan Shelar',
    'siddhantparulekar5@gmail.com':'owner of this email id is Siddhant Parulekar'}


    prompt = (
        f"User query: {query}\n"
        f"Available emails: {emails}\n"
    )
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    history = chat_history
    # Create the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8190,
      "response_mime_type": "text/plain",
    }

    email_data_selector = genai.GenerativeModel(
      model_name="gemini-1.5-pro",
      generation_config=generation_config,
      system_instruction="""
                          Given the input query and available emails, determine if an email action is required and construct an appropriate email.

                          1️⃣ Email Data Handling:
                          - The available emails are provided in dictionary format:
                            {"email_id": "owner's name"}
                          - If the recipient's email is missing in the query, search for a matching name in available emails and retrieve the corresponding email ID.
                          - If recipient's email is not found in available emails too, find the relevant email id from chat history.

                          2️⃣ Extracting Email Content:
                          - Identify the email subject and body from the user query.
                          - If either is missing, search the chat history for relevant details.
                          - The email subject and body must accurately resolve the user’s query.

                          3️⃣ Determining Email Action:
                          - If the user requests an email action and a valid recipient email is found (either in the query or in available emails), set:
                            "email_action": true
                          - Otherwise, set:
                            "email_action": false

                          4️⃣ Formatting the Email Body:
                          - Always end the email body with:
                            "Written by Jarvis on command of {user’s actual name}."
                          - Extract the user’s actual name from chat history.(if not found then bydefault use 'abhiraj's custom-MCP')

                          5️⃣ Expected JSON Output Format:
                          {
                            "email_action": true or false,
                            "tool": "send_email",
                            "parameters": {
                              "email_id": "recipient's email or null",
                              "subject": "Generated subject or null",
                              "body": "Generated body ending with 'Written by Jarvis on command of {user's actual name}' or null"
                            }
                          }

                          6️⃣ Handling Missing Data:
                          - If any required parameters (email_id, subject, or body) are missing, return null for those values instead of generating incorrect data.
                          """
    )
    chat_session = email_data_selector.start_chat(
                history=history
            )
    
    response = chat_session.send_message(prompt)
    model_response=response.text

    lines = model_response.splitlines()
    json_content = "\n".join(lines[1:-1])
    print("\nemail before json parsing:\n", json_content)
    try:
        data = json.loads(json_content)
    except Exception as e:
        return 'error sending mail'
    print("\nemail after json parsing:\n", data)
    return data
    
def fetch_linkedin_details(query,chat_history):
  # linkedin_details = {'abhiraj-singh-rajpurohit-9647b427b/':'owner of this email id is Abhiraj singh rajpurohit'}

  prompt = (
        f"User query: {query}\n"
        # f"Available linkedin details: {linkedin_details}\n"
    )
    
  genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
  history = chat_history
    # Create the model
  generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8190,
      "response_mime_type": "text/plain",
    }

  linkedin_details_selector = genai.GenerativeModel(
      model_name="gemini-1.5-flash-8b",
      generation_config=generation_config,
      system_instruction="""Given the input query, the user is asking for LinkedIn account details.

### **LinkedIn Details Extraction Rules:**
1. **Check if the query explicitly mentions a LinkedIn username.**  
   - If a username is directly mentioned, use it.  

2. **If no username is mentioned, check if a relevant username is stored in chat history.**  
   - If a username exists in the chat history, use it.  


3. **If no username is found in the query or chat history, set `"username": null`.**  

4. **Explicitly set `linkedin_action = false` if `"username": null`.**  
   - `"linkedin_action": true` **only if a valid username is found.**  
   - `"linkedin_action": false` **if no username is found.**  

### **Return Response Format:**
```json
{
  "linkedin_action": true or false,  # Boolean
  "tool": "fetch_linkedin_details",
  "parameters": {
    "username": "username"  # LinkedIn username OR null if missing
  }
}


                            """
    )
  chat_session = linkedin_details_selector.start_chat(
                history=history
            )
  response = chat_session.send_message(prompt)
  model_response=response.text
  lines = model_response.splitlines()
  json_content = "\n".join(lines[1:-1])
  data = json.loads(json_content)
  # print("Linkedin details data:", data)
  return data

def get_github_commits(query,chat_history):
    
    prompt = (
        f"User query: {query}\n"
    )
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    history = chat_history
    # Create the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8190,
      "response_mime_type": "text/plain",
    }

    github_commits_selector = genai.GenerativeModel(
      model_name="gemini-1.5-flash-8b",
      generation_config=generation_config,
      system_instruction="""
                            Given the input query, analyze it to determine if the user is asking for GitHub commits.  
                            - If the query is not well-structured, infer the user’s intent based on context. 
                            -If user_name or repo_name is missing in query, search the chat history for relevant details.
                            -user name and repository may be provided in the query in the following format: "username/repo_name".
                            -If user_name or repo_name is not found in chat history, return null for those values and turn get_github_commits to false(boolean).
                            - Identify how many commits the user is requesting.  
                            - Determine what details the user wants to retrieve: "message," "author," "date," or "all."
                            - bydefault detail_type is "all" if not specified.
                            - bydefault num_commits is 5 if not specified.
                            If any parameters are missing, return a null value for those parameters and set get_github_commits to false(boolean).
                            value "get_github_commits" for tool is constant.
                            Return the response in the following JSON format:  
                            {
                              "get_github_commits": true,  # Boolean
                              "tool": "get_github_commits", #constant
                              "parameters": {
                                "user_name": "username",  # GitHub username
                                "repo_name": "repo_name",  # GitHub repository name
                                "detail_type": "all",  # Options: "message", "author", "date", or "all"
                                "num_commits": 5  # Number of commits requested
                              }
                            }
                            """
    )
    chat_session = github_commits_selector.start_chat(
                history=history
            )
    response = chat_session.send_message(prompt)
    model_response=response.text
    lines = model_response.splitlines()
    json_content = "\n".join(lines[1:-1])
    try:
        data = json.loads(json_content)
    except Exception as e:
        return {"error": f"ERROR OCCURED WHILE FETCHING GITHUB COMMITS, TRY AGAIN"}
    # print("GitHub commits data:", data)
    return data

def send_whatsapp_message(query,chat_history):
    
    available_numbers = {'8450995752':'Abhiraj singh rajpurohit','8828296303':'karan shelar'}
    prompt = (
        f"User query: {query}\n"
        f"Available numbers: {available_numbers}\n"
    )
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    history = chat_history
    # Create the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8190,
      "response_mime_type": "text/plain",
    }

    whatsapp_message_selector = genai.GenerativeModel(
      model_name="gemini-1.5-flash-8b",
      generation_config=generation_config,
      system_instruction="""
                           Analyze the input query to determine if the user is requesting to send a WhatsApp message.

                            Guidelines:
                            1. First check if a phone number is explicitly provided in the query
                            2. If no phone number is found:
                               - Extract any person/contact name mentioned in the query
                               - Search the available_numbers dictionary {number: owner's name} for matching names
                               - Use the corresponding number if a name match is found

                            3. Extracting Message Content:
                                                      - Identify the message content from the user query.
                                                      - If message is missing, search the chat history for relevant details.
                                                      - The message must accurately resolve the user’s query.

                            4. If either phone_number (direct or via name lookup) or message is not found:
                               - Set send_whatsapp_message to false
                               - Set the missing parameter(s) to null
                            5. Always use "send_whatsapp_message" as the tool value

                            Return JSON response in this format:
                            {
                              "send_whatsapp_message": boolean,  // true only if both phone_number and message are valid
                              "tool": "send_whatsapp_message",   // constant value
                              "parameters": {
                                "phone_number": string,  // extracted phone number, number from name lookup, or null if not found
                                "message": string        // extracted message content or null if not found
                              }
                            }
                            """
    )
    chat_session = whatsapp_message_selector.start_chat(
                history=history
            )
    response = chat_session.send_message(prompt)
    model_response=response.text
    lines = model_response.splitlines()
    json_content = "\n".join(lines[1:-1])
    try:
        data = json.loads(json_content)
    except Exception as e:
        return {"error": f"ERROR OCCURED WHILE FETCHING GITHUB COMMITS, TRY AGAIN"}
    # print("GitHub commits data:", data)
    return data

def get_llm_decision(query, tools, chat_history):
    """
    Send the user query and available tools to Gemini.
    Gemini is expected to decide which tool to use and provide necessary parameters.
    """
    chat_history = chat_history[-2:] if len(chat_history) >= 2 else chat_history

    prompt = (
      f"Chat history: {chat_history}\n"
      f"current User query: {query}\n"
      f"Available tools: {tools}\n"
    )
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    history = chat_history
    # Create the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8190,
      "response_mime_type": "text/plain",
    }

    tool_selector = genai.GenerativeModel(
      model_name="gemini-1.5-flash-8b",
      generation_config=generation_config,
      system_instruction=""" you are a assistant named jarvis.
                          given the input query, last user-model interaction chat history and tools analyze if the query needs a tool to be executed.
                          if user query is not well structured try to understand meaning behind the query.
                          deeply check if the query needs a tool to be executed or it is a general query containing words like email,github,commits.
                          if the query is general and dont need a tool then return tool value as null.
                          if tool is selected output the tool name in the following JSON format:
                          {
                            "tool": "tool_name"
                          }
                          """
    )
    chat_session = tool_selector.start_chat(
                history=history
            )
    response = chat_session.send_message(prompt)
    
    model_response=response.text
    # print("\nModel Response:\n", model_response)
    lines = model_response.splitlines()

    json_content = "\n".join(lines[1:-1])

    data = json.loads(json_content)
    print(data)

    if data['tool'] is not None and data['tool'] == 'send_email':
        return email_llm(query, chat_history)
    elif data['tool'] is not None and data['tool'] == 'get_github_commits':
        return get_github_commits(query, chat_history)
    elif data['tool'] is not None and data['tool'] == 'fetch_linkedin_details':
        return fetch_linkedin_details(query, chat_history)
    elif data['tool'] is not None and data['tool'] == 'send_whatsapp_message':
        return send_whatsapp_message(query, chat_history)


    return data

def execute_tool(tool_name, parameters):
    data = {
        "tool_name": tool_name,
        "parameters": parameters
    }
    response = requests.post(f"{SERVER_URL}/execute", json=data)
    print("Response status code:", response.status_code)
    # print("Response text:", response.text)
    try:
        return response.json()
    except Exception as e:
        return {"error": f"Response not valid JSON: {response.text}"}


def main():
    linkedin_data = []
    # Step 1: Fetch available tools from the local server.
    tools = fetch_available_tools()
    chat_history = []
    while True:
        # Step 2: Accept a query from the user.
        
        query = input("user: ")
        # Convert chat history into a formatted conversation
        history_text = "\n".join([f"{entry['role'].capitalize()}: {entry['parts'][0]['text']}" for entry in chat_history])

        # Combine with the new query
        model_query = f"{history_text}\nUser: {query}\nAssistant:"
        if query.lower() == "exit":
            break
        result = ""
        # Step 3: Send the query and available tools to Gemini.
        llm_output = get_llm_decision(query, tools,chat_history)

        print(llm_output, "\n")


        if "email_action" in llm_output and llm_output["email_action"] == True:
          if llm_output["parameters"]["subject"] is  None:
            result = f'please provide content, what email you want me to send to {llm_output["parameters"]["email_id"]}'
          elif llm_output["parameters"]["body"] is None:
            result = f'please provide content, what email you want me to send to {llm_output["parameters"]["email_id"]}'
          else:
            # Step 4: Instruct the local server to execute the tool.
            result = execute_tool(llm_output["tool"], llm_output["parameters"])
            result = f"\ncontext: {result}"
            print("\nTool Execution Result:\n")
        
        elif "email_action" in llm_output and llm_output["email_action"] == False:
          if llm_output["parameters"]["email_id"] is None:
            result = 'no relevant email id found in available emails and in our chat history please provide a valid email id.'
          

        elif "get_github_commits" in llm_output and llm_output["get_github_commits"] == True:
            # Step 5: Instruct the local server to execute the tool.
            result = execute_tool(llm_output["tool"], llm_output["parameters"])
            result = f"\ncontext: {result}"
            print("\nTool Execution Result:\n")
        
        elif "get_github_commits" in llm_output and llm_output["get_github_commits"] == False:
          if llm_output["parameters"]["user_name"] is None and llm_output["parameters"]["repo_name"] is None:
            result = 'context: please provide github user_name and repo_name'
          elif llm_output["parameters"]["user_name"] is None:
            result = 'context: please provide github user_name'
          elif llm_output["parameters"]["repo_name"] is None:
            result = 'context: please provide github repo_name'
        
        elif "linkedin_action" in llm_output and llm_output["linkedin_action"] == True:
          if llm_output["parameters"]["username"] is None:
            result = 'please provide linkedin username'
          else:
            # Step 5: Instruct the local server to execute the tool.
            result = execute_tool(llm_output["tool"], llm_output["parameters"])
            try:
              linkedin_data.append({'username':result.split('username:')[1].split('||')[0].strip(),"data":result})
            except:
              pass
            result = f"\ncontext: {result}"
            print("\nTool Execution Result:\n")

        elif "linkedin_action" in llm_output and llm_output["linkedin_action"] == False:
          result = 'please provide linkedin username'

        elif "send_whatsapp_message" in llm_output and llm_output["send_whatsapp_message"] == True:
          if llm_output["parameters"]["phone_number"] is None and llm_output["parameters"]["message"] is None:
            result = 'context: please provide phone number and message'
          elif llm_output["parameters"]["phone_number"] is None:
            result = 'context: please provide phone number'
          elif llm_output["parameters"]["message"] is None:
            result = 'context: please provide message'
          else:
            # Step 5: Instruct the local server to execute the tool.
            result = execute_tool(llm_output["tool"], llm_output["parameters"])
            result = f"\ncontext: {result}"
            print("\nTool Execution Result:\n")

        elif "send_whatsapp_message" in llm_output and llm_output["send_whatsapp_message"] == False:
          if llm_output["parameters"]["phone_number"] is None and llm_output["parameters"]["message"] is None:
            result = 'context: please provide phone number and message'
          elif llm_output["parameters"]["phone_number"] is None:
            result = 'context: please provide phone number'
          elif llm_output["parameters"]["message"] is None:
            result = 'context: please provide message'

        elif llm_output['tool'] is None:
            print("\n go with simple chat as no tools required detected.")
            pass
        final_query = model_query + result
        # Create the model
        print(result)
        # print("\nModel Query:\n", model_query)
        generation_config = {
          "temperature": 1,
          "top_p": 0.95,
          "top_k": 40,
          "max_output_tokens": 8190,
          "response_mime_type": "text/plain",
        }

        chat_model = genai.GenerativeModel(
          model_name="gemini-1.5-flash-8b",
          generation_config=generation_config,
          system_instruction = """You are an assistant named Jarvis—loyal to the user and a chill, friendly companion.

                            Start the chat with a warm greeting.
                            Keep track of the entire conversation history, as the user may ask you to remember things or reference past discussions.
                            Engage in a friendly, natural way, like a real friend. Keep the conversation smooth and enjoyable.
                            If a query includes a provided "context," always assume that this context was generated by a tool available on the server and not provided directly by the user.
                            The context is the result of a tool’s execution, such as fetching recent data, retrieving stored information, or generating content, and it contains the necessary details to resolve the user's query.
                            Use the given context to generate accurate and relevant responses to resolve the user's query.
                            Utilize chat history to maintain continuity and understand the flow of the conversation.
                            **IMPORTANT**: Always maintain an active memory of the ENTIRE conversation history. Before responding to any query, carefully review all previous messages in the current conversation.
                            When the user references something mentioned earlier, search through the conversation history to find the relevant information before responding.
                            Never claim you can't remember something that was mentioned in the current conversation thread.
                            If the user asks about previously mentioned information (like names, facts, or events from earlier messages), reference your conversation history to provide accurate responses
                            """)
        chat_session = chat_model.start_chat(
                    history=chat_history
                )
        response = chat_session.send_message(final_query)

        model_response=response.text
        print("\nModel Response:\n", model_response)
        chat_history.append({"role": "user", "parts": [{"text": final_query}]})
        chat_history.append({"role": "assistant", "parts": [{"text": model_response}]})

if __name__ == "__main__":
    # Configure Gemini with your API key.
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    main()
