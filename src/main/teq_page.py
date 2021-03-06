import tkinter as tk
from tkinter import *
from console import *
import main_page as mp
import reports_page as rp
from login_page import *
from create_account_page import *
from agency_page import *
from file_upload_page import *
from delete_account_page import *

class TEQPage(tk.Frame):
    def __init__(self, parent, controller, name):
        self.cont = controller
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Hello " + name +
                         ". What would you like to do?")
        label.pack(side=TOP,fill=X)

        b1 = Button(self, text="Generate Reports", 
                    command=lambda: self.cont.set_page(rp.ReportsPage, name))
        b1.pack(side=TOP,fill=X)
        
        b2 = Button(self, text="Delete Account",
                    command=lambda: self.cont.set_page(DeleteAccountPage,name))
        b2.pack(side=TOP,fill=X)
        
        back = Button(self, text="Back",
                            command=lambda: self.cont.display(mp.MainPage))
        back.pack(side=TOP,fill=X)
