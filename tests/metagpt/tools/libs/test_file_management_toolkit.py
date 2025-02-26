import asyncio
from metagpt.roles.di.data_interpreter import DataInterpreter


async def main(requirement: str):
    role = DataInterpreter(tools=["file_management_toolkit"])  # 集成工具
    await role.run(requirement)


def test_shell_tool(mocker):
    requirement = r"请在地址'C:\Users\m01216.METAX-TECH\Desktop\code\MetaGPT\tests\metagpt\tools\libs\data'下创建一个文件并且写入字符串“123”"
    asyncio.run(main(requirement))
