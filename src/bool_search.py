#进行bool查询
import pickle
from src.preprocessing import tokenize

def bool_search(inverted_idx_path):#give inverted_idx
    #inverted_idx = './result/allennp_inverted_idx.pkl'
    with open(inverted_idx_path,'rb') as file1:
        inverted_idx = pickle.load(file1)
    
    not_flag = 0
    query_string = input()
    query_or = query_string.split(' or ')
    answer_or = set()
    for query1 in query_or:
        query_and = query1.split(' and ')# and split
        answer_and = []
        for query2 in query_and:
            query_space = query2.split()# space == 'and'
            for query3 in query_space:
                if query3 == 'not':
                    not_flag = 1
                else:
                    word = tokenize(query3)[0]
                    if not_flag == 1:# not
                        not_flag = 0 
                        if (len(answer_and) == 0):
                            answer_and = [i for i in range(2000) if i not in inverted_idx[word][1]]
                        else:
                            answer_and = [i for i in answer_and if i not in inverted_idx[word][1]]
                    else:
                        if (len(answer_and) == 0):
                            answer_and = inverted_idx[word][1]
                        else:
                            answer_and = [i for i in answer_and if i in inverted_idx[word][1]]
        if (len(answer_or) == 0):
            answer_or = set(answer_and)
        else:
            answer_or = answer_or.union(set(answer_and)) 
    print(answer_or)
    return(answer_or)
    #每个print 都是对结果的进行and或者or或者not 的处理
