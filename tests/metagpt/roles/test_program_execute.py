import asyncio
import os

import pytest

from metagpt.llm import LLM
from metagpt.logs import logger
from metagpt.roles.config_deploy import ConfigDeploy
from metagpt.roles.program_execute import ProgramExecute
from metagpt.roles.project_reasoner import ProjectReasoner
from metagpt.utils.text import generate_prompt_chunk

prompt = """
# 目标，任务描述
***
{goal}
***
# 短期记忆
***
{memory_short}
***
# 长期记忆
***
{memory_long}
***
# 限制
***
{output_demand}
***
# 输出

"""

# import jionlp as jio
task_description = r'当前项目目标是”对wudao数据集和lama3-8B模型在1机1卡上适配Nvidia A100的GPU显卡，最后得到loss数值和tokens per gpu per second(tgs)“。'
role = r'您是项目的第三位处理人，负责项目在机器上执行，首先你会阅读上一位处理人输出的配置完成报告（```短期记忆```），然后进行理解和执行、运行程序过程中，会出现异常情况则思考出解决方案，并且调用工具解决，通过shell工具运行程序保证运行成功。运行成功后，对最后运行结果进行搜集'
requirements = r'当前运行环境是linux，当前FlagPerf的git库地址在"/home/hengtao/debug/step3/FlagPerf",数据和模型地址在"/home/hengtao/code/task/llama3_8B/megatron_llama3/data_dir",调用工具一定不要有删除卸载等高危操作。当前执行环境是在容器内。'
goal = f'{task_description}。{role}。{requirements}'

# 再通过shell工具查看当前环境是否具备运行调试等的条件
memory_short = ''
memory_long = ''
output_demand = '''尽量完成项目任务，不能逃避和客套话回复（如"要不咱们换个话题？"）。
'''


async def test_program_execute():
    # mocker.patch("metagpt.actions.di.execute_nb_code.ExecuteNbCode.run", return_value=("a successful run", True))

    content = ""
    p2 = r'C:\Users\m01216.METAX-TECH\Desktop\code\MetaGPT\metagpt\roles\data\project_reasoner\step3_input_0306.txt'
    if os.path.exists(p2):
        pass
    else:
        p2 = r'/home/hengtao/debug/MetaGPT/metagpt/roles/data/project_reasoner/step3_input_0306.txt'
    with open(p2, "r", encoding="utf-8") as f:
        ls = f.readlines()
    memory_short = content + "\n" + "---" * 1 + "\n文件地址" + p2 + "\n文件中内容:\n" + ''.join(ls) + "\n" + "---" * 1

    p2 = r'C:\Users\m01216.METAX-TECH\Desktop\code\FlagPerf\README.md'
    if os.path.exists(p2):
        pass
    else:
        p2 = r'/home/hengtao/debug/step3/FlagPerf/README.md'
    with open(p2, "r", encoding="utf-8") as f:
        ls = f.readlines()
    memory_long = content + "\n" + "---" * 1 + "\n文件地址" + p2 + "\n文件中内容:\n" + ''.join(ls) + "\n" + "---" * 1
    l=max(1,len(memory_long) - 30000)
    requirement = prompt.format(goal=goal, memory_short=memory_short,
                                memory_long=memory_long[0:l], output_demand=output_demand)

    di = ProgramExecute(react_mode="react", tools=["shell_tool"])
    rsp = await di.run(requirement)
    logger.info(f"final result:{rsp}")
    assert len(rsp.content) > 0


# C:\Users\m01216.METAX-TECH\.conda\envs\metagpt\python.exe  C:\Users\m01216.METAX-TECH\Desktop\code\MetaGPT\tests\metagpt\roles\test_project_reasoner.py
#   /home/hengtao/miniconda3/envs/metagpt39/bin/python   /home/hengtao/debug/MetaGPT/tests/metagpt/roles/test_program_execute.py
if __name__ == '__main__':
    asyncio.run(test_program_execute())
