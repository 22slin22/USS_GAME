from tkinter import *

class Menu():
    def __init__(self, tk):
        self.tk = Tk()
        self.pad = 3
        self._geom = '1000x800+0+0'
        self.tk.geometry("{0}x{1}+0+0".format(self.tk.winfo_screenwidth() - self.pad, self.tk.winfo_screenheight() - self.pad))

        self.tk.mainloop()