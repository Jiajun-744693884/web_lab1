import os
from preprocessing import preprocess_email
from collections import Counter

def inverted_index_merge(inverted_index:dict,word_count,file_count):
    for word,count in word_count.items():
        if word in inverted_index.keys():
            inverted_index[word][0] += 1
            inverted_index[word][1].append([file_count,count])
        else:
            inverted_index[word] = []
            inverted_index[word].append(1)
            inverted_index[word].append([[file_count,count]])
    return inverted_index

def trainning(root_path):
    file_index={} #dict
    inverted_index = {} #todo:how to optimize our inverted_index on space and searching efficient
    for root, dirs, files in os.walk(root_path):
        file_count = 0
        for filename in files:
            filepath = os.path.join(root, filename)
            word_list = preprocess_email(filepath)
            word_count = Counter(word_list)
            inverted_index_merge(inverted_index,word_count,file_count)
            file_index[file_count]=filepath #create_num2file
            file_count += 1
        print(file_count)

'''
inverted_index:dict
键：单词
值：list
list里面包括：1.出现的文档数,2.list,该list包含两个元素 (1)出现在哪个文档中(2)出现在这个文档中的次数
{'word_a':[10,[[1,5],[2,7],[101,6]]]}
'''
path=".\\web_lab1\\dataset\\maildir\\allen-p\\_sent_mail"
trainning(path)