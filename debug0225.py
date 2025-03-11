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
    r="import subprocess\nimport os\n\n# 基础路径配置校验\nflagperf_root = \"/home/hengtao/debug/step2/FlagPerf\"\nconfig_path = \"/home/hengtao/debug/step2/FlagPerf/training/nvidia/llama3_8B-megatron/config/config_A100x1x1.py\"\n\n# 步骤0: 强制修复仓库结构\nif not os.path.exists(flagperf_root):\n    print(\"🔄 正在克隆FlagPerf仓库...\")\n    subprocess.run(f\"git clone https://github.com/FlagPerf/FlagPerf.git {flagperf_root}\", shell=True, check=True)\nelse:\n    print(\"🔄 正在更新FlagPerf仓库...\")\n    subprocess.run(f\"cd {flagperf_root} && git pull\", shell=True, check=True)\n\n# 步骤1: 验证关键路径\nrequired_paths = {\n    \"训练脚本\": os.path.join(flagperf_root, \"training/run_benchmark.sh\"),\n    \"配置文件\": config_path,\n    \"数据目录\": \"/home/hengtao/code/task/llama3_8B/megatron_llama3/data_dir\"\n}\n\nfor name, path in required_paths.items():\n    if not os.path.exists(path):\n        raise FileNotFoundError(f\"❌ 关键路径缺失: {name} ({path})\\n请执行:\\nmkdir -p {os.path.dirname(path)}\")\n\n# 步骤2: 修正配置文件\nif os.path.exists(config_path):\n    with open(config_path, \"r+\") as f:\n        content = f.read()\n        # 确保单卡配置正确\n        content = content.replace(\"pipeline_parallel = 2\", \"pipeline_parallel = 1\")\n        content = content.replace(\"tensor_parallel = 8\", \"tensor_parallel = 1\")\n        f.seek(0)\n        f.write(content)\n        f.truncate()\nelse:\n    raise FileNotFoundError(f\"⚠️ 配置文件不存在，请从模板创建：\\ncp {flagperf_root}/training/nvidia/llama3_8B-megatron/config/config_A100x1x8.py {config_path}\")\n\n# 步骤3: 设置执行权限\nscript_path = required_paths[\"训练脚本\"]\nsubprocess.run(f\"chmod +x {script_path} && chmod +x {flagperf_root}/training/*.sh\", shell=True, check=True)\n\n# 步骤4: 启动训练任务\nrun_cmd = f\"\"\"\ncd {flagperf_root}/training\n./run_benchmark.sh \\\\\n-n llama3_8B \\\\\n-t megatron_core060 \\\\\n-d A100 \\\\\n-x 1 \\\\\n-g 1 \\\\\n-i 1 \\\\\n--model_config_path {config_path}\n\"\"\"\n\nprint(\"🚀 启动训练任务，命令如下：\")\nprint(run_cmd)\n\nprocess = subprocess.Popen(\n    run_cmd,\n    shell=True,\n    stdout=subprocess.PIPE,\n    stderr=subprocess.STDOUT,\n    text=True,\n    bufsize=1\n)\n\n# 步骤5: 实时日志捕获\nprint(\"\\n📜 实时训练日志：\")\ntry:\n    while True:\n        line = process.stdout.readline()\n        if not line and process.poll() is not None:\n            break\n        print(line.strip())\nexcept KeyboardInterrupt:\n    print(\"\\n🛑 用户中断，正在清理进程...\")\n    process.terminate()\n\n# 步骤6: 结果验证\nif process.returncode == 0:\n    print(\"\\n✅ 训练成功！关键结果文件：\")\n    print(f\"Loss曲线: {flagperf_root}/training/result/loss_curve.png\")\n    print(f\"性能指标: {flagperf_root}/training/result/metrics.json\")\nelse:\n    print(f\"\\n❌ 训练失败 (退出码: {process.returncode})，请检查：\")\n    print(f\"1. NVIDIA驱动版本：nvidia-smi\")\n    print(f\"2. CUDA环境变量：echo $CUDA_HOME\")\n    print(f\"3. 完整错误日志：{flagperf_root}/training/debug.log\")\n\n# 步骤7: 资源监控\nsubprocess.Popen(\n    f\"nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 5 > {flagperf_root}/training/gpu_stats.csv &\",\n    shell=True\n)\nprint(f\"\\n📊 GPU监控数据保存至: {flagperf_root}/training/gpu_stats.csv\")\n"
    print(r)

if __name__ == '__main__':

    # requirement = r"请查看地址'C:\Users\m01216.METAX-TECH\Downloads\node-v23.8.0-win-x64'下的所有文件"
    # asyncio.run(main(requirement))
    # r='\u8981\u4e0d\u54b1\u4eec\u6362\u4e2a\u8bdd\u9898\uff1f'
    # print(r)
    f1()