import os
from email.parser import Parser
from email.header import decode_header

path = '.\\web_lab1\\dataset\\maildir\\allen-p\\_sent_mail' #文件的地址

def guess_charset(msg): #判断是什么格式的字符编码
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def print_info(msg):
    value = msg.get('Subject', '')
    if value:
        value = decode_str(value)
    print('Subject: %s' % (value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('part %s' % (n))
            print_info(part)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('Text: %s' % (content))
        else:
            print('Attachment: %s' % (content_type))

def decode_str(s):#decode成str
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

'''for root, dirs, files in os.walk(path):
    for filename in files:
        filepath = os.path.join(root,filename)
        try:
            with open(filepath, 'r') as f:
                msg_content = f.read()
                msg = Parser().parsestr(msg_content)
                print_info(msg,indent=0)
        except:
            print("having a error")
'''

filepath = path + '\\2'
with open(filepath, 'r') as f:
    msg_content = f.read()
    msg = Parser().parsestr(msg_content)
    print_info(msg)