from tkinter import *
from tkinter.messagebox import showerror

def centerWindow(root, w, h):
    #gets the width and height of the screen
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    #sets the cordinates of the window to be the middle of the screen
    x = int((ws/2) - (w/2))
    y = int((hs/2) - (h/2))
    root.geometry('{}x{}+{}+{}'.format(w, h, x, y))

def validate(char, entry_value):
    chars=entry_value[:-1] #Selects all the text in the textbox except the last character
    if (not char.isdigit() and not "." in char and not "-" in char) or ("." in chars and "." in char) or ("-" in chars and "-" in char):
        """if entered char is not a digit or is not "." or is not "-" then return false.
           If the entered char is "." and there is already a "." in text, return false"""
        return False
    else:
        return True

def ui():
    def showHelp():
        #Creates a window that goes on top of the main root and configures it
        root=Toplevel()
        root.title("Help")
        root.geometry("{}x{}".format(500,300))
        root.resizable(False, False)
        root.configure(background="#e3fdff")

        #Opens the file and reads from it and immediately closes
        file=open("help.txt","r")
        text=""
        text+=file.read()
        file.close()

        #Creates the label and sets the text to it
        helpLabel=Label(root, text=text, anchor="w", justify="left")
        helpLabel.pack(fill=X)
        helpLabel.configure(background="#e3fdff")

        quitButton=Button(root, text="Quit", command=root.destroy)
        quitButton.pack(fill=X, side=BOTTOM, pady=10)

        root.mainloop()

    def start():
        areaOpened=False
        totalArea=0
        i=0
        #a sub-routine inside a sub-routine allows for variables inside the main sub-routine to be
        #accessible within the sub-routine inside the main sub-routine
        def getArea():
            #Since these variables are not global, and are also not inside this sub-routine, they need to be set a nonlocal to allow to edit them
            nonlocal areaOpened, totalArea
            if not areaOpened:
                areaOpened=True
                root=Toplevel()
                centerWindow(root, 400,400)
                root.resizable(False, False)
                root.configure(background="#e3fdff")

                def closeWindow():
                    nonlocal areaOpened
                    areaOpened=False
                    root.destroy()

                #This allows me to set a custom sub-routine for when the window closes
                root.protocol("WM_DELETE_WINDOW", closeWindow)
                #It registers the validate sub-routine to allow me to use it inside some controls
                vcmd = (root.register(validate), '%S', '%P')

                def addArea( ):
                    nonlocal i, areaOpened, totalArea
                    areaOpened=False
                    i+=1
                    areaButton.configure(text="Get Area: "+str(i))
                    heightValue=0
                    lengthValue=0
                    if heightEntry.get()!="":
                        heightValue=float(heightEntry.get())
                    if lengthEntry.get()!="":
                        lengthValue=float(lengthEntry.get())
                    #Ensures if the input in inside the range
                    if heightValue < 2 or heightValue > 6:
                        showerror("Error","Height has to be between 2 and 6")
                        return
                    if lengthValue < 1 or lengthValue > 25:
                        showerror("Error","Length has to be between 1 and 25")
                        return
                    totalArea+=heightValue*lengthValue
                    totalAreaLabel.configure(text="Total Area: "+str(totalArea)+" m^2")
                    root.destroy()
                    #Only allows for 4 input windows
                    if i > 3:
                        areaButton.destroy()
                        finishButton.grid(in_=bottom, row=2, column=0)
                    else:
                        getArea()

                #Creates frames inside the window to help me create a good structure of the program
                topFrame=Frame(root)
                topFrame.pack(fill=X)
                topFrame.configure(bg="#e3fdff")
                Label(root, text="Total Area: "+str(totalArea)+"m^2", bg="#e3fdff").grid(row=0, column=0, in_=topFrame)

                bottomFrame=Frame(root)
                bottomFrame.pack(fill=X)
                bottomFrame.configure(bg="#e3fdff")

                Label(root, text="Height", bg="#e3fdff").grid(row=1, column=0, in_=bottomFrame)
                heightEntry=Entry(root, validate = 'key', validatecommand = vcmd)
                heightEntry.grid(row=1, column=1, in_=bottomFrame)

                Label(root, text="Length", bg="#e3fdff").grid(row=2, column=0, in_=bottomFrame)
                lengthEntry=Entry(root, validate = 'key', validatecommand = vcmd)
                lengthEntry.grid(row=2, column=1, in_=bottomFrame)


                Button(root, text="Complete", command=addArea).grid(row=3, column=0, in_=bottomFrame)

                root.mainloop()
            else:
                showerror("Error","Window already opened")

        def calculatePrice():
            totalCost=0
            undercoatCost=0
            undercoat=undercoatVar.get()
            paintType=selectPaintType.get()
            if paintType==0:
                totalCost=1.75*totalArea
            elif paintType==1:
                totalCost=1*totalArea
            elif paintType==2:
                totalCost=0.45*totalArea
            text=""

            if undercoat==1:
                undercoatCost=0.5*totalArea
                text=" | Total Cost without undercoat: £{:,.2f}".format(totalCost)
                undercoatCostLabel.configure(text="Undercoat Cost: £{:,.2f}".format(undercoatCost))
                undercoatCostLabel.pack(in_=textFrame, fill=X)
            else:
                undercoatCostLabel.pack_forget()


            totalCostLabel.configure(text="Total Cost: £{:,.2f}".format(totalCost+undercoatCost)+text)
            totalCostLabel.pack(in_=textFrame, fill=X)

        root=Toplevel()
        root.geometry("{}x{}".format(400,400))
        root.resizable(False, False)
        root.configure(background="#e3fdff")

        top=Frame(root)
        top.pack(side=TOP, fill=X)
        top.configure(background="#e3fdff")

        bottom=Frame(root)
        bottom.pack(fill=X)
        bottom.configure(background="#e3fdff")

        textFrame=Frame(root)
        textFrame.pack(fill=X)
        textFrame.configure(background="#e3fdff")

        totalAreaLabel=Label(root, text="Total Area: 0 m^2", bg="#e3fdff")
        totalAreaLabel.pack(in_=top)

        areaButton=Button(root, text="Get Area: 0", command=getArea)
        areaButton.pack(in_=top,fill=X, pady=5)

        selectPaintType=IntVar()
        lRadioButton=Radiobutton(root, text="Luxury", variable=selectPaintType, value=0, bg="#e3fdff", activebackground="#e3fdff")
        lRadioButton.grid(in_=bottom, row=0,column=0, padx=0)


        sRadioButton=Radiobutton(root, text="Standard", variable=selectPaintType, value=1, bg="#e3fdff", activebackground="#e3fdff")
        sRadioButton.grid(in_=bottom, row=0,column=1, padx=0)


        eRadioButton=Radiobutton(root, text="Economic", variable=selectPaintType, value=2, bg="#e3fdff", activebackground="#e3fdff")
        eRadioButton.grid(in_=bottom, row=0,column=2, padx=0)

        undercoatVar=IntVar()

        undercoatCheckbox=Checkbutton(root, text="Undercoat", variable=undercoatVar, bg="#e3fdff", activebackground="#e3fdff")
        undercoatCheckbox.grid(in_=bottom, row=1, column=1, padx=0)

        finishButton=Button(root, text="Finish", command=calculatePrice)

        undercoatCostLabel=Label(root, text="Undercoat Cost", anchor="w", bg="#e3fdff")

        totalCostLabel=Label(root, text="Total Cost", anchor="w", bg="#e3fdff")

        root.mainloop()


    root=Tk()
    root.title("Assignment 2")
    root.resizable(False, False)
    root.configure(background="#e3fdff")
    centerWindow(root, 800,450)

    helpButton=Button(root, text="Help", command=showHelp)
    helpButton.pack(fill=X, pady=10)

    startButton=Button(root, text="Start", command=start)
    startButton.pack(fill=X, pady=10)

    quitButton=Button(root, text="Quit", command=root.destroy)
    quitButton.pack(fill=X, side="bottom", pady=10)

    root.mainloop()

ui()
