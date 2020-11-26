import os
import json
import progressbar
from src.preprocessing import preprocess_email, get_file_num
from collections import Counter
import pickle

def term_selection(root_path, select_n: int =1000, store_path: str = '../result/'):
    '''
    Traverse all files and summarize frequency of words.
    Then select top ${select_n} words, dump them to a pickle file and return list of them. \n
    :param root_path:
    :param select_n: number of selected words
    :param store_path
    :return: list of selected terms
    '''
    tf_dict = {}
    file_count = 0
    p = progressbar.ProgressBar()
    file_total = get_file_num(root_path)
    p.start(file_total)

    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if 'word_count.pkl' not in filename:
                continue
            filepath = os.path.join(root, filename)
            try:
                # word_list = preprocess_email(filepath)
                # word_count = Counter(word_list)
                with open(filepath, 'rb') as f:
                    word_count = pickle.load(f)
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
        with open(store_path+'selected_term_list.pkl', 'wb') as f:
            pickle.dump(selected_term_list, f)

    except Exception as e:
        print(f"[Exception] at writing file: {str(e)}")

    return selected_term_list

def inverted_index_merge(inverted_index:dict, selected_term_list, word_count, file_count):
    '''
    Merge info of each file into final inverted index dictionary.
    :param inverted_index:
    :param selected_term_list:
    :param word_count:
    :param file_count:
    :return:
    '''
    for word,count in word_count.items():
        if word in selected_term_list:
            if word in inverted_index.keys():
                inverted_index[word][0] += 1 # num of doc containing this word
                inverted_index[word][1].append(file_count)
            else:
                inverted_index[word] = []
                inverted_index[word].append(1)
                inverted_index[word].append([file_count])
    return inverted_index

def build_inverted_index(root_path, store_path):
    '''
    Build inverted index dictionary.
    :param root_path:
    :return:
    '''
    file_index={} #dict
    inverted_index_dict = {} #todo:how to optimize our inverted_index on space and searching efficient

    with open(store_path+'selected_term_list.pkl', 'rb') as f:
        selected_term_list = pickle.load(f)

    p = progressbar.ProgressBar()
    file_total = get_file_num(root_path)
    p.start(file_total)
    file_count = 0
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if 'word_count.pkl' not in filename:
                continue
            filepath = os.path.join(root, filename)
            try:
                # word_list = preprocess_email(filepath)
                # word_count = Counter(word_list)
                with open(filepath, 'rb') as f:
                    word_count = pickle.load(f)
                inverted_index_dict = inverted_index_merge(inverted_index_dict, selected_term_list, word_count, file_count)
                file_index[file_count]=filepath #create_num2file # TODO: optimize this using Btree
                file_count += 1
                p.update(file_count)

            except Exception:
                print(f"[Exception] at {filepath}")

    p.finish()
    with open(store_path+'num2file.pkl','wb') as f:
        pickle.dump(file_index, f)
    with open(store_path + 'num2file.json', 'w') as f:
        json.dump(file_index, f)

    with open(store_path+'inverted_idx.json', "w") as inverted_idx_json:
        json.dump(inverted_index_dict, inverted_idx_json)
    with open(store_path+'inverted_idx.pkl', "wb") as f:
        pickle.dump(inverted_index_dict, f)

    return inverted_index_dict

'''
inverted_index:dict
键：单词
值：list
list里面包括：1.出现的文档数,2.list,该list包含两个元素 (1)出现在哪个文档中(2)出现在这个文档中的次数
{'word_a':[10,[[1,5],[2,7],[101,6]]]}
'''