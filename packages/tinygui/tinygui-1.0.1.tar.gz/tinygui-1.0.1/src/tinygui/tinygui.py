import tkinter as tk
import pygame
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

# pygame窗口显示文本方法
def draw_text(screen, text, pos, mark=0):
    # 设置文本框的外观
    text_box_rect = pygame.Rect(pos, (100, 40))
    text_layer = pygame.Surface(pos, pygame.SRCALPHA)
    text_layer.fill((255, 255, 255, 0))
    screen.blit(text_layer, pos)
    font = pygame.font.Font(None, 55)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=text_box_rect.center)
    screen.blit(text_surface, text_rect)
    pygame.display.update()



