import tkinter as tk
import tkinter.messagebox,tkinter.commondialog
import threading
import sqlite3
from pytube import YouTube


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.dic = {}
        self.resolve = False
        

    def create_widgets(self):
        self.label = tk.Label(self)
        self.label['text'] = "输入youtube播放链接"
        self.label.grid(row=0,column=0,columnspan=2, pady=10)
        
        self.entry_link = tk.Entry(self)
        self.entry_link['width'] = 80
        self.entry_link.grid(row=1,column=0,columnspan=2,pady=10)


        # self.label_proxy = tk.Label(self)
        # self.label_proxy['text'] = "请输入代理链接"
        # self.label_proxy.grid(row=2,column=0,columnspan=2,pady=10)

        # self.entry_proxy = tk.Entry(self)
        # self.entry_proxy['width'] = 80
        # self.entry_proxy.grid(row=3,column=0,columnspan=2,pady=10)

        self.label_resolution = tk.Label(self)
        self.label_resolution['text'] = "选择分辨率"
        self.label_resolution.grid(row=4,column=0,pady=10)

        self.resolution = tk.StringVar(self)
        #self.resolution.set('360p')
        self.optionmenu_resolution = tk.OptionMenu(self,self.resolution,'360p')
        # self.optionmenu_resolution.insert(0,'360p')
        # self.optionmenu_resolution.insert(0,'720p')
        # self.optionmenu_resolution.insert(0,'1080p')
        self.optionmenu_resolution.grid_forget()
        #self.optionmenu_resolution.grid(row=4,column=1,columnspan=2,pady=10)

        self.button_search = tk.Button(self)
        self.button_search['text'] = "检索"
        self.button_search['width'] = 20
        self.button_search['command'] = self.search
        self.button_search['bg'] = "red"
        self.button_search['fg'] = "black"
        self.button_search.grid(row=5,column=0,padx=10,pady=30)

        self.button_download = tk.Button(self)
        self.button_download['text'] = "下载"
        self.button_download['width'] = 20
        self.button_download['bg'] = "black"
        self.button_download['fg'] = "white"
        self.button_download['command'] = self.download
        self.button_download.grid(row=5,column=1,padx=10,pady=30)


    def search(self):
        link = self.entry_link.get()
        #proxy = self.entry_proxy.get()
        if link:
            t2 = threading.Thread(target=self.youtube_download)
            t2.start()
        else:
            tk.messagebox.showerror('错误','url不能为空')
            exit   
    def dic_get(self, dic, serach):
        for key in dic:
            if dic[key] == serach:
                return key        
        return False

    def dic_exist(self, dic, search):
        for key in dic:
            if dic[key] == search:
                return True
        return False     

    def download(self):
        if self.resolve == False:
            tk.messagebox.showwarning('warning','请等待url解析')
        else:    
            t1 = threading.Thread(target=self.process_download)
                
            t1.start()


    def process_download(self):
        print('start to downloading...')
        resolution = self.resolution.get()

        index = self.dic_get(self.dic, resolution)
        
        print(index)
        self.streams[index].download('./')
        self.resolve = False
        tk.messagebox.showinfo('success','下载完成') 

    def youtube_download(self):
        #TODO:异常抛出给客户端
        link = self.entry_link.get()
        print(link)
        proxy = ""
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        info = c.execute("SELECT value from SETTING")
        for item in info:
            proxy = item[0]

        
        try:
            print(proxy)
            yt = YouTube(link,proxies={"https":proxy})
            self.streams= yt.streams
            for i in range(len(self.streams)):
                if self.streams[i].type == 'video':
                    if(self.dic_exist(self.dic, self.streams[i].resolution)==False):
                        self.dic[i] = self.streams[i].resolution

            
            self.optionmenu_resolution = tk.OptionMenu(self,self.resolution,*self.dic.values())
            self.optionmenu_resolution.grid(row=4,column=1,columnspan=2,pady=10)
            self.resolve = True

        except:
            tk.messagebox.showerror("警告","网络异常")

class Setting(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.label_proxy = tk.Label(self)
        self.label_proxy['text'] = "代理地址"
        self.label_proxy.grid(row =0, column = 0, pady = 10)

        self.entry_proxy = tk.Entry(self)
        self.entry_proxy['width'] = 50
        self.entry_proxy.grid(row=0,column=1, pady = 10)

        self.button_save = tk.Button(self)
        self.button_save['text'] = '保存信息'
        self.button_save['bg'] = 'grey'
        self.button_save['fg'] = '#ff0000'
        self.button_save['width'] = 10
        self.button_save['command'] = self.save_proxy
        self.button_save.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 20)

    def save_proxy(self):
        conn = sqlite3.connect('test.db')
        proxy = self.entry_proxy.get()
        print("Opened database successfully")
        print(proxy)
        c = conn.cursor()
        c.execute("""DROP TABLE SETTING;""")
        c.execute('''CREATE TABLE SETTING
            (ID INT PRIMARY KEY     NOT NULL,
            NAME           CHAR(50),   
            VALUE        CHAR(50));''')
        print("Table created successfully")
        c.execute("INSERT INTO SETTING(ID,NAME,VALUE) VALUES('{}','{}','{}')".format(1,'proxy',proxy))
        conn.commit()
        conn.close()

def about():
    tk.messagebox.showinfo("关于","本软件由梦回故里开发制作，只限于研究使用，切勿进行非法用途")



def setting():
    popwindow = Setting()
    popwindow.title("设置全局信息")
    popwindow.geometry("400x300")


    
    #tk.messagebox.showinfo("setting")

if __name__ == "__main__":
    #TODO:关闭窗口，关闭线程
    root = tk.Tk()

    proxy = ""

    #root.title("youtube下载助手")

    root.geometry('800x600')

    app = Application(master=root)

    app.master.title("youtube下载助手")

    MenuBar = tk.Menu(root)

    root.config(menu=MenuBar)

    fileBar = tk.Menu(MenuBar,tearoff = 0)
    fileBar.add_command(label='全局', command = setting)

    MenuBar.add_cascade(label='设置',menu = fileBar)
    MenuBar.add_cascade(label='关于',command = about)

    app.mainloop()
 
