from __future__ import annotations

from typing import (
    Any,
)

from langchain_community.agent_toolkits import FileManagementToolkit

from metagpt.tools.tool_registry import register_tool


@register_tool(tags=["file_management_toolkit"])
def file_management_toolkit(root_dir, selected_tool: str, file_path: str, destination_path: str, text: str) -> Any:
    """Toolkit for interacting with local files.

        *Security Notice*: This toolkit provides methods to interact with local files.
            If providing this toolkit to an agent on an LLM, ensure you scope
            the agent's permissions to only include the necessary permissions
            to perform the desired operations.

            By **default** the agent will have access to all files within
            the root dir and will be able to Copy, Delete, Move, Read, Write
            and List files in that directory.

            Consider the following:
            - Limit access to particular directories using `root_dir`.
            - Use filesystem permissions to restrict access and permissions to only
              the files and directories required by the agent.
            - Limit the tools available to the agent to only the file operations
              necessary for the agent's intended use.
            - Sandbox the agent by running it in a container.

            See https://python.langchain.com/docs/security for more information.

        Parameters:
            root_dir: Optional. The root directory to perform file operations.
                If not provided, file operations are performed relative to the current
                working directory.
            selected_tool: Optional. The tools to include in the toolkit. If not
                provided,  tool is empty. 获取特定工具 "move_file","file_search","copy_file","write_file","read_file","list_directory"
            file_path:
            destination_path:
            text:
        """
    toolkit = FileManagementToolkit(
        root_dir=str(root_dir),
        selected_tools=[selected_tool, ]
    )  # If you don't provide a root_dir, operations will default to the current working directory
    tools = toolkit.get_tools()

    # 获取特定工具 "move_file","file_search","copy_file","write_file","read_file","list_directory"

    tool = next(tool for tool in tools)
    result = ""

    if selected_tool == "move_file":
        result = tool.invoke({"source_path": file_path, 'destination_path': destination_path})

    if selected_tool == "file_search":
        result = tool.invoke({"dir_path": file_path})

    if selected_tool == "copy_file":
        result = tool.invoke({"source_path": file_path, 'destination_path': destination_path})

    if selected_tool == "write_file":
        result = tool.invoke({
            "file_path": file_path,
            "text": text
        })

    if selected_tool == "read_file":
        result = tool.invoke({"file_path": file_path})

    if selected_tool == "list_directory":
        result = tool.invoke({"dir_path": file_path})

    return result
