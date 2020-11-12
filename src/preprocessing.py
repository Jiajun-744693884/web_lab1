from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import string
import re
import nltk

ps = nltk.stem.PorterStemmer()
#nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))
# add more stop words here.
stop_words.update(['enron', 'cc', 'bcc', 'com', 'subject'])

def guess_charset(msg): #判断是什么格式的字符编码
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def parse_msg(msg) -> str:
    '''
    :param msg: email message object
    :return: a final string = msg header string + msg body string
    '''
    final_str = ''
    subject = msg.get('Subject', '')
    if subject:
        subject = decode_str(subject)
    subject.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
    final_str += subject

    if(msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            final_str += parse_msg(part)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            body = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                body = body.decode(charset)
            body.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
            final_str += body
        else:
            pass # ignore non-text attachment

    return final_str

def decode_str(s):#decode成str
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def tokenize(s:str)->list:
    '''
    :param s: string
    :return: token list after regex, stop words and stemming
    '''
    tokens = re.findall("[a-zA-Z]+", s);
    tokens = [t.lower() for t in tokens]

    tokens = [t for t in tokens if t not in stop_words]
    tokens = [ps.stem(t) for t in tokens]

    tokens = [t for t in tokens if len(t) > 1]
    # tokens = [lemma.lemmatize(t) for t in tokens] # 3. lemmatize words.(Too SLOW!!!)
    return tokens


def preprocess_email(filepath):
    '''
    :param filepath: email path
    :return: **list** of tokens in msg after regex, stop words filtering and stemming
    '''
    with open(filepath, 'r') as f:
        msg_content = f.read()
        msg = Parser().parsestr(msg_content)
        pmsg = parse_msg(msg)
        pmsg = tokenize(pmsg)
        return pmsg
