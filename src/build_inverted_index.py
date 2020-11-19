import os
import json
import progressbar
from src.preprocessing import preprocess_email
from collections import Counter
import pickle

# def file_traverse(path, func...)
# {
#     pass
# }

store_path = '../result/'
def term_selection(root_path, select_n=1000):
    tf_dict = {}
    file_count = 0
    p = progressbar.ProgressBar()
    file_total = 517408+5
    p.start(file_total)

    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if '.json' in filename or '.DS_Store' in filename or '.txt' in filename:
                continue
            filepath = os.path.join(root, filename)
            try:
                word_list = preprocess_email(filepath)
                word_count = Counter(word_list)
                for word, count in word_count.items():
                    if word in tf_dict.keys():
                        tf_dict[word] += count
                    else:
                        tf_dict[word] = count

                file_count += 1
                p.update(file_count)

            except Exception as e:
                print(f"[Exception] at {filepath}: {str(e)}")

    tf_dict = {k: v for k, v in sorted(tf_dict.items(), key = lambda item : item[1], reverse=True)}
    selected_term_list = list(tf_dict.keys())[0: select_n]
    p.finish()
    try:
        # with open(root_path+'tf_dict', 'w') as f:
        #     for item in  tf_dict:
        #         f.write(f"{item}, ")

        with open(store_path+'selected_term_list.pkl', 'wb') as f:
            pickle.dump(selected_term_list, f)

    except Exception as e:
        print(f"[Exception] at writing file: {str(e)}")

    return selected_term_list




def inverted_index_merge(inverted_index:dict,word_count, file_count):
    for word,count in word_count.items():
        if word in inverted_index.keys():
            inverted_index[word][0] += 1 # num of doc containing this word
            inverted_index[word][1].append(file_count)
        else:
            inverted_index[word] = []
            inverted_index[word].append(1)
            inverted_index[word].append([file_count])
    return inverted_index

def training(root_path):
    file_index={} #dict
    inverted_index = {} #todo:how to optimize our inverted_index on space and searching efficient
    for root, dirs, files in os.walk(root_path):
        if '.DS_Store' not in files:
            file_count = 0
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    word_list = preprocess_email(filepath)
                    word_count = Counter(word_list)
                    inverted_index = inverted_index_merge(inverted_index,word_count,file_count)
                    file_index[file_count]=filepath #create_num2file # TODO: optimize this using Btree
                    file_count += 1
                except Exception:
                    print(f"[Exception] at {filepath}")

            print(file_count)
    with open(root_path+'inverted_idx.json', "w") as inverted_idx_json:
        json.dump(inverted_index, inverted_idx_json)
    return inverted_index

'''
inverted_index:dict
键：单词
值：list
list里面包括：1.出现的文档数,2.list,该list包含两个元素 (1)出现在哪个文档中(2)出现在这个文档中的次数
{'word_a':[10,[[1,5],[2,7],[101,6]]]}
'''
path=".\\web_lab1\\dataset\\maildir\\allen-p\\_sent_mail"
training(path)