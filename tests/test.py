def dic_exist(dic, search):
    for key in dic:
        if dic[key] == search:
            return True
    return False   

#dic = {0:'360p',1:'720p',2:'2160p'}

# if (dic_exist(dic, '114p') == False):
#     print("不在")
# else:
#     print("在")

dic = {0: '360p', 1: '720p', 2: '2160p', 3: '1440p', 4: '1080p', 8: '480p', 12: '240p', 14: '144p'}


Lang = ['Python', 'PHP', 'CPP', 'C', 'Java', 'JavaScript', 'VBScript']

print(tuple(dic.values()))

print(tuple(Lang))
