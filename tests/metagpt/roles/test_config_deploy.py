import asyncio
import os

from metagpt.logs import logger
from metagpt.roles.config_deploy import ConfigDeploy

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
role = r'您是项目的第二位处理人，负责项目在机器上配置部署，首先你会阅读上一位处理人输出的项目分析报告（```短期记忆```），你是按照```短期记忆```里包含的行动内容为指导进行操作，然后进行理解和执行、确定自己做哪些,比如哪些操作准备，下载哪些数据、代码和模型checkpoint等，要修改哪些代码，和操作一些必要的前置条件，通过工具执行具体的配置部署。不要运行和监听flagperf基准测试，这是属于第三位处理人的工作。'
requirements = r'当前运行环境是linux正在运行的容器中，当前FlagPerf的git库地址在"/home/hengtao/debug/step2/FlagPerf",数据和模型地址在"/home/hengtao/code/task/llama3_8B/megatron_llama3/data_dir",参考的模板地址是“/home/hengtao/debug/step2/FlagPerf/training/nvidia/llama3_8B-megatron/config/config_A100x1x8.py”,magatron的地址是“/workspace/Megatron-LM”,调用工具一定不要有删除卸载等高危操作'
goal = f'{task_description}。{role}。{requirements}'

# 再通过shell工具查看当前环境是否具备运行调试等的条件
memory_short = ''
memory_long = ''
output_demand = '''尽量完成项目任务，不能逃避和客套话回复（如"要不咱们换个话题？"）。
'''


async def test_config_deploy():
    # mocker.patch("metagpt.actions.di.execute_nb_code.ExecuteNbCode.run", return_value=("a successful run", True))

    content = ""
    p2 = r'C:\Users\m01216.METAX-TECH\Desktop\code\MetaGPT\metagpt\roles\data\project_reasoner\step2_input_0228.txt'
    if os.path.exists(p2):
        pass
    else:
        p2 = r'/home/hengtao/debug/MetaGPT/metagpt/roles/data/project_reasoner/step2_input_0228.txt'
    with open(p2, "r", encoding="utf-8") as f:
        ls = f.readlines()
    memory_short = content + "\n" + "---" * 1 + "\n文件地址" + p2 + "\n文件中内容:\n" + ''.join(ls) + "\n" + "---" * 1

    requirement = prompt.format(goal=goal, memory_short=memory_short, memory_long="", output_demand=output_demand)

    di = ConfigDeploy(react_mode="plan_and_act", tools=["shell_tool"], max_react_loop=2)
    rsp = await di.run(requirement)
    logger.info(f"final result:{rsp}")
    logger.info(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    assert len(rsp.content) > 0


# C:\Users\m01216.METAX-TECH\.conda\envs\metagpt\python.exe  C:\Users\m01216.METAX-TECH\Desktop\code\MetaGPT\tests\metagpt\roles\test_project_reasoner.py
#  /home/hengtao/miniconda3/envs/metagpt39/bin/python  /home/hengtao/debug/MetaGPT/tests/metagpt/roles/test_config_deploy.py
if __name__ == '__main__':
    asyncio.run(test_config_deploy())
