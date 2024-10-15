from log.log import logger
from model.qwen_model import qwen_max_0919,llm_qwen2_72b

class UserAuthTool:

    def __init__(self, sql: str):
        self.messages = [
        {'role': 'user', 'content': f"""
任务指令：作为MySQL数据库工程师，给你一个 SQL 语句 和一个  "APPLY_USER in ('张三')" 的过滤条件，APPLY_USER 是 fint_apl_m 表的一个字段。你需判断这个SQL语句中是否有使用到 fint_apl_m 表 。如果有，则给 fint_apl_m 表添加 上这个 ‘APPLY_USER in (xxx,xxx)’ 过滤条件。如果没有，则返回原有的sql语句则可。
## 必须遵守的原则：
 - 注意考虑表的别名，确保改造后的SQL 语法的合法性。
 - 如果没有涉及到 fint_apl_m 表，则返回原SQL。
 - 输出结果只输出改造的SQL，不要输出分析过程！
 - 输出结果只输出改造的SQL，不要输出分析过程！
 - 输出结果只输出改造的SQL，不要输出分析过程！
 
## 给定SQL：
{sql}

##  fint_apl_m 表中 字段 APPLY_USER 的过滤条件：
 APPLY_USER in ('张三')

请根据给定SQL 和过滤条件，改造SQL，并输出改造后的SQL。
"""
         }]


    def execute(self):
        responses = llm_qwen2_72b.chat(messages=self.messages,  stream=False)[0]
        # responses = model_api.chat(messages=self.messages)['choices'][0]['message']
        logger.info(f'# user_auth_tool: {responses}')
        logger.info(' ')
        return responses
