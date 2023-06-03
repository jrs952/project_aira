# define a function to set up Github Tools
from langchain.agents import Tool
import GithubManager

def setup_tools(ghManager: GithubManager):
    tools = [
        Tool(
            name=ghManager.creator_tool_name,
            description=ghManager.creator_tool_description,
            action=ghManager.create_repo
        ),
        Tool(
            name=ghManager.addFile_tool_name,
            description=ghManager.addFile_tool_description,
            action=ghManager.add_file
        ),
        Tool(
            name=ghManager.updateFile_tool_name,
            description=ghManager.updateFile_tool_description,
            action=ghManager.update_file
        )
    ]
    return tools
