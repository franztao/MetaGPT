import asyncio
import os

import pytest

from metagpt.llm import LLM
from metagpt.logs import logger
from metagpt.roles.project_reasoner import ProjectReasoner
from metagpt.utils.text import generate_prompt_chunk

# # 背景
# 【AI芯片基准测试标准化难题及FlagPerf诞生的背景】
# 1.行业痛点
# - 缺乏公认标准：AI芯片领域长期缺乏统一的基准测试规范和标准体系
# - 技术生态复杂：呈现"三维爆炸"特征
# - 硬件维度：X款异构芯片架构百花齐放
# - 软件维度：Y个主流AI框架技术栈差异大
# - 算法维度：Z类模型持续涌现，覆盖CV/NLP/多模态等场景
# 2.标准化挑战
# - 适配复杂度指数级增长：理论需完成X×Y×Z种组合的适配验证
# - 动态扩展压力：各维度技术栈持续快速演进
# - 落地实施难度：传统方案需投入大量人力完成环境部署、接口适配、版本兼容
#
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
task_description = r'当前项目目标是”对wudao数据集和lama3-8B模型在1机8卡上适配沐曦 C500的GPU显卡，最后得到loss数值和tokens per gpu per second(tgs)“。'
role = r'您是项目的第一位处理人（项目经理，产品经理，架构师），首先你会阅读大量资料如readme等（```长期记忆```），然后进行理解、分析和推理，确定项目接下来的负责人（配置部署工程师）还需要做哪些,比如接下来的负责人需要做哪些操作准备，下载哪些数据、代码和模型checkpoint等，需要修改哪些代码，和一些必要的前置条件，如果自己有不清楚和疑问,通过工具通过ls,cat等linux查询命令去查看当前环境信息。如果通过工具还有不清楚的就提出问题来。最后列出接下来的负责人需要做哪些的清单，自己不要调用工具去改变当前运行环境。'
requirements = r'当前运行环境是linux正在运行的容器中，当前FlagPerf的git库地址在"/home/htao/debug/FlagPerf",调用的工具一定在提供的工具列表范围内，不要捏造和越权调用其它未指定的工具。调用工具一定不要有删除卸载等（rm,delete）高危操作。调用工具出现权限不够的情况就不要再去解决，在最后总结出有这个问题存在就行。'
goal = f'{task_description}。{role}。{requirements}'

# 再通过shell工具查看当前环境是否具备运行调试等的条件
memory_short = ''
memory_long = ''
output_demand = '''你调用工具只有查的权限，没有增删改的权限。输出结论包括：
项目接下来的负责人（配置部署工程师）还需要做哪些,比如需要做哪些操作准备，下载哪些数据、代码和模型checkpoint等，需要修改哪些代码，和一些必要的前置条件。尽量完成项目任务，不能逃避和客套话回复（如"要不咱们换个话题？"）。
'''


def judge_path(p2, content):
    if p2.endswith(".md") or p2.endswith(".sh"):
        print(p2)
        with open(p2, "r", encoding="utf-8") as f:
            ls = f.readlines()
        content = content + "\n" + "---" * 1 + "\n文件地址" + p2 + "\n文件中内容:\n" + ''.join(ls) + "\n" + "---" * 1
    return content


def rec_dir(src, content):
    fs1 = os.listdir(src)
    content = ""
    for f1 in fs1:
        p2 = os.path.join(src, f1)
        if os.path.isdir(p2):
            fs2 = os.listdir(p2)
            for f2 in fs2:
                p3 = os.path.join(src, f1, f2)
                if os.path.isdir(p3):
                    fs3 = os.listdir(p3)
                    for f3 in fs3:
                        p4 = os.path.join(src, f1, f2, f3)
                        if os.path.isdir(p4):
                            fs4 = os.listdir(p4)
                            for f4 in fs4:
                                pass
                            continue
                        else:
                            content = judge_path(p4, content)
                    continue
                else:
                    content = judge_path(p3, content)
            continue
        else:
            content = judge_path(p2, content)
    return content


async def get_content(content):
    # content = content.inner_text
    chunk_summaries = []
    query = task_description
    from metagpt.actions.research import WEB_BROWSE_AND_SUMMARIZE_PROMPT
    prompt_template = WEB_BROWSE_AND_SUMMARIZE_PROMPT.format(query=query, content="{}")
    llm = LLM()
    pts=generate_prompt_chunk(content, prompt_template, "DeepSeek-R1", "", 4096)
    # l=len(list(pts))
    # logger.debug(f"pts:{l}")
    for prompt in pts:
        logger.debug(prompt)
        summary = await llm.aask(prompt, [""])
        logger.info(f"get_content:{summary}")
        if summary == "Not relevant.":
            continue
        chunk_summaries.append(summary)

    if len(chunk_summaries) == 1:
        return chunk_summaries[0]

    content = "\n".join(chunk_summaries)
    # prompt = WEB_BROWSE_AND_SUMMARIZE_PROMPT.format(query=query, content=content)
    # summary = await llm.aask(prompt, [system_text])
    return content


