from Tkinter import *
#import Tkinter 
import tkMessageBox as messagebox
import tkFileDialog as filedialog
from zipfile import ZipFile
from random import randint
from PIL import Image, ImageTk
import os
import sys
import math
import cv2
import compare_images_Levenshtein
import Apk2Png
import getOneMethod


path = os.getcwd()

def capDimensions(width, height, maxPixels):
    imageSize = int(math.ceil(math.sqrt(maxPixels)))
    return (imageSize, imageSize)

def getSimilars():
    import sys
    images = {}
  
    for file in os.listdir(path + "/imageDex/"):
        images[file]=Image.open(path + "/imageDex/" +file)
    
    j=0
    k=0
    results, i = {}, 1
    reportLabel = Label(top, text = "ATTENTION: Check these pairs", bg='red', fg = 'white', font = 'Helvetica 10 bold')
    reportLabel.place(x=470, y=200)
    for namea, imga in images.items():
        for nameb, imgb in images.items():

            if namea==nameb or nameb==namea in results:
                continue            
            cmp = compare_images_Levenshtein.FuzzyImageCompare(imga, imgb)
            sim = cmp.similarity()
            results[(namea, nameb)] = sim
            #print sim            
            if sim > 55.0:
                #namea = namea.split(".")[0]+".apk"
                #nameb = nameb.split(".")[0]+".apk"
                choices[k] = "Click here for details: "+namea.split(".")[0]+".apk" +" "+nameb.split(".")[0]+".apk"
                k+=1
            i += 1
    
    for key,value in choices.items():
         b = Radiobutton(top, text=value, bg='white', fg = 'black', activeforeground = '#262d2d', font = 'Helvetica 10', indicatoron = 0, width = 50, padx=20, variable=v, value=key, command = getApk)
         b.place(x=405, y=220+j)
         j+=20
    
def getApk():
    answer=v.get()
    apk1 = (choices[answer].split(" ")[4]).split(".")[0]+".apk"
    apk2 = (choices[answer].split(" ")[5]).split(".")[0]+".apk"
    compareApk(apk1, apk2)

def compareApk(file1, file2):
    #print file1, file2
    home = os.path.dirname(os.path.realpath(sys.argv[0]))
    app = Apk2Png.Apk2Png()
    app.check_tools(home)
    app.compare(file1, file2)
    app.getIdenticalMethods()
    app.getSimilarMethods()
    app.getNewMethods()
    app.getOriginalColors()
    app.getRepackedColors()
    #if 'R' in file1:
    imgO = (file1.split(".")[0]) + "_" + (file2.split(".")[0])+"_1"
    imgR = (file1.split(".")[0]) + "_" + (file2.split(".")[0])+"_2"
    #else:
    #imgO = file1.split(".")[0]+"_o"
    #imgR = (file2.split(".")[0]).replace("R","_")+"r"
    openInteractiveImage("image/",imgR)
    openSimpleImage("image/",imgO)
    
    os.chdir(path)
    print os.getcwd()
def openSimpleImage(folder, fileName):
    novi = Toplevel()
    novi.title(fileName)
    novi.geometry("%dx%d+%d+%d" % (500, 500, 150, 100))
    canvas = Canvas(novi, width = 500, height = 500)
    
    basewidth = 500
    img = Image.open(path+"/"+folder+fileName+".png")
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(path+"/"+folder+fileName+".png")
    
    imgCV = cv2.imread(path+"/"+folder+fileName+".png")
    gif1 = PhotoImage(file = path+"/"+folder+fileName+".png")
    canvas.create_image(0, 0, image = gif1, anchor = NW)
    canvas.gif1 = gif1
    canvas.pack(expand = YES, fill = BOTH)
    

