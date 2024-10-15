import logging
from logging.handlers import RotatingFileHandler

# 创建一个logger对象
logger = logging.getLogger('web_app_logger')

# 设置日志级别为DEBUG，意味着记录所有级别的日志
logger.setLevel(logging.DEBUG)

# 设置日志处理器，文件最大5MB，最多保留3个旧文件
handler = RotatingFileHandler('app.log', maxBytes=5*1024*1024, backupCount=3)
handler.setLevel(logging.DEBUG)

# 创建一个处理器，输出日志到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 定义日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


console_handler.setFormatter(formatter)
handler.setFormatter(formatter)
# 将处理器添加到logger中
logger.addHandler(console_handler)
logger.addHandler(handler)

