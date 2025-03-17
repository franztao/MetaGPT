import json


def f1():
    src="from metagpt.tools.libs.shell_tool import shell_tool\n\nprint(\"检查nvidia目录下的llama3-pytorch配置...\")\n# 验证配置目录是否存在\nprint(\"检查配置目录结构:\")\nshell_tool(\"ls -l /home/hengtao/debug/FlagPerf/training/nvidia/llama3_8B-pytorch/config\")\n\nprint(\"\\n对比已有模型配置(以bert-pytorch为例):\")\nshell_tool(\"ls -l /home/hengtao/debug/FlagPerf/training/nvidia/bert-pytorch/config\")\n\nprint(\"\\n需要人工处理事项:\")\nprint(\"1. 若nvidia/llama3_8B-pytorch目录不存在，需从其他模型复制模板:\")\nprint(\"   cp -r nvidia/bert-pytorch nvidia/llama3_8B-pytorch\")\nprint(\"2. 修改config_A100x1x1.py中的关键参数:\")\nprint(\"   - train_batch_size (根据单卡显存调整)\")\nprint(\"   - learning_rate\")\nprint(\"   - max_steps (测试时建议设为较小值)\")\nprint(\"3. 检查Dockerfile中的基础镜像是否包含pytorch 2.0+\")\nprint(\"4. 确认run_pretraining.py中的模型初始化逻辑适配llama3-8B架构\")\n"
    print(src)
    # print(json.dumps(src,ensure_ascii=False))

if __name__ == '__main__':
    f1()