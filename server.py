from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from mail_sender import send_email
from github_commits_fetcher import get_github_commits
from linkedin_details_fetcher import fetch_linkedin_details

app = FastAPI()

# Define available tools with descriptions.
available_tools = {
    "send_email": "Send an email to a provided email id",
    "get_github_commits": "Get recent commits from a GitHub repository",
    "fetch_linkedin_details": "Get details from a LinkedIn profile"
}

# Request model for executing a tool.
class ExecuteRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]

@app.get("/tools")
async def get_tools():
    """
    Endpoint to retrieve all available tools.
    """
    return {"available_tools": available_tools}

@app.post("/execute")
async def execute_tool(request: ExecuteRequest):
    """
    Endpoint to execute a specified tool with given parameters.
    """
    tool_name = request.tool_name
    parameters = request.parameters
    if tool_name not in available_tools:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    if tool_name == "send_email":
        # Extract parameters for sending email.
        email_id = parameters.get("email_id")
        subject = parameters.get("subject", "No Subject")
        body = parameters.get("body", "")
        
        if not email_id:
            raise HTTPException(status_code=400, detail="Missing email_id parameter")

        # Call our email_sender.send_email function
        result = send_email(email_id, subject, body)
        return result
    elif tool_name == "get_github_commits":
        # Extract parameters for getting GitHub commits.
        user_name = parameters.get("user_name")
        repo_name = parameters.get("repo_name")
        detail_type = parameters.get("detail_type").lower()
        num_commits = parameters.get("num_commits")
        
        # Call our github_commit.get_github_commits function
        result = get_github_commits(detail_type, num_commits, user_name, repo_name)
        return result
    elif tool_name == "fetch_linkedin_details":
        # Extract parameters for fetching LinkedIn details.
        username = parameters.get("username")
        
        if not username:
            raise HTTPException(status_code=400, detail="Missing username parameter")
        
        # Call our linkedin_details_fetcher.fetch_linkedin_details function
        result = fetch_linkedin_details(username)
        return result
    
    raise HTTPException(status_code=400, detail="Tool execution not implemented")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
