import tkinter as tk

root = tk.Tk()

MenuBar = tk.Menu(root)
# 将菜单栏放到主窗口
root.config(menu =MenuBar)
# 创建文件菜单，不显示分窗
fileBar = tk.Menu(MenuBar, tearoff=0)

# 添加文件菜单项
fileBar.add_command(label="open")
fileBar.add_command(label="save")
fileBar.add_command(label="save as")
# 创建分割线
fileBar.add_separator()
fileBar.add_command(label="exit", command=root.destroy)
# 将文件菜单添加到菜单栏
MenuBar.add_cascade(label="File", menu=fileBar)

root.mainloop()