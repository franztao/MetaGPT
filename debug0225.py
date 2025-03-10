


import asyncio
# from metagpt.roles.di.data_interpreter import DataInterpreter
#
#
# async def main(requirement: str):
#     role = DataInterpreter(tools=["shell_tool"]) # 集成工具
#     await role.run(requirement)
#

def f1():
    r="import shutil\n\nsource_log_dir = \"/home/hengtao/debug/step3/FlagPerf/training/result/run20250218153849\"\narchive_dir = \"/home/hengtao/debug/MetaGPT/result\"\ndest_log_dir = os.path.join(archive_dir, \"run20250218153849\")\n\ntry:\n    if os.path.exists(source_log_dir):\n        # Copy entire log directory to archive location\n        shutil.copytree(source_log_dir, dest_log_dir, dirs_exist_ok=True)\n        print(f\"Successfully archived log directory to: {dest_log_dir}\")\n    else:\n        print(f\"Warning: Source log directory not found at {source_log_dir}\")\nexcept Exception as e:\n    print(f\"Error during archiving: {str(e)}\")\n\n# Verify metrics file exists\nresult_file = os.path.join(archive_dir, \"training_metrics.txt\")\nif os.path.exists(result_file):\n    print(f\"Metrics file verified at: {result_file}\")\nelse:\n    print(\"Warning: Metrics file not found in archive directory\")\n"
    print(r)

if __name__ == '__main__':

    # requirement = r"请查看地址'C:\Users\m01216.METAX-TECH\Downloads\node-v23.8.0-win-x64'下的所有文件"
    # asyncio.run(main(requirement))
    # r='\u8981\u4e0d\u54b1\u4eec\u6362\u4e2a\u8bdd\u9898\uff1f'
    # print(r)
    f1()