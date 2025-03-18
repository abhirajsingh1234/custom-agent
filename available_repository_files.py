import requests
import os
def get_github_repository_files(owner, repo, path=""):
    """
    Get a list of files and directories from a GitHub repository at a specific path.
    
    Parameters:
    -----------
    owner : str
        The GitHub username or organization that owns the repository
    repo : str
        The repository name
    path : str, optional
        Directory path within the repository (defaults to root)
    api_key : str, optional
        GitHub personal access token for authentication
    
    Returns:
    --------
    dict
        Dictionary containing lists of files and directories
    """
    api_key = os.getenv("GITHUB_TOKEN")
    try:
        headers = {}
        if api_key:
            headers["Authorization"] = f"token {api_key}"
        
        # GitHub API endpoint for repository contents
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors

        contents = response.json()

        # If it's a single file, wrap it in a list for consistent handling
        if not isinstance(contents, list):
            contents = [contents]

        files = []
        directories = []

        for item in contents:
            item_info = {
                "name": item["name"],
                "path": item["path"],
                "type": item["type"]
            }

            if item["type"] == "dir":
                directories.append(item_info)
            elif item["type"] == "file":
                files.append(item_info)

        return {
            "repository": f"{owner}/{repo}",
            "path": path if path else "root",
            "total files": len(files),
            "total directories": len(directories),
            "directories": directories,
            "files": files
        }
    except requests.exceptions.HTTPError as e:
        return f"error while fetching repository files for {owner}/{repo}"
# Example usage
if __name__ == "__main__":
    owner = "abhirajsingh1234"
    repo = "custom-MCP"
    
    try:
        # Get repository root contents
        repo_contents = get_github_repository_files(owner, repo)
        
        print(f"Contents of {repo_contents['repository']} ({repo_contents['path']}):")
        
        print("\nDirectories:")
        for directory in repo_contents["directories"]:
            print(f"📁 {directory['name']}")
            
        print("\nFiles:")
        for file in repo_contents["files"]:
            print(f"📄 {file['path']}")
            
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")