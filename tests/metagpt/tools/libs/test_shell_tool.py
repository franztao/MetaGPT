


import asyncio
from metagpt.roles.di.data_interpreter import DataInterpreter


async def main(requirement: str):
    role = DataInterpreter(tools=["shell_tool"]) # 集成工具
    await role.run(requirement)

def test_shell_tool(mocker):
    requirement = r"请查看地址'C:\Users\m01216.METAX-TECH\Downloads\node-v23.8.0-win-x64'下的所有文件"
    asyncio.run(main(requirement))