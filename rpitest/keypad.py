import tkinter, tkinter.ttk as ttk
import random
from GPIO import GPIOon, GPIOoff
import time
import mysql.connector as mariadb
 
mariadb_connection = mariadb.connect(user='admin', password='pass', database='smart_lock')
cursor = mariadb_connection.cursor()

class FrameSize(tkinter.Tk):
    def Size(self):
        x, y = self.winfo_width(), self.winfo_height()
        self.minsize(x, y); self.maxsize(x, y)

    def Buttons(self, ButtonList, NewLine = 3):
        self.Row = 0
        self.Col = 0

        for Button in ButtonList:
            Button.grid(row = self.Row, column = self.Col)
            self.Col += 1

            if self.Col == NewLine:
                self.Row += 1
                self.Col = 0
                continue

class Box(FrameSize):
    def __init__(self, **args):
        super(Box, self).__init__()

        self.EntryFrame = ttk.Frame(self)
        self.PadFrame = ttk.Frame(self)

        self.EntryFrame.pack(padx = 5, pady = 5)
        self.PadFrame.pack(padx = 5, pady = 5)

        self.AllButtons = []
        self.CanWrite = True
        self.Code = 1111
        self.Timer = args.get("timer") or 2000

        

        for x in range(1, 10):
            self.AllButtons.append(ttk.Button(self.PadFrame, width = 4, text = x, command = lambda y = x: self.Update(y)))
            self.bind(str(x), lambda CatchEvent, y = x: self.Update(y))
        self.Buttons(self.AllButtons)

        self.ZeroButton = ttk.Button(self.PadFrame, width = 4, text = 0, command = lambda: self.Update(0))
        self.SubmitButton = ttk.Button(self.PadFrame, width = 4, text = "Ent", command = self.CheckCode)
        self.ClearButton = ttk.Button(self.PadFrame, width = 4, text = "C", command = lambda: self.Update(-1))

        self.ClearButton.grid(row = self.Row, column = 0)
        self.ZeroButton.grid(row = self.Row, column = 1)
        self.SubmitButton.grid(row = self.Row, column = 2)

        self.bind("0", lambda CatchEvent: self.Update(0))
        self.bind("<Return>", lambda CatchEvent: self.CheckCode())
        
        self.KeyEnter = ttk.Entry(self.EntryFrame, state = "disabled")
        self.KeyEnter.pack()

        self.after(5, self.Size)

    def Update(self, x):
        if self.CanWrite:
            self.KeyEnter["state"] = "normal"

            if x == -1:
                self.KeyEnter.delete(0, tkinter.END)
            else:
                self.KeyEnter.insert(tkinter.END, x)

            self.KeyEnter["state"] = "disabled"

    def CheckCode(self):
        Key = self.KeyEnter.get()
        self.Update(-1)
        measure1 = time.time()
        measure2 = time.time()
        count = 1
        if Key == str(self.Code):
            self.Update("Correct Pin")
            GPIOon()
            # while count < 11:
            #     if measure2 - measure1 >= 2:
            #         GPIOon()
            #         measure1 = measure2
            #         measure = time.time()
            #         count += 1
            #     else:
            #         measure2 = time.time()               
            
               
        else:
            self.Update("Incorrect Pin")

        self.ChangeWritePerms()
        self.after(self.Timer, self.ChangeWritePerms)

    def ChangeWritePerms(self):
        if self.CanWrite:
            self.CanWrite = False

        else:
            self.CanWrite = True
            self.Update(-1)
        

Box().mainloop()
            

























