import pickle

def output_num2file(answers:list,file_index_path):
    with open(file_index_path,'rb') as file:
        file_index = pickle.load(file)
        for answer in answers:
            file_num = str(answer)
            file_path = file_index[file_num]
            print("%s : %s" %(file_num, file_path))