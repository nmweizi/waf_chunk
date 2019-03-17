- 看到http://gv7.me/articles/2019/chunked-coding-converter/ 用Burp实现的方法，不免心痒，用mitmproxy实现一个。 
- 需要修改mitmproxy中的assemble.py，谁有其他方法，烦告知。
```python 
def assemble_body(headers, body_chunks):                                                                         
    if "chunked" in headers.get("transfer-encoding", "").lower() and  'test' not in headers.get("test", "").lower():                                                                                                               
        for chunk in body_chunks:                                                                                
            if chunk:                                                                                            
                yield b"%x\r\n%s\r\n" % (len(chunk), chunk)                                                      
        yield b"0\r\n\r\n"                                                                                       
    else:                                                                                                        
        for chunk in body_chunks:                                                                                
            yield chunk      
```
