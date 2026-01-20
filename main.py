import datetime as dt
import tkinter as tk
from datetime import datetime
from mainPrompt import MainPrompt
from helpers import helperFunctions
from alerts import Alert



class Finance_Automator_App:
    def __init__(self):
        self.root = self.createMainWindow()
        self.currentDay = dt.datetime.now()
        self.todayDay = self.currentDay.strftime("%A") #day as a string
        self.todayDate = self.currentDay.strftime("%D")#string in the format: mm/dd/yy
        self.todayDateObj = datetime.strptime(self.todayDate, "%m/%d/%y") #returns as a datetime object in the form yyyy-mm-dd 00:00:00 ---> used for comparison
        self.helpers = helperFunctions(self)
        self.alerts = Alert.getAllAlerts()
        self.checkAlerts = self.helpers.checkForNull()
        self.main_prompt = MainPrompt(self)

    def createMainWindow(self):
        root = tk.Tk()
        root.configure(bg='white')
        root.resizable(False, False)
        root.withdraw()
        self.setWindowOverride(root)
        root.update_idletasks() 
        window_width = root.winfo_reqwidth()
        window_height = root.winfo_reqheight()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.setWindowOverride(root, False)
        root.title("Log Hours")
        root.geometry("400x300")
        return root
    
    def setWindowOverride(self, window, value = True):
        if value:
            window.attributes('-topmost', value)
        else:
            window.attributes('-topmost', value)
            window.deiconify()

    def closeRoot(self, window):
        window.destroy()

    
    def run(self):
        self.root.mainloop()




if __name__ == "__main__":
    app = Finance_Automator_App()
    app.run()
