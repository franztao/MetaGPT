


import asyncio
# from metagpt.roles.di.data_interpreter import DataInterpreter
#
#
# async def main(requirement: str):
#     role = DataInterpreter(tools=["shell_tool"]) # 集成工具
#     await role.run(requirement)
#

def f1():
    r="import os\nimport re\nfrom pathlib import Path\n\n# Define paths\nlog_dir = \"/home/hengtao/debug/step3/FlagPerf/training/result/run20250218153849\"\narchive_dir = \"/home/hengtao/debug/MetaGPT/result\"\n\n# Create archive directory if not exists\nPath(archive_dir).mkdir(parents=True, exist_ok=True)\n\n# Regular expressions for metric extraction\nloss_pattern = re.compile(r'loss\\s*=\\s*([\\d.]+)')\ntgs_pattern = re.compile(r'tokens per gpu per second\\s*:\\s*([\\d.]+)')\n\n# Store results\nmetrics = {'loss': None, 'tgs': None}\n\n# Parse log files\nfor root, _, files in os.walk(log_dir):\n    for file in files:\n        if file.endswith('.log'):\n            log_path = os.path.join(root, file)\n            with open(log_path, 'r') as f:\n                for line in f:\n                    loss_match = loss_pattern.search(line)\n                    if loss_match:\n                        metrics['loss'] = float(loss_match.group(1))\n                    tgs_match = tgs_pattern.search(line)\n                    if tgs_match:\n                        metrics['tgs'] = float(tgs_match.group(1))\n\n# Save results to archive\nresult_file = os.path.join(archive_dir, 'training_metrics.txt')\nwith open(result_file, 'w') as f:\n    f.write(f\"Final Loss: {metrics['loss']}\\n\")\n    f.write(f\"Tokens per GPU per second: {metrics['tgs']}\\n\")\n\nprint(f\"Results saved to {result_file}\")\nprint(f\"Final Loss: {metrics['loss']}\")\nprint(f\"Tokens per GPU per second: {metrics['tgs']}\")\n"
    print(r)

if __name__ == '__main__':

    # requirement = r"请查看地址'C:\Users\m01216.METAX-TECH\Downloads\node-v23.8.0-win-x64'下的所有文件"
    # asyncio.run(main(requirement))
    # r='\u8981\u4e0d\u54b1\u4eec\u6362\u4e2a\u8bdd\u9898\uff1f'
    # print(r)
    f1()