import requests
import json

class QwenModelAPI:
    def __init__(self):
        self.base_url = 'http://192.168.10.12:3008'
        self.headers = {
            'Authorization': 'sk-PAlcOJUXuackZtyK107b1394227640039d0eC0Fa178dD0C3',
            'Content-Type': 'application/json'
        }

    def chat(self, messages, model="qwen:32b", temperature=0.7):
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }

        response = requests.post(
            f"{self.base_url}/v1/chat/completions",
            headers=self.headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Request failed with status {response.status_code}"}

model_api = QwenModelAPI()

# 示例使用
if __name__ == "__main__":
    base_url = "http://192.168.10.12:3008"
    api_key = "PAlcOJUXuackZtyK107b1394227640039d0eC0Fa178dD0C3"

    # 创建API对象
    model_api = QwenModelAPI(base_url, api_key)

    # 定义要发送的消息
    messages = [
        {"role": "user", "content": "why sky is blue"}
    ]

    # 调用 chat 方法获取响应
    response = model_api.chat(messages)

    # 输出响应
    logger.info(json.dumps(response, indent=4, ensure_ascii=False))
