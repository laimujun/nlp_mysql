import json

from log.log import logger
from model.qwen_model import llm_qwen2_72b

class StatisticsDataTool:
    def __init__(self, data_query_prompt: str,prompt: str, base_data: str):
        self.messages = [
            {
                "role": "system",
                "content": f"""
                ## 任务指令： 作为数据分析师，你需要根据用户的历史提问和 SQL查询结果记录来回答用户的问题。在分析的过程中，遵循以下步骤执行分析：
                1. 根据用户的历史问答记录分析，针对用户的提问，你还需要做哪些工作。你可能还需要做的工作有：对查询结果做统计分析、格式处理等。
                2. 你需要优先考虑使用工具函数，比如 add、subtract、multiply、divide等。
                3. 如果给出的 SQL查询结果 数据为空，则直接回答 未找到相关数据 之类的回答即可，不必进行后续的推理流程。
                3. 不可在回答中暴露你的推理过程，比如体现 基础数据 相关的字眼。
                ## 输出格式要求
                1. 如何SQL查询结果不为空，则以markdown 格式展示结果。如何SQL查询结果为空，则输出自然语言回答，尽量简单、通俗易懂，不可对结果做假设。
                2. 你的回答中不能 暴露 sql 语句 或表结构信息。
                3. 不可在回答中暴露你的推理过程，比如体现 数据统计提示、sql执行结果 相关的字眼。
                4. 如果用户没有指定输出格式，则默认以 markdown 格式展示结果，但不用告知用户默认输出格式。
                
                ## 用户历史提问：
                {data_query_prompt}
                ## SQL查询结果：
                {base_data}
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        self.functions = [{
            "name": "add",
            "description": "加法器，计算一组数的和",
            "parameters": {
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "参与计算的相加数",
                    }
                },
                "required": ["numbers"],
            }
        },{
            "name": "subtract",
            "description": "减法器，计算一组数的差",
            "parameters": {
                "type": "object",
                "properties": {
                    "minuend": {
                        "type": "number",
                        "description": "被减数"
                    },
                    "subtrahends": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "减数",
                    }
                },
                "required": ["minuend", "subtrahends"],
            }
        },{
            "name": "multiply",
            "description": "乘法器，计算一组数的积",
            "parameters": {
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "参与计算的因数",
                    }
                },
                "required": ["numbers"],
            }
        },{
            "name": "divide",
            "description": "除法器，计算一组或多组数的商，多组数的 被除数顺序要和除数组的顺序一致",
            "parameters": {
                "type": "object",
                "properties": {
                    "dividends": {
                        "type": "array",
                        "items": {
                            "type": "float",
                            "description": "被除数"
                        },
                        "description": "被除数，计算多组数的商时，有多个被除数,且被除数的组数必须与除数的组数相等",
                    },
                    "divisors": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "description": "除数",
                            "items": {
                                "type": "float"
                            }
                        },
                        "description": "除数，计算多组数的商时，会有多组除数，每一组除数也可能用多个",
                    }
                },
                "required": ["dividend", "divisors"],
            }
        }
        ]

    def execute(self):
        response = None
        for i in range(3):
            response = llm_qwen2_72b.chat(messages=self.messages, functions=self.functions, stream=False)[0]
            # responses = model_api.chat(messages=self.messages)['choices'][0]['message']
            if response.get('function_call') is not None:
                logger.info(f'# statistics_data_tool_calling: {response}')
                logger.info('')
                self.messages.append(response)
                function_name = response.get('function_call').get('name')
                if function_name == 'add':
                    args = json.loads(response.get('function_call').get('arguments'))
                    numbers = args['numbers']
                    result = sum(numbers)
                    self.messages.append({
                        "role": "function",
                        "content": str(result)
                    })
                elif function_name == 'divide':
                    args = json.loads(response.get('function_call').get('arguments'))
                    dividends = args['dividends']
                    divisors = args['divisors']
                    results = []
                    for i in range(len(dividends)):
                        result = dividends[i]
                        if i <= len(divisors)-1:
                            for divisor in divisors[i]:
                                result = result / divisor
                        else:
                            for divisor in divisors[len(divisors)-1]:
                                result = result / divisor
                        results.append(result)
                    self.messages.append({
                        "role": "function",
                        "content": str(results)
                    })
            else:
                break

        logger.info(f'# statistics_data_tool: {response}')
        logger.info(' ')
        return response

if __name__ == '__main__':
    prompt = "请根据每个产品线的 产品线名称、产品线销售额，统计出 所有产品线总销售额、各产品线销售额占比，且销售额保留两位小数"
    base_data = (('Vintage Cars', 1755309.57), ('Classic Cars', 3774647.39), ('Trucks and Buses', 1024113.57), ('Trains', 179144.85), ('Ships', 611486.04), ('Planes', 903119.39), ('Motorcycles', 1117515.62))
    statisticsDataTool = StatisticsDataTool(prompt, str(base_data))
    response = statisticsDataTool.execute()





