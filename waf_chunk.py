#coding:utf8
from mitmproxy import http
from mitmproxy import ctx
import random, string


"""
hack mimtproxy  assemble.py
修改headers中的transfer-encoding后，mitmproxy会自动在content中增加content的大小，服务器会解析错误

def assemble_body(headers, body_chunks):                                                                         
    if "chunked" in headers.get("transfer-encoding", "").lower() and 
       'test' not in headers.get("test", "").lower():                                                                                                               
        for chunk in body_chunks:                                                                                
            if chunk:                                                                                            
                yield b"%x\r\n%s\r\n" % (len(chunk), chunk)                                                      
        yield b"0\r\n\r\n"                                                                                       
    else:                                                                                                        
        for chunk in body_chunks:                                                                                
            yield chunk                                                                                          
"""

def request(flow: http.HTTPFlow) -> None:
    if flow.request.method == 'POST':
        # flow.request.headers['Content-Length'] = '0'
        # del flow.request.headers['Content-Length']
        #print('-'*15)
        # """
        a = flow.request.text

        if a:
            flow.request.headers['Transfer-Encoding'] = 'Chunked'
            flow.request.headers['test'] = 'test'

            #print(a)
            #a = flow.request.decode(a)
            ctx.log.info('-'*10)
            ctx.log.info(a)
            b = ''
            l = 13
            for i in range(len(a)//l+1):
                if a[i*l:(i+1)*l]:
                    b = f'{b}' \
                        f'{len(a[i*l:(i+1)*l]):0x};{"".join(random.sample(string.ascii_letters + string.digits, 10))}' \
                        f'\r\n' \
                        f'{a[i * l:(i + 1) * l]}\r\n'

            b = f'{b}0\r\n\r\n'
            flow.request.text = b

            del flow.request.headers['Content-Length']

            #flow.request.replace('[cC]ontent-[lL]ength: (\d)+','')
            # print('-' * 10)
            # print(flow.request.headers)
            ctx.log.info('-' * 10)
            ctx.log.info(flow.request.text)

