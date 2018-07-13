import json
from mitmproxy import http, ctx
import re
import uuid

session_id = uuid.uuid4().hex[:24]

def response(flow: http.HTTPFlow) -> None:
    global session_id
    
    # config override
    if flow.request.url.endswith(".api.appsee.com/config"):
        with open("config.json", "rb") as file:
            config = json.loads(file.read())

            config["SessionId"] = session_id

            flow.response.content = json.dumps(config).encode("utf-8")

    elif flow.request.url.endswith(".api.appsee.com/upload"):
        content = flow.request.content
        
        decoded_content = content.decode("ascii", "backslashreplace")
        filename = re.search('filename="(.+?.)"', decoded_content).group(1)
        start = decoded_content.index("Content-Type: application/octet-stream")

        file_data = content[start + 42:-50]

        with open(filename, "ba") as file:
            file.write(file_data)

        with open("upload_response.json", "rb") as file:
            flow.response.content = file.read()

        
        session_id = uuid.uuid4().hex[:24]


