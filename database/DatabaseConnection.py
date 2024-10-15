
from database.DataBasePool import connection_pool
from log.log import logger


def ask_database(connection,sql):
    logger.info('执行SQL:'+ sql)
    # 从连接池获取连接
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        logger.info('SQL结果:'+ str(records))
        return records
    except Exception as e:
        logger.error(f"执行查询时发生错误: {e}")
        raise e

def save_database(connection,sql):
    logger.info('执行SQL:'+ sql)
    # 从连接池获取连接
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        logger.info('SQL结果:'+ str(records))
        return records
    except Exception as e:
        logger.error(f"执行插入时发生错误: {e}")

