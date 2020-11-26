from email.parser import Parser
from email.header import decode_header
from collections import Counter
from email.utils import parseaddr
import progressbar
import pickle
import string
import re
import os
import nltk
import json

ps = nltk.stem.PorterStemmer()
#nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))
# add more stop words here.
stop_words.update(['enron', 'cc', 'bcc', 'com', 'subject'])

def guess_charset(msg):
    '''
    判断是什么格式的字符编码 \n
    :param msg:
    :return:
    '''
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
        else: # 'charset=' is not in header, then search the whole message
            str_msg = msg.as_string()
            pos = str_msg.find('charset=')
            if pos >= 0:
                charset = str_msg[pos + 8:].splitlines()[0]
            pass
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
        if subject is not None:
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
    else:
        return None


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
    with open(filepath, 'r', errors='ignore') as f:
        msg_content = f.read()
        msg = Parser().parsestr(msg_content)
        pmsg = parse_msg(msg)
        pmsg = tokenize(pmsg)
        return pmsg

def get_file_num(root_path):
    '''
    Get the total number of files under rootpath
    :param rootpath:
    :return:
    '''
    file_n = 0
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if '.json' in filename or '.DS_Store' in filename or '.txt' in filename:
                continue
            if 'word_count.pkl' not in filename:
                continue
            else:
                file_n += 1
    return file_n

def preprocess_all_files(root_path):
    file_count = 0
    p = progressbar.ProgressBar()
    file_total = get_file_num(root_path)
    p.start(file_total)

    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if '.json' in filename or '.DS_Store' in filename or '.txt' in filename or '.pkl' in filename:
                continue
            filepath = os.path.join(root, filename)
            try:
                word_list = preprocess_email(filepath)
                word_count = Counter(word_list)
                with open(filepath + '_word_count.pkl', 'wb') as f:
                    pickle.dump(word_count, f)

                file_count += 1
                p.update(file_count)

            except Exception as e:
                print(f"[Exception] at {filepath}: {str(e)}")

    p.finish()

