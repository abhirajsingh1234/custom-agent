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
    'karanshelar8775@gmail.com':'owner of this email id is Karan Shelar'}


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
                          - Extract the user’s actual name from chat history.

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

                            Return the response in the following JSON format:  
                            {
                              "get_github_commits": true,  # Boolean
                              "tool": "get_github_commits",
                              "parameters": {
                                "user_name": "username",  # GitHub username
                                "repo_name": "repo_name",  # GitHub repository name
                                "detail_type": "all",  # Options: "message", "author", "date", or "all"
                                "num_commits": 5  # Number of commits requested
                              }
                            }
                            
                            If any parameters are missing, return a null value for that parameter.
                            """
    )
    chat_session = github_commits_selector.start_chat(
                history=history
            )
    response = chat_session.send_message(prompt)
    model_response=response.text
    lines = model_response.splitlines()
    json_content = "\n".join(lines[1:-1])
    data = json.loads(json_content)
    # print("GitHub commits data:", data)
    return data

def get_llm_decision(query, tools, chat_history):
    """
    Send the user query and available tools to Gemini.
    Gemini is expected to decide which tool to use and provide necessary parameters.
    """

    prompt = (
        f"User query: {query}\n"
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
                          given the input query and tools analyze if the query needs a tool to be executed.
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
    # print(data)

    if data['tool'] is not None and data['tool'] == 'send_email':
        return email_llm(query, chat_history)
    elif data['tool'] is not None and data['tool'] == 'get_github_commits':
        return get_github_commits(query, chat_history)

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
    
    # Step 1: Fetch available tools from the local server.
    tools = fetch_available_tools()
    chat_history = []
    while True:
        # Step 2: Accept a query from the user.
        
        query = input("user: ")
        if query.lower() == "exit":
            break
        result = ""
        # Step 3: Send the query and available tools to Gemini.
        llm_output = get_llm_decision(query, tools,chat_history)

        print(llm_output, "\n")


        if "email_action" in llm_output and llm_output["email_action"] == True:
            # Step 4: Instruct the local server to execute the tool.
            result = execute_tool(llm_output["tool"], llm_output["parameters"])
            result = f"\ncontext: {result}"
            print("\nTool Execution Result:\n")

        elif "get_github_commits" in llm_output and llm_output["get_github_commits"] == True:
            # Step 5: Instruct the local server to execute the tool.
            result = execute_tool(llm_output["tool"], llm_output["parameters"])
            result = f"\ncontext: {result}"
            print("\nTool Execution Result:\n")

        elif "email_action" in llm_output and llm_output["email_action"] == False:
          result = 'no relevant email id found in available emails and in our chat history.'

        elif "get_github_commits" in llm_output and llm_output["get_github_commits"] == True:
          if llm_output["parameters"]["user_name"] is None and llm_output["parameters"]["repo_name"] is None:
            result = 'please provide github user_name and repo_name'
          elif llm_output["parameters"]["user_name"] is None:
            result = 'please provide github user_name'
          elif llm_output["parameters"]["repo_name"] is None:
            result = 'please provide github repo_name'

        elif llm_output['tool'] is None:
            print("\n go with simple chat as no tools required detected.")
            pass
        model_query = query + result
        # Create the model
        print("\nModel Query:\n", model_query)
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
                            Ask for the user's name in the second message, but only if they haven't already provided it. Once they share it, remember it throughout the conversation.
                            Engage in a friendly, natural way, like a real friend. Keep the conversation smooth and enjoyable.
                            If a query includes a provided "context," always assume that this context was generated by a tool available on the server and not provided directly by the user.
                            The context is the result of a tool’s execution, such as fetching recent data, retrieving stored information, or generating content, and it contains the necessary details to resolve the user's query.
                            Use the given context to generate accurate and relevant responses.
                            Utilize chat history to maintain continuity and understand the flow of the conversation."
                            """)
        chat_session = chat_model.start_chat(
                    history=chat_history
                )
        response = chat_session.send_message(model_query)

        model_response=response.text
        print("\nModel Response:\n", model_response)
        chat_history.append({"role": "user", "parts": [{"text": query}]})
        chat_history.append({"role": "assistant", "parts": [{"text": model_response}]})


if __name__ == "__main__":
    # Configure Gemini with your API key.
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    main()
