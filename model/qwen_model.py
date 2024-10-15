import os

from dotenv import load_dotenv, find_dotenv
from qwen_agent.llm import get_chat_model


_ = load_dotenv(find_dotenv())
aes_key = os.getenv('AES_KEY')
api_key = 'sk-1039c340867b49da8a6131e4c7ca7a30'

llm_qwen2_72b = get_chat_model({
    'model': 'qwen2-72b-instruct',
    'model_server': 'dashscope',
    'top_p': '0.8',
    'temperature': '1.0',
    'api_key': api_key,
})


llm_qwen_long = get_chat_model({
    # 'model': 'qwen2-72b-instruct',
    # 'model': 'qwen-max',
    'model': 'qwen-long',
    'model_server': 'dashscope',
    'top_p': '0.8',
    'temperature': '1.0',
    'api_key': api_key,
})

qwen_max_0919 = get_chat_model({
    # 'model': 'qwen2-72b-instruct',
    'model': 'qwen-max-0919',
    # 'model': 'qwen-long',
    'model_server': 'dashscope',
    'top_p': '0.8',
    'temperature': '1.0',
    'api_key': api_key,
})

llm_qwen2_32b = get_chat_model({
    'model': 'qwen2.5-32b-instruct',
    'model_server': 'dashscope',
    'top_p': '0.8',
    'temperature': '1.0',
    'api_key': api_key,
})

llm_qwen_turbo_0919 = get_chat_model({
    'model': 'qwen-turbo-0919',
    'model_server': 'dashscope',
    'top_p': '0.8',
    'temperature': '1.0',
    'api_key': api_key,
})


