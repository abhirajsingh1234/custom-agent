import requests
import os
import dotenv

dotenv.load_dotenv()
# GitHub repository details




# Authentication (for private repos, use a Personal Access Token)
  # Store your token as an environment variable

# Function to retrieve commits
def get_github_commits(detail_type="all",num_commits=5,GITHUB_USERNAME = "abhirajsingh1234",REPO_NAME = "custom-MCP",BRANCH_NAME = "main"):
    # GitHub API URL
    API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/commits?sha={BRANCH_NAME}"
    print("API URL:", API_URL)
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    response = requests.get(API_URL, headers=headers)
    print("Response status code:", response.status_code)
    if response.status_code == 200:
        commits = response.json()
        
        print(f"\nRecent commits from {REPO_NAME} (filtered by: {detail_type}):\n")

        commit_author = [commit["commit"]["author"]["name"] for commit in commits[:num_commits]]
        commit_date = [commit["commit"]["author"]["date"] for commit in commits[:num_commits]]
        commit_message = [commit["commit"]["message"] for commit in commits[:num_commits]]

        if detail_type == "message":
            return f"- {commit_message}"
        elif detail_type == "author":
            return f"- {commit_author}"
        elif detail_type == "date":
            return f"- {commit_date}"
        else:  # If "all" or unspecified, return everything
            return [f"commit '{commit_message}' by {commit_author} on {commit_date}" for commit_message, commit_author, commit_date in zip(commit_message, commit_author, commit_date)]

    else:
        return f"Error fetching commits: on {GITHUB_USERNAME}/{REPO_NAME} check if the user or repository exists and you have the correct permissions."

