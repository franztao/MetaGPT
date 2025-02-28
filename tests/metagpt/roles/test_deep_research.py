import asyncio
import os

import pytest

from metagpt.llm import LLM
from metagpt.logs import logger
from metagpt.roles.config_deploy import ConfigDeploy
from metagpt.roles.deep_research import DeepResearch
from metagpt.roles.program_execute import ProgramExecute
from metagpt.roles.project_reasoner import ProjectReasoner
from metagpt.utils.text import generate_prompt_chunk

prompt = """
# 背景
【AI芯片基准测试标准化难题及FlagPerf诞生的背景】
1.行业痛点
- 缺乏公认标准：AI芯片领域长期缺乏统一的基准测试规范和标准体系
- 技术生态复杂：呈现"三维爆炸"特征
- 硬件维度：X款异构芯片架构百花齐放
- 软件维度：Y个主流AI框架技术栈差异大
- 算法维度：Z类模型持续涌现，覆盖CV/NLP/多模态等场景
2.标准化挑战
- 适配复杂度指数级增长：理论需完成X×Y×Z种组合的适配验证
- 动态扩展压力：各维度技术栈持续快速演进
- 落地实施难度：传统方案需投入大量人力完成环境部署、接口适配、版本兼容
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
task_description = r'当前项目目标是”对wudao数据集和lama3-8B模型在1机1卡上适配Nvidia A100的GPU显卡，最后得到loss数值和okens per gpu per second(tgs)“。'
role = r'您项目的第四位处理人，负责项目在最后结果的汇总和登记，首先你会阅读上一位处理人输出的运行结果报告（```短期记忆```）和本地程序运行生成的结果（```长期记忆```），然后进行理解和分析、然后通过工具将结果汇总放到归档文件下'
requirements = r'当前运行环境是linux，当前FlagPerf的git库地址在"/home/hengtao/debug/FlagPerf",数据和模型地址在"/home/hengtao/code/task/llama3_8B/megatron_llama3/data_dir"，归档文件地址在"/home/hengtao/debug/MetaGPT/result",调用工具一定不要有删除卸载等高危操作'
goal = f'{task_description}。{role}。{requirements}'

# 再通过shell工具查看当前环境是否具备运行调试等的条件
memory_short = ''
memory_long = ''
output_demand = '''
'''




async def test_deep_research():
    # mocker.patch("metagpt.actions.di.execute_nb_code.ExecuteNbCode.run", return_value=("a successful run", True))

    requirement=""
    di = DeepResearch(react_mode="plan_and_act", tools=["shell_tool"])
    rsp = await di.run(requirement)
    logger.info(rsp)
    assert len(rsp.content) > 0


# C:\Users\m01216.METAX-TECH\.conda\envs\metagpt\python.exe  C:\Users\m01216.METAX-TECH\Desktop\code\MetaGPT\tests\metagpt\roles\test_project_reasoner.py
# python /home/hengtao/debug/MetaGPT/tests/metagpt/roles/test_project_reasoner.py
if __name__ == '__main__':
    asyncio.run(test_deep_research())