def openInteractiveImage(folder, fileName):
    identical_methods = 0
    similar_methods = 0
    new_methods = 0
    
    file = (fileName.split("_"))[0] + "_" + (fileName.split("_"))[1]
    dex1= fileName.split("_")[0]
    dex2= fileName.split("_")[1]

    novi = Toplevel()
    novi.title(fileName)
    novi.geometry("%dx%d+%d+%d" % (500, 500, 670, 100))
    canvas = Canvas(novi, width = 500, height = 500)
    
    basewidth = 500
    img = Image.open(path+"/"+folder+fileName+".png")
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(path+"/"+folder+fileName+".png")
    
    imgCV = cv2.imread(path+"/"+folder+fileName+".png")
    gif1 = PhotoImage(file = path+"/"+folder+fileName+".png")
    canvas.create_image(0, 0, image = gif1, anchor = NW)
    canvas.gif1 = gif1

    label_legend = Label(canvas, text = "The green section represents identical methods\n The blue section represents similar methods\nThe red section represents new methods\nFor details on similar and new methods click on the respective sections.", font = 'Helvetica 9 bold', bg='#6e6c0f', fg='white')
    label_legend.place(x = 40, y = 5)
    
    #lettura report generale
    os.chdir(path+"/Report/")
    if os.path.exists(file+".txt"):
        f=open(file+".txt")
        for line in f:
            if "IDENTICAL:" in line:
                identical_methods = line.split("\t")[-1]
            if "SIMILAR:" in line:
                similar_methods = line.split("\t")[-1]
            if "NEW:" in line:
                new_methods = line.split("\t")[-1]
    
    def leftclick(event):
        print(imgCV[event.y, event.x]) 
        if(imgCV[event.y, event.x][2] <= 5):
            tmp = messagebox.askyesno("Continue?", "Do you want to start loading "+similar_methods+"similar methods?", parent = novi)           
            if tmp is True:            
		        os.chdir(path+"/Report/")
		        # frame to display method diff    
		        frame=Toplevel()
		        labelcanvas=Canvas(frame,bg='#FFFFFF',width=800,height=500,scrollregion=(0,0,6000,6000))
		        hbar=Scrollbar(frame,orient=HORIZONTAL)
		        hbar.pack(side=BOTTOM,fill=X)
		        hbar.config(command=labelcanvas.xview)
		        vbar=Scrollbar(frame,orient=VERTICAL)
		        vbar.pack(side=RIGHT,fill=Y)
		        vbar.config(command=labelcanvas.yview)
		        labelcanvas.config(width=800,height=500)
		        labelcanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
		        labelcanvas.pack(side=LEFT,expand=True,fill=BOTH)
		        canvas_id = labelcanvas.create_text(10, 10, anchor="nw")
		        if os.path.exists(file+"_s.txt"):
		            textLabel=''
		            with open(file+"_s.txt", 'r') as s_file:
		                data = s_file.readlines()                    
		                textLabel=''
		                for line in data:
		                    classNameO = line.split(" ")[0]
		                    methodNameO = line.split(" ")[1]
		                    classNameR = line.split(" ")[2]
		                    methodNameR = line.split(" ")[3]
		                    textLabel += classNameO+" "+methodNameO+" "+classNameR+" "+methodNameR+" \n"+getOneMethod.diffMethod(path+"/dex/"+dex1+".dex", path+"/dex/"+dex2+".dex", classNameO, methodNameO, classNameR, methodNameR)+"*********************************************************************************************\n"
		                    labelcanvas.itemconfig(canvas_id, text = textLabel)
            else:
                return False

        #else:
            #messagebox.showinfo("Information", identical_methods+" identical methods\nClick OK", parent = novi)
                        
        if(imgCV[event.y, event.x][0] <= 5):
            tmp = messagebox.askyesno("Continue?", "Do you want to start loading "+new_methods+"new methods?", parent = novi)
            if tmp is True:
		        os.chdir(path+"/Report/")
		        # frame to display method diff    
		        frame=Toplevel()
		        labelcanvas=Canvas(frame,bg='#FFFFFF',width=800,height=500,scrollregion=(0,0,6000,6000))
		        hbar=Scrollbar(frame,orient=HORIZONTAL)
		        hbar.pack(side=BOTTOM,fill=X)
		        hbar.config(command=labelcanvas.xview)
		        vbar=Scrollbar(frame,orient=VERTICAL)
		        vbar.pack(side=RIGHT,fill=Y)
		        vbar.config(command=labelcanvas.yview)
		        labelcanvas.config(width=800,height=500)
		        labelcanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
		        labelcanvas.pack(side=LEFT,expand=True,fill=BOTH)
		        canvas_id = labelcanvas.create_text(10, 10, anchor="nw")
		        if os.path.exists(file+"_n.txt"):
		            with open(file+"_n.txt", 'r') as n_file:
		                data = n_file.readlines()                    
		                textLabel=''
		                for line in data:
		                    line = line.split("\n")[0]
		                    classNameR = line.split(" ")[0]
		                    methodNameR = line.split(" ")[1]
		                    textLabel += classNameR+" "+methodNameR+" \n"+getOneMethod.getNewMethods(path+"/dex/"+dex2+".dex", classNameR, methodNameR)+"*********************************************************************************************\n"
		                    labelcanvas.itemconfig(canvas_id, text = textLabel)
            else:
                return False
        if(imgCV[event.y, event.x][2] != 0 and imgCV[event.y, event.x][0] > 5):
        #else:
            messagebox.showinfo("Information", identical_methods+"identical methods", parent = novi)
    
    canvas.bind("<Button-1>", leftclick)
    canvas.pack(expand = YES, fill = BOTH)

