
from database import DatabaseConnection


def get_user_underling(connection,user_id):
    # SQL 查询语句
    query = f"""
        SELECT USERID
        FROM fbpa_clm_m 
        WHERE SUPERIOR ='{user_id}'  
        GROUP BY USERID;
    """

    # 执行查询
    sql_result = DatabaseConnection.ask_database(connection,query)

    if sql_result:
        return sql_result
    else:
        return None
