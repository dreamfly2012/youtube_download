from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=10uVS5pmm-g",proxies={"https":"http://127.0.0.1:1080"})

info= yt.streams

exist_list = ['144p','240p','360p','480p','720p','1080p','1440p','2160p']

dic = {}

def dic_exist(dic, search):
    for key in dic:
        if dic[key] == search:
            return True
    return False         

for i in range(len(info)):
    if info[i].type == 'video':
        if(self.dic_exist(dic, info[i].resolution)==False):
            dic[i] = info[i].resolution
        

stream = yt.streams[2]
print(dic)


#stream.download('./')