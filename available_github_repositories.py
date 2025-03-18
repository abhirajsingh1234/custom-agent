import requests
import os

def get_github_repositories(username):
    """
    Fetch all GitHub repositories for a given username using the GitHub API.
    
    Parameters:
    -----------
    username : str
        The GitHub username whose repositories you want to retrieve
    api_key : str, optional
        GitHub personal access token for authentication
        Using an API key increases rate limits and allows access to private repos
    
    Returns:
    --------
    list
        A list of repository names belonging to the specified user
    
    Raises:
    -------
    requests.exceptions.HTTPError
        If the API request fails (e.g., user not found, rate limit exceeded)
    """
    api_key = os.getenv("GITHUB_TOKEN")
    headers = {}
    if api_key:
        headers["Authorization"] = f"token {api_key}"
    
    # GitHub API endpoint for user repositories
    url = f"https://api.github.com/users/{username}/repos"
    
    # Parameters to get all repositories (100 per page is the max)
    params = {
        "per_page": 100,
        "page": 1
    }
    
    all_repos = []
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Get repositories from current page
        repos_page = response.json()
        
        # If no more repositories, break the loop
        if not repos_page:
            break
            
        # Extract repo names and add to our list
        repo_names = [repo["name"] for repo in repos_page]
        all_repos.extend(repo_names)
        
        # Move to the next page
        params["page"] += 1
        
        # Check if we're on the last page using Link header
        if "Link" not in response.headers or 'rel="next"' not in response.headers["Link"]:
            break
    numbered_repos = [f"{i+1}. {repo}," for i, repo in enumerate(all_repos)]
    newline = "\n"
    repo_list = newline.join(numbered_repos)
    return {
        "username": username,
        "total repositories": len(all_repos),
        "repositories": repo_list
    }

# Example usage
if __name__ == "__main__":
    username = "abhirajsingh1234"  # Example GitHub username
    api_key = os.getenv("GITHUB_TOKEN")  # Optional
    
    try:
        repos = get_github_repositories(username)
        print(f"{repos}")
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")