import tkinter as tk
from tkinter import ttk
import tkinter.messagebox,tkinter.commondialog,tkinter.filedialog
import threading
import sqlite3
from pytube import YouTube
import shutil
import sys


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.dic = {}
        self.resolve = False
        """
            判断表是否存在,如果不存在创建表
        """
        if(db.checktable()==False):
            db.createtable()

    def __delete__(self):
        print('组件销毁执行')
    """创建页面组件

    """ 
    def create_widgets(self):
        self.label = tk.Label(self)
        self.label['text'] = "输入youtube播放链接"
        self.label.grid(row=0,column=0,columnspan=2, pady=10)
        
        self.entry_link = tk.Entry(self)
        self.entry_link['width'] = 80
        self.entry_link.grid(row=1,column=0,columnspan=2,pady=10)
    
        self.label_resolution = tk.Label(self)
        self.label_resolution['text'] = "选择分辨率"
        self.label_resolution.grid(row=4,column=0,pady=10)

        self.resolution = tk.StringVar(self)
        
        self.optionmenu_resolution = tk.OptionMenu(self,self.resolution,'360p')
        # self.optionmenu_resolution.insert(0,'360p')
        # self.optionmenu_resolution.insert(0,'720p')
        # self.optionmenu_resolution.insert(0,'1080p')
        self.optionmenu_resolution.grid_forget()
        
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

        # 设置下载进度条
        self.label_process = tk.Label(self, text='下载进度:', )
        self.label_process.grid(row = 6, column = 0, padx = 10, pady =20)
        self.progressbar = ttk.Progressbar(self,orient="horizontal",length=300,mode="determinate")
        self.progressbar["value"]= 0
        self.progressbar["maximum"]=100
        
        # self.canvas_process = tk.Canvas(self, width=465, height=22, bg="white")
        # self.canvas_process.grid(row = 6, column =1,  pady =20)
        self.progressbar.grid(row = 6, column =1,  pady =20)

    def search(self):
        link = self.entry_link.get()
        if link:
            t2 = threading.Thread(target=self.youtube_download)
            t2.setDaemon(True)
            t2.start()
        else:
            tk.messagebox.showerror('错误','url不能为空')
            return
              
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
            return 

        else:    
            t1 = threading.Thread(target=self.process_download)
            t1.setDaemon(True)
            t1.start()


    def process_download(self):
        print('start to downloading...')
        resolution = self.resolution.get()
        self.index = self.dic_get(self.dic, resolution)
        info = db.getdata()
        try:
            self.streams[self.index].download(info[1])
        except Exception as e:
            tk.messagebox.showerror('错误', e)
            return     
        self.resolve = False
        tk.messagebox.showinfo('success','下载完成') 

    # 下载进度处理
    # Prints something like "15.555% done..." 
    def progress_function(self, stream, chunk, bytes_remaining):
        video = self.streams[self.index]
        file_size = video.filesize
        
        percent = (100*(file_size-bytes_remaining))/file_size
        print("{:00.0f}% downloaded".format(percent))
        self.progressbar["value"] = percent
        self.progressbar.update()


      


    #定义执行下载操作    
    def youtube_download(self):
        link = self.entry_link.get()
        info = db.getdata()
        proxy = info[0]
        print(link)
        print(proxy)

        if not link:
            tk.messagebox.showerror("警告", "链接不能为空")
            return

        if not proxy:
            tk.messagebox.showerror('错误', '代理不能为空')
            return    
        
        try:
            yt = YouTube(link,on_progress_callback=self.progress_function, proxies={"https":proxy})
            self.streams= yt.streams
            for i in range(len(self.streams)):
                if self.streams[i].mime_type == 'video/mp4':
                    if self.streams[i].resolution!=None:
                        self.dic[i] = self.streams[i].resolution

            self.resolution.set("请选择")
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

        self.label_emtpy = tk.Label(self)
        self.label_emtpy.grid(row = 0, column = 2, pady = 10)

        self.label_path = tk.Label(self)
        self.label_path['text'] = "保存路径"
        self.label_path.grid(row=1,column=0,pady=10)

        self.entry_path = tk.Entry(self)
        self.entry_path['width'] = 50
        self.entry_path.grid(row=1,column=1,pady=10)


        self.button_path = tk.Button(self)
        self.button_path['text'] = '选择保存路径'
        self.button_path['command'] = self.choose_filedialog
        self.button_path.grid(row=1, column=2, pady = 10)
      
        self.button_save = tk.Button(self)
        self.button_save['text'] = '保存信息'
        self.button_save['bg'] = 'grey'
        self.button_save['fg'] = '#ff0000'
        self.button_save['width'] = 10
        self.button_save['command'] = self.save_data
        self.button_save.grid(row = 2, column = 0, columnspan = 3, padx = 10, pady = 20)

        #get data from database;
        info = db.getdata()
        proxy = info[0]
        path = info[1]
        self.entry_proxy.insert(0, proxy)
        self.entry_path.insert(0, path)

    def choose_filedialog(self):
        self.filedialog_path = tk.filedialog.askdirectory()
        print(self.filedialog_path)
        self.entry_path.insert(0 , self.filedialog_path)
    
    def save_data(self):
        proxy = self.entry_proxy.get()
        path = self.entry_path.get()
        if(proxy=='' or path == ''):
            tk.messagebox.showwarning('警告','代理和保存路径不能为空')
            return
        
        db.save(proxy=proxy,path=path)
        self.destroy()

class DB():
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('test.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()
        
    def getdata(self):
        result = self.cursor.execute("SELECT value FROM SETTING where name='proxy'")
        info = self.cursor.fetchone()
        try:
            proxy = info[0]
        except:
            tk.messagebox.showerror('没有设置代理')
            return

        result = self.cursor.execute("SELECT value FROM SETTING where name='path'")
        info = self.cursor.fetchone()
        try:
            path = info[0]
        except:
            tk.messagebox.showerror('没有设置保存路径')
            return

        return (proxy,path)

    def save(self,proxy='',path=''):
        self.cursor.execute("DELETE from setting where name='proxy' or name='path'")
        self.cursor.execute("INSERT INTO SETTING(ID,NAME,VALUE) VALUES('{}','{}','{}')".format(1,'proxy',proxy))
        self.cursor.execute("INSERT INTO SETTING(ID,NAME,VALUE) VALUES('{}','{}','{}')".format(2,'path',path))
        self.conn.commit()
    

    def checktable(self):
        info = self.cursor.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='SETTING'")
        result = self.cursor.fetchone()
        num = result[0]
        if(num==0):
            return False
        else:
            return True

    def createtable(self):
        sql = '''CREATE TABLE SETTING
            (ID INT PRIMARY KEY     NOT NULL,
            NAME           CHAR(50),   
            VALUE        CHAR(50));'''  

        self.cursor.execute(sql)
        self.conn.commit()



def about():
    tk.messagebox.showinfo("关于","本软件由梦回故里开发制作，只限于研究使用，切勿进行非法用途")



def setting():
    popwindow = Setting()
    popwindow.title("设置全局信息")
    popwindow.geometry("500x300")

def _delete_window():
    print("close all")

    root.destroy()
    #tk.messagebox.showinfo("setting")

if __name__ == "__main__":
    #TODO:关闭窗口，关闭线程
    root = tk.Tk()
    
    db = DB()

    position = 0

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