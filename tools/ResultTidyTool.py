from log.log import logger
from model.qwen_model import llm_qwen2_72b

class ResulTidyTool:
    def __init__(self, prompt: str, sql: str, result: str,statistics_prompt: str):
        self.messages = [
            {
                "role": "user",
                "content": f"""
                    ## Goal
                    你是一个 Mysql 数据库管理员，根据用户的提问、执行的sql语句、sql查询结果以及数据统计提示等信息将查询结果整理成自然语言输出,，遵循以下步骤执行分析：
                1. 输出自然语言回答 尽量简单、通俗易懂，不可对结果做假设。
                2. 你的回答中不能 暴露 sql 语句 或表结构信息。
                3. 不可在回答中暴露你的推理过程，比如体现 数据统计提示、sql执行结果 相关的字眼。
                4. 如果用户没有指定输出格式，则默认以 markdown 格式展示结果，但不用告知用户默认输出格式。
                    
                    ## 用户的提问
                    {prompt}
                    
                    ## 获取基础数据执行的sql语句
                    {sql}
                    
                    ## sql语句执行的结果
                    {result}
                    
                    ## 数据统计提示
                    {statistics_prompt}
                """
            }]

    def execute(self):
        responses = llm_qwen2_72b.chat(messages=self.messages, stream=False)[0]
        # responses = model_api.chat(messages=self.messages)['choices'][0]['message']
        logger.info(f'# resul_tidy_tool: {responses}')
        logger.info(' ')
        return responses
