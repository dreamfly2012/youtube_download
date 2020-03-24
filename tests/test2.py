import tkinter as tk


root = tk.Tk()

variable = tk.StringVar(root)

dic = {0: '360p', 1: '720p', 2: '2160p', 3: '1440p', 4: '1080p', 8: '480p', 12: '240p', 14: '144p'}

strings = ','.join(dic.values())



s = tuple(dic.values())

#s = tuple([1,2,3,4])

tk.OptionMenu(root, variable, *s).pack()

root.mainloop()
