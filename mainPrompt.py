import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from excelWriter import WritingToExcel
from alerts import Alert

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")



class MainPrompt:
    def __init__(self, app):
        self.app = app #Everything in the financeAutomatorApp class (main.py file)
        self.frame = tk.Frame(app.root, bg = 'white')
        self.frame.pack(fill="both", expand=True)
        
        
        mainLabel = tk.Label(self.frame, text = "Do you need to log hours today?", font = ("Courier", 18), bg='white')
        mainLabel.pack(pady = 25)

        buttonContainer = tk.Frame(self.frame, bg = 'white')
        buttonContainer.pack(pady = 10)
        

        yesButton = tk.Button(buttonContainer, text = "yes", command = lambda: self.logTime(app.todayDateObj, app.todayDay, self.frame), font = ("Courier", 14), highlightbackground='white') #app._____ references attributes in the main.py init file
        yesButton.pack(side = tk.LEFT, padx = 5)
        

        noButton = tk.Button(buttonContainer, text = "No", command = lambda: self.zeroLog(self.frame), font = ("Courier", 14), highlightbackground='white')
        noButton.pack(side = tk.LEFT, padx = 5)

        otherLogButton = tk.Button(buttonContainer, text = "Log for previous day", command = lambda: self.otherLog(self.frame), font = ("Courier", 14), highlightbackground='white')
        otherLogButton.pack(side = tk.LEFT)
        self.alertFrame = None
        if (len(self.app.alerts) > 0):
            self.alertFrame = tk.Frame(app.root, bg = "white")
            self.alertFrame.pack(fill = 'both', expand = 'True', padx = 10, pady = 10)
            if len(self.app.alerts) == 1:
                alertNotif = "You have 1 alert"
            else:
                alertNotif = "!!You have " + str(len(self.app.alerts)) + " alerts!!"

            alertsLabel = tk.Label(self.alertFrame, text = alertNotif, font = ("Courier", 15, 'bold'), bg='white')
            alertsLabel.pack()
            viewAlerts = tk.Button(self.alertFrame, text = "View Alerts", command = lambda: self.alertView(self.frame, self.alertFrame), highlightbackground='white', font = ("Courier", 12, 'bold'))
            viewAlerts.pack()
            #print("we see it", self.app.alerts)

    
    def alertView(self, currentFrame, alertFrame):
        for widget in currentFrame.winfo_children():
            widget.destroy()
        for widget in alertFrame.winfo_children():
            widget.destroy()

        allAlerts = self.app.alerts

        print (allAlerts)

        viewAlertsTitle = tk.Label(currentFrame, text = "Alerts:", bg = 'white', font = ('Courier', 15, 'bold'))
        viewAlertsTitle.pack(pady = (20, 0))
        #Makes the scrollable frame
        scrollFrame = ScrollableFrame(alertFrame)
        scrollFrame.pack(fill="both", expand = True, padx=0, pady=0)
        for alert in allAlerts:


            alertRow = alert.rowNum
            alertCol = alert.columnNum

            alertContainer = tk.Frame(scrollFrame.scrollable_frame, bg = 'white')
            alertContainer.pack(fill = 'x', padx = 20, pady = 10)
            linebreak = "--------------------------------------"
            lineBreaker = tk.Label(alertContainer, text = linebreak, font = ("Courier", 14), bg = 'white')
            lineBreaker.pack()
            alertWidget = tk.Label(alertContainer, text = alert.message, font = ("Courier", 12), bg = 'white')
            alertWidget.pack(pady =(0, 10))
            buttonContainerAlerts = tk.Frame(alertContainer, bg = 'white')
            buttonContainerAlerts.pack()
            alertYes = tk.Button(buttonContainerAlerts, text = "Yes", highlightbackground='white', command = lambda r = alertRow, c=alertCol: self.logAlertTime(r, c, True, currentFrame, alertFrame))
            alertYes.pack(side = tk.LEFT, padx = 10)
            alertNo = tk.Button(buttonContainerAlerts, text = "No", highlightbackground = 'white', command = lambda r = alertRow, c=alertCol: self.logAlertTime(alertRow, alertCol, False, currentFrame, alertFrame))
            alertNo.pack(side = tk.LEFT, padx = 10)
            print(alert.message)



    def on_finish(self, currentFrame, inputFrame, todayDateObj, todayDay, hourEnterS, minuteEnterS, hourEnterE, minuteEnterE, notZero = True):
            try: 
                hourEnterStart = int(hourEnterS.get())
                minuteEnterStart = int(minuteEnterS.get())
                hourEnterEnd = int(hourEnterE.get())
                minuteEnterEnd = int(minuteEnterE.get())
                print("got them")

                # if hourEnterStart or minuteEnterStart or hourEnterEnd or minuteEnterE == None:
                #     incompleteAlert = tk.Label(inputFrame, text = "Invalid. Please enter in the format #:##")
                #     incompleteAlert.pack()
            except:
                print("Exception Triggered")
                hourEnterStart = 0
                minuteEnterStart = 0
                hourEnterEnd = 0
                minuteEnterEnd = 0
            writer = WritingToExcel(self, hourEnterStart, minuteEnterStart, hourEnterEnd, minuteEnterEnd, todayDateObj, todayDay, currentFrame, inputFrame)
             #This is the call to actually write to the excel file
            WritingToExcel.writeToCell(hourEnterStart, hourEnterEnd, minuteEnterStart, minuteEnterEnd, self, currentFrame, inputFrame, fromInstance = True,
                                      helper = writer.helper, selectedDay = todayDay, dayObject = todayDateObj)

    def on_finishAlert(self, hourStart, minuteStart, hourEnd, minuteEnd, rowNum, colNum, mainFrame, currentFrame, enterTimeFrame):
        print("Alert response writing...")
        try: 
            hourEnterStart = int(hourStart.get())
            minuteEnterStart = int(minuteStart.get())
            hourEnterEnd = int(hourEnd.get())
            minuteEnterEnd = int(minuteEnd.get())
            print("got them")
        except:
            print("Exception Triggered")
            hourEnterStart = 0
            minuteEnterStart = 0
            hourEnterEnd = 0
            minuteEnterEnd = 0

        WritingToExcel.writeToCell(hourEnterStart, hourEnterEnd, minuteEnterStart, minuteEnterEnd, self, mainFrame, currentFrame, rowNum = rowNum, colNum = colNum, enterTimeFrame = enterTimeFrame, fromAlert = True)

        

    def logAlertTime(self, rowNum, colNum, isWriting, mainFrame, currentFrame):
        """creates the UI to input time in reaction to responding to an alert"""
        if isWriting:
            for widget in currentFrame.winfo_children():
                widget.destroy()
            for widget in mainFrame.winfo_children():
                widget.destroy()
            questionLog = tk.Label(mainFrame, text = "What are the hours you would like to log, Charlie?", 
                 font = ("Courier", 12), bg='white')
            questionLog.my_tag = "theq"
            questionLog.pack(pady = 10)

            enteringTime = tk.Frame(mainFrame, bg = 'white')
            enteringTime.pack()

            tk.Label(enteringTime, text ="Start", bg='white').grid(row = 0, column = 0)
            hourEnterS = tk.Entry(enteringTime, width = 2, highlightbackground='white')
            hourEnterS.grid(row = 1, column = 0)
            tk.Label(enteringTime, text = ":", bg='white').grid(row = 1, column = 2, padx = 1)
            minuteEnterS = tk.Entry(enteringTime, width = 2, highlightbackground='white')
            minuteEnterS.grid(row = 1, column = 3)
            
            tk.Label(enteringTime, text ="to", bg='white').grid(row = 1, column = 4)
            
            
            hourEnterE = tk.Entry(enteringTime, width = 2, highlightbackground='white')
            hourEnterE.grid(row = 1, column = 5)
            tk.Label(enteringTime, text = ":", bg='white').grid(row = 1, column = 6, padx = 1)
            minuteEnterE = tk.Entry(enteringTime, width = 2, highlightbackground='white')
            minuteEnterE.grid(row = 1, column = 7)
            tk.Label(enteringTime, text = "End", bg='white').grid(row = 0, column = 5)
            finishButton = tk.Button(enteringTime, text="Finish", highlightbackground='white', command= lambda: self.on_finishAlert(hourEnterS, minuteEnterS, hourEnterE, minuteEnterE, rowNum, colNum, mainFrame, currentFrame, enteringTime))
            finishButton.grid(row=2, column=0, columnspan=8, pady=10)

        else:
            self.on_finishAlert(0, 0, 0, 0, rowNum, colNum, mainFrame, currentFrame, None)

        for alert in Alert.alertList:
            if alert.rowNum == rowNum and alert.columnNum == colNum:
                Alert.alertList.remove(alert)
                break



            
        
        

    def logTime(self, todayDateObj, todayDay, currentFrame, alertsToClear = True):


        """logging time when 'yes' is clicked initially -- "what are the hours..." page"""
        for widget in currentFrame.winfo_children():
            widget.destroy()
        if alertsToClear and self.alertFrame:
            for widget in self.alertFrame.winfo_children(): ## CLEARED -->causes an error because it is expecting an alert
                widget.destroy()
            self.alertFrame.destroy()
        questionLog = tk.Label(currentFrame, text = "What are the hours you would like to log, Charlie?", 
                 font = ("Courier", 12), bg='white')
        questionLog.my_tag = "theq" ## Had to assign the tag in logtime as well... Doing so just in alert time and not in normal log brings up error that causes program to crash
        questionLog.pack(pady = 10)
        inputFrame = tk.Frame(currentFrame)
        inputFrame.configure(bg='white')
        inputFrame.pack(pady=5)

        tk.Label(inputFrame, text ="Start", bg='white').grid(row = 0, column = 0)
        hourEnterS = tk.Entry(inputFrame, width = 2, highlightbackground='white')
        hourEnterS.grid(row = 1, column = 0)
        tk.Label(inputFrame, text = ":", bg='white').grid(row = 1, column = 2, padx = 1)
        minuteEnterS = tk.Entry(inputFrame, width = 2, highlightbackground='white')
        minuteEnterS.grid(row = 1, column = 3)
        
        tk.Label(inputFrame, text ="to", bg='white').grid(row = 1, column = 4)
        
        
        hourEnterE = tk.Entry(inputFrame, width = 2, highlightbackground='white')
        hourEnterE.grid(row = 1, column = 5)
        tk.Label(inputFrame, text = ":", bg='white').grid(row = 1, column = 6, padx = 1)
        minuteEnterE = tk.Entry(inputFrame, width = 2, highlightbackground='white')
        minuteEnterE.grid(row = 1, column = 7)
        tk.Label(inputFrame, text = "End", bg='white').grid(row = 0, column = 5)

        

        #tk.Button(inputFrame, text="Back", command = main).pack()
        finishButton = tk.Button(inputFrame, text="Finish", highlightbackground='white', command= lambda: self.on_finish(currentFrame, inputFrame, todayDateObj, todayDay, hourEnterS, minuteEnterS, hourEnterE, minuteEnterE))
        finishButton.grid(row=2, column=0, columnspan=8, pady=10)
        backButton = tk.Button(inputFrame, text="Back", command=self.back)

    def back(self):
        pass





    def zeroLog(self, frame):
        """Simply logs 0 hours for the date"""
        self.on_finish(frame, tk.Frame(self.app.root), self.app.todayDateObj, self.app.todayDay, 0, 0, 0, 0, False)
        self.app.root.destroy()
        
        
        

    def otherLog(self, frame):
        """Promting the user to select a date from the Calendar GUI which can then be used to log hours for the selected date"""
        for widget in frame.winfo_children():
            widget.destroy()
        for widget in self.app.root.winfo_children():
            widget.destroy()

        self.frame = tk.Frame(self.app.root, bg = 'white')
        self.frame.pack()

        headerLabel = tk.Label(self.frame, text = "Please select the date for the entry.", font = ('Courier', 13), bg = 'white')
        headerLabel.pack(pady = 10)

        print("YERRRR")

        calSelect = Calendar(self.frame, selectmode = 'day', selectforeground = 'lightblue', selectbackground = 'red', foreground = 'black', background = 'white')
        calSelect.pack(pady = 10)
        close = tk.Button(self.frame, text = "close", highlightbackground= 'white', command = lambda: self.app.closeRoot(self.app.root)) #need to make a funtion in main.py called 'closeRoot()'
        close.pack()
        complete = tk.Button(self.frame, text = "select", highlightbackground= 'white', command = lambda: self.selectDateLog(calSelect, self.frame))
        complete.pack()
        
       



    def selectDateLog(self, selectedDateCal, frame): #Uses the calendar for the user to select the desired date

        """Pulls the selected Month/Day from calendar GUI and uses that data to log time into excel calendar"""
        selectedDateRaw = selectedDateCal.get_date()
        dateString1 = datetime.strptime(selectedDateRaw, "%m/%d/%y") 
        dateString = dateString1.strftime("%A, %D")
        selectedDay, selectedDate = dateString.split(", ") #string in form day, m/d/y
        selectedDateObj = datetime.strptime(selectedDate, "%m/%d/%y") #date time object in form m/d/y
        self.logTime(selectedDateObj, selectedDay, frame, alertsToClear = False)


    def resetUserInterface(self):
        for widget in self.app.root.winfo_children():
            widget.destroy()
    
        self.__init__(self.app)
    



    
    