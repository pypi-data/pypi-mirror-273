# 关于InforeWss简单使用
    
## 使用方法
    安装相关模块后
    url = ""
    data = {}
    ws = InforeWss(url)
    await ws.connect_to_server()
    await ws.send_and_recv(data)
### 简单说明
    需要异步调用处理 

    

  