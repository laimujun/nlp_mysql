
import json
import os
import time
from typing import Dict
from datetime import datetime

from dotenv import load_dotenv, find_dotenv
from functools import partial
from database import DatabaseConnection
from database.DataBasePool import connection_pool
from log.log import logger
from service.AuthorityService import get_user_auth
import re
from service.ChatHistoryService import save_chat_history, get_session_id, get_chat_history_page_size, \
    get_chat_history_count
from service.UserService import get_user_underling
from tools.DemandAnalysisTool import DemandAnalysisTool
from tools.ResultTidyTool import ResulTidyTool
from tools.SqlCreateTool import SqlCreateTool
from tools.StatisticsDataTool import StatisticsDataTool
from fastapi import  Response

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tools.UserAuthTool import UserAuthTool

app = FastAPI()

_ = load_dotenv(find_dotenv())
aes_key = os.getenv('AES_KEY')
aes_iv = os.getenv('AED_IV')
try_time = os.getenv('TRY_TIME')
# 设置允许的源
origins = [
    "http://127.0.0.1:5173",  # 您的 Vue 应用运行的地址
    "http://localhost:5173",
    "http://192.168.122.46:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/chat',  response_model=Dict[object, object])
def chat(item: dict):
    logger.info(' =================== 【发起聊天请求】【开始】=======================')
    logger.info(f"请求参数：{{'prompt': {item.get('prompt')}, 'userId': {item.get('userId')},'sessionId': {item.get('sessionId')},'platform': {item.get('platform')}}}")

    if item.get("prompt") == '' or item.get("prompt") is None:
        return {"data":  "", "code": "500", "msg": "prompt 不能为空"}
    if item.get("userId") == '' or item.get("userId") is None:
        return {"data":  "", "code": "500", "msg": "userId 不能为空"}
    if item.get("sessionId") == '' or item.get("sessionId") is None:
        return {"data":  "", "code": "500", "msg": "sessionId 不能为空"}
    if item.get("platform") == '' or item.get("platform") is None:
        return {"data":  "", "code": "500", "msg": "platform 不能为空"}
    result = run(item["prompt"], item["userId"],item["sessionId"],item["platform"])
    logger.info(' =================== 【发起聊天请求】【结束】=================== ')
    return result

@app.post('/chat2')
def chat2(item: dict):
    logger.info(' =================== 【发起聊天请求】【开始】=======================')
    logger.info(f"请求参数：{{'prompt': {item.get('prompt')}, 'userId': {item.get('userId')},'sessionId': {item.get('sessionId')},'platform': {item.get('platform')}}}")

    if item.get("prompt") == '' or item.get("prompt") is None:
        return {"data":  "", "code": "500", "msg": "prompt 不能为空"}
    if item.get("userId") == '' or item.get("userId") is None:
        return {"data":  "", "code": "500", "msg": "userId 不能为空"}
    if item.get("sessionId") == '' or item.get("sessionId") is None:
        return {"data":  "", "code": "500", "msg": "sessionId 不能为空"}
    if item.get("platform") == '' or item.get("platform") is None:
        return {"data":  "", "code": "500", "msg": "platform 不能为空"}
    result = run(item["prompt"], item["userId"],item["sessionId"],item["platform"])
    logger.info(' =================== 【发起聊天请求】【结束】=================== ')
    logger.info(result.get("data"))
    logger.info(result.get("data")["answer"])
    return result.get("data")["answer"]


@app.post('/chat/findHistoryPage',  response_model=Dict[object, object])
def chat_history(item: dict):
    logger.info(' =================== 【历史聊天记录查询】【开始】=======================')
    logger.info(f"请求参数：{{'userId': {item.get('userId')},'sessionId': {item.get('sessionId')},'pageNum': {item.get('pageNum')},'pageSize': {item.get('pageSize')},'platform': {item.get('platform')}}}")
    connection = connection_pool.get_connection()
    if item.get("sessionId") == '' or item.get("sessionId") is None:
        return {"data":  "", "code": "500", "msg": "sessionId 不能为空"}
    if item.get("userId") == '' or item.get("userId") is None:
        return {"data":  "", "code": "500", "msg": "userId 不能为空"}
    if item.get("pageNum") == '' or item.get("pageNum") is None:
        return {"data":  "", "code": "500", "msg": "pageNum 不能为空"}
    if item.get("pageSize") == '' or item.get("pageSize") is None:
        return {"data":  "", "code": "500", "msg": "pageSize 不能为空"}
    if item.get("platform") == '' or item.get("platform") is None:
        return {"data":  "", "code": "500", "msg": "platform 不能为空"}

    try:
        offset = (item.get("pageNum") - 1) * item.get("pageSize")
        if offset < 0:
            offset = 0
        result = get_chat_history_page_size(connection, item.get("userId"), item.get("sessionId"), item.get("platform"), offset,item.get("pageSize"))
        count = get_chat_history_count(connection, item.get("userId"), item.get("sessionId"), item.get("platform"))
        connection.commit()
        return  {"data":   result, "count": count, "code": "200", "msg": ""}
    except Exception as e:
        connection.rollback()
        logger.info(f"执行聊天历史对话查询时发生错误: {e}")
        return {"data":  "", "count": 0, "code": "500", "msg": f"{e}"}
    finally:
        # 释放连接
        if connection:
            connection_pool.release_connection(connection)
        logger.info(' =================== 【历史聊天记录查询】【结束】=================== ')

@app.get('/chat/sessionId/{userId}/{platform}',  response_model=Dict[object, object])
def chat_session_id( userId: str, platform: str):
    logger.info(' =================== 【sessionId查询】【开始】=======================')
    logger.info(f"请求参数：{{'userId': {userId},'platform': {platform}}}")
    if userId == '' or userId is None:
        return {"data":  "", "code": "500", "msg": "userId 不能为空"}

    connection = connection_pool.get_connection()
    try:
        result = get_session_id(connection, userId, platform)
        connection.commit()
        return {"data":   {"sessionId":result}, "code": "200", "msg": ""}
    except Exception as e:
        connection.rollback()
        logger.info(f"执行sessionId查询时发生错误: {e}")
        return {"data": "", "code": "500", "msg": f"{e}"}
    finally:
        # 释放连接
        if connection:
            connection_pool.release_connection(connection)
        logger.info(' =================== 【sessionId查询】【结束】=================== ')

def run(prompt: str,user_id: str, session_id: str,platform: str):
    connection = connection_pool.get_connection()

    try:
        logger.info('开始调用 demand_analysis_tool...')
        # ================== 将问题分解 ====================
        # 第一步：分析用户的需求，对用户的prompt 进行优化、分解，得到基础问题、统计问题
        demand_analysis_response = DemandAnalysisTool(prompt, user_id, session_id, platform,connection).execute()

        # 保存聊天记录
        save_chat_history(connection,user_id, session_id, platform,'user', prompt)

        result = ''
        if 'base_prompt' in demand_analysis_response.get('content') or 'prompt' in demand_analysis_response.get('content'):
            demand_analysis_response_json = json.loads(demand_analysis_response.get('content'))
            if 'base_prompt' in demand_analysis_response.get('content'):
                base_prompt = demand_analysis_response_json.get('base_prompt')
            elif 'prompt' in demand_analysis_response.get('content'):
                base_prompt = demand_analysis_response_json.get('prompt')

            sql_result = None
            current_try_time = 1
            sql = '暂无错误sql示例'
            while True:
                # 第二步：生成 SQL 语句
                logger.info('开始调用 sql_create_tool...')
                sql_create_response = SqlCreateTool(sql, base_prompt).execute()
                sql_create_response_content = sql_create_response.get('content')
                if '```sql\n' not in sql_create_response_content and sql_create_response_content.startswith(
                        'select') == False and sql_create_response_content.startswith('SELECT') == False:
                    result = '对不起，您的问题过于复杂了，等我学习后再告诉您好吗'
                    save_chat_history(connection,user_id, session_id,  platform,'assistant', str(result).replace('\'','\\\'').replace('"','\\\"'))
                    connection.commit()
                    return {"data":  {"answer": f'{result}','currentTime': f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}'} , "code": "200", "msg": ""}
                else:
                    sql = sql_create_response.get('content')
                    if '```sql\n' in sql:
                        sql = sql[sql.rfind('```sql\n') + len('```sql\n'):]
                    if '```' in sql:
                        sql = sql[:sql.rfind('```')]
                    if '```' in sql:
                        sql = sql[:sql.rfind('```')]
                    # 第三步：执行sql语句
                    try:
                        if 'fint_apl_m' in sql:
                            # 查询用户权限
                            user_auth = get_user_auth(connection,user_id)
                            if user_auth is None or user_auth != 'accessQuery' and user_auth != 'accessApprove' and user_auth != 'projectQuery':
                                user_underling_list = get_user_underling(connection,user_id)
                                if user_underling_list is None:
                                    user_underling_str = f"'{user_id}'"
                                else:
                                    user_underling_list = list(get_user_underling(connection,user_id))
                                    user_underling_list.append((user_id,))
                                    user_underling_strings_list = [t[0] for t in user_underling_list]
                                    user_underling_str = ",".join([f"'{s}'" for s in user_underling_strings_list])
                                logger.info('开始调用 user_auth_tool...')
                                sql = UserAuthTool(sql).execute().get('content')
                                if '```sql\n' in sql:
                                    sql = sql[sql.rfind('```sql\n') + len('```sql\n'):]
                                if '```' in sql:
                                    sql = sql[:sql.rfind('```')]
                                if '```' in sql:
                                    sql = sql[:sql.rfind('```')]
                                sql = str(sql).replace("'张三'", user_underling_str)
                        if  'update' in sql or 'delete' in sql or 'drop' in sql:
                            result = '对不起，您没有权限执行此操作'
                            save_chat_history(connection,user_id, session_id, platform,'assistant', str(result).replace('\'','\\\'').replace('"','\\\"'))
                            connection.commit()
                            return {"data":  {"answer": f'{result}','currentTime': f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}'} , "code": "200", "msg": ""}
                        logger.info('根据用户提问所生成的SQL:'+ sql)
                        # sql解密处理
                        dec_sql = decrypt_sql(sql,aes_key,aes_iv)
                        logger.info('解密处理后的sql:'+ dec_sql)
                        if len(dec_sql) != len(sql):
                            DatabaseConnection.ask_database(connection, "set  block_encryption_mode ='aes-128-cbc'")

                        sql_result = DatabaseConnection.ask_database(connection, dec_sql)
                        logger.info('')
                        break
                    except:
                        if current_try_time <= int(try_time):
                            logger.error(f'# sql_result：sql执行异常，尝试再次生成sql执行')
                            current_try_time += 1
                        else:
                            logger.error(f'# sql_result：sql执行异常，尝试次数超过2次，请求终止')
                            result = '小助手还不太懂您的意思哦，请再具体描述您的问题'
                            break
            if result == '':
                logger.info('开始调用 statistics_data_tool...')
                statistics_data_tool_response = StatisticsDataTool(base_prompt,prompt, str(sql_result)).execute()
                result = statistics_data_tool_response.get('content')

        else:
            time.sleep(1)
            result = demand_analysis_response.get('content')

        # 第五步：保存历史对话记录
        save_chat_history(connection,user_id, session_id,  platform,'assistant', str(result).replace('\'','\\\'').replace('"','\\\"'))
        connection.commit()
        return {"data":  {"answer": f'{result}','currentTime': f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}'} , "code": "200", "msg": ""}
    except Exception as e:
        logger.error(f"执行聊天对话时发生错误: {e}")
        if 'Error code: 400. Error message: The input messages exceed the maximum' in str(e):
            result = '您查询的数据量过大哦，建议您缩小查询范围，我会更快更准确的为您解答'
        else:
            result = str(e)
        save_chat_history(connection,user_id, session_id,  platform,'assistant', result)
        connection.commit()
        return {"data":  {"answer": f'{result}','currentTime': f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}'} , "code": "200", "msg": ""}
    finally:
        # 释放连接
        if connection:
            connection_pool.release_connection(connection)


# 替换函数，将匹配的表别名.ORGNAME 或 ORGNAME 替换为 COALESCE(AES_deCRYPT(...))
def replace_match(match,key:str,iv:str):
    preceding_char = match.group(1)  # 空格或者逗号
    table_alias = match.group(2)     # 表别名（可能为空）
    field_name = match.group(3)      # 字段名（ORGNAME 或 orgname）

    # 如果有别名，用别名.ORGNAME，否则直接用 ORGNAME
    if table_alias:
        full_field_name = f"{table_alias}{field_name}"
    else:
        full_field_name = field_name

    # 构造替换的字符串，保留前面的空格或逗号
    return f"{preceding_char}COALESCE(AES_deCRYPT(from_base64({full_field_name}),'{key}','{iv}'), {field_name})"

def decrypt_sql(sql: str,key:str,iv:str):
    # 正则表达式：确保前面有空格或逗号，并匹配带别名或不带别名的 ORGNAME 或 orgname
    # \b[a-zA-Z]\b 表示匹配单个字母别名，(?:\.[a-zA-Z]+\b)? 表示别名部分可选
    pattern = r'([\s,])([a-zA-Z_]+\.)?(ORGNAME|orgname|COUNTERPARTY_NAME|counterparty)\b'
    # 使用 functools.partial 将外部参数传入 replace_match
    replace_with_keys = partial(replace_match, key=key, iv=iv)
    # 使用 re.sub 进行替换
    modified_sql_query = re.sub(pattern, replace_with_keys, sql)
    return modified_sql_query;
