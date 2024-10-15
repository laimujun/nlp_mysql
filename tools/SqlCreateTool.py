from log.log import logger
from model.qwen_model import qwen_max_0919,llm_qwen2_72b,llm_qwen_turbo_0919

class SqlCreateTool:

    def __init__(self, error_sql: str, prompt: str):
        logger.info(f'# error_sql: {error_sql}')
        self.messages = [
        {'role': 'system', 'content': f"""
任务指令：作为MySQL 5.7.0数据库管理员，根据用户查询需求及指定的表结构，精确构建可执行的SQL查询语句。请严格遵守以下准则构造SQL：

1. **用户信息包含性**：当查询结果关联用户时，确保SELECT子句中包含`USER_NAME`字段。
2. **状态筛选**：在WHERE子句中加入必要的状态字段条件，以排除不满足条件的记录。
3. **表结构严谨性**：仅依据已知的表名与字段详情构建查询，严禁假设额外字段或表。
4. **表字段一致性**：维护SQL中表与字段关系与给定结构完全一致，避免引用不存在的字段。
5. **数值处理**：对于可能存在小数位数需求的结果，应用`ROUND`函数做四舍五入处理。
6. **关键字规避**：禁止使用`OF`作为表别名。
7. **逻辑删除过滤**：若涉及的表含有`DEL_FLAG`字段，必须在查询条件中加入`DEL_FLAG = 0`，确保不返回已删除数据。
8. **转义字符禁用**：生成的SQL中不得包含转义字符。
9. **状态翻译**：存在`INT_LOAN_STATUS`字段时，利用`CASE WHEN THEN`转换其值为中文描述（1=待准入，2=待补充，3=已准入，4=已拒绝，5=已撤回）。
10. **用户名模糊查询**：针对用户名的搜索，应用`LIKE`操作符进行模糊匹配，特别是中文名应参考`fbpa_clm_m.USER_NAME`。涉及用户ID或信息的查询，结果必须包含`USER_NAME`字段。
11. **金额查询标准**：除非另有说明，所有与金额相关的查询均应基于`ANNUAL_TURNOVER`字段进行。
12. **上级ID的嵌套查询**： 对于同一个中文姓名，在客户经理信息表可能有多条有效记录，当使用嵌套子查询得到 SUPERIOR 时，注意应使用 in 而不用 = 。

请确保在构造SQL时，每个细节都符合上述规范，以实现高效且准确的数据检索。

### 用户需求：
{prompt}
### 已知表结构信息：
```sql
create table xxxx (
    xxxx1             varchar comment 'xxxx',
    xxxx2          varchar comment 'xxxx',
    xxxx3       varchar comment 'xxxx'
)comment 'xxxx表';
	

	
```

### 错误的sql示例
以下是根据用户的提问生成的一个异常的sql，请不要生成跟以下一模一样的sql：
{error_sql}

### 优化后的执行流程：
1. **需求分析**：首先，根据用户的需求以及任务指令中SQL生成的准则，明确用户查询的具体需求，包括但不限于需要筛选的条件、期望的输出字段等。
2. **状态逻辑验证**：基于用户提问，如果用户提问中涉及到 '准入'、'拒绝'、'补充'、'撤回'等字眼，则要检查是否能明确利用`INT_LOAN_STATUS`字段进行有效过滤,否则不用考虑使用`INT_LOAN_STATUS`字段。
3. **SQL构建**：根据明确的需求，利用给定表结构信息编写SQL查询，确保所有字段和表名直接来源于用户提供的表结构，且不包含转义字符，sql生成过程中不允许任何的假设，如有不明确的的地方，请输出缺失的信息。
3. **SQL校验**：根据生成的sql和表结构信息，校验表名、表别名、字段是否都存在，校验sql中表与字段的对应关系是否使用正确，不可使用未定义的表别名。如有异常给与矫正。
12. **过滤逻辑校验**  在 where 条件中 同时使用 and 和 or 时，需考虑优先级问题，必要时要将优先执行的多个过滤条件添加括号，确保逻辑正确。 
4. **输出结果**：若SQL成功构建，直接输出完整的可直接执行的SQL查询语句，不得输出任何其他信息，不得输出任何其他信息，不得输出任何其他信息！若因信息不足无法构建，不则输出分析过程'。
"""
         },
        {'role': 'user', 'content': prompt}]


    def execute(self):
        responses = qwen_max_0919.chat(messages=self.messages,  stream=False)[0]
        # responses = model_api.chat(messages=self.messages)['choices'][0]['message']
        logger.info(f'# sql_create_tool: {responses}')
        logger.info(' ')
        return responses
