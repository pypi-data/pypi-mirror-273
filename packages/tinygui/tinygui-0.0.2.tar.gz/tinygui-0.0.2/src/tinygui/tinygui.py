import tkinter as tk
from tkinter.ttk import *
from tkinter import*
pwd = ''
root = ''
def tk_init(txt=''):
    global pwd,root
    pwd = ''
    root = tk.Tk()
    # 创建一个Label组件
    label = tk.Label(root,text=txt,bg='white')
    #root.iconphoto(False,'pwd.png')
    root.title('')
    label.pack()
    root.geometry("300x120+500+140")
    root.resizable(width=False, height=False)
    root.configure(bg='white')

def input_text(txt=''):
    tk_init(txt)
    def get_pwd():
       global pwd
       pwd = password_entry.get()
       #root.destroy()
       #print(pwd)
       root.destroy()
       #return pwd
    def on_close():
        global pwd
        pwd = ''
        root.destroy()

    password_entry = tk.Entry(root, show="",bd=5,width=35)
    password_entry.pack()
    ensureButton = Button(root, text ="确定", command = get_pwd)
    ensureButton.pack(padx = 25,ipadx=10,side='left')
    cancleButton = Button(root,text='取消',command=on_close)
    cancleButton.pack(padx = 25,ipadx=10,side='right')
    # 创建一个Entry组件，设置显示形式为星号
    # 运行主循环
    try:
        mainloop()
    except:
        pass
    return str(pwd)

def get_value():
    return str(pwd)