def compare2Apks():
    os.chdir(path)
    selected_apk1 = filedialog.askopenfilename()
    selected_apk2 = filedialog.askopenfilename()
    apk1= selected_apk1.split("/")[-1]
    apk2= selected_apk2.split("/")[-1]
    compareApk(apk1, apk2)

def choose_file():    
    selected_apk = filedialog.askopenfilename()
    zip_ref = ZipFile(selected_apk)
    selected_dex = selected_apk.split("/")[-1]
    selected_dex = selected_dex.split(".")[0]
    #selected_dex = selected_dex.split("_")[0] 
    if not os.path.exists(path+"/dex"):
        os.makedirs(path+"/dex")
    os.chdir(path+"/dex")
    zip_ref.extract('classes.dex')
    os.rename('classes.dex', selected_dex+'.dex')
    selected_dex = selected_dex+'.dex'
    
    with open(selected_dex, 'rb') as in_file:
        data=in_file.read()
        binaryValues=[]
        resultSet=[]
        index=0

        for byte in data:
            binaryValues.append(byte)

     
        while(index<len(binaryValues)):
            R= ord(binaryValues[index])
            G= ord(binaryValues[index])
            B= ord(binaryValues[index])
            index=index+1
            resultSet.append((R,G,B))
        
        num_pixels= index
        height= 1000
        width= 1000            
      
    image = Image.new('RGB', capDimensions(1000, 1000, num_pixels), "black")
    image.putdata(resultSet)
    
    print('Making image...')
    print('Saving image...')
    imgName = selected_dex.split("/")[-1]
    if not os.path.exists(path+"/imageDex"):
        os.makedirs(path+"/imageDex")
    image.save(path+"/imageDex/"+imgName+".png", "PNG")
    os.chdir(path)
    
    Result = Button(top, text = "Result", command = openSimpleImage("imageDex/",imgName))

top = Tk()
top.title("Apk Visualization")
top.configure(background='#262d2d')
top.geometry("%dx%d+%d+%d" % (1200, 600, 100, 100))
icona= PhotoImage(file= 'py.png')
top.tk.call("wm", "iconphoto", top._w,icona)

v = IntVar()
v.set(0)
choices = {}

img_visualize = PhotoImage(file = 'visualize.png')
img_similars = PhotoImage(file = 'view_similars.png')
img_compare = PhotoImage(file = 'compare.png')

visualize_label = Label(top, text = "Visualize APK\nConvert choosen APK in a greyscale image", bg='#262d2d', fg = 'white', font = 'Helvetica 10 bold')
visualize_label.place(x = 50, y = 120)
Visualize = Button(top, image = img_visualize, bg = 'white', bd = 0, command = choose_file)
Visualize.config(width='60', height='60')
Visualize.place(x = 160,y = 50)

similars_label = Label(top, text = "Get *similars APKs\nFrom a **set of APKs finds similar ones", bg='#262d2d', fg = 'white', font = 'Helvetica 10 bold')
similars_label.place(x = 450, y = 120)
nb_label2 = Label(top, text = "** The search for similar APKs is made on greyscale images obtained through \"Visualize APK\"", bg='#262d2d', fg = 'white', font = 'Helvetica 11 bold italic')
nb_label2.place(x = 58, y = 570)
Similars = Button(top, image = img_similars, bg = 'black', bd = 0, command = getSimilars)
Similars.config(width='59', height='60')
Similars.place(x = 535,y = 50)
nb_label1 = Label(top, text = "* Pairs of similar apk are obtained by considering both the comparison verses (e.g. Apk1-Apk2 and Apk2-Apk1)", bg='#262d2d', fg = 'white', font = 'Helvetica 11 bold italic')
nb_label1.place(x = 58, y = 545)
compare_label = Label(top, text = "Compare 2 APKs\nConvert the two selected APKs\ninto color images to simplify the display of differences", bg='#262d2d',fg = 'white', font = 'Helvetica 10 bold')
compare_label.place(x = 800, y = 120)
Compare = Button(top, image = img_compare, bg = 'black', bd = 0, command = compare2Apks)
Compare.config(width='60', height='60')
Compare.place(x = 935,y = 50)
#top.iconbitmap("py.png")
top.mainloop()





