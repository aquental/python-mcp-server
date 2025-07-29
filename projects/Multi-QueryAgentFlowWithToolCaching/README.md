# Multi-Query Agent Flow With Tool Caching

```plaintext
INFO:     Started server process [227]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
INFO:     127.0.0.1:39204 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:39218 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:39218 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:39218 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:36:50] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:39218 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:36:52] INFO     Processing request of type CallToolRequest                                          server.py:551
INFO:     127.0.0.1:39218 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:36:54] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:39218 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:36:57] INFO     Processing request of type CallToolRequest                                          server.py:551
INFO:     127.0.0.1:39218 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:36:59] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:39218 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:37:02] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:39218 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:37:05] INFO     Processing request of type CallToolRequest                                          server.py:551
INFO:     127.0.0.1:60896 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:37:12] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:60896 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:37:14] INFO     Processing request of type CallToolRequest                                          server.py:551
INFO:     127.0.0.1:60896 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:37:15] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:60896 - "POST /messages/?session_id=f37db5d145be44a292b1a82fa7ea7cdb HTTP/1.1" 202 Accepted
[07/29/25 14:37:17] INFO     Processing request of type CallToolRequest                                          server.py:551
INFO:     127.0.0.1:55792 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
[07/29/25 14:51:58] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
[07/29/25 14:52:00] INFO     Processing request of type CallToolRequest                                          server.py:551
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
[07/29/25 14:52:02] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
[07/29/25 14:52:04] INFO     Processing request of type CallToolRequest                                          server.py:551
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
[07/29/25 14:52:06] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
[07/29/25 14:52:08] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
[07/29/25 14:52:10] INFO     Processing request of type CallToolRequest                                          server.py:551
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
[07/29/25 14:52:13] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:55800 - "POST /messages/?session_id=d545a8d805804e399caa75011fc20ed1 HTTP/1.1" 202 Accepted
[07/29/25 14:52:16] INFO     Processing request of type ListToolsRequest                                         server.py:551
```

```python
async with MCPServerSse(
    params=server_params,
    cache_tools_list=True # enable cache
) as mcp_server:
```

```plaintext
INFO:     Started server process [224]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
INFO:     127.0.0.1:60042 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:60050 - "POST /messages/?session_id=196fdd81362d4ab2a92cc8b82d519b4a HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:52964 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:52966 - "POST /messages/?session_id=226031824fe946bfa17d123df3a5580b HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:52966 - "POST /messages/?session_id=226031824fe946bfa17d123df3a5580b HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:52966 - "POST /messages/?session_id=226031824fe946bfa17d123df3a5580b HTTP/1.1" 202 Accepted
[07/29/25 15:05:18] INFO     Processing request of type ListToolsRequest                                         server.py:551
INFO:     127.0.0.1:52966 - "POST /messages/?session_id=226031824fe946bfa17d123df3a5580b HTTP/1.1" 202 Accepted
[07/29/25 15:05:19] INFO     Processing request of type CallToolRequest                                          server.py:551
INFO:     127.0.0.1:52966 - "POST /messages/?session_id=226031824fe946bfa17d123df3a5580b HTTP/1.1" 202 Accepted
[07/29/25 15:05:23] INFO     Processing request of type CallToolRequest                                          server.py:551
INFO:     127.0.0.1:49462 - "POST /messages/?session_id=226031824fe946bfa17d123df3a5580b HTTP/1.1" 202 Accepted
[07/29/25 15:05:31] INFO     Processing request of type CallToolRequest                                          server.py:551
```
