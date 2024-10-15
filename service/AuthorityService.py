
from datetime import datetime
from database import DatabaseConnection


def get_user_auth(connection,user_id):
    # SQL 查询语句
    query = f"""
        SELECT ROLEID
        FROM sipa_btr_m 
        WHERE USERID ='{user_id}'  and ROLEID in ('accessQuery','accessApprove','projectQuery')
        ORDER BY LAST_MOD_DATE DESC limit 1;
    """

    # 执行查询
    sql_result = DatabaseConnection.ask_database(connection,query)

    if sql_result:
        return sql_result[0][0]
    else:
        return None
