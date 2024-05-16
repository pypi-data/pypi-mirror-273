# 快速上手

正常情况（可以参考websocket.WebSocket的传参)

```python
import L2dvExApi
api =  L2dvExApi.WebSocket()
api.connect("ws://127.0.0.1:8888/api")
api.ShowTextBubble(0, "Hello, World!")
api.close()
```

使用`wit ... as ...`自动开启/关闭链接(推荐)

```python
import L2dvExApi
with L2dvExApi.WebSocket("ws://127.0.0.1:8888/api") as api:
    api.ShowTextBubble(0, "Hello, World!")
```

# API列表

```python
import L2dvExApi
print(L2dvExApi.ApiList.Msg_name_to_code.keys())
```