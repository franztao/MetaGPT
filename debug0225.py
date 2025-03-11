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
    r="---------------------------------------------------------------------------\nValueError                                Traceback (most recent call last)\nCell In[2], line 80\n     77     print(f\"Enhanced results saved to {report_path}\")\n     79 if __name__ == \"__main__\":\n---> 80     main()\n\nCell In[2], line 73, in main()\n     71 f.write(\"-\"*40 + \"\\n\")\n     72 f.write(f\"Final Loss: {final_metrics.get('loss', 'N/A'):.4f}\\n\")\n---> 73 f.write(f\"Tokens/GPU/sec: {final_metrics.get('tgs', 'N/A'):.2f}\\n\")\n     74 f.write(\"\\nProcessed Files:\\n\")\n     75 f.write(\"\\n\".join(log_files))\n\nValueError: Unknown format code 'f' for object of type 'str'"
    print(r)

if __name__ == '__main__':

    # requirement = r"请查看地址'C:\Users\m01216.METAX-TECH\Downloads\node-v23.8.0-win-x64'下的所有文件"
    # asyncio.run(main(requirement))
    # r='\u8981\u4e0d\u54b1\u4eec\u6362\u4e2a\u8bdd\u9898\uff1f'
    # print(r)
    f1()