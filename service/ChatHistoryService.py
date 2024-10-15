
from datetime import datetime

from database import DatabaseConnection
from log.log import logger


def get_chat_history_page_size(connection,user_id, session_id, platform,offset: int,limit_count: int):
    # SQL 查询语句
    query = f"""
        SELECT ROLE, CONTENT,CREATE_DATE FROM (
        SELECT ROLE, CONTENT,CREATE_DATE
        FROM chat_history
        WHERE USER_ID ='{user_id}' AND SESSION_ID = '{session_id}' and platform = '{platform}'
        ORDER BY CREATE_DATE DESC limit {offset},{limit_count}) t order by CREATE_DATE
    """
    # 执行查询
    sql_result = DatabaseConnection.ask_database(connection,query)

    # 结果整理
    chat_history = []
    for row in sql_result:
        chat_history.append({"role": row[0], "content": row[1],"time":row[2]})
    # 返回 JSON 格式数据
    return chat_history

def get_chat_history_count(connection,user_id, session_id,platform):
    # SQL 查询语句
    query = f"""
        SELECT COUNT(*)
        FROM chat_history
        WHERE USER_ID ='{user_id}' AND SESSION_ID = '{session_id}' and platform = '{platform}'
    """
    # 执行查询
    sql_result = DatabaseConnection.ask_database(connection,query)

    if sql_result:
        return sql_result[0][0]
    else:
        return 0

def get_chat_history(connection,user_id, session_id, platform, limit_count: int):
    # SQL 查询语句
    query = f"""
    SELECT  ROLE, CONTENT FROM (
        SELECT ROLE, CONTENT, CREATE_DATE
        FROM chat_history 
        WHERE USER_ID ='{user_id}' AND SESSION_ID = '{session_id}' and platform = '{platform}'
        ORDER BY CREATE_DATE DESC limit {limit_count}) t ORDER BY t.CREATE_DATE  ASC;
    """

    # 执行查询
    sql_result = DatabaseConnection.ask_database(connection,query)

    # 结果整理
    chat_history = []
    for row in sql_result:
        chat_history.append({"role": row[0], "content": row[1]})

    # 返回 JSON 格式数据
    return chat_history

def get_session_id(connection,user_id,platform):
    # SQL 查询语句
    query = f"""
        SELECT SESSION_ID
        FROM chat_history 
        WHERE USER_ID ='{user_id}'  and platform = '{platform}'
        ORDER BY CREATE_DATE DESC limit 1;
    """

    # 执行查询
    sql_result = DatabaseConnection.ask_database(connection,query)

    if sql_result:
        return sql_result[0][0]
    else:
        return '1'


# 定义保存对话记录的方法
def save_chat_history(connection,user_id: str, session_id: str,platform:str, role: str, content: str):
    # 获取当前时间
    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 定义插入对话记录的 SQL 语句
    insert_query = f"""
        INSERT INTO chat_history (USER_ID, SESSION_ID,platform, ROLE, CONTENT, CREATE_DATE)
        VALUES ('{user_id}', '{session_id}',  '{platform}', '{role}', '{content}', '{create_date}')
    """

    # 执行插入操作
    DatabaseConnection.save_database(connection, insert_query)

    # 提交更改到数据库
    logger.info(f'对话记录已成功保存。')
