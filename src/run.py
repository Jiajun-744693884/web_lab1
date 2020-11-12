'''
处理50W份邮件，并生成倒排索引表，以及计算td-idf值等
'''

#进行bool查询

query_string = input()

query_or = query_string.split('or')
for query1 in query_or:
    query_and = query1.split('and')
    for query2 in query_and:
        query_space = query2.split()
        for query3 in query_space:
            if ('not' in query3):
                print("!=",query3)#进行and和not处理
            else:
                print(query3)#进行and和not处理
    print(query1)#进行or处理

#每个print 都是对结果的进行and或者or或者not 的处理
