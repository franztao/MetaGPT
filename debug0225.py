# -*- coding: utf-8 -*-


import asyncio
# from metagpt.roles.di.data_interpreter import DataInterpreter
#
#
# async def main(requirement: str):
#     role = DataInterpreter(tools=["shell_tool"]) # 集成工具
#     await role.run(requirement)
#

def f1():

    r="from metagpt.tools.libs.shell_tool import shell_tool\nimport os\n\n# 1. 设置容器内启动环境变量\nos.environ[\"EXEC_IN_CONTAINER\"] = \"True\"\n\n# 2. 检查并安装必要监控工具\ntry:\n    shell_tool(\"dpkg -l | grep sysstat || apt-get install -y sysstat\")\n    shell_tool(\"dpkg -l | grep ipmitool || apt-get install -y ipmitool\")\nexcept Exception as e:\n    print(f\"安装监控工具时出错: {e}\")\n\n# 3. 验证GPU可见性\ngpu_check = shell_tool(\"nvidia-smi --query-gpu=name --format=csv,noheader\")\nif \"A100\" not in gpu_check:\n    raise RuntimeError(\"GPU检测失败，未找到A100显卡\")\n\n# 4. 运行基准测试（前台运行以便捕获错误）\ntry:\n    # 检查FlagPerf路径是否存在\n    shell_tool(\"ls /home/hengtao/debug/step3/FlagPerf/training/run_benchmarks/run.py\")\n    \n    # 执行训练任务\n    result = shell_tool(\"python3 /home/hengtao/debug/step3/FlagPerf/training/run_benchmarks/run.py\")\n    print(\"训练任务输出:\", result)\n    \nexcept Exception as e:\n    print(f\"运行异常: {e}\")\n    # 处理常见依赖问题\n    if \"ModuleNotFoundError\" in str(e):\n        shell_tool(\"pip install -r /home/hengtao/debug/step3/FlagPerf/requirements.txt\")\n\n# 5. 结果收集（假设FlagPerf输出到标准路径）\nlog_analysis = shell_tool(\"grep -E 'loss:|tokens per gpu per second' /home/hengtao/debug/step3/FlagPerf/training/results/*/log.txt\")\nprint(\"关键指标结果:\\n\", log_analysis)\n"
    print(r)

if __name__ == '__main__':

    # requirement = r"请查看地址'C:\Users\m01216.METAX-TECH\Downloads\node-v23.8.0-win-x64'下的所有文件"
    # asyncio.run(main(requirement))
    # r='\u8981\u4e0d\u54b1\u4eec\u6362\u4e2a\u8bdd\u9898\uff1f'
    # print(r)
    # f1()
    import os
    # from openai import OpenAI
    #
    # client = OpenAI(
    #     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    #     api_key="sk-f7f3039f52e3402bbafda926f4da7cb3",
    #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # )
    # completion = client.chat.completions.create(
    #     model="qwen-max",
    #     # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    #     messages=[
    #         {'role': 'system', 'content': 'You are a helpful assistant.'},
    #         {'role': 'user', 'content': '你是谁？'}],
    # )
    #
    # print(completion.model_dump_json())

    import os
    from openai import OpenAI

    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-f7f3039f52e3402bbafda926f4da7cb3",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen-vl-max",
        # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "这是什么"},
            {"type": "image_url",
             "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}}
        ]}],
        tools=[],
    )



    print(completion.model_dump_json())