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
    r="import os\nimport re\nfrom metagpt.tools.libs.shell_tool import shell_tool\n\n# 定义日志目录和归档路径\nlog_dir = \"/home/hengtao/debug/FlagPerf/training/result/run20250218153849\"\narchive_dir = \"/home/hengtao/debug/MetaGPT/result\"\nresult_file = os.path.join(archive_dir, \"training_result_summary.txt\")\n\n# 创建结果文件头\nshell_tool(f\"echo '### Training Result Summary ###' > {result_file}\")\n\n# 查找所有日志文件并处理\nlog_files = shell_tool(f\"find {log_dir} -type f \\( -name '*.log' -o -name '*.txt' \\)\")\nfor file_path in log_files.split('\\n'):\n    if not file_path.strip():\n        continue\n    \n    # 提取loss数值\n    loss_output = shell_tool(f\"grep -iE 'loss: [0-9.]+' {file_path} | tail -n 1\")\n    if loss_match := re.search(r'loss: ([\\d.]+)', loss_output, re.IGNORECASE):\n        shell_tool(f\"echo 'Loss: {loss_match.group(1)}' >> {result_file}\")\n\n    # 提取tokens/s数值\n    tgs_output = shell_tool(f\"grep -iE 'tokens per gpu per second: [0-9.]+' {file_path} | tail -n 1\")\n    if tgs_match := re.search(r'tokens per gpu per second: ([\\d.]+)', tgs_output, re.IGNORECASE):\n        shell_tool(f\"echo 'Tokens per GPU per second: {tgs_match.group(1)}' >> {result_file}\")\n\n# 添加分隔符\nshell_tool(f\"echo '\\n-----------------------------' >> {result_file}\")\nprint(f\"结果已归档至：{result_file}\")\n"
    print(r)

if __name__ == '__main__':

    # requirement = r"请查看地址'C:\Users\m01216.METAX-TECH\Downloads\node-v23.8.0-win-x64'下的所有文件"
    # asyncio.run(main(requirement))
    # r='\u8981\u4e0d\u54b1\u4eec\u6362\u4e2a\u8bdd\u9898\uff1f'
    # print(r)
    f1()