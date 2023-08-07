# Library and Modules used 
import os
import cv2
import numpy as np
import customtkinter as ctk
from tkinter import *
from rembg import remove
from pathlib import Path
from threading import Thread
from datetime import datetime
from deepface import DeepFace
from PIL import Image ,ImageTk
from tkinter import ttk, filedialog
from pdf2image import convert_from_path
from tkinter.messagebox import showerror, showinfo

# Creating functions whihch used to provide fnctionality to pages
def Imgo( file, w, h) :

    # Image processing
    img = Image.open( file )
    pht = ImageTk.PhotoImage( img.resize( (w,h), Image.Resampling.LANCZOS))
    return pht

def change( can, page) :

    # Switching canvas
    can.destroy()
    page()

def mistake( message) :

    # Pop up window for errors
    showerror( title = "Error Occured", message = message )

def inform( message) :

    # Pop up window for info
    showinfo( title = "Done", message = message )

def analysis1( path1, path2, sample ) :

    # First method for image analysis 
    result_1 = DeepFace.verify( img1_path = path1 , img2_path = path2,
                                    enforce_detection = False, model_name = "VGG-Face",
                                        distance_metric = "cosine", detector_backend = "opencv" )
                                        
    if result_1["verified"] :

        # Add image if match
        matches.add( sample )

def analysis2( path1, path2, sample ) :

    # Second method for image analysis
    result_2 = DeepFace.verify( img1_path = path1 , img2_path = path2,
                                    enforce_detection = False, model_name = "VGG-Face",
                                        distance_metric = "euclidean_l2", detector_backend = "ssd" )

    if result_2["verified"] :

        # Add image if match
        matches.add( sample )

def sortingImages() :

    # Sorting Images and Saving them in folders
    if ( values[2] != "" and values[4] != "" ) :

        main_img = {}
        check_img = {}

        # Processing First folder 
        for img in os.listdir( values[2] ) :

            main_path = values[2] + '/' + str(img)
            main_img[img] = cv2.imread( main_path )

        # Processing Second folder
        for img in os.listdir( values[4] ) :

            check_path = values[4] + '/' + str(img)
            check_img[img] = cv2.imread( check_path )

        # Analysing both the folders together
        for x in main_img.keys() :

            for y in check_img.keys() :

                # Both at same time
                Thread(target = analysis1( main_img[x], check_img[y], y )).start()
                Thread(target = analysis2( main_img[x], check_img[y], y )).start()

            new_dir = os.path.join( values[2], str( x[ : len(x)-4] + "match") )
            os.mkdir( new_dir )

            for i in matches :

                # Saving Images to new directory
                cv2.imwrite( os.path.join( new_dir, i), check_img[i] )
            
            # Clearing the previous data from set
            matches.clear()

        # Message of completion
        inform( "Sorted And Saved" )
        values[2] = ""
        values[4] = ""
    
    else :

        # Showing error due to empty credientials
        mistake( "Empty Fields" )

def findingImages( label ) :

    # Finding similar images
    if ( values[0] != "" and values[2] != "" ) :

        # Processing image
        values[1] = cv2.imread( values[0] )

        # Getting into images of given folder
        for img in os.listdir( values[2] ) :

            img2_path = values[2] + '/' + str(img)
            values[3] = cv2.imread( img2_path )

            # Both at same time
            Thread(target = analysis1( values[1], values[3], img )).start()
            Thread(target = analysis2( values[1], values[3], img )).start()

        # For searching folder, method 2

        # df = DeepFace.find( img_path = values[0], db_path = values[2], enforce_detection = False )
        # res = pd.DataFrame( df )
        # for i in res["identity"] :
        #     print(i)
    
    # Show data
    if matches == set() :

        # Message in the frame
        label.configure( text = "No File Found")
    
    else :
        
        # Showing results in order
        x = 50
        output = ""

        for i in matches :
            
            if ( len(output + i) > x ) :

                x = x + 50
                output = output + os.linesep

            output = str(output + i + ", ")
        
        label.configure( text = output[:len(output)-2], 
                            text_font = (ft[1], 20, "bold"))
        label.place_configure( x = 50, y = 50, anchor = "nw" )

    # Clearing previously processed data
    values[0] = ""
    values[1] = np.array([0,0,0])
    values[2] = ""
    values[3] = np.array([0,0,0])
    matches.clear()

def convertFile( can, formate ) :

    # Coverting files to another specified formate
    convert_to = formate.get()
    file_types = { "Select Type " : False, 
                    "   PDF" : [ "PDF file", "*.pdf"], 
                     "   PNG" : [ "PNG file", "*.png"], 
                      "   JPG" : [ "JPG file", "*.jpg"],
                       "   JPEG" : [ "JPEG file", "*.jpeg"] }
    
    # Formate to which we have to convert
    convert_to = file_types[convert_to]

    # Checking Entrybox
    if( values[0][-3:] == convert_to[1][2:] ) :

        # Error due to converting to same formate
        mistake("SAME FORMATE")

    elif ( values[0] != "" ) and convert_to :

        # Converting pdf files
        if ( values[0][-3:] == 'pdf' ) :

            # Finding address to save file
            dirc = filedialog.askdirectory( initialdir = os.getcwd(), title = "Save file")

            # Poppler's Path
            poppler_path = os.path.join( os.getcwd(), r"poppler-23.01.0\Library\bin")

            # Processing page(s) of pdf
            pages = convert_from_path( pdf_path = values[0], poppler_path = poppler_path )

            # Getting into page(s) of pdf
            for page in pages :
                
                file = datetime.now().strftime('%Y%m%d%H%M%S')
                file = dirc + '/' + str(file) + convert_to[1][1:]
                page.save(  Path(file), convert_to[1][2:])

        # Converting to pdf formate
        elif ( convert_to[1][2:] == "pdf" ) :

            # Finding address to save file
            file = filedialog.asksaveasfile( initialdir = os.getcwd(), 
                                                title = "Save file",
                                                    defaultextension = f"{convert_to[1]}",
                                                        filetypes =[( convert_to[0], f"{convert_to[1]}" )] )

            # Saving file
            let = Image.open( values[0] )
            to_pdf = let.convert('RGB')
            to_pdf.save( file.name )
            file.close()
        
        # For other types of formate conversion
        else :

            # Finding address to save file
            file = filedialog.asksaveasfile( initialdir = os.getcwd(), title = "Save file",
                                                defaultextension = f"{convert_to[1]}",
                                                    filetypes =[( convert_to[0], f"{convert_to[1]}" )] )

            # Saving file
            values[1] = cv2.imread( values[0] )
            cv2.imwrite( file.name, values[1])
            file.close()
        
        # Clearing previously processed data
        values[0] = ""
        values[1] = np.array([0,0,0])

        # Message of complition and return back
        inform( "FILE SAVED" )
        change( can, menuPage)

    else :

        # Showing error due empty credientials
        mistake( "ENTER FILE NAME!" )

def removeBackground( click ) :

    # Removing the background of given Image
    
    # Checking entry
    if values[0] == "" :

        # Showing error due to empty credientials
        mistake( "FILE NOT FOUND!")

    else :

        # Removing the background of the Image
        original = cv2.imread( values[0] )
        values[1] = remove(original)
        values[0] = ""

        # Disabling the button after removing 
        click.configure( state = DISABLED)

def savingFile( can ) :

    # Saving the file to a particular address
    if values[1].any() != 0 :

        # Finding address to save file
        file = filedialog.asksaveasfile( initialdir = os.getcwd(), title = "Save file",
                                            defaultextension = "*.png",
                                                filetypes = [( "PNG file", "*.png"), ( "JPG file", "*.jpg")] )

        # Saving file
        cv2.imwrite( file.name, values[1])
        values[1] = np.array([0,0,0])
        file.close()

        # Showing message of complition and returning back
        inform( "FILE SAVED" )
        change( can, menuPage)

    else :

        # Showing error due to empty credientials
        mistake( "ENTER FILE NAME!" )

def openingFolder( folder_path ) :

    # Opening Folder using filedialog
    if ( folder_path.get() != "" ) :

        # Getting path of folder from entry box
        open_folder = folder_path.get()

    else :

        # Getting path of folder from dialog
        open_folder = filedialog.askdirectory( initialdir = os.getcwd() ,title = "Browse Folder")

    # Checking for empty address
    if ( open_folder != "" ) :

        values[2] = open_folder

        if ( folder_path.get() != "" ) :
            folder_path.delete( 0, END)
        
        folder_path.insert( 0, open_folder )

    else :

        # Showing error due to empty credientials
        mistake( "FIELD EMPTY!" )

def openingFolder2( folder_path ) :

    # Opening Folder using filedialog
    if ( folder_path.get() != "" ) :

        # Getting path of folder from entry box
        open_folder = folder_path.get()

    else :

        # Getting path of folder from dialog
        open_folder = filedialog.askdirectory( initialdir = os.getcwd(), title = "Browse Folder")

    # Checking for empty address
    if ( open_folder != "" ) :

        values[4] = open_folder

        if ( folder_path.get() != "" ) :
            folder_path.delete( 0, END)
        
        folder_path.insert( 0, open_folder )

    else :

        # Showing error due to empty credientials
        mistake( "FIELD EMPTY!" )

def openingFile( file_path, file_formate ) :

    # Opening File
    if ( file_path.get() != "" ) :

        # Getting path of file from entry box
        open_file = file_path.get()

    else :

        # Getting path of file from filedialog
        open_file = filedialog.askopenfilename( initialdir = os.getcwd(), title = "Open file", filetypes = file_formate )

    # Checking for empty address
    if ( open_file != "" ) :
    
        values[0] = open_file

        if ( file_path.get() != "" ) :
            file_path.delete( 0, END)
        
        file_path.insert( 0, open_file )
       
    else :

        # Showing error due to empty credientials
        mistake( "FIELD EMPTY!" )

def checkLogin( can, page, user, pwrd ) :

    # Checking the login credientials
    if ( user.get() != "" and pwrd.get() != "" ) :

        if ( user.get() == "JustFunfact" and pwrd.get() == "star is burning" ) :

            # Login, same entry found
            change( can, page )
        
        else :

            # Showing error due to no match
            mistake("ENTRY DOESN'T MATCH")

    else :

        # Showing error due to empty credientials
        mistake( "EMPTY FIELDS")

# Designing pages of respective functionality
def clearBack() :

    # Image Background removing 

    # Defining Structure
    third_page = Canvas( root, 
                          width = wid, height = hgt, 
                           bg = "black", highlightcolor = "#3c5390", 
                            borderwidth = 0 )
    third_page.pack( fill = "both", expand = True )

    # Background Image
    back_image = Imgo( os.path.join( os.getcwd(), "Background\Clear_Back_Page.jpg" ), 1498, 875)
    third_page.create_image( 0, 0, image = back_image , anchor = "nw")

    # Heading
    third_page.create_text( 500, 120, text = "Remove Background", 
                             font = ( ft[0], 45, "bold"), fill = "#1c54df" )

    # Return Button
    ret = Imgo( os.path.join( os.getcwd(), r'Design\arrow.png' ), 45, 35)
    ret_bt = ctk.CTkButton( master = root, image = ret, text = None, 
                             width = 60, height = 40, corner_radius = 23,
                              bg_color = "#d3eafc", fg_color = "red", 
                               hover_color = "#ff5359", border_width = 0,
                                command = lambda : change( third_page, menuPage) )
    ret_bt_win = third_page.create_window( 30, 20, anchor = "nw", window = ret_bt )

    # Accessing the file
    file_path = ctk.CTkEntry( master = root, 
                                placeholder_text = "Enter Path", text_font = ( ft[4], 20 ), 
                                 width = 580, height = 30, corner_radius = 14,
                                  placeholder_text_color = "#494949", text_color = "#242424", 
                                   fg_color = "#c3c3c3", bg_color = "#d3eafc", 
                                    border_color = "white", border_width = 3)
    file_path_win = third_page.create_window( 125, 200, anchor = "nw", window = file_path )

    file_formate = [( "PNG file", "*.png"), ( "JPG file", "*.jpg")]

    # Adding file path
    add_bt = ctk.CTkButton( master = root, 
                             text = "Add..", text_font = ( ft[1], 20 ), 
                              width = 60, height = 40, corner_radius = 14,
                               bg_color = "#d3eafc", fg_color = "red", text_color = "white", 
                                hover_color = "#ff5359", border_width = 0,
                                 command = lambda : openingFile( file_path, file_formate) )
    add_bt_win = third_page.create_window( 860, 200-2, anchor = "nw", window = add_bt )

    #Design to display 
    img_to_rem = Imgo( os.path.join( os.getcwd(), 'Design\Clear_back_design.png' ), 370, 370)
    third_page.create_image( 600-20, 350, image = img_to_rem , anchor = "nw")

    # Background removing button
    rem_bt = ctk.CTkButton( master = root, 
                             text = "Remove", text_font = ( ft[4], 25 ), 
                              width = 170, height = 50, corner_radius = 14,
                               bg_color = "#98e2fe", fg_color = "red", text_color = "white", 
                                hover_color = "#ff5359", border_width = 0,
                                text_color_disabled = "#a4a4a4",
                                 command = lambda : removeBackground(rem_bt) )
    rem_bt_win = third_page.create_window( 300, 500, anchor = "nw", window = rem_bt )

    # Saving Image button
    save_bt = ctk.CTkButton( master = root, 
                             text = "Save Image", text_font = ( ft[4], 25 ), 
                              width = 220, height = 50, corner_radius = 14,
                               bg_color = "#98e2fe", fg_color = "red", text_color = "white", 
                                hover_color = "#ff5359", border_width = 0,
                                 command = lambda : savingFile( third_page) )
    save_bt_win = third_page.create_window( 1000, 500, anchor = "nw", window = save_bt )

    root.mainloop()

def convertImage() :

     # Defining Structure
    fourth_page = Canvas( root, 
                           width = wid, height = hgt, 
                            bg = "black", highlightcolor = "#3c5390", 
                             borderwidth = 0 )
    fourth_page.pack( fill = "both", expand = True )

    # Background Image
    back_image = Imgo( os.path.join( os.getcwd(), "Background\Convert_Img_Page.jpg" ), 1498, 875)
    fourth_page.create_image( 0, 0, image = back_image , anchor = "nw")

    # Heading
    fourth_page.create_text( 500, 120, text = "Convert Images", 
                                font = ( ft[0], 45, "bold" ), fill = "#1c54df" )

    # Return Button
    ret = Imgo( os.path.join( os.getcwd(), r'Design\arrow.png' ), 45, 35)
    ret_bt = ctk.CTkButton( master = root, 
                             image = ret, text = None, 
                              width = 60, height = 40, corner_radius = 23,
                               bg_color = "#d3eafc", fg_color = "red", 
                                hover_color = "#ff5359", border_width = 0,
                                 command = lambda : change( fourth_page, menuPage) )
    ret_bt_win = fourth_page.create_window( 30, 20, anchor = "nw", window = ret_bt )

    # Accessing the file
    file_path = ctk.CTkEntry( master = root, 
                                placeholder_text = "Enter Path", text_font = ( ft[4], 20 ), 
                                 width = 580, height = 30, corner_radius = 14,
                                  placeholder_text_color = "#494949", text_color = "#242424", 
                                   fg_color = "#c3c3c3", bg_color = "#d3eafc", 
                                    border_color = "white", border_width = 3)
    file_path_win = fourth_page.create_window( 300, 210, anchor = "nw", window = file_path )

    file_formate = [( "PNG file", "*.png"), ( "JPG file", "*.jpg"), ( "JPEG file", "*.jpeg"), ( "PDF file", "*.pdf") ]

    # Adding file path
    add_bt = ctk.CTkButton( master = root, 
                             text = "Add..", text_font = ( ft[1], 20 ), 
                              width = 60, height = 40, corner_radius = 14,
                               bg_color = "#d3eafc", fg_color = "red", text_color = "white", 
                                hover_color = "#ff5359", border_width = 0,
                                 command = lambda : openingFile( file_path, file_formate) )
    add_bt_win = fourth_page.create_window( 1035, 210-2, anchor = "nw", window = add_bt )

    #Design to display 
    img_to_con = Imgo( os.path.join( os.getcwd(), "Design\Convert_img_design.png" ), 390, 390)
    fourth_page.create_image( 600-50, 350, image = img_to_con , anchor = "nw")

    # Option menu
    opt = ctk.StringVar(value = "Select Type " )
    com = ctk.CTkOptionMenu( master = root, variable = opt,
                              values = [ "   PDF", "   PNG", "   JPG", "   JPEG"],
                               text_font = ( ft[4], 20),
                                width = 170, height = 40, corner_radius = 15,
                                 bg_color = "#9ae2fe", fg_color = "red", text_color = "white",
                                  button_color = "#363fc8", button_hover_color = "#676fe8",
                                   dropdown_color = "#ff6c3d", dropdown_hover_color = "red", 
                                    dropdown_text_color = "white", dropdown_text_font = ( ft[4], 16),
                                     dynamic_resizing = True )
    # com.set("Select File")
    com_win = fourth_page.create_window( 1000, 400, anchor = "nw", window = com )

    # Saving Image button
    save_bt = ctk.CTkButton( master = root, 
                             text = "Save Image", text_font = ( ft[4], 22 ), 
                              width = 200, height = 40, corner_radius = 14,
                               bg_color = "#98e2fe", fg_color = "red", text_color = "white", 
                                hover_color = "#ff5359", border_width = 0,
                                 command = lambda : convertFile( fourth_page, com) )
    save_bt_win = fourth_page.create_window( 1005, 620, anchor = "nw", window = save_bt )

    root.mainloop()

def findImage() :

     # Defining Structure
    fifth_page = Canvas( root, width = 
                          wid, height = hgt, 
                           bg = "black", highlightcolor = "#3c5390", 
                            borderwidth = 0 )
    fifth_page.pack( fill = "both", expand = True )

    # Background Image
    back_image = Imgo( os.path.join( os.getcwd(), "Background\Find_Img_Page.jpg" ), 1498, 875)
    fifth_page.create_image( 0, 0, image = back_image , anchor = "nw")

    # Heading
    fifth_page.create_text( 400, 120, text = "Find Image", font = ( ft[0], 45, "bold" ), fill = "#1c54df" )

    # Return Button
    ret = Imgo( os.path.join( os.getcwd(), r'Design\arrow.png' ), 45, 35 )
    ret_bt = ctk.CTkButton( master = root, 
                             image = ret, text = None, 
                              width = 60, height = 40, corner_radius = 23,
                               bg_color = "#d3eafc", fg_color = "red", 
                                hover_color = "#ff5359", border_width = 0, 
                                 command = lambda : change( fifth_page, menuPage) )
    ret_bt_win = fifth_page.create_window( 30, 20, anchor = "nw", window = ret_bt )

    # Accessing the image
    file_path = ctk.CTkEntry( master = root, 
                                placeholder_text = "Enter Image Path", text_font = ( ft[4], 20 ), 
                                 width = 603, height = 30, corner_radius = 14,
                                  placeholder_text_color = "#494949", text_color = "#242424", 
                                   fg_color = "#c3c3c3", bg_color = "#d3eafc", 
                                    border_color = "white", border_width = 3)
    file_path_win = fifth_page.create_window( 300, 210, anchor = "nw", window = file_path )

    file_formate = [( "PNG file", "*.png"), ( "JPG file", "*.jpg") ]

    # Adding image path
    add_bt = ctk.CTkButton( master = root, 
                             text = "Add..", text_font = ( ft[1], 20 ), 
                              width = 60, height = 40, corner_radius = 14,
                               bg_color = "#d3eafc", fg_color = "red", text_color = "white", 
                                hover_color = "#ff5359", border_width = 0,
                                 command = lambda : openingFile( file_path, file_formate) )
    add_bt_win = fifth_page.create_window( 1065, 210-2, anchor = "nw", window = add_bt )

    # Accessing the folder
    folder_path = ctk.CTkEntry( master = root, 
                                 placeholder_text = "Enter Folder Path", text_font = ( ft[4], 20 ), 
                                  width = 580, height = 30, corner_radius = 14,
                                   placeholder_text_color = "#494949", text_color = "#242424", 
                                    fg_color = "#c3c3c3", bg_color = "#d3eafc", 
                                     border_color = "white", border_width = 3)
    folder_path_win = fifth_page.create_window( 300, 295, anchor = "nw", window = folder_path )

    # Browse folder button
    browse_bt = ctk.CTkButton( master = root, 
                                text = "Browse", text_font = ( ft[1], 20 ), 
                                  width = 100, height = 40, corner_radius = 14,
                                   bg_color = "#d3eafc", fg_color = "red", text_color = "white", 
                                    hover_color = "#ff5359", border_width = 0,
                                     command = lambda : openingFolder( folder_path ) )
    browse_bt_win = fifth_page.create_window( 1035, 295-2, anchor = "nw", window = browse_bt )

    # Frame
    mess = ctk.CTkFrame( master = fifth_page, 
                          width = 780, height = 300, corner_radius = 30,
                           bg_color = "#d5eafd", fg_color = "#97e1fe",
                            border_color = "#4d89eb", border_width = 6)
    mess.place_configure( x = 280, y = 480, anchor = "nw")

    # Label in frame
    frm_label = ctk.CTkLabel( master = mess, 
                                text = "Insert Values", text_font = (ft[0], 45, "bold"),
                                 width = 200, height = 50, corner_radius = 15,
                                  bg_color = "#97e1fe", fg_color = "#97e1fe", text_color = "#1c54df"  )
    frm_label.place_configure( x = 220, y = 120, anchor = "nw" )

    # Image Finding button
    find_bt = ctk.CTkButton( master = root, 
                                text = "Find", text_font = ( ft[1], 24 ), 
                                  width = 160, height = 45, corner_radius = 14,
                                   bg_color = "#d3eafc", fg_color = "red", text_color = "white", 
                                    hover_color = "#ff5359", border_width = 0,
                                     command = lambda : findingImages( frm_label ) )
    find_bt_win = fifth_page.create_window( 650, 400, anchor = "nw", window = find_bt )

    root.mainloop()

def sortImage() :

     # Defining Structure
    sixth_page = Canvas( root, 
                          width = wid, height = hgt, 
                           bg = "black", highlightcolor = "#3c5390", 
                            borderwidth = 0 )
    sixth_page.pack( fill = "both", expand = True )

    # Background Image
    back_image = Imgo( os.path.join( os.getcwd(), "Background\Sort_Image_Page.jpg" ), 1498, 875)
    sixth_page.create_image( 0, 0, image = back_image , anchor = "nw")

    # Heading
    sixth_page.create_text( 400, 120, text = "Sort Images", 
                                font = ( ft[0], 45, "bold" ), fill = "#1c54df" )

    # Return Button
    ret = Imgo( os.path.join( os.getcwd(), r'Design\arrow.png' ), 45, 35)
    ret_bt = ctk.CTkButton( master = root, 
                             image = ret, text = None, 
                              width = 60, height = 40, corner_radius = 23,
                               bg_color = "#d3eafc", fg_color = "red", 
                                hover_color = "#ff5359", border_width = 0, 
                                 command = lambda : change( sixth_page, menuPage) )
    ret_bt_win = sixth_page.create_window( 30, 20, anchor = "nw", window = ret_bt )

    # Accessing the folder1
    folder1_path = ctk.CTkEntry( master = root, 
                                  placeholder_text = "Enter Folder 1 Path", text_font = ( ft[4], 20 ), 
                                   width = 580, height = 30, corner_radius = 14,
                                    placeholder_text_color = "#494949", text_color = "#242424", 
                                     fg_color = "#c3c3c3", bg_color = "#d3eafc", 
                                      border_color = "white", border_width = 3)
    folder1_path_win = sixth_page.create_window( 300, 210, anchor = "nw", window = folder1_path )

    # Browse folde1 button
    browse_bt_1 = ctk.CTkButton( master = root, 
                                  text = "Browse", text_font = ( ft[1], 20 ), 
                                    width = 100, height = 40, corner_radius = 14,
                                     bg_color = "#d3eafc", fg_color = "red", text_color = "white", 
                                      hover_color = "#ff5359", border_width = 0,
                                       command = lambda : openingFolder( folder1_path ) )
    browse_bt_1_win = sixth_page.create_window( 1035, 210-2, anchor = "nw", window = browse_bt_1 )

    # Accessing the folder2
    folder2_path = ctk.CTkEntry( master = root, 
                                  placeholder_text = "Enter Folder 2 Path", text_font = ( ft[4], 20 ), 
                                   width = 580, height = 30, corner_radius = 14,
                                    placeholder_text_color = "#494949", text_color = "#242424", 
                                     fg_color = "#c3c3c3", bg_color = "#d3eafc", 
                                      border_color = "white", border_width = 3)
    folder2_path_win = sixth_page.create_window( 300, 295, anchor = "nw", window = folder2_path )

    # Browse folder2 button
    browse_bt_2 = ctk.CTkButton( master = root, 
                                  text = "Browse", text_font = ( ft[1], 20 ), 
                                    width = 100, height = 40, corner_radius = 14,
                                     bg_color = "#d3eafc", fg_color = "red", text_color = "white", 
                                      hover_color = "#ff5359", border_width = 0,
                                       command = lambda : openingFolder2( folder2_path ) )
    browse_bt_2_win = sixth_page.create_window( 1035, 295-2, anchor = "nw", window = browse_bt_2 )

    # Sorting button
    sort_bt = ctk.CTkButton( master = root, 
                                text = "Start Sorting", text_font = ( ft[0], 24 ), 
                                  width = 250, height = 45, corner_radius = 14,
                                   bg_color = "#99e2fe", fg_color = "red", text_color = "white", 
                                    hover_color = "#ff5359", border_width = 0,
                                     command = lambda : sortingImages() )
    sort_bt_win = sixth_page.create_window( 610, 540, anchor = "nw", window = sort_bt )

    root.mainloop()

def menuPage() :

    # Defining Structure
    second_page = Canvas( root, 
                           width = wid, height = hgt, 
                            bg = "black", highlightcolor = "#3c5390", 
                             borderwidth = 0 )
    second_page.pack( fill = "both", expand = True )

    # Background Image
    back_image = Imgo( os.path.join( os.getcwd(), "Background\Menu_Page.jpg" ), 1498, 875)
    second_page.create_image( 0, 0, image = back_image , anchor = "nw")

    # Heading
    second_page.create_text( 350, 120, text = "Content...", 
                                font = ( ft[0], 45, "bold" ), fill = "#1c54df" )

    # Back Ground remover page window
    backRem = Imgo( os.path.join( os.getcwd(), "Design\Clear_Back_logo.png" ), 220, 200 )
    backRem_bt = ctk.CTkButton( master = root, 
                                 image = backRem, compound = "top", 
                                  text = "Clear Back", text_font = ( ft[0], 22, "bold" ), 
                                   text_color = "white",
                                    width = 230, height = 240, corner_radius = 10, 
                                     bg_color = "#d3eafc", fg_color = "#2d435b", 
                                      hover_color = "#fdbf38", border_width = 0, 
                                       command = lambda : change( second_page, clearBack ))
    backRem_bt_win = second_page.create_window( 190, 250, anchor = "nw", window = backRem_bt)

    # Image converter page window
    imgConvert = Imgo( os.path.join( os.getcwd(), "Design\Convert_Img_logo.png" ), 220, 200 )
    imgConvert_bt = ctk.CTkButton( master = root, 
                                    image = imgConvert, compound = "top",
                                     text = "Converter", text_font = ( ft[0], 22, "bold" ),
                                      text_color = "white",
                                       width = 230, height = 240, corner_radius = 10, 
                                        bg_color = "#d3eafc", fg_color = "#2d435b", 
                                         hover_color = "#fdbf38", border_width = 0, 
                                          command = lambda : change( second_page, convertImage ))
    imgConvert_bt_win = second_page.create_window( 500, 400, anchor = "nw", window = imgConvert_bt )

    # Search image page window
    findImg = Imgo( os.path.join( os.getcwd(), "Design\Find_Img_logo.png" ), 220, 200 )
    findImg_bt = ctk.CTkButton( master = root, 
                                 image = findImg, compound = "top", 
                                  text = "Find Image", text_font = ( ft[0], 22, "bold" ),
                                   text_color = "white",
                                    width = 230, height = 240, corner_radius = 10,
                                     bg_color = "#d3eafc", fg_color = "#2d435b",   
                                      hover_color = "#fdbf38", border_width = 0,
                                       command = lambda : change( second_page, findImage ))
    findImg_bt_win = second_page.create_window( 810, 250, anchor = "nw", window = findImg_bt )

    # Sort image page window
    imgSort =Imgo( os.path.join( os.getcwd(), "Design\Sort_Img_logo.png" ), 220, 200 )
    imgSort_bt = ctk.CTkButton( master = root, 
                                 image = imgSort, compound = "top", 
                                  text = "Sort Images", text_font = ( ft[0], 22, "bold" ), 
                                   text_color = "white",
                                    width = 230, height = 240, corner_radius = 10,
                                     bg_color = "#d3eafc", fg_color = "#2d435b",
                                      hover_color = "#fdbf38",  border_width = 0,
                                       command = lambda : change( second_page, sortImage ))
    imgSort_bt_win = second_page.create_window( 1120, 400, anchor = "nw", window = imgSort_bt )

    # Logout button
    log = Imgo( os.path.join( os.getcwd(), "Design\logout.png" ), 35, 35 )
    log_bt = ctk.CTkButton( master = root, 
                             image = log, text = None, 
                              width = 45, height = 45, corner_radius = 23, 
                               bg_color = "#357adf", fg_color = "red", 
                                hover_color = "#ff5359", border_width = 0, 
                                 command = lambda : change( second_page, loginPage ))
    log_bt_win = second_page.create_window( 1420, 20, anchor = "nw", window = log_bt )

    root.mainloop()

def loginPage() :

    global user, pwrd, first_page

    # Defining Structure
    first_page = Canvas( root, 
                          width = wid, height = hgt, 
                           bg = "black", highlightcolor = "#3c5390", 
                            borderwidth = 0 )
    first_page.pack( fill = "both", expand = True )

    # Background Image
    back_image = Imgo( os.path.join( os.getcwd(), "Background\Login_Page.jpg" ), 1498, 875)
    design_image = Imgo( os.path.join( os.getcwd(), "Design\Login_Design.png" ), 600, 400)
    first_page.create_image( 0, 0, image = back_image , anchor = "nw")
    first_page.create_image( 350, 325, image = design_image, anchor = "nw")

    # Heading
    first_page.create_text( 450, 150, text = "Image Sorter", 
                                font = ( ft[0], 45, "bold" ), fill = "#1c54df" )
    first_page.create_text( 1150, 380, text = "Welcome\n    Back", 
                                font = ( ft[0], 26, "bold" ), fill = "#0b4bf5" )

    # Entry of username and password
    user = ctk.CTkEntry( master = root, 
                          placeholder_text = "Username", text_font = ( ft[1], 20 ), 
                           width = 220, height = 30, corner_radius = 14,
                            placeholder_text_color = "#666666", text_color = "#191919", 
                             fg_color = "#e1f5ff", bg_color = "#9ae2fe", 
                              border_color = "white", border_width = 3)
    user_win = first_page.create_window( 1015, 470, anchor = "nw", window = user )

    pwrd = ctk.CTkEntry( master = root, 
                          placeholder_text = "Password", text_font = ( ft[1], 20 ), 
                           width = 220, height = 30, corner_radius = 14,
                            placeholder_text_color = "#666666", text_color = "#191919", 
                             fg_color = "#e1f5ff", bg_color = "#9ae2fe", 
                              border_color = "white", border_width = 3, show = "*" )
    pwrd_win = first_page.create_window( 1015, 550, anchor = "nw", window = pwrd )

    # Login button
    log_bt = ctk.CTkButton( master = root, 
                             text = "Login", text_font = ( ft[0], 22 ), 
                              text_color = "white", 
                               width = 50, height = 25, corner_radius = 15, 
                                bg_color = "#9ae2fe", fg_color = "red", 
                                 hover_color = "#ff5359", border_width = 0, 
                                  command = lambda : checkLogin( first_page, menuPage, user, pwrd ))
    log_bt_win = first_page.create_window( 1090, 650, anchor = "nw", window = log_bt )

    root.mainloop()

if __name__  == "__main__" :

    # Defining Main theme of all widgets
    ctk.set_appearance_mode( "dark" )
    ctk.set_default_color_theme( "dark-blue" )
    wid = 1200
    hgt = 700

    global root

    root = ctk.CTk()
    root.title( "Image Sorter" )
    root.iconbitmap( os.path.join( os.getcwd(), "Design\Project_Icon.ico" ))
    root.geometry( "1200x700+200+80" )
    root.resizable( False, False )
    ft = [ "Tahoma", "Seoge UI", "Heloia", "Book Antiqua", "Microsoft Sans Serif"]
    values = [ "", np.array([0,0,0]), "", np.array([0,0,0]), ""]
    matches = set()

    loginPage()