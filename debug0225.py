


import asyncio
# from metagpt.roles.di.data_interpreter import DataInterpreter
#
#
# async def main(requirement: str):
#     role = DataInterpreter(tools=["shell_tool"]) # 集成工具
#     await role.run(requirement)
#

def f1():
    r="import os\nimport glob\nimport re\nfrom metagpt.tools.libs.shell_tool import shell_tool\n\n# 定义关键路径\nlog_dir = \"/home/hengtao/debug/FlagPerf/training/result/run20250218153849\"\narchive_dir = \"/home/hengtao/debug/MetaGPT/result\"\nresult_file = os.path.join(archive_dir, \"training_results.txt\")\n\n# 创建归档目录\nos.makedirs(archive_dir, exist_ok=True)\n\n# 查找所有日志文件（支持.log和.txt）\nlog_files = glob.glob(os.path.join(log_dir, \"*.log\")) + glob.glob(os.path.join(log_dir, \"*.txt\"))\n\n# 初始化结果存储\nresults = {\"loss\": None, \"tgs\": None}\n\n# 解析日志文件\nfor file_path in log_files:\n    with open(file_path, \"r\", encoding=\"utf-8\") as f:\n        for line in f:\n            # 匹配loss数值（支持不同格式）\n            loss_match = re.search(r'(loss|Loss|LOSS)[\\s:=]+([0-9]+\\.[0-9]+)', line)\n            if loss_match and not results[\"loss\"]:\n                results[\"loss\"] = loss_match.group(2)\n            \n            # 匹配tokens per gpu per second（支持不同格式）\n            tgs_match = re.search(r'(tokens per gpu per second|TGS|throughput)[\\s:=]+([0-9]+\\.[0-9]+)', line)\n            if tgs_match and not results[\"tgs\"]:\n                results[\"tgs\"] = tgs_match.group(2)\n\n# 写入归档文件\nwith open(result_file, \"w\") as f:\n    f.write(f\"Final Training Results:\\n\")\n    f.write(f\"Loss: {results['loss'] or 'Not found'}\\n\")\n    f.write(f\"Tokens per GPU per second: {results['tgs'] or 'Not found'}\\n\")\n\n# 使用工具进行结果登记（安全操作）\nshell_tool(f\"echo 'Results archived to {result_file}'\", verbose=True)\n"
    print(r)

if __name__ == '__main__':

    # requirement = r"请查看地址'C:\Users\m01216.METAX-TECH\Downloads\node-v23.8.0-win-x64'下的所有文件"
    # asyncio.run(main(requirement))
    # r='\u8981\u4e0d\u54b1\u4eec\u6362\u4e2a\u8bdd\u9898\uff1f'
    # print(r)
    f1()