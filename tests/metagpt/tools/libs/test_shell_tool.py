


import asyncio
from metagpt.roles.di.data_interpreter import DataInterpreter


async def main(requirement: str):
    role = DataInterpreter(tools=["file_management_toolkit"]) # 集成工具
    await role.run(requirement)

def test_shell_tool(mocker):
    requirement = r"请查看系统状态"
    asyncio.run(main(requirement))