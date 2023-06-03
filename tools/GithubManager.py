from github import Github, GithubException
import json

class GithubManager():
    def __init__(self, token):
        self.github = Github(token)
        self.user = self.github.get_user()

    def repo_exists(self, repo_name):
        return any(repo.name == repo_name for repo in self.user.get_repos())

    def create_repo(self, repo_name):
        if self.repo_exists(repo_name):
            raise GithubException(f'Repository "{repo_name}" already exists in your account.')
        else:
            try:
                self.user.create_repo(repo_name)
                print(f'Successfully created repository "{repo_name}"')
            except GithubException as e:
                print(f'An error occurred: {e}')

    def add_file(self, json_input:str):
        arguments_dictory = json.loads(json_input)
        repo_name = arguments_dictory["repository_name"]
        file_name = arguments_dictory["file_name"]
        file_path = arguments_dictory["file_path"]
        file_content = arguments_dictory["file_content"]

        repo = self.get_repo(repo_name)
        try:
            repo.create_file(file_path, f"add file {file_path}", file_content)
            print(f'Successfully added file "{file_path}" to repository "{repo_name}"')
        except GithubException as e:
            print(f'An error occurred: {e}')

    def get_file_sha(self, repo, file_path):
        contents = repo.get_contents(file_path)
        return contents.sha

    def update_file(self, json_input:str):
        arguments_dictory = json.loads(json_input)
        repo_name = arguments_dictory["repository_name"]
        file_path = arguments_dictory["file_path"]
        file_content = arguments_dictory["file_content"]
        
        repo = self.get_repo(repo_name)
        try:
            sha = self.get_file_sha(repo, file_path)
            repo.update_file(file_path, f"update file {file_path}", file_content, sha)
            print(f'Successfully updated file "{file_path}" in repository "{repo_name}"')
        except GithubException as e:
            print(f'An error occurred: {e}')    
    

    # Tool Names, Formats, and Descriptions
    creator_tool_name = "GithubRepoCreator"
    creator_tool_description = "Helps to create a Github Repository with a specified name."

    addFile_tool_name = "GithubAddFile"
    addFile_tool_requestFormat = '{{"repository_name":"<string>","file_name": "<string>", "file_path": "<string>", "file_content": "<string>"}}'
    addFile_tool_description = f"Helps to add a file to a Github Repository.  Input should be JSON in the following format: {addFile_tool_requestFormat}"

    updateFile_tool_name = "GithubUpdateFile"
    updateFile_tool_requestFormat = '{{"repository_name":"<string>","file_path": "<string>", "file_content": "<string>"}}'
    updateFile_tool_description = f"Helps to update a file in a Github Repository.  Input should be JSON in the following format: {updateFile_tool_requestFormat}"
    
