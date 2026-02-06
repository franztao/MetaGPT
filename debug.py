# -*- encoding:utf-8 -*-
from openai import OpenAI

pt=r"""
# 背景
您是一位GPU显卡硬件评测引擎，旨在建立以产业实践为导向的指标体系，评测AI硬件在软件栈组合（模型+框架+编译器）下的实际能力。
现在给你目标，你最终需要做的的事情的方向。
然后给你短期记忆，由于大语言模型的输出限制，会先生成部分的分析结论。
再给你长期记忆，结合短期记忆的分析结论作为前提，分析和推理长期记忆的内容。
最后给出限制要求，具体输出的结论是什么，输出的格式是什么
# 目标
```
FlagPerf:AI硬件评测引擎下，如何对wudao数据集和lama3-8B模型在1机8卡上适配nvidia GPU显卡
```
# 短期记忆
```

```
# 长期记忆
```

---------------
C:\Users\m01216.METAX-TECH\Desktop\code\FlagPerf\docs\base\base-case-doc.md
# 基础规格评测研发与适配文档

## 评测方案简介

为了对AI芯片这一芯片细分领域进行基础规格评测，本方案从算力、（内）存储、互联、能耗四大角度开展评测。

算力、存储、互联角度均具有若干评测项，每个评测项包含3条结果记录：**PyTorch算子或原语评测结果**、**厂商专用工具评测结果**和**厂商公布理论值**。其中：

1. **PyTorch算子或原语评测结果**：本方案仅基于PyTorch的基本算子或通信原语，实现与英伟达硬件无关的标准程序，并提供英伟达运行配置、英伟达硬件相关接口实现。**厂商需实现硬件相关接口，并提供自身运行配置**。每个评测项均会针对其所有从属配置给出调整约束，厂商可在约束内自由调整相关配置以达到更适应自身硬件特点的评测结果。**PyTorch算子或原语评测结果体现了上层用户使用时的实际情况**。
2. **厂商专用工具评测结果**：本方案引用英伟达及相关供应商-提供的二进制可执行文件或CUDA C/C++源码及Makefile，在英伟达机器上运行并获取结果。在此基础上，本方案将规定精简且信息完整的结果输出格式，并提供针对英伟达相关工具的结果处理程序（parser）。**厂商需提供自身用于评测基础规格的二进制可执行文件或C/C++级别源码及Makefile，并提供结果处理程序**，解析整理自身工具输出。**厂商专用工具评测结果体现了运行时厂商自认可合理的实际情况**。
3. **厂商公布理论值**：本方案将引用英伟达产品相关白皮书，填写所有评测项对应的理论值。**厂商在本次评测方案中可自由选择公布或保密理论值**。

能耗角度通过监控结果呈现。在上述每个评测项的每条待评测结果记录运行过程中，本方案将以固定时间间隔的方式对**AI芯片和整体服务器**进行能耗采样，形成**能耗值时间序列**。此外，本方案还将在较长时间段内采样AI芯片、整体服务器的**静默能耗**。在本方案的任何测试中，均不会由评测程序本身对功耗进行限制，只做记录。

## 工程组织形式

```
.
├── benchmarks
│   └── computation-FP32
│       ├── case_config.yaml
│       ├── main.py
│       ├── README.md
│       ├── <otherfiles>
│       └── nvidia
│           ├──A100
│             ├── case_config.yaml
│             ├── env.sh
│             ├── README.md
│             └── requirements.txt
├── configs
│   └── host.yaml
├── container_main.py
├── run.py
├── toolkits
│   └── computation-FP32
│       └── nvidia
│           ├──A100
│              ├── <otherfiles>
│              ├── main.sh
│              └── README.md
├── utils
│   ├── <otherfiles>
├── vendors
│   └── nvidia
│       ├── nvidia_analysis.py
│       ├── nvidia_monitor.py
│       └── pytorch_2.3
│           ├── Dockerfile
│           └── pytorch2.3_install.sh
```

```
# 限制
```
输出的结论首先是整体的规划，然后是要适配这个模型需要的硬件环境配置和软件环境配置，并且如何在linux操作系统里如何查阅这些配置,要完成这个适配任务需要准备什么代码，模型，数据，镜像等
```
# 输出
"""
# base_url="https://ai.gitee.com/v1",
	# api_key="XWKOBFEFOYJYDXAIONEQBBHLX5TTEEUIN70JTZA6",
# model="DeepSeek-R1",
# client = OpenAI(
# 	base_url="https://ai.gitee.com/v1",
# 	api_key="XWKOBFEFOYJYDXAIONEQBBHLX5TTEEUIN70JTZA6",
# 	# base_url="https://api.deepseek.com",
#     # api_key="sk-ebcb53f7e81a4ee88e1e140a41522f19"
# 	# default_headers={"X-Package":"1910"},
# )
# # model="DeepSeek-R1",
# response = client.chat.completions.create(
# 	model="DeepSeek-R1",
# 	# model="deepseek-chat",
# 	# stream=True,
# 	# max_tokens=8196,
# 	# temperature=0.6,
# 	# top_p=0.8,
# 	# extra_body={
# 	# 	"top_k": 20,
# 	# },
# 	# frequency_penalty=1.1,
# 	messages=[
# 		# {
# 		# 	"role": "system",
# 		# 	"content": "You are a helpful and harmless assistant. You should think step-by-step."
# 		# },
# 		{
# 			"role": "user",
# 			"content": ''.join([pt]*2)
# 		}
# 	],
# )
#

from openai import OpenAI
client = OpenAI(
	base_url="https://ai.gitee.com/v1",
	api_key="XWKOBFEFOYJYDXAIONEQBBHLX5TTEEUIN70JTZA6",)

