from github import Github, GithubException
import json

class GithubManager():
    def __init__(self, token):
        self.github = Github(token)
        self.user = self.github.get_user()

    def repo_exists(self, repo_name):
        return any(repo.name == repo_name for repo in self.user.get_repos())
    
    def repo_lookup(self, json_input:str):
        arguments_dictory = json.loads(json_input)
        repo_name = arguments_dictory["repository_name"]

        if self.repo_exists(repo_name):
            return f'Repository "{repo_name}" exists in your account.'
        else:
            return f'Repository "{repo_name}" does not exist in your account.'

    def create_repo(self, json_input:str):
        arguments_dictory = json.loads(json_input)
        repo_name = arguments_dictory["repository_name"]

        if self.repo_exists(repo_name):
            return f'Repository "{repo_name}" already exists in your account.'
        else:
            try:
                print(f'Creating repository "{repo_name}"')
                self.user.create_repo(repo_name)
                return f'Successfully created repository "{repo_name}"'
            except GithubException as e:
                return f'Repository Already Exists: {e}'

    def add_file(self, json_input:str):
        arguments_dictory = json.loads(json_input)
        repo_name = arguments_dictory["repository_name"]
        file_path = arguments_dictory["file_path"]
        file_content = arguments_dictory["file_content"]

        repo = self.get_repo(repo_name)
        try:
            repo.create_file(file_path, f"add file {file_path}", file_content)
            return f'Successfully added file "{file_path}" to repository "{repo_name}"'
        except GithubException as e:
            return f'An error occured {e}'

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
            return f'Successfully updated file "{file_path}" in repository "{repo_name}"'
        except GithubException as e:
            return f'An error occurred: {e}'
    
    def get_repo(self, repo_name):
        if self.repo_exists(repo_name):
            return self.user.get_repo(repo_name)
        else:
            return GithubException(f'Repository "{repo_name}" does not exist in your account.')

    # Tool Names, Formats, and Descriptions
    creator_tool_name = "GithubRepoCreator"
    creator_tool_requestFormat = '{{"repository_name":"<string>"}}'
    creator_tool_description = f"Helps to create a Github Repository with a specified name. Input should be JSON in the following format: {creator_tool_requestFormat}.  Use Double Quotes around property names and values."

    addFile_tool_name = "GithubAddFile"
    addFile_tool_requestFormat = '{{"repository_name":"<string>", "file_path": "<string>", "file_content": "<string>"}}'
    addFile_tool_description = f"Helps to add a file to a Github Repository.  Input should be JSON in the following format: {addFile_tool_requestFormat}.  Use Double Quotes around property names and values."

    updateFile_tool_name = "GithubUpdateFile"
    updateFile_tool_requestFormat = '{{"repository_name":"<string>","file_path": "<string>", "file_content": "<string>"}}'
    updateFile_tool_description = f"Helps to update a file in a Github Repository.  Input should be JSON in the following format: {updateFile_tool_requestFormat}.  Use Double Quotes around property names and values."

    lookup_repo_tool_name = "GithubLookupRepo"
    lookup_repo_tool_requestFormat = '{{"repository_name":"<string>"}}'
    lookup_repo_tool_description = f"Helps to lookup a Github Repository.  Input should be JSON in the following format: {lookup_repo_tool_requestFormat}.  Use Double Quotes around property names and values."
