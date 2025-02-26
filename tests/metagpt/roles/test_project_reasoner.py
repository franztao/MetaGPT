import os

import pytest

from metagpt.logs import logger
from metagpt.roles.project_reasoner import ProjectReasoner

prompt = """
# 背景
您是一位GPU显卡硬件评测引擎，旨在建立以产业实践为导向的指标体系，评测AI硬件在软件栈组合（模型+框架+编译器）下的实际能力。您是项目的第一位负责人，首先你会阅读大量资料，然后分析和推理，再通过shell工具查看当前环境是否具备运行调试等的条件，确定项目接下来还需要具备哪些条件和内容，如果自己不清楚和疑问的就提出来。
# 目标，任务描述
```
{goal}
```
# 短期记忆
```
{memory_short}
```
# 长期记忆
```
{memory_long}
```
# 限制
```
{output_demand}
```
# 输出

"""

# import jionlp as jio
goal = r'在FlagPerf AI硬件评测引擎下，如何对wudao数据集和lama3-8B模型在1机8卡上适配Nvidia A100的GPU显卡。当前运行环境是linux，当前FlagPerf的git库地址在"/home/hengtao/debug/FlagPerf"'
memory_short = ''
memory_long = ''
output_demand = '''输出结论包括：
整体规划
适配该模型所需的硬件环境配置和软件环境配置
在Linux操作系统中如何查阅这些配置
完成适配任务所需的代码、模型、数据、镜像等
'''


def judge_path(p2, content):
    if p2.endswith(".md"):
        print(p2)
        with open(p2, "r", encoding="utf-8") as f:
            ls = f.readlines()
        content = content + "\n" + "---" * 5 + "\n文件地址" + p2 + "\n文件中内容:\n" + ''.join(ls) + "\n" + "---" * 5
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


def f1():
    content = ""
    # src = r'C:\Users\m01216.METAX-TECH\Desktop\code\FlagPerf'
    src = r'C:\Users\m01216.METAX-TECH\Desktop\code\FlagPerf\training\nvidia\llama3_8B-megatron'
    content = rec_dir(src, content)
    # src = r'C:\Users\m01216.METAX-TECH\Desktop\code\FlagPerf\training\benchmarks\llama3_8B\megatron'
    # content = rec_dir(src, content)

    # p2 = r'C:\Users\m01216.METAX-TECH\Desktop\code\FlagPerf\README.md'
    # with open(p2, "r", encoding="utf-8") as f:
    #     ls = f.readlines()
    # content = content + "\n" + "---" * 5 + "\n文件地址" + p2 + "\n文件中内容:\n" + ''.join(ls) + "\n" + "---" * 5

    pt = prompt.format(goal=goal, memory_short=memory_short, memory_long=content, output_demand=output_demand)
    print(pt)
    # print(content)
    print(len(pt))
    return pt


@pytest.mark.asyncio
async def test_interpreter_react_mode(mocker):
    # mocker.patch("metagpt.actions.di.execute_nb_code.ExecuteNbCode.run", return_value=("a successful run", True))

    content = f1()
    requirement = content

    di = ProjectReasoner(react_mode="react", tools=["shell_tool"])
    rsp = await di.run(requirement)
    logger.info(rsp)
    assert len(rsp.content) > 0