async def f1():
    content = ""
    # src = r'C:\Users\m01216.METAX-TECH\Desktop\code\FlagPerf'
    src = r'C:\Users\m01216.METAX-TECH\Desktop\code\FlagPerf\training\nvidia\llama3_8B-megatron'
    if os.path.exists(src):
        pass
    else:
        src = r'/home/htao/debug/FlagPerf/training/nvidia/llama3_8B-megatron'
    content = rec_dir(src, content)

    src = r'C:\Users\m01216.METAX-TECH\Desktop\code\FlagPerf\training\benchmarks\llama3_8B\megatron'
    if os.path.exists(src):
        pass
    else:
        src = r'/home/htao/debug/FlagPerf/training/benchmarks/llama3_8B/megatron'
    content = rec_dir(src, content)

    p2 = r'C:\Users\m01216.METAX-TECH\Desktop\code\FlagPerf\README.md'
    if os.path.exists(p2):
        pass
    else:
        p2 = r'/home/htao/debug/FlagPerf/README.md'
    with open(p2, "r", encoding="utf-8") as f:
        ls = f.readlines()
    content = content + "\n" + "---" * 1 + "\n文件地址" + p2 + "\n文件中内容:\n" + ''.join(ls) + "\n" + "---" * 1

    p2 = r'C:\Users\m01216.METAX-TECH\Desktop\code\MetaGPT\metagpt\roles\data\project_reasoner\input1.txt'
    if os.path.exists(p2):
        pass
    else:
        p2 = r'/home/htao/debug/MetaGPT/metagpt/roles/data/project_reasoner/input1.txt'
    with open(p2, "r", encoding="utf-8") as f:
        ls = f.readlines()
    content = content + "\n" + "---" * 1 + "\n文件地址" + p2 + "\n文件中内容:\n" + ''.join(ls) + "\n" + "---" * 1

    p2 = r'C:\Users\m01216.METAX-TECH\Desktop\code\MetaGPT\metagpt\roles\data\project_reasoner\input2.txt'
    if os.path.exists(p2):
        pass
    else:
        p2 = r'/home/htao/debug/MetaGPT/metagpt/roles/data/project_reasoner/input2.txt'
    with open(p2, "r", encoding="utf-8") as f:
        ls = f.readlines()
    content = content + "\n" + "---" * 1 + "\n文件地址" + p2 + "\n文件中内容:\n" + ''.join(ls) + "\n" + "---" * 1


    p2 = r'C:\Users\m01216.METAX-TECH\Desktop\code\MetaGPT\metagpt\roles\data\project_reasoner\input3.txt'
    if os.path.exists(p2):
        pass
    else:
        p2 = r'/home/htao/debug/MetaGPT/metagpt/roles/data/project_reasoner/input3.txt'
    with open(p2, "r", encoding="utf-8") as f:
        ls = f.readlines()
    content = content + "\n" + "---" * 1 + "\n文件地址" + p2 + "\n文件中内容:\n" + ''.join(ls) + "\n" + "---" * 1


    content = await get_content(content)

    pt = prompt.format(goal=goal, memory_short=memory_short, memory_long=content, output_demand=output_demand)
    print(pt)
    # print(content)
    print(len(pt))
    return pt


# mocker
# @pytest.mark.asyncio
async def test_interpreter_react_mode():
    # mocker.patch("metagpt.actions.di.execute_nb_code.ExecuteNbCode.run", return_value=("a successful run", True))

    content = await f1()
    print(content)
    requirement = content

    di = ProjectReasoner(react_mode="plan_and_act", tools=["shell_tool"], max_react_loop=3)
    rsp = await di.run(requirement)
    logger.info(f"final result:{rsp}")
    logger.info(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    assert len(rsp.content) > 0


# C:\Users\m01216.METAX-TECH\.conda\envs\metagpt\python.exe  C:\Users\m01216.METAX-TECH\Desktop\code\MetaGPT\tests\metagpt\roles\test_project_reasoner.py
# /home/htao/miniconda3/envs/metagpt39/bin/python /home/htao/debug/MetaGPT/tests/metagpt/roles/test_project_reasoner.py
if __name__ == '__main__':
    asyncio.run(test_interpreter_react_mode())
