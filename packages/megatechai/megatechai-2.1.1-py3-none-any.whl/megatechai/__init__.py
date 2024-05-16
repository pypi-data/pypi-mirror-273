import os

from .model_api import model_api

api_key = os.environ.get("API_KEY", "mega")

api_timeout_seconds = 300

model_api_url = os.environ.get(
    "MEGATECHAI_MODEL_API_URL", "http://192.168.1.188:3004/model-api"#"http://region-31.seetacloud.com:39638/api/chat-process"
)