messages = [
    {'role': 'system', 'content': 'you are an assistant-like content'},
    {'role': 'user', 'content': 'Question'},
    {'role': 'assistant',
     'tool_calls': [
         {'id': 'call_id',
          'function': {
            'name': 'get_function',
            'arguments': '{"args":"args"}'
          },
          'type': 'function'}
     ]},
    {'tool_call_id': 'call_id', 'role': 'tool', 'content': "content"}
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_function",
            "description": "A function to get something.",
            "parameters": {
                "type": "object",
                "properties": {
                    "args": {"type": "string"}
                },
                "required": ["args"]
            },
        }
    }
]

response = client.chat.completions.create(
	model="QwQ-32B",
	# model="Qwen/QwQ-32B",
    # model="Qwen2.5-Coder-32B-Instruct",
	# model="deepseek-chat",
    messages=messages,
    tools=tools,
    # tool_choice="auto",
    # response_format={"type": "json_object"}
)
#
# # Handle and print the response or error
# try:
#     print(response)
# except Exception as e:
#     print(f"Error: {e}")

print(response.to_dict())
# from openai import OpenAI
# client = OpenAI(api_key="sk-2dcfb5f8f3f24c04ad1bc13843c7e491", base_url="https://api.deepseek.com")
#
# # Round 1
# messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=messages
# )
#
# reasoning_content = response.choices[0].message.reasoning_content
# content = response.choices[0].message.content
# print(content)
# #
#
# metagpt "Develop a data analysis and visualization tool that takes a dataframe as input and outputs various relevant statistical metrics from the table." --project-name  "task1_deepseek"
#
# metagpt "Write a login interface where users can input their username and password. If the entered username does not exist, a registration interface will pop up. If the username exists, a ’Login Successful’ message will be displayed." --project-name  "task2_deepseek"
#
# metagpt "Create a 2048 game" --project-name  "task3_deepseek"


# from metagpt.utils.repair_llm_raw_output import extract_content_from_output
#
# output = (
#         """[CONTENT]
# {
#     "Language": "en_us",
#     "Programming Language": "Python",
#     "Original Requirements": "Develop a data analysis and visualization tool that takes a dataframe as input and outputs various relevant statistical metrics from the table.",
#     "Product Goals": [
#         "Provide comprehensive statistical analysis capabilities",
#         "Offer intuitive and interactive data visualization",
#         "Ensure ease of use for both technical and non-technical users"
#     ],
#     "User Stories": [
#         "As a data analyst, I want to input a dataframe and receive detailed statistical metrics so that I can understand the data better.",
#         "As a business user, I want to visualize data trends and patterns easily so that I can make informed decisions.",
#         "As a developer, I want to integrate this tool into my existing workflows with minimal setup so that I can save time.",
#         "As a non-technical user, I want to use the tool without needing to write code so that I can analyze data independently."
#     ],
#     "Competitive Analysis": [
#         "Tableau: Powerful visualization but requires a steep learning curve and is expensive.",
#         "Power BI: Great for business users but limited in advanced statistical analysis.",
#         "Pandas Profiling: Excellent for quick data profiling but lacks interactive visualization.",
#         "Google Data Studio: Free and easy to use but limited in customization and advanced analytics.",
#         "Matplotlib/Seaborn: Highly customizable but requires significant coding knowledge."
#     ],
#     "Competitive Quadrant Chart": "quadrantChart\n    title \"Reach and engagement of data analysis tools\"\n    x-axis \"Low Reach\" --> \"High Reach\"\n    y-axis \"Low Engagement\" --> \"High Engagement\"\n    quadrant-1 \"We should expand\"\n    quadrant-2 \"Need
# to promote\"\n    quadrant-3 \"Re-evaluate\"\n    quadrant-4 \"May be improved\"\n    \"Tableau\": [0.8, 0.7]\n    \"Power BI\": [0.75, 0.65]\n    \"Pandas Profiling\": [0.6, 0.5]\n    \"Google Data Studio\": [0.7, 0.4]\n    \"Matplotlib/Seaborn\": [0.5, 0.6]\n    \"Our Target Product\": [0.7, 0.7]",
#     "Requirement Analysis": "The tool must handle various types of data inputs, provide a wide range of statistical metrics, and offer interactive visualizations. It should be user-friendly for both technical and non-technical users, with minimal setup required for integration.",
#     "Requirement Pool": [
#         [
#             "P0",
#             "The tool should accept a dataframe as input and output key statistical metrics such as mean, median, mode, standard deviation, etc."
#         ],
#         [
#             "P0",
#             "The tool should provide interactive visualizations such as histograms, scatter plots, and box plots."
#         ],
#         [
#             "P1",
#             "The tool should offer a user-friendly interface that requires no coding for basic operations."
#         ],
#         [
#             "P1",
#             "The tool should be easily integrable with existing Python workflows."
#         ],
#         [
#             "P2",
#             "The tool should support exporting visualizations and reports in multiple formats (PDF, PNG, etc.)."
#         ]
#     ],
#     "UI Design draft": "The UI will feature a clean, modern design with a sidebar for input options, a main display area for visualizations, and a bottom panel for statistical metrics. Users can drag and drop data files or input data directly. Interactive elements like sliders and dropdowns will allow for dynamic data exploration.",
#     "Anything UNCLEAR": "Clarify the specific statistical metrics and visualization types required by the end-users. Also, confirm the preferred level of interactivity and customization for the visualizations."
# }
# [/CONTENT]
# """
#     )
# output = extract_content_from_output(output)
# print(output)

# DeepSeek-V3

