import cv2
from tkinter import *
from tkinter import ttk
from PIL import Image ,ImageTk
from tkinter.messagebox import showerror
import customtkinter as ctk
from tabulate import tabulate
import openpyxl as oxl

# Defining Main theme of all widgets
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
wid = 1200
hgt = 700

def Imgo(file,w,h) :

    # Image processing
    img=Image.open(file)
    pht=ImageTk.PhotoImage(img.resize((w,h), Image.ANTIALIAS))
    return pht

def change(can,page) :

    # Switching canvas
    can.destroy()
    page()

def menuPage() :

    # Defining Structure
    second_page=Canvas( root, width = wid, height = hgt, bg = "black", highlightcolor = "#3c5390", borderwidth = 0 )
    second_page.pack( fill = "both", expand = True )

    # Background Image
    back_image = Imgo("back5.png", 1498, 875)
    entry_image = Imgo("back3.png", 600, 400)
    second_page.create_image( 0, 0, image = back_image , anchor = "nw")
    # second_page.create_image(350, 325, image = entry_image, anchor = "nw")

    # Heading
    second_page.create_text(450,150,text="Content...",font=(ft[0],45,"bold"),fill="#1c54df")

    # Back Ground remover page window
    backRem=Imgo("back4.png",220,170)
    backRem_bt=ctk.CTkButton(master=root,image=backRem, text="Profile", text_font=("Book Antiqua",22,"bold"), compound="top",
                         corner_radius=10, bg_color="#fafafa", fg_color="#2d435b", hover_color="#fdbf38", text_color="white",
                         width=230, height=200, border_width=0, command= lambda : print("Google"))
    backRem_bt_win=second_page.create_window(200,300,anchor="nw",window=backRem_bt)

    # Image converter page window
    imgConvert=Imgo("back4.png",220,170)
    imgConvert_bt=ctk.CTkButton(master=root,image=imgConvert, text="Profile", text_font=("Book Antiqua",22,"bold"), compound="top",
                         corner_radius=10, bg_color="#fafafa", fg_color="#2d435b", hover_color="#fdbf38", text_color="white",
                         width=230, height=200, border_width=0, command= lambda : print("Google"))
    imgConvert_bt_win=second_page.create_window(500,300,anchor="nw",window=imgConvert_bt)

    # Search image page window
    findImg=Imgo("back4.png",220,170)
    findImg_bt=ctk.CTkButton(master=root,image=findImg, text="Profile", text_font=("Book Antiqua",22,"bold"), compound="top",
                         corner_radius=10, bg_color="#fafafa", fg_color="#2d435b", hover_color="#fdbf38", text_color="white",
                         width=230, height=200, border_width=0, command= lambda : print("Google"))
    findImg_bt_win=second_page.create_window(800,300,anchor="nw",window=findImg_bt)

    # Sort image page window
    imgSort=Imgo("back4.png",220,170)
    imgSort_bt=ctk.CTkButton(master=root,image=imgSort, text="Profile", text_font=("Book Antiqua",22,"bold"), compound="top",
                         corner_radius=10, bg_color="#fafafa", fg_color="#2d435b", hover_color="#fdbf38", text_color="white",
                         width=230, height=200, border_width=0, command= lambda : print("Google"))
    imgSort_bt_win=second_page.create_window(1100,300,anchor="nw",window=imgSort_bt)

    root.mainloop()

def loginPage() :

    global user,pwrd,first_page

    # Defining Structure
    first_page=Canvas( root, width = wid, height = hgt, bg = "black", highlightcolor = "#3c5390", borderwidth = 0 )
    first_page.pack( fill = "both", expand = True )

    # Background Image
    back_image = Imgo("back12.jpg", 1498, 875)
    design_image = Imgo("back3.png", 600, 400)
    first_page.create_image( 0, 0, image = back_image , anchor = "nw")
    first_page.create_image(350, 325, image = design_image, anchor = "nw")

    # Heading
    first_page.create_text(450,150,text="Image Sorter",font=(ft[0],45,"bold"),fill="#1c54df")
    first_page.create_text(1150,380,text="Welcome\n    Back",font=(ft[0],26,"bold"),fill="#0b4bf5")

    # Entry of username and password
    user=ctk.CTkEntry(master=root, placeholder_text="Username", text_font=(ft[1],20), width=220, height=30, corner_radius=14,
                        text_color="black", fg_color="#e1f5ff", bg_color="#9ae2fe", border_color="white", border_width=3)
    pwrd=ctk.CTkEntry(master=root, placeholder_text="Password", text_font=(ft[1],20), width=220, height=30, corner_radius=14,
                        text_color="black", fg_color="#e1f5ff", bg_color="#9ae2fe", border_color="white", border_width=3,show="*")
    user_win=first_page.create_window(1015,470,anchor="nw",window=user)
    pwrd_win=first_page.create_window(1015,550,anchor="nw",window=pwrd)

    # Login button
    log_bt=ctk.CTkButton(master=root, text="Login", text_font=(ft[0],22), width=50, height=25, corner_radius=15,
                         text_color="white", bg_color="#9ae2fe", fg_color="red", hover_color="#ff5359", 
                         border_width=0, command = lambda : change(first_page,menuPage) )
    log_bt_win=first_page.create_window(1090,650,anchor="nw",window=log_bt)

    root.mainloop()

global root
root=ctk.CTk()
root.title("Image Sorter")
root.iconbitmap("image.ico")
root.geometry("1200x700+200+80")
root.resizable(False,False)
ft = ["Tahoma","Seoge UI","Heloia"]
loginPage()