import pymysql
from threading import Lock
from queue import Queue
from datetime import datetime, timedelta
import os
from datetime import datetime

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv

from log.log import logger


class MySQLConnectionPool:
    def __init__(self, min_conn, max_conn, queue_size, idle_timeout, dbconfig):
        """初始化连接池"""
        self.min_conn = min_conn  # 最小连接数
        self.max_conn = max_conn  # 最大连接数
        self.queue_size = queue_size  # 队列长度
        self.idle_timeout = idle_timeout  # 最长空闲等待时间
        self.dbconfig = dbconfig  # 数据库配置
        self.lock = Lock()  # 线程锁，确保并发安全
        self.pool = Queue(maxsize=queue_size)  # 使用Queue管理连接
        self._initialize_pool()  # 初始化连接池

    def _initialize_pool(self):
        """初始化最小数量的连接并放入连接池"""
        for _ in range(self.min_conn):
            conn = self._create_connection()
            self.pool.put((conn, datetime.now()))

    def _create_connection(self):
        """创建一个新的数据库连接"""
        try:
            return pymysql.connect(**self.dbconfig)
        except pymysql.MySQLError as e:
            raise Exception(f"数据库连接错误: {e}")

    def get_connection(self):
        """从连接池中获取连接"""
        with self.lock:
            while not self.pool.empty():
                conn, timestamp = self.pool.get()
                if datetime.now() - timestamp > timedelta(seconds=self.idle_timeout):
                    # 如果连接超过空闲时间，则关闭该连接并创建新的连接
                    conn.close()
                else:
                    return conn
            # 如果连接池已空且未达到最大连接数，创建新连接
            if self.pool.qsize() < self.max_conn:
                return self._create_connection()
            raise Exception("连接池已满，无法获取更多连接。")

    def release_connection(self, conn):
        """释放连接，归还到连接池"""
        with self.lock:
            try:
                if self.pool.qsize() < self.max_conn:
                    self.pool.put((conn, datetime.now()))
                else:
                    conn.close()
            except Exception as e:
                logger.error(f"释放连接时发生错误: {e}")
                conn.close()

    def close_all_connections(self):
        """关闭所有连接，清空连接池"""
        while not self.pool.empty():
            conn, _ = self.pool.get()
            try:
                conn.close()
            except Exception as e:
                logger.error(f"关闭连接时发生错误: {e}")


# ================== 创建数据库对象 =====================
_ = load_dotenv(find_dotenv())
dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
dbconfig = {
    'host': host,
    'user': user,
    'password': password,
    'database': dbname,
    'port': int(port),
    'charset': 'utf8mb4'
}

# 创建连接池
connection_pool = MySQLConnectionPool(min_conn=2, max_conn=5, queue_size=5, idle_timeout=300, dbconfig=dbconfig)
