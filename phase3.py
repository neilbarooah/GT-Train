import pymysql
from tkinter import *
from re import *
import datetime
import calendar


class Trains:

    def __init__(self):
        self.loginPage()
        #just put the below to test my page (FYI, totally the way to do it. super easy. yay)
        #self.chooseFunctionalityPage()
        
          
	
    #Connect to database
    def connect(self):
        try: 
        #USE THIS URL TO GET INTO DB: http://www.phpmyadmin.co/ 
            db = pymysql.connect(host = 'academic-mysql.cc.gatech.edu', db='cs4400_Team_9', user = 'cs4400_Team_9', passwd = '1anHU4fr')
      
        #pymysql.connect will return a connection to the database 
            return db
        except:
            messagebox.showerror(title='Error', message='Could not connect to database')
        
    #Disconnect from database
    def disconnect(self, db):
        db.commit()
        db.close()
            
    # Login
    def loginPage(self):
        self.winLogin = Tk()
        frame1 = Frame(self.winLogin, borderwidth=3, relief=RAISED)
        frame1.grid(row=0, column=0)

        #String variables to store written answers
        self.sv1 = StringVar()
        self.sv2 = StringVar()
        self.ticketsBooked = []
        
        #create username row
        LA = Label(frame1, text="Username")
        #LA.grid(row=1, column=0, STICKY=E) fix sticky
        LA.grid(row=1, column=0)
        self.usernameEntry = Entry(frame1, width=30, textvariable=self.sv1)
        self.usernameEntry.grid(row=1, column=1, padx=5, pady=5) 
        #create password row
        LB = Label(frame1, text="Password")
        #LB.grid(row=2, column=0, STICKY=E) gotta fix the sticky
        LB.grid(row=2, column=0)
        self.pswdEntry = Entry(frame1, width=30, textvariable=self.sv2)
        self.pswdEntry.grid(row=2, column=1, padx=5, pady=5)
        
        login = Button(frame1, text="Login", command=self.loginCheck)
        login.grid(row=3, column=0)
        
        register = Button(frame1, text="Register", command=self.toRegister)
        register.grid(row=3, column=1)
        
        self.winLogin.mainloop()
                            
    # UI screen for Registration
    def registrationPage(self):
        self.winRegistration = Tk()
        frame = Frame(self.winRegistration)
        frame.grid(row=0, column=0)
        
        sv3 = StringVar()
        sv4 = StringVar()

        L1 = Label(frame, text = "Username")
        L1.grid(row=1, column=0)
        self.usernameEntry = Entry(frame, width = 25, textvariable=self.sv1)
        self.usernameEntry.grid(row = 1, column = 1, padx=5, pady=5)


        L2 = Label(frame, text = "Email Address")
        L2.grid(row=2, column=0)
        self.emailEntry = Entry(frame, width = 25, textvariable=sv3)
        self.emailEntry.grid(row = 2, column = 1, padx=5, pady=5)
        
        L3 = Label(frame, text = "Password")
        L3.grid(row=3, column=0)
        self.pswdEntry = Entry(frame, width = 25, textvariable=self.sv2)
        self.pswdEntry.grid(row = 3, column = 1)

        
        L4 = Label(frame, text = "Confirm Password")
        L4.grid(row = 4, column = 0)
        self.confpwdEntry = Entry(frame, width = 25, textvariable = sv4)
        self.confpwdEntry.grid(row = 4, column = 1)

        
        create = Button(frame, text = "Create", command = self.registerCheck)
        create.grid(row = 5, column = 3)
        
        self.winRegistration.mainloop()

    def toLogin(self):
        self.winRegistration.withdraw()
        self.winLogin.deiconify()
        
    def createCallback(self):
    
        try:
            db = self.connect()
            cursor = db.cursor()

            add_user = "INSERT INTO USER (Username, Password) VALUES (%s, %s)"
            exe = cursor.execute(add_user, (self.usernameEntry.get(), self.pswdEntry.get()))
            c2 = db.cursor()
            add_customer = "INSERT INTO CUSTOMER (Username, Email) VALUES (%s, %s)"
            exe2 = c2.execute(add_customer, (self.usernameEntry.get(), self.emailEntry.get()))
            messagebox.showinfo("Registration Complete", "You have successfully registered")
            self.winRegistration.withdraw()
            self.winLogin.deiconify()
            cursor.close()
            c2.close()
            db.commit()
            self.toLogin()
        except:
            return
        #self.cursor.execute(add_user) incorrect syntax
        #self.disconnect() incorrect syntax
    
    #Check to see if login info exists in database
    def loginCheck(self):
        db = self.connect()
        c = db.cursor()
        usernames = "SELECT Username FROM USER"
        exe = c.execute(usernames)
        users = c.fetchall()
        passwords = "SELECT Password FROM USER"
        exe2 = c.execute(passwords)
        pswd = c.fetchall()
        managernames = "SELECT Username FROM MANAGER"
        exe3 = c.execute(managernames)
        managers = c.fetchall()
        flag = False
        for u in users:
            if str(u[0]) == self.usernameEntry.get():
                #check if the username is a manager. if yes, then check password and if correct, go to manager functionality page
                for m in managers:
                    if str(m[0]) == self.usernameEntry.get():
                        for p in pswd:
                            if str(p[0]) == self.pswdEntry.get():
                                messagebox.showinfo(title='Success!', message='You have successfully logged into sql3113465')
                                self.winLogin.withdraw()
                                flag = True
                                self.chooseManagerFunctionalityPage()
                #if we reach here, username is not a manager. check password and if correct, go to user functionality page
                for p in pswd:
                    if str(p[0]) == self.pswdEntry.get():
                        messagebox.showinfo(title='Success!', message='You have successfully logged into sql3113465')
                        self.winLogin.withdraw()
                        flag = True
                        self.chooseFunctionalityPage()
                        
        if flag == False: 
            #no match
            messagebox.showerror(title='Invalid', message='This is an invalid username/password combination')
            self.sv1.set("")
            self.sv2.set("")
        db.commit()
        c.close()
    
	#Switch screens from Login screen to Registration page
    def toRegister(self):
        self.winLogin.withdraw()
        self.registrationPage()

    def registerCheck(self):
        db = self.connect() 
        cursor = db.cursor()
        flag1 = True

        cursor.execute("SELECT Username FROM USER") 
        dbUsers = cursor.fetchall()
        
        for users in dbUsers:
            if users[0] == self.usernameEntry.get():
                flag1 = False
        if flag1 == False:
            messagebox.showerror(title='Already Exists', message='Username already exists in system')
            return
        
        if self.pswdEntry.get() != self.confpwdEntry.get():
            messagebox.showerror(title="Password Incorrect", message="Passwords do not match")
            return
        else:
            self.createCallback()
    
    #create UI for Choose Functionality Screen	
    def chooseFunctionalityPage(self):
        self.winChooseFunctionality = Tk()
        self.winChooseFunctionality.title("Choose Functionality")
        titleLabel = Label(self.winChooseFunctionality, text = "Choose Functionality")
        titleLabel.grid(row=0,column=0)
        viewTrainButton = Button(self.winChooseFunctionality, text = "View Train Schedule", command = self.toViewTrainSchedule)
        viewTrainButton.grid(row=2,column=0)
        newReservationButton = Button(self.winChooseFunctionality, text = "Make a new reservation", command = self.toSearchTrain)
        newReservationButton.grid(row=3, column=0)
        updateReservationB = Button(self.winChooseFunctionality, text = "Update a reservation", command = self.toUpdateReservation)
        updateReservationB.grid(row=4, column = 0)
        cancelReservationB = Button(self.winChooseFunctionality, text = "Cancel a reservation", command = self.toCancelReservation1)
        cancelReservationB.grid(row=5, column = 0)
        giveReviewB = Button(self.winChooseFunctionality, text = "Give Review", command = self.toGiveReview)
        giveReviewB.grid(row=6, column=0)
        viewReviewB = Button(self.winChooseFunctionality, text = "View Review", command = self.toViewReview)
        viewReviewB.grid(row=7, column=0)
        addSchoolInfoB = Button(self.winChooseFunctionality, text = "Add school information (student discount)", command = self.toAddSchoolInfo)
        addSchoolInfoB.grid(row=8, column=0)
          
        self.winChooseFunctionality.mainloop() 

    def toViewTrainSchedule(self):
        self.winChooseFunctionality.withdraw()
        self.ViewSchedulePage()
        
    def ViewSchedulePage(self):
        self.winSearchSchedule = Tk()
        self.winSearchSchedule.title("View Train Schedule")
        l = Label(self.winSearchSchedule, text="View Train Schedule")
        l.grid(row=0,column=0)
        frame = Frame(self.winSearchSchedule, borderwidth = 3, relief = RAISED)
        frame.grid(row = 1, column = 0)
            
        self.sv3 = StringVar()
        
        L1 = Label(frame, text = "Train Number")
        L1.grid(row=1, column=0)
        self.trainNumber = Entry(frame, width = 25, textvariable=self.sv3)
        self.trainNumber.grid(row = 1, column = 1, padx=5, pady=5)

        search = Button(self.winSearchSchedule, text = "Search", command = self.scheduleCallback)
        search.grid(row = 5, column = 3)
        
        self.winSearchSchedule.mainloop()

    def scheduleCallback(self):
        db = self.connect()
        c = db.cursor()
        get_trains = """SELECT Train_Number, S_Name, Arrival_Time, Departure_Time FROM STOP
                 WHERE Train_Number = %s"""
        exe = c.execute(get_trains, (self.trainNumber.get()))
        trainNames = c.fetchall()
        
        if len(trainNames) != 0:
            self.winSearchSchedule.withdraw()
            self.ViewSchedule()
        else:
            messagebox.showerror("Invalid train number", "Train number not in system")
            
    def ViewSchedule(self):
        
        self.winTrainSchedule = Tk()
        self.winTrainSchedule.title("View Train Schedule")
        title = Label(self.winTrainSchedule, text = "View Train Schedule")
        title.grid(row = 0, column = 1)
        
        tableFrame1 = Frame(self.winTrainSchedule, bd=2, bg='black')
        tableFrame1.grid(row=1, column=0)
        tableFrame2 = Frame(self.winTrainSchedule, bd=2, bg='black')
        tableFrame2.grid(row=1, column=1)
        tableFrame3 = Frame(self.winTrainSchedule, bd=2, bg='black')
        tableFrame3.grid(row=1, column=2)
        tableFrame4 = Frame(self.winTrainSchedule, bd=2, bg='black')
        tableFrame4.grid(row=1, column=3)
        backB = Button(self.winTrainSchedule, text = "Back", command = self.backToFunctionalityPage)
        backB.grid(row=2, column=0)
        
        trainLabel = Label(tableFrame1, text = "Train (Train Number)", bg='dark grey')
        trainLabel.grid(row=0,column=0)
        timeLabel = Label(tableFrame2, text = "Arrival Time", bg='dark grey')
        timeLabel.grid(row=0,column=0)
        class1Label = Label(tableFrame3, text = "Departure Time", bg='dark grey')
        class1Label.grid(row=0, column=0)
        class2Label = Label(tableFrame4, text = "Station", bg='dark grey')
        class2Label.grid(row=0, column=0)

        db = self.connect()
        c = db.cursor()
        get_trains = """SELECT Train_Number, S_Name, Arrival_Time, Departure_Time FROM STOP
                 WHERE Train_Number = %s"""
        exe = c.execute(get_trains, (self.trainNumber.get()))
        trainNames = c.fetchall()
        
        count = 1
        
        for entry1 in trainNames:
            viewTrainList = [entry1[0], entry1[1], entry1[2], entry1[3]]

            if count % 2 == 0 or count == 0:
                color = "light grey"
            else:
                color = "white"
            l1 = Label(tableFrame1, text=viewTrainList[0], bg=color)
            l2 = Label(tableFrame2, text=viewTrainList[2], bg=color)
            l3 = Label(tableFrame3, text=viewTrainList[3], bg=color)
            l4 = Label(tableFrame4, text=viewTrainList[1], bg=color)
            l1.grid(row=count, column=0, sticky=EW)
            l2.grid(row=count, column=0, sticky=EW)
            l3.grid(row=count, column=0, sticky=EW)
            l4.grid(row=count, column=0, sticky=EW)
            count += 1

        self.winTrainSchedule.mainloop()

    def backToFunctionalityPage(self):
        self.winTrainSchedule.withdraw()
        self.chooseFunctionalityPage()

    def toSearchTrain(self):
        self.winChooseFunctionality.withdraw()
        self.SearchTrainPage()
    
    def SearchTrainPage(self):
        db = self.connect()
        ## Setup window##
        self.winSearchTrain = Tk()
        self.winSearchTrain.title("Search Train")
        titleL = Label(self.winSearchTrain, text = "Search Train")
        titleL.grid(row=0, column=1)
        departsL = Label(self.winSearchTrain, text = "Departs From")
        departsL.grid(row=1, column=0)
        arrivesL = Label(self.winSearchTrain, text = "Arrives At")
        arrivesL.grid(row=2, column=0)
        departureDateL = Label(self.winSearchTrain, text = "Departure Date")
        departureDateL.grid(row=3, column=0)

        findTrainsB = Button(self.winSearchTrain, text = "Search Trains", command = self.toSelectDeparture)
        findTrainsB.grid(row=4, column=2)

        ## retrieve names from database to populate dropdown windows #
        c = db.cursor()
        SQL = "SELECT * FROM STATION"
        exe = c.execute(SQL)
        stationNames = c.fetchall()

        stationNamesList = []
        for name in stationNames:
            stationNamesList.append(name[0]+"(" + name[1] + ")")

        self.departVar = StringVar(self.winSearchTrain)
        self.departVar.set(stationNamesList[0])

        self.arriveVar = StringVar(self.winSearchTrain)
        self.arriveVar.set(stationNamesList[0])

        departsMenu = OptionMenu(self.winSearchTrain, self.departVar, *stationNamesList)
        departsMenu.grid(row=1, column=1)

        arrivesMenu = OptionMenu(self.winSearchTrain, self.arriveVar, *stationNamesList)
        arrivesMenu.grid(row=2, column=1)

        dateFrame = Frame(self.winSearchTrain)
        dateFrame.grid(row=3,column=1)
        
        self.daySV = StringVar()       
        self.monthSV = StringVar()
        self.yearSV = StringVar()


        self.monthEntry = Entry(dateFrame, width=5, textvariable=self.monthSV)
        self.monthEntry.grid(row=0, column=0)
        self.dayEntry = Entry(dateFrame, width=5, textvariable=self.daySV)
        self.dayEntry.grid(row=0, column=1)
        self.yearEntry = Entry(dateFrame, width=10, textvariable=self.yearSV)
        self.yearEntry.grid(row=0,column=2)
        
        dateL = Label(self.winSearchTrain, text = "mm-dd-yyyy")
        dateL.grid(row=3, column=2)


        c.close()
        db.commit()
        self.winSearchTrain.mainloop()

    def toSelectDeparture(self):
        day = self.dayEntry.get()
        month = self.monthEntry.get()
        year = self.yearEntry.get()
        today = str(datetime.date.today())
        currentMo = int(today[5:7])
        currentYr = int(today[0:4])
        currentDay = int(today[8:10])
        
        if day=="" or month=="" or year=="" or len(day)!=2 or len(month)!=2 or len(year)!=4 or int(day)>31 or int(month)>12:
            messagebox.showerror("Error", "Incorrect date format.")
        elif int(month)==currentMo and int(day)<=currentDay and int(year)<=currentYr:
            messagebox.showerror("Error", "Please choose a date in the future")
        elif int(year)<currentYr:
            messagebox.showerror("Error", "Please choose a date in the future")
        elif int(month)<currentMo and int(year)==currentYr:
            messagebox.showerror("Error", "Please choose a date in the future")
        else:
            self.winSearchTrain.withdraw()
            self.selectDeparturePage()

    def selectDeparturePage(self):
        db=self.connect()
        #grab variables from search train page
        departStat = self.departVar.get()
        arrivalStat = self.arriveVar.get()
        
        self.winSelectDepart = Toplevel()
        self.winSelectDepart.title("Select Departure")
        titleL = Label(self.winSelectDepart, text = "Select Departure")
        titleL.grid(row=0, column=0)
        tableFrame1 = Frame(self.winSelectDepart, bd=2, bg='black')
        tableFrame1.grid(row=1, column=0)
        tableFrame2 = Frame(self.winSelectDepart, bd=2, bg='black')
        tableFrame2.grid(row=1, column=1)
        tableFrame3 = Frame(self.winSelectDepart, bd=2, bg='black')
        tableFrame3.grid(row=1, column=2)
        tableFrame4 = Frame(self.winSelectDepart, bd=2, bg='black')
        tableFrame4.grid(row=1, column=3)
        backB = Button(self.winSelectDepart, text = "Back", command= self.toSearchTrainFromSelectDepart)
        backB.grid(row=2, column=0)
        nextB = Button(self.winSelectDepart, text = "Next", command = self.toTravelExtras)
        nextB.grid(row=2, column=1)

        trainLabel = Label(tableFrame1, text = "Train (Train Number)", bg='dark grey')
        trainLabel.grid(row=0,column=0)
        timeLabel = Label(tableFrame2, text = "Time (Duration)", bg='dark grey', width=22)
        timeLabel.grid(row=0,column=0)
        class1Label = Label(tableFrame3, text = "1st Class Price", bg='dark grey')
        class1Label.grid(row=0, column=0)
        class2Label = Label(tableFrame4, text = "2nd Class Price", bg='dark grey')
        class2Label.grid(row=0, column=0)

        c = db.cursor()
        departStat = findall("([^\(]*)", departStat)
        departStat = departStat[0]
        arrivalStat = findall("([^\(]*)", arrivalStat)
        arrivalStat = arrivalStat[0]
        #SQL = """SELECT * FROM TRAIN_ROUTE NATURAL JOIN STOP
         #      WHERE (S_Name = %s AND Arrival_Time!= 'NULL')
         #      OR (S_Name= %s AND Departure_Time!='NULL')"""
        SQL = """SELECT a.Train_Number, a.Arrival_Time, b.Departure_Time, a.1st_Class_Price, a.2nd_Class_Price FROM (SELECT * FROM TRAIN_ROUTE NATURAL JOIN STOP
               WHERE S_Name = %s AND Arrival_Time!= 'NULL') as a,(SELECT * FROM TRAIN_ROUTE NATURAL JOIN STOP
               WHERE S_Name= %s AND Departure_Time!='NULL') as b WHERE a.Train_Number=b.Train_Number"""
        c.execute(SQL, (arrivalStat, departStat))

        sqlTable = c.fetchall()

        count = 1
        completeTable = []
        self.svRadioClass = StringVar()
        for row1 in sqlTable:
            trainNumber = row1[0]
            arrivalTime = row1[1]
            departTime = row1[2]
            class1 = row1[3]
            class2 = row1[4]
            duration = arrivalTime-departTime
            
            newDepartTime = str(departTime)[0:5] + "am"
            newArrivalTime = str(arrivalTime)[0:5] + "am"

            if newDepartTime[1] == ":":
                newDepartTime = "0" + newDepartTime

            if newArrivalTime[1] == ":":
                newArrivalTime = "0" + newArrivalTime
            
            if int(newDepartTime[0:2]) == 12:
                newDepartTime = newDepartTime[0:5] + "pm"
            if int(newArrivalTime[0:2]) == 12:
                newArrivalTime = newArrivalTime[0:5] + "pm"
            if int(newDepartTime[0:2]) == 24:
                newDepartTime = newDepartTime[0:5] + "am"
            elif int(newDepartTime[0:2]) > 12:
                currentNum = int(newDepartTime[0:2]) - 12
                newDepartTime = str(currentNum) + newDepartTime[2:5] + "pm"
            if int(newArrivalTime[0:2]) == 24:
                newArrivalTime = newArrivalTime[0:5] + "pm"
            elif int(newArrivalTime[0:2]) > 12:
                currentNum = int(str(arrivalTime)[0:2]) - 12
                newArrivalTime = str(currentNum) + newArrivalTime[2:5] + "pm"

        
            durationStr = str(duration)
            if durationStr[1] == ":":
                durationStr = "0" + durationStr

            durationStr = durationStr[0:2] + "hr" + durationStr[3:5] + "min"
            month = self.monthEntry.get()
            day = self.dayEntry.get()
            if str(duration)[0:6] == "-1 day":
                newArrivalTime = newArrivalTime + "(" + month + "-" + day + ")"
                durationStr = str(duration)[8:]
                durationStr = durationStr[0:2] + "hr" + durationStr[3:5] + "min"

            durationFormat = newDepartTime + "-" + newArrivalTime + "\n" + durationStr
            selectDepartList = [trainNumber, durationFormat, class1, class2]

            if count % 2 == 0 or count == 0:
                color = "light grey"
            else:
                color = "white"
            radioValueList1 = str(selectDepartList[0]) + ";" + str(durationFormat) + ";" + str(selectDepartList[2]) + ";" + '1st Class'
            radioValueList2 = str(selectDepartList[0]) + ";" + str(durationFormat) + ";" + str(selectDepartList[3]) + ";" + '2nd Class'
            ltrainNum = Label(tableFrame1, text=selectDepartList[0], bg=color, height = 3, justify=LEFT)
            lduration = Label(tableFrame2, text=selectDepartList[1], bg=color, height = 3, justify=LEFT)
            RB1class = Radiobutton(tableFrame3, text="$"+ str(selectDepartList[2]),variable = self.svRadioClass, value=radioValueList1, bg=color, height = 3, justify=LEFT)
            RB2class = Radiobutton(tableFrame4, text="$" + str(selectDepartList[3]),variable = self.svRadioClass, value=radioValueList2,  bg=color, height = 3, justify=LEFT)
            ltrainNum.grid(row=count, column=0, sticky=EW)
            lduration.grid(row=count, column=0, sticky=EW)
            RB1class.grid(row=count, column=0, sticky=EW)
            RB2class.grid(row=count, column=0, sticky=EW)
            count = count + 1
        self.svRadioClass.set(None)


        self.winSelectDepart.mainloop()
        

    def toSearchTrainFromSelectDepart(self):
        self.winSelectDepart.withdraw()
        self.winSearchTrain.deiconify()
    
    def toTravelExtras(self):
        self.winSelectDepart.withdraw()
        if not self.ticketsBooked:
            self.addTravelExtrasPage()
        else:
            for reservation in self.ticketsBooked:
                aList = reservation.split(";")
                trainNum = aList[0]
                bList = self.svRadioClass.get()
                cList = bList.split(";")
                selectTrain = cList[0]
                if trainNum == selectTrain:
                    messagebox.showerror("Error", "You cannot travel on the same train twice under the same reservation")
                    self.SearchTrainPage()
            self.addTravelExtrasPage()
    
    def addTravelExtrasPage(self):
        
        self.winTravelExtras = Tk()
        
        self.winTravelExtras.title("Travel Extras & Passenger Info")
        titleL = Label(self.winTravelExtras, text = "Travel Extras & Passenger Info")
        titleL.grid(row = 0, column = 0)

        L1 = Label(self.winTravelExtras, text = "Number of baggage")
        L1.grid(row=1, column=0)
                
        db = self.connect()
        c = db.cursor()
        SQL = "SELECT Max_No_Bags FROM SYSTEM_INFO"
        exe = c.execute(SQL)
        maxBags = c.fetchall()

        c.close()

        c = db.cursor()
        SQL = "SELECT No_Free_Bags FROM SYSTEM_INFO"
        exe = c.execute(SQL)
        freeBags = c.fetchall()

        c.close()

        bagsList = []
        counter = 0
        for i in range(maxBags[0][0] + 1):
            bagsList.append(counter)
            counter += 1

        self.baggageVar = StringVar(self.winTravelExtras)
        self.baggageVar.set(1)
        baggageMenu = OptionMenu(self.winTravelExtras, self.baggageVar, *bagsList)
        baggageMenu.grid(row=1, column=1)
        
        L2 = Label(self.winTravelExtras, text = "Every passenger can bring up to " + str(maxBags[0][0]) + " bags. " + str(freeBags[0][0]) + " bags free of charge, " + str((maxBags[0][0] - freeBags[0][0])) + " bags for $30 per bag""")
        L2.grid(row = 2, column = 0)
        
        self.passName = StringVar()
        
        L3 = Label(self.winTravelExtras, text = "Passenger Name")
        L3.grid(row = 3, column = 0)
        self.passengerName = Entry(self.winTravelExtras, width=30, textvariable = self.passName)
        self.passengerName.grid(row=3, column=1, padx=5, pady=5) 
        
        backB = Button(self.winTravelExtras, text = "Back", command = self.backToSelectDeparture)
        backB.grid(row=5, column=0)
        
        nextB = Button(self.winTravelExtras, text = "Next", command = self.toMakeReservation)
        nextB.grid(row = 5, column = 1)
        
        self.winTravelExtras.mainloop()
        
    def backToSelectDeparture(self):
        self.winTravelExtras.withdraw()
        self.selectDeparturePage()

    def toMakeReservation(self):
        self.winTravelExtras.withdraw()
        if self.passengerName.get() == "":
            messagebox.showerror('Invalid','Please enter your name.')
            self.addTravelExtrasPage()
        radio = self.svRadioClass.get()
        aList = radio.split(";")
        totalPrice = aList[2]
        
        totalPrice = int(totalPrice)
        numBags = int(self.baggageVar.get())
        if (numBags > 2):
            totalPrice += (numBags - 2) * 30
        
        strPrice = str(totalPrice)

        strBags = str(numBags)
        month = str(self.monthEntry.get())
        day = str(self.dayEntry.get())
        year = str(self.yearEntry.get())
        #date = month + "/" + day + "/" + year
        date = year + month + day
        radio += ";" + self.passengerName.get() + ";" + self.arriveVar.get() + ";" + self.departVar.get() + ";" + strPrice + ";" + strBags + ";" + date
        self.ticketsBooked.append(radio)
        self.makeReservation()
   
    def makeReservation(self):
        self.winMakeReservation = Tk()
        self.winMakeReservation.title("Make Reservation")
        title = Label(self.winMakeReservation, text = "Make Reservation")
        title.grid(row = 0, column = 2)

        text1 = Label(self.winMakeReservation, text = "Currently Selected")
        text1.grid(row = 2, column = 0)
        frame1 = Frame(self.winMakeReservation, bd=2, bg='dark grey')
        frame1.grid(row = 3, column = 0)
        frame2 = Frame(self.winMakeReservation, bd=2, bg='dark grey')
        frame2.grid(row = 3, column = 1)
        frame3 = Frame(self.winMakeReservation, bd=2, bg='dark grey')
        frame3.grid(row = 3, column = 2)
        frame4 = Frame(self.winMakeReservation, bd=2, bg='dark grey')
        frame4.grid(row = 3, column = 3)
        frame5 = Frame(self.winMakeReservation, bd=2, bg='dark grey')
        frame5.grid(row = 3, column = 4)
        frame6 = Frame(self.winMakeReservation, bd=2, bg='dark grey')
        frame6.grid(row = 3, column = 5)
        frame7 = Frame(self.winMakeReservation, bd=2, bg='dark grey')
        frame7.grid(row = 3, column = 6)
        frame8 = Frame(self.winMakeReservation, bd=2, bg='dark grey')
        frame8.grid(row = 3, column = 7)
        frame9 = Frame(self.winMakeReservation, bd=2, bg='dark grey')
        frame9.grid(row = 3, column = 8)

        L1 = Label(frame1, text = "Train (Train Number)", bg='dark grey')
        L1.grid(row=0,column=0)
        L2 = Label(frame2, text = "Time (Duration)", bg='dark grey')
        L2.grid(row=0,column=0)
        L3 = Label(frame3, text = "Departs From", bg='dark grey')
        L3.grid(row=0, column=0)
        L4 = Label(frame4, text = "Arrives At", bg='dark grey')
        L4.grid(row=0, column=0)
        L5 = Label(frame5, text = "Class", bg='dark grey')
        L5.grid(row=0,column=0)
        L6 = Label(frame6, text = "Price", bg='dark grey')
        L6.grid(row=0,column=0)
        L7 = Label(frame7, text = "Passenger Name", bg='dark grey')
        L7.grid(row=0, column=0)
        L8 = Label(frame8, text = "Remove", bg='dark grey')
        L8.grid(row=0, column=0)

        self.makeReserveCount = 0

        for reservation in self.ticketsBooked:

            aList = reservation.split(";")
            
            if self.makeReserveCount % 2 == 0 or self.makeReserveCount == 0:
                color = "light grey"
            else:
                color = "white"
            train = Label(frame1, text=aList[0], bg=color)
            train.grid(row = self.makeReserveCount+1, column = 0, sticky=EW)
        
            time = Label(frame2, text=aList[1], bg=color)
            time.grid(row = self.makeReserveCount+1, column = 0, sticky=EW)
        
            departure = Label(frame3, text=aList[6], bg = color)
            departure.grid(row = self.makeReserveCount+1, column = 0, sticky=EW)
        
            arrive = Label(frame4, text = aList[5], bg = color)
            arrive.grid(row = self.makeReserveCount+1, column = 0, sticky=EW)
        
            ticketClass = Label(frame5, text=aList[3], bg = color)
            ticketClass.grid(row = self.makeReserveCount+1, column = 0, sticky=EW)
        
            price = Label(frame6, text=aList[7], bg=color)
            price.grid(row = self.makeReserveCount+1, column = 0, sticky=EW)
        
            passenger = Label(frame7, text = aList[4], bg = color)
            passenger.grid(row = self.makeReserveCount+1, column = 0, sticky=EW)
        
            remove = Button(frame8, text = "Remove", command = lambda: self.removeReservation(reservation))
            remove.grid(row = self.makeReserveCount+1, column = 0, sticky=EW)

            self.makeReserveCount += 1

        totalPay = 0
        for reservation in self.ticketsBooked:
            aList = reservation.split(";")
            totalPay += int(aList[7])

        db = self.connect()
        c = db.cursor()
        SQL = """SELECT Is_Student FROM CUSTOMER WHERE Username = %s"""
        c.execute(SQL, (self.usernameEntry.get()))
        is_student = c.fetchall()

        if is_student:
            c = db.cursor()
            SQL = "SELECT Student_Discount FROM SYSTEM_INFO"
            exe = c.execute(SQL)
            discount = c.fetchall()

            c.close()
            L9 = Label(self.winMakeReservation, text = "Student Discount Applied", bg='light grey')
            L9.grid(row=4,column=0)
            totalPay *= (1 - discount[0][0])

        self.finalPay = totalPay

        L10 = Label(self.winMakeReservation, text = "Total Cost", bg = 'light grey')
        L10.grid(row=5,column=0)
        
        L12 = Label(self.winMakeReservation, text = totalPay, bg = 'light grey')
        L12.grid(row=5, column = 1)

        L11 = Label(self.winMakeReservation, text = "Use Card", bg = 'light grey')
        L11.grid(row=6, column = 1)
        db = self.connect()

        c = db.cursor()

        SQL = """SELECT Card_Number FROM PAYMENT_INFO WHERE C_Username = %s"""
        c.execute(SQL, (self.usernameEntry.get()))
        
        creditCards = c.fetchall()
        cardsList = []
        for card in creditCards:
            cardsList.append(card)

        self.cardVar = StringVar(self.winMakeReservation)
        cardList = OptionMenu(self.winMakeReservation, self.cardVar, *cardsList)
        cardList.grid(row=6, column=2)
        addCard = Button(self.winMakeReservation, text = "Add or delete card", command = self.toNewPayment)
        addCard.grid(row=6, column=3)

        addTrain = Button(self.winMakeReservation, text = "Add another train", command = self.addNewTrain)
        addTrain.grid(row=7, column = 0)

        submitB = Button(self.winMakeReservation, text = "Submit", command = self.toConfirmPage)
        submitB.grid(row=8, column = 1)

        

    def addNewTrain(self):
        self.winMakeReservation.withdraw()
        self.SearchTrainPage()
             
    def removeReservation(self, reservation):
        self.winMakeReservation.withdraw()
        if reservation in self.ticketsBooked:
            self.ticketsBooked.remove(reservation)
            self.makeReserveCount -= 1
        self.makeReservation()
        
    def toNewPayment(self):
        self.winMakeReservation.withdraw()
        self.paymentInfo()

    def toConfirmPage(self):
        if self.cardVar.get() == "":
            messagebox.showerror("Error", "Please select a credit card you'd like to pay with")
            self.winMakeReservation.withdraw()
            self.makeReservation()
        else:
            self.winMakeReservation.withdraw()
            self.confirmReservation()

    def confirmReservation(self):
        self.winConfirmReservation = Tk()
        self.winConfirmReservation.title("Confirmation")
        title = Label(self.winConfirmReservation, text = "Confirmation")
        title.grid(row = 0, column = 0)
        db = self.connect()
        # insert reservation details into RESERVATION
        c = db.cursor()
        SQL = """INSERT INTO RESERVATION (Is_Cancelled, Card_Number, C_Username, Total_Cost) VALUES (%s, %s, %s, %s)"""
        exe = c.execute(SQL, (0, self.cardVar.get()[2:18], self.usernameEntry.get(), self.finalPay))
        c.close()
        
        c = db.cursor()
        # get reservation ID from db
        SQL1 = "SELECT MAX(Reservation_ID) FROM RESERVATION" 
        exe = c.execute(SQL1)
        reserve_ID = c.fetchall()
        c.close()
        
        counter = 0
        # insert each ticket into RESERVES
        for reservation in self.ticketsBooked:

            aList = reservation.split(";")
            trainNum = aList[0]
            ticketClass = aList[3][0]
            departs = aList[6]
            final_depart = departs.split("(")
            arrives = aList[5]
            final_arrive = arrives.split("(")
            passenger = aList[4]
            departureDate = aList[9]
            no_bags = aList[8]
            c = db.cursor()
            SQL2 = """INSERT INTO RESERVES (Reservation_ID, Train_Number, Class, Departure_Date, Passenger_name, No_Bags, Departs_From, Arrives_At)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            exe = c.execute(SQL2, (reserve_ID[0][0], trainNum, ticketClass, departureDate, passenger, no_bags, final_depart[0], final_arrive[0]))
            c.close()
            counter += 1      

        db.commit()
        text1 = Label(self.winConfirmReservation, text = "Reservation ID: ")
        text1.grid(row = 2, column = 0)
        text3 = Label(self.winConfirmReservation, text = reserve_ID)
        text3.grid(row = 2, column = 1)
        text2 = Label(self.winConfirmReservation, text = "Thank you for your purchase! Please save reservation ID for your records")
        text2.grid(row = 3, column = 0)

        backB = Button(self.winConfirmReservation, text = "Back to Choose Functionality", command = self.backChooseF)
        backB.grid(row=4, column = 0)

    def backChooseF(self):
        self.winConfirmReservation.withdraw()
        self.ticketsBooked.clear()
        self.chooseFunctionalityPage()
    
    def paymentInfo(self):
        self.winPayment = Tk()
        title = Label(self.winPayment, text="Payment Info", font="bold")
        title.grid(row=0, column=0, columnspan=2, sticky=NSEW)
                        
        frame1 = Frame(self.winPayment, borderwidth=3, relief=RAISED)
        frame1.grid(row=1, column=0)

        frame2 = Frame(self.winPayment, borderwidth=3, relief=RAISED)
        frame2.grid(row=1, column=1)
                        
        #String variables to store written answers
        svname = StringVar()
        svcard = StringVar()
        svcvv = StringVar()
        svexpMo = StringVar()
        svexpYr = StringVar()

        #Left side frame
        title_add = Label(frame1, text = "Add Card")
        title_add.grid(row=0, column=0, stick=NSEW, columnspan=3)

        L1 = Label(frame1, text = "Name on Card")
        L1.grid(row=1, column=0)
        self.SVcardname = Entry(frame1, width = 25, textvariable=svname)
        self.SVcardname.grid(row = 1, column = 1, padx=5, pady=5, columnspan=2)

        L2 = Label(frame1, text = "Card Number")
        L2.grid(row=2, column=0)
        self.SVcardnumber = Entry(frame1, width = 25, textvariable=svcard)
        self.SVcardnumber.grid(row = 2, column = 1, padx=5, pady=5, columnspan=2)

        L3 = Label(frame1, text = "CVV")
        L3.grid(row=3, column=0)
        self.SVcvv1 = Entry(frame1, width = 25, textvariable=svcvv)
        self.SVcvv1.grid(row = 3, column = 1, padx=5, pady=5, columnspan=2)

        L0 = Label(frame1, text = "Format: xx - xxxx")
        L0.grid(row=4, column=1, columnspan=2)
        
        L4 = Label(frame1, text = "Expiration Date")
        L4.grid(row=5, column=0)
        self.SVExpMo = Entry(frame1, width = 5, textvariable=svexpMo)
        self.SVExpMo.grid(row = 5, column = 1, padx=5, pady=5)
        self.SVExpYr = Entry(frame1, width=10, textvariable=svexpYr)
        self.SVExpYr.grid(row=5, column=2)
        
        submit_add = Button(frame1, text="Submit", command=self.checkAddPaymentInfo)
        submit_add.grid(row=6, column=0, columnspan=3, sticky=NSEW)

        #Deleting frame

        #need to grab available cards
        db = self.connect()
        cursor = db.cursor()
        cards = "SELECT Card_Number FROM PAYMENT_INFO WHERE C_Username = %s"
        exe = cursor.execute(cards, self.usernameEntry.get())
        options = list(cursor.fetchall())
        
        self.svcard_del = StringVar(self.winPayment)
        self.svcard_del.set(options[0])
        
        title_delete = Label(frame2, text="Delete Card")
        title_delete.grid(row=0, column=0, sticky=NSEW, columnspan=5)

        L5 = Label(frame2, text = "Card Number")
        L5.grid(row=1, column=0)
        self.SVcardname_del = OptionMenu(frame2, self.svcard_del, *options)
        self.SVcardname_del.grid(row = 1, column = 1)

        space1 = Label(frame2)
        space1.grid(row=2, column=0)
        space2 = Label(frame2)
        space2.grid(row=3, column=0)
        space3 = Label(frame2)
        space3.grid(row=3, column=0)
        space4 = Label(frame2)
        space4.grid(row=4, column=0)
        space5 = Label(frame2)
        space5.grid(row=5, column=0)
        space6 = Label(frame2)
        space6.grid(row=5, column=0)
        
        submit_del = Button(frame2, text="Submit", command=self.checkDelPaymentInfo)
        submit_del.grid(row=6, column=0, columnspan=2, sticky=NSEW)

        self.winPayment.mainloop()

    def checkAddPaymentInfo(self):
        today = str(datetime.date.today())
        currentMo = int(today[5:7])
        currentYr = int(today[0:4])

        #series of checks to see if expiration date is valid before adding card to database
        if self.SVcardname.get() != "" and self.SVcardnumber.get() != "" and self.SVcvv1.get() != "" and self.SVExpYr.get() != "" and self.SVExpMo.get() != "":         
            if len(self.SVExpMo.get()) >2:
                messagebox.showerror("Incorrect expiration day", "Day of expiration is incorrect")
            elif len(self.SVExpYr.get()) !=4:
                messagebox.showerror("Incorrect expiration year", "Year of expiration is incorrect")
            elif len(self.SVcardnumber.get()) != 16 and type(self.SVcardnumber.get()) != int:
                messagebox.showerror("Incorrect card number", "Card number is not 16 integers in length")
            elif len(self.SVcvv1.get()) != 3 and type(self.SVcvv1.get()) != int:
                messagebox.showerror("Incorrect CVV", "CVV is not 3 integers in length")
            else:
                if int(self.SVExpYr.get()) > currentYr:
                    #All payment info is good to be inserted into database
                    self.insertAddPayment()
                elif int(self.SVExpYr.get()) == currentYr and int(self.SVExpMo.get()) > currentMo:
                    #All payment info is good to be inserted into database
                    self.insertAddPayment()
                else:
                    messagebox.showerror("Incorrect expiration date", "Expiration date must be greater than today")
        else:
            messagebox.showerror("Fields missing", "You have some missing fields")

    def insertAddPayment(self):
        db = self.connect()
        cursor = db.cursor()
        try:
            yr = self.SVExpYr.get()
            exp_date = str(self.SVExpMo.get()) + "-" + yr[2:3]

            #check piazza to see if put constraint of int length for card no and cvv in sql or python
            add_payment = "INSERT INTO PAYMENT_INFO VALUES (%s, %s, %s, %s, %s)"
            exe = cursor.execute(add_payment, (self.SVcardnumber.get(), self.SVcvv1.get(), exp_date, self.SVcardname.get(), self.usernameEntry.get()))
            messagebox.showinfo("Success!", "Card was successfully added")
            self.winPayment.withdraw()
            #self.winMakeReservation.deiconify()
            cursor.close()
            db.commit()
            self.makeReservation()
        except:
            messagebox.showerror("Type error", "Check your info for incorrect data types") 
            
            
    def checkDelPaymentInfo(self):
        db = self.connect()
        cursor = db.cursor()
        today = str(datetime.date.today())
        currentMo = int(today[5:7])
        currentYr = int(today[0:4])
        currentDay = int(today[8:10])
        
        #check to see if card is being used in a transaction aka the departure date has not passed
        #so need to check departure dates of card that was typed in

        #table RESERVES attr Train_Number attr Departure_Date attr Reservation_ID
        #--> table RESERVATION attr Reservation_ID attr Card_Number
        select_departure= "SELECT Card_Number, Departure_Date FROM RESERVES NATURAL JOIN RESERVATION WHERE Reservation_ID = Reservation_ID AND C_Username = %s" 
        exe = cursor.execute(select_departure, self.usernameEntry.get())
        result = cursor.fetchall()
        card_depart = list(result)
        flag = 0
        if card_depart == "": 
                messagebox.showinfo("No matches", "There aren't any cards that were used in transactions for this user")
        else:
            for i in card_depart:
                aStr = str(self.svcard_del.get())
                card = aStr[2:-3]
                if int(i[0]) == int(card):
                    #card is in system. now check to see if being used in a transaction. aka departure date of a trip is in the future
                    card_dates = str(i[1])
                    depart_yr = int(card_dates[0:4])
                    depart_mo = int(card_dates[5:7])
                    depart_day = int(card_dates[8:10])
                    if  depart_yr > currentYr:
                        flag = 1
                    elif depart_yr == currentYr and depart_mo > currentMo:
                        flag = 1
                    elif depart_yr == currentYr and depart_mo == currentMo and depart_day > currentDay:
                        flag = 1
                    else:
                        #delete the card from database
                        flag = 0
                else:
                    flag = 0
        if flag == 1:
            messagebox.showerror("Can't delete card", "Card cannot be deleted because it's being used in a transaction that hasn't ended yet")            
        else:
            self.deletePayment()
            
        cursor.close()
        db.commit()
        
        
    def deletePayment(self):
        try:
            db = self.connect()
            cursor = db.cursor()

            card1 = self.svcard_del.get()
            card = card1[2:-3]
            delete = "DELETE FROM PAYMENT_INFO WHERE Card_Number = %s"
            exe = cursor.execute(delete, str(card))
            messagebox.showinfo("Success!", "Card was successfully deleted")
            cursor.close()
            db.commit()
            self.winPayment.withdraw()
            self.winMakeReservation.deiconify()
        except:
            messagebox.showerror("Error", "Card could not be deleted from database")


#START OF MICHELLE'S UPDATE RESERVATION------------------------------------------------------------------------


    def toChooseFunctionality1(self):
        self.winUpdate1.withdraw()
        self.winChooseFunctionality.deiconify()
        
    def toChooseFunctionality2(self):
        self.winUpdate2.withdraw()
        self.winChooseFunctionality.deiconify()

    def toChooseFunctionality3(self):
        self.winUpdate3.withdraw()
        self.winChooseFunctionality.deiconify()
        
    def updateReservation1(self):
        self.winChooseFunctionality.withdraw()
        self.winUpdate1 = Tk()
        title = Label(self.winUpdate1, text="Update Reservation", font="bold")
        title.grid(row=0, column=0, columnspan=3, sticky=NSEW)
                        
        frame1 = Frame(self.winUpdate1, borderwidth=3, relief=RAISED)
        frame1.grid(row=1, column=0)
                        
        svreservationID = StringVar()

        label1 = Label(frame1, text = "Reservation ID")
        label1.grid(row=0, column=0, stick=NSEW)

        self.SVreservationID = Entry(frame1, width = 15, textvariable=svreservationID)
        self.SVreservationID.grid(row = 0, column = 1, padx=5, pady=5)

        search = Button(frame1, text="Search", command=self.checkUpdateReservation)
        search.grid(row=0, column=2, sticky=NSEW)

        back = Button(frame1, text="Back", command=self.toChooseFunctionality1)
        back.grid(row=2, column=0, columnspan=3, sticky=NSEW)

        self.winUpdate1.mainloop()

    def toUpdateReservation(self):
        self.winChooseFunctionality.withdraw()
        self.updateReservation1()
        
    def checkUpdateReservation(self):
        #connecting to DB to see if ID in system and linked to user
        try:
            ID = int(self.SVreservationID.get())
        except:
            messagebox.showerror("Reservation ID not an integer", "Reservation ID must be an integer")
        if type(ID) == int:
            try:
                db = self.connect()
                cursor = db.cursor()
                select_IDs = "SELECT Username, Reservation_ID FROM USER JOIN RESERVATION ON Username = C_Username WHERE Username = %s AND Reservation_ID = %s"
                exe2 = cursor.execute(select_IDs, (self.usernameEntry.get(), ID))
                result = cursor.fetchall()
                
                if len(result) != 0:
                    self.winUpdate1.withdraw()
                    self.updateReservation2()
                else:
                    messagebox.showerror("Reservation ID not found", "Either this reservation ID could not be found or the reservation was not made by the customer")
            except:
                return 
        else:
            return


    def toSearchTrainFromUpdate(self):
        self.winUpdate3.withdraw()
        self.searchTrainPage()

    def updateReservation2(self):
        self.winUpdate2 = Toplevel()

        title = Label(self.winUpdate2, text="Update Reservation", font="bold")
        title.grid(row=0, column=0, columnspan=10, sticky=NSEW)
                        
        frame1 = Frame(self.winUpdate2, borderwidth=3, relief=RAISED)
        frame1.grid(row=1, column=0)
        frame2 = Frame(self.winUpdate2, borderwidth=3, relief=RAISED)
        frame2.grid(row=1, column=1)
        frame3 = Frame(self.winUpdate2, borderwidth=3, relief=RAISED)
        frame3.grid(row=1, column=2)
        frame4 = Frame(self.winUpdate2, borderwidth=3, relief=RAISED)
        frame4.grid(row=1, column=3)
        frame5 = Frame(self.winUpdate2, borderwidth=3, relief=RAISED)
        frame5.grid(row=1, column=4)
        frame6 = Frame(self.winUpdate2, borderwidth=3, relief=RAISED)
        frame6.grid(row=1, column=5)
        frame7 = Frame(self.winUpdate2, borderwidth=3, relief=RAISED)
        frame7.grid(row=1, column=6)
        frame8 = Frame(self.winUpdate2, borderwidth=3, relief=RAISED)
        frame8.grid(row=1, column=7)
        frame9 = Frame(self.winUpdate2, borderwidth=3, relief=RAISED)
        frame9.grid(row=1, column=8)

        backB = Button(self.winUpdate2, text = "Back", command= self.toChooseFunctionality2)
        backB.grid(row=2, column=0)
        nextB = Button(self.winUpdate2, text = "Next", command = self.toUpdate3)
        nextB.grid(row=2, column=1)

        label1 = Label(frame1, text="Select", font="bold")
        label1.grid(row=0,column=0)
        label2 = Label(frame2, text="Train (Train Number)", font="bold")
        label2.grid(row=0,column=0)                
        label3 = Label(frame3, text="Time (Duration)", font="bold")
        label3.grid(row=0,column=0)
        label4 = Label(frame4, text="Departs From", font="bold")
        label4.grid(row=0,column=0)
        label5 = Label(frame5, text="Arrives At", font="bold")
        label5.grid(row=0,column=0)                
        label6 = Label(frame6, text="Class", font="bold")
        label6.grid(row=0,column=0)
        label7 = Label(frame7, text="Price", font="bold")
        label7.grid(row=0,column=0)
        label8 = Label(frame8, text="# of Baggages", font="bold")
        label8.grid(row=0,column=0)                
        label9 = Label(frame9, text="Passenger Name", font="bold")
        label9.grid(row=0,column=0)

        db = self.connect()
        c = db.cursor()

        #need username from reservation, price from train_route, times from stop, and everything else from reserves
        SQL = """SELECT R.Train_Number, I.Arrival_Time, I.Departure_Time, R.Departs_From, R.Arrives_At, R.Class,
              I.1st_Class_Price, I.2nd_Class_Price, R.No_Bags, R.Passenger_Name, R.Departure_Date FROM RESERVES
              AS R Natural Join Reserve_Info as I WHERE R.Train_Number=I.Train_Number AND I.Depart_Station=R.Departs_From
              AND I.Arrival_Station=R.Arrives_At AND R.Reservation_ID = %s"""
        
        c.execute(SQL, self.SVreservationID.get())
        sqlTable = c.fetchall()
        count = 1
        completeTable = []
        self.svUpdateRB = StringVar()

        for row1 in sqlTable:
            trainNumber = row1[0]
            arrivalTime = row1[1]
            departTime = row1[2]
            departsFrom = row1[3]
            ArrivesAt = row1[4]
            classDecision = row1[5]
            class1 = row1[6]
            class2 = row1[7]
            bags = row1[8]
            passengerName = row1[9]
            departDate = row1[10]
            duration = arrivalTime-departTime
                
            dep = str(departTime)
            arr = str(departTime)
            if dep[1] == ":":
                departTime = "0" + dep
            if arr[1] == ":":
                arrivalTime = "0" + arr
            
            newDepartTime = str(departTime)[0:5] + "am"
            newArrivalTime = str(arrivalTime)[0:5] + "am"

            
            if int(newDepartTime[0:2]) == 12:
                newDepartTime = newDepartTime[0:5] + "pm"
            if int(newArrivalTime[0:2]) == 12:
                newArrivalTime = newArrivalTime[0:5] + "pm"
            if int(newDepartTime[0:2]) == 24:
                newDepartTime = newDepartTime[0:5] + "am"
            elif int(newDepartTime[0:2]) > 12:
                currentNum = int(newDepartTime[0:2]) - 12
                newDepartTime = str(currentNum) + newDepartTime[2:5] + "pm"
            if int(newArrivalTime[0:2]) == 24:
                newArrivalTime = newArrivalTime[0:5] + "pm"
            elif int(newArrivalTime[0:2]) > 12:
                currentNum = int(str(arrivalTime)[0:2]) - 12
                newArrivalTime = str(currentNum) + newArrivalTime[2:5] + "pm"

        
            durationStr = str(duration)
            if durationStr[1] == ":":
                durationStr = "0" + durationStr

            durationStr = durationStr[0:2] + "hr" + durationStr[3:5] + "min"
            
            if str(duration)[0:6] == "-1 day":
                newArrivalTime = newArrivalTime
                durationStr = str(duration)[8:]
                durationStr = durationStr[0:2] + "hr" + durationStr[3:5] + "min"

            departDateMonth =  calendar.month_abbr[departDate.month] 

            durationFormat = newDepartTime + "-" + newArrivalTime + "\n" + durationStr

            if count % 2 == 0 or count == 0:
                color = "light grey"
            else:
                color = "white"
    
            if classDecision == 1:
                classPrice = class1
            if classDecision == 2:
                classPrice = class2
                
            updateList = [trainNumber, durationFormat, departsFrom, ArrivesAt, classDecision, classPrice, bags, passengerName, departDate]
            radioValueList = str(updateList[0]) + ";" + str(durationFormat) + ";" + str(updateList[2]) + ";" + str(updateList[3]) + ";" + str(updateList[4]) + ";" + str(updateList[5]) + ";" + str(updateList[6]) + ";"+ str(updateList[7]) + ";" + str(updateList[8])
            self.RBselect = Radiobutton(frame1, variable=self.svUpdateRB, value=radioValueList, bg=color, height=3, justify=LEFT)
            ltrainNum = Label(frame2, text=trainNumber, bg=color, height = 3, justify=LEFT)
            lduration = Label(frame3, text=durationFormat, bg=color, height = 3, justify=LEFT)
            ldepartsFrom = Label(frame4, text=departsFrom, bg=color, height = 3, justify=LEFT)
            lArrivesAt = Label(frame5, text=ArrivesAt, bg=color, height = 3, justify=LEFT)
            lclassDecision = Label(frame6, text=classDecision, bg=color, height = 3, justify=LEFT)
            lclassPrice = Label(frame7, text="$"+str(classPrice), bg=color, height = 3, justify=LEFT)
            lbags = Label(frame8, text=bags, bg=color, height = 3, justify=LEFT)
            lpassengerName = Label(frame9, text=passengerName, bg=color, height = 3, justify=LEFT)

            self.RBselect.grid(row=count, column=0, sticky=EW)
            ltrainNum.grid(row=count, column=0, sticky=EW)
            lduration.grid(row=count, column=0, sticky=EW)
            ldepartsFrom.grid(row=count, column=0, sticky=EW)
            lArrivesAt.grid(row=count, column=0, sticky=EW)
            lclassDecision.grid(row=count, column=0, sticky=EW)
            lclassPrice.grid(row=count, column=0, sticky=EW)
            lbags.grid(row=count, column=0, sticky=EW)
            lpassengerName.grid(row=count, column=0, sticky=EW)
            self.svUpdateRB.set(radioValueList)
            
            count += 1
            
        self.winUpdate2.mainloop()

    def toUpdate3(self):
        self.winUpdate2.withdraw()
        self.updateReservation3()

    def updateReservation3(self):
        self.winUpdate3 = Tk()
        title = Label(self.winUpdate3, text="Update Reservation", font="bold")
        title.grid(row=0, column=0, columnspan=8, sticky=NSEW)

        label1 = Label(self.winUpdate3, text="Current Train Ticket", font="bold")
        label1.grid(row=1,column=0, sticky=NSEW)
        
        frame1 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame1.grid(row=2, column=0)
        frame2 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame2.grid(row=2, column=1)
        frame3 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame3.grid(row=2, column=2)
        frame4 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame4.grid(row=2, column=3)
        frame5 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame5.grid(row=2, column=4)
        frame6 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame6.grid(row=2, column=5)
        frame7 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame7.grid(row=2, column=6)
        frame8 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame8.grid(row=2, column=7)
        frame8y = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame8y.grid(row=2,column=8)

        label2 = Label(frame1, text="Train (Train Number)", font="bold", bg="dark grey")
        label2.grid(row=0,column=0)                
        label3 = Label(frame2, text="Time (Duration)", font="bold", bg="dark grey")
        label3.grid(row=0,column=0)
        label4 = Label(frame3, text="Departs From", font="bold", bg="dark grey")
        label4.grid(row=0,column=0)
        label5 = Label(frame4, text="Arrives At", font="bold", bg="dark grey")
        label5.grid(row=0,column=0)                
        label6 = Label(frame5, text="Class", font="bold", bg="dark grey")
        label6.grid(row=0,column=0)
        label7 = Label(frame6, text="Price", font="bold", bg="dark grey")
        label7.grid(row=0,column=0)
        label8 = Label(frame7, text="# of Baggages", font="bold", bg="dark grey")
        label8.grid(row=0,column=0)                
        label9 = Label(frame8, text="Passenger Name", font="bold", bg="dark grey")
        label9.grid(row=0,column=0)
        labely = Label(frame8y, text="Departure Date", font="bold", bg="dark grey")
        labely.grid(row=0, column=0)                                                                                                                                                                                                                        

        #display the ONE reservation that was selected via radiobutton
        radio = self.svUpdateRB.get()
        self.aaList = radio.split(";")
        db = self.connect()
        c2 = db.cursor()
        SQL2 = """SELECT Total_Cost FROM RESERVATION WHERE Reservation_ID =%s"""
        exe = c2.execute(SQL2, (self.SVreservationID.get()))
        totalCost = c2.fetchall()

        self.priceToUpdate = totalCost[0][0]

        departDate = self.aaList[8].split("-")
        self.depMonth = departDate[1]
        self.depDay = departDate[2]
        self.depYear = departDate[0]
                                                                                                                                                                                                   
        self.updateTotalPrice = totalCost[0][0]
        date = self.depMonth + "-" + self.depDay + "-" + self.depYear
        
        numBags = int(self.aaList[6])
        #self.updateTotalPrice = int(self.updateTotalPrice) + 50
           
        ztrainNum = Label(frame1, text=self.aaList[0])
        zduration = Label(frame2, text=self.aaList[1])
        zdepartsFrom = Label(frame3, text=self.aaList[2])
        zarrivesAt = Label(frame4, text=self.aaList[3])
        zclass = Label(frame5, text=self.aaList[4])
        zclassPrice = Label(frame6, text=self.aaList[5])
        znoBags = Label(frame7, text=self.aaList[6])
        zpassengerName= Label(frame8, text=self.aaList[7])
        zdepartDate = Label(frame8y, text=date)
        
        ztrainNum.grid(row=1, column=0)
        zduration.grid(row=1, column=0)
        zdepartsFrom.grid(row=1, column=0)
        zarrivesAt.grid(row=1, column=0)
        zclass.grid(row=1, column=0)
        zclassPrice.grid(row=1, column=0)
        znoBags.grid(row=1, column=0)
        zpassengerName.grid(row=1, column=0)
        zdepartDate.grid(row=1,column=0)
        
        frame9 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame9.grid(row=3,column=0, columnspan=8)

        label10 = Label(frame9, text="New Departure Date. (Format mm-dd-yyyy)", font="bold")
        label10.grid(row=0,column=0)
        
        svMonth = StringVar()
        self.newMonth = Entry(frame9, width=10, textvariable=svMonth)
        self.newMonth.grid(row=0,column=1)

        svDay = StringVar()
        self.newDay = Entry(frame9, width=10, textvariable=svDay)
        self.newDay.grid(row=0,column=2)

        svYear = StringVar()
        self.newYear = Entry(frame9, width=10, textvariable=svYear)
        self.newYear.grid(row=0,column=3)
       
        searchButton = Button(frame9, text="Search availability", command=self.searchForUpdates)
        searchButton.grid(row=0,column=4)

        backB = Button(self.winUpdate3, text = "Back", command= self.toChooseFunctionality3)
        backB.grid(row=7, column=0)


    def searchForUpdates(self):
        
        #check that update is at least 1 day earlier than departure date
        if int(self.newYear.get()) > int(self.depYear):
            messagebox.showinfo("Date can be updated", "Date can be updated!")
            self.updatedChanges()
        elif int(self.newYear.get()) == int(self.depYear) and int(self.newMonth.get()) > int(self.depMonth):
            messagebox.showinfo("Date can be updated", "Date can be updated!")
            self.updatedChanges()
        elif int(self.newYear.get()) == int(self.depYear) and int(self.newMonth.get()) == int(self.depMonth) and int(self.newDay.get()) > int(self.depDay):
            messagebox.showinfo("Date can be updated", "Date can be updated!")
            self.updatedChanges()
        else:
            messagebox.showerror("Can't update", "Reservation can only be updated if done at least 1 day earlier than the departure date")


    def updatedChanges(self):
        # SECOND PART OF SAME WINDOW 

        label11 = Label(self.winUpdate3, text="Updated train ticket", font="bold")
        label11.grid(row=4,column=0)

        frameb1 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frameb1.grid(row=5, column=0)
        frameb2 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frameb2.grid(row=5, column=1)
        frameb3 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frameb3.grid(row=5, column=2)
        frameb4 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frameb4.grid(row=5, column=3)
        frameb5 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frameb5.grid(row=5, column=4)
        frameb6 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frameb6.grid(row=5, column=5)
        frameb7 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frameb7.grid(row=5, column=6)
        frameb8 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frameb8.grid(row=5, column=7) 
        frameb9 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frameb9.grid(row=5, column=8)                                                                                                                                                                                                                        

        label12 = Label(frameb1, text="Train (Train Number)", font="bold", bg="dark grey")
        label12.grid(row=0,column=0)                
        label13 = Label(frameb2, text="Time (Duration)", font="bold", bg="dark grey")
        label13.grid(row=0,column=0)
        label14 = Label(frameb3, text="Departs From", font="bold", bg="dark grey")
        label14.grid(row=0,column=0)
        label15 = Label(frameb4, text="Arrives At", font="bold", bg="dark grey")
        label15.grid(row=0,column=0)                
        label16 = Label(frameb5, text="Class", font="bold", bg="dark grey")
        label16.grid(row=0,column=0)
        label17 = Label(frameb6, text="Price", font="bold", bg="dark grey")
        label17.grid(row=0,column=0)
        label18 = Label(frameb7, text="# of Baggages", font="bold", bg="dark grey")
        label18.grid(row=0,column=0)                
        label19 = Label(frameb8, text="Passenger Name", font="bold", bg="dark grey")
        label19.grid(row=0,column=0)
        labelz = Label(frameb9, text="Departure Date", font="bold", bg="dark grey")
        labelz.grid(row=0, column=0)                                                                                                                                                                                                                        

        #display the ONE UPDATED reservation that was selected via radiobutton
        ytrainNum = Label(frameb1, text=self.aaList[0], bg="light grey")
        yduration = Label(frameb2, text=self.aaList[1], bg="light grey")
        ydepartsFrom = Label(frameb3, text=self.aaList[2], bg="light grey")
        yarrivesAt = Label(frameb4, text=self.aaList[3], bg="light grey")
        yclass = Label(frameb5, text=self.aaList[4], bg="light grey")
        yclassPrice = Label(frameb6, text=self.aaList[5], bg="light grey")
        ynoBags = Label(frameb7, text=self.aaList[6], bg="light grey")
        ypassengerName= Label(frameb8, text=self.aaList[7], bg="light grey")
        ddate = str(self.newMonth.get())+"-"+str(self.newDay.get())+"-"+str(self.newYear.get())
        ydate = Label(frameb9, text=ddate, bg="light grey")                                                                                                                                                                                                                        
        
        ytrainNum.grid(row=1, column=0)
        yduration.grid(row=1, column=0)
        ydepartsFrom.grid(row=1, column=0)
        yarrivesAt.grid(row=1, column=0)
        yclass.grid(row=1, column=0)
        yclassPrice.grid(row=1, column=0)
        ynoBags.grid(row=1, column=0)
        ypassengerName.grid(row=1, column=0)
        ydate.grid(row=1, column=0)

        frame11 = Frame(self.winUpdate3, borderwidth=3, relief=RAISED)
        frame11.grid(row=6,column=0)

        db = self.connect()
        cursor = db.cursor()
        fee = "SELECT Change_Fee FROM SYSTEM_INFO"
        exe = cursor.execute(fee)
        change_Fee = cursor.fetchall()
        change_Fee1 = change_Fee[0][0]
        
        label20 = Label(frame11, text="Change fee = "+str(change_Fee1), font="bold")
        label20.grid(row=0,column=0)

        self.total = int(change_Fee1)+int(self.updateTotalPrice)
        label21 = Label(frame11, text="Updated Total Cost = "+str(self.total), font="bold")
        label21.grid(row=1, column=0)

        submitB = Button(self.winUpdate3, text = "Submit", command = self.toSubmitUpdates)
        submitB.grid(row=7, column=1)

        
    def toSubmitUpdates(self):
        try:
            db = self.connect()
            cursor = db.cursor()
            date = str(self.newYear.get()+'-'+self.newMonth.get()+ '-'+self.newDay.get())

            updateReservationDate = "UPDATE RESERVES SET Departure_Date = %s WHERE Reservation_ID = %s AND Train_Number = %s"
            cursor.execute(updateReservationDate, (date, self.SVreservationID.get(), self.aaList[0]))
            
            updateReservationCost= "UPDATE RESERVATION SET Total_Cost = %s WHERE Reservation_ID = %s"
            cursor.execute(updateReservationCost, (self.total, self.SVreservationID.get()))

            messagebox.showinfo("Success", "Reservation date successfully updated")

            cursor.close()
            db.commit()
            self.toChooseFunctionality3()
        except:
            return
        

# END OF MICHELLE'S UPDATE RESERVATION --------------------------------------------
# START KARA"S CANCEL RESERVATION

    def toCancelReservation1(self):
        self.winChooseFunctionality.withdraw()
        self.cancelReservationPage1()

    def cancelReservationPage1(self):
        self.cancelReservationWin = Toplevel()
        self.cancelReservationWin.title("Cancel Reservation")
        l = Label(self.cancelReservationWin, text = "Cancel Reservation")
        l.grid(row=0, column=0)
        f = Frame(self.cancelReservationWin)
        f.grid(row=1, column=0)
        l2 = Label(f, text="Reservation ID")
        l2.grid(row=0,column=0)
        self.cancelResSV = StringVar()
        self.cancelResEntry = Entry(f, textvariable=self.cancelResSV)
        self.cancelResEntry.grid(row=0, column=1)
        searchB = Button(f, text = "Search", command=self.cancel1to2)
        searchB.grid(row=0,column=2)
        backB = Button(self.cancelReservationWin, text="Back", command=self.cancelToFunc)
        backB.grid(row=2, column=0)

        self.cancelReservationWin.mainloop()

    def cancelToFunc(self):
        self.cancelReservationWin.withdraw()
        self.winChooseFunctionality.deiconify()

    def cancel1to2(self):
        db = self.connect()
        c = db.cursor()
        reservationId = self.cancelResEntry.get()
        SQL = """SELECT Is_Cancelled FROM RESERVATION WHERE Reservation_ID = %s"""
        exe = c.execute(SQL, (reservationId))
        cancelation = c.fetchall()
        for entry in cancelation:
            if entry[0] == 1:
                messagebox.showerror("Error", "This reservation has already been cancelled.")
            if entry[0] == 0:
                self.cancelReservationWin.withdraw()
                self.cancelReservationPage2()

    def cancelReservationPage2(self):
        self.cancelReservationWin2 = Toplevel()
        self.cancelReservationWin2.title("Cancel Reservation")
        l = Label(self.cancelReservationWin2, text = "Cancel Reservation")
        l.grid(row=0, column=0)
        tableFrame = Frame(self.cancelReservationWin2)
        tableFrame.grid(row=1,column=0)
        frame2 = Frame(self.cancelReservationWin2)
        frame2.grid(row=2,column=0)
        label1 = Label(frame2, text = "Total Cost of Reservation")
        label1.grid(row=0,column=0)
        totalCostSV = StringVar()
        totalCostEntry = Entry(frame2, textvariable= totalCostSV)
        totalCostEntry.grid(row=0,column=1)
        label2 = Label(frame2, text = "Date of Cancellation")
        label2.grid(row=1,column=0)
        cancelDateSV = StringVar()
        cancelDateEntry = Entry(frame2, textvariable = cancelDateSV)
        cancelDateEntry.grid(row=1,column=1)
        label3 = Label(frame2, text = "Amount to be Refunded")
        label3.grid(row=2,column=0)
        refundAmtSV = StringVar()
        refundAmtEntry = Entry(frame2, textvariable = refundAmtSV)
        refundAmtEntry.grid(row=2,column=1)
        backB = Button(frame2, text="Back", command=self.reserve2to1)
        backB.grid(row=3, column=0)
        submitB = Button(frame2, text="Submit", command= self.submitCancelRes)
        submitB.grid(row=3,column=1)
        f1 = Frame(tableFrame, bd=2, bg='black')
        f1.grid(row=0,column=0)
        f2 = Frame(tableFrame, bd=2, bg='black')
        f2.grid(row=0,column=1)
        f3 = Frame(tableFrame, bd=2, bg='black')
        f3.grid(row=0,column=2)
        f4 = Frame(tableFrame, bd=2, bg='black')
        f4.grid(row=0,column=3)
        f5 = Frame(tableFrame, bd=2, bg='black')
        f5.grid(row=0,column=4)
        f6 = Frame(tableFrame, bd=2, bg='black')
        f6.grid(row=0,column=5)
        f7 = Frame(tableFrame, bd=2, bg='black')
        f7.grid(row=0,column=6)
        f8 = Frame(tableFrame, bd=2, bg='black')
        f8.grid(row=0,column=7)

        l1 = Label(f1, text = "Train \n (Train Number)", bg='dark grey')
        l1.grid(row=0, column=0, sticky=EW)
        l2 = Label(f2, text = "Time \n (Duration)", bg='dark grey')
        l2.grid(row=0, column=0, sticky=EW)
        l3 = Label(f3, text = "Departs From", bg='dark grey')
        l3.grid(row=0, column=0, sticky=EW)
        l4 = Label(f4, text = "Arrives At", bg='dark grey')
        l4.grid(row=0, column=0, sticky=EW)
        l5 = Label(f5, text = "Class", bg='dark grey')
        l5.grid(row=0, column=0, sticky=EW)
        l6 = Label(f6, text = "Price", bg='dark grey')
        l6.grid(row=0, column=0, sticky=EW)
        l7 = Label(f7, text = "# of Baggages", bg='dark grey')
        l7.grid(row=0, column=0, sticky=EW)
        l8 = Label(f8, text = "Passenger Name", bg='dark grey')
        l8.grid(row=0, column=0, sticky=EW)

        reservationId = self.cancelResEntry.get()

        db = self.connect()
        c = db.cursor()
        SQL = """SELECT R.Train_Number, I.Arrival_Time, I.Departure_Time, R.Departs_From, R.Arrives_At,
                        R.Class, I.1st_Class_Price, I.2nd_Class_Price, R.No_Bags, R.Passenger_Name, R.Departure_Date
                        FROM RESERVES AS R Natural Join Reserve_Info as I
                        WHERE R.Train_Number=I.Train_Number AND I.Depart_Station=R.Departs_From AND
                        I.Arrival_Station=R.Arrives_At AND R.Reservation_ID = %s"""
        exe = c.execute(SQL, (reservationId))
        reservations = c.fetchall()

        count = 1
        earliestDate = datetime.date(9999, 5, 6)
        totalPrice = 0

        for row1 in reservations:
            trainNumber = row1[0]
            arrivalTime = row1[1]
            departTime = row1[2]
            departsFrom = row1[3]
            ArrivesAt = row1[4]
            classDecision = row1[5]
            class1 = row1[6]
            class2 = row1[7]
            bags = row1[8]
            passengerName = row1[9]
            departDate = row1[10]
            duration = arrivalTime-departTime

            if departDate < earliestDate:
                earliestDate = departDate
                
            dep = str(departTime)
            arr = str(departTime)
            if dep[1] == ":":
                departTime = "0" + dep
            if arr[1] == ":":
                arrivalTime = "0" + arr
            
            newDepartTime = str(departTime)[0:5] + "am"
            newArrivalTime = str(arrivalTime)[0:5] + "am"

            
            if int(newDepartTime[0:2]) == 12:
                newDepartTime = newDepartTime[0:5] + "pm"
            if int(newArrivalTime[0:2]) == 12:
                newArrivalTime = newArrivalTime[0:5] + "pm"
            if int(newDepartTime[0:2]) == 24:
                newDepartTime = newDepartTime[0:5] + "am"
            elif int(newDepartTime[0:2]) > 12:
                currentNum = int(newDepartTime[0:2]) - 12
                newDepartTime = str(currentNum) + newDepartTime[2:5] + "pm"
            if int(newArrivalTime[0:2]) == 24:
                newArrivalTime = newArrivalTime[0:5] + "pm"
            elif int(newArrivalTime[0:2]) > 12:
                currentNum = int(str(arrivalTime)[0:2]) - 12
                newArrivalTime = str(currentNum) + newArrivalTime[2:5] + "pm"

        
            durationStr = str(duration)
            if durationStr[1] == ":":
                durationStr = "0" + durationStr

            durationStr = durationStr[0:2] + "hr" + durationStr[3:5] + "min"
            
            if str(duration)[0:6] == "-1 day":
                newArrivalTime = newArrivalTime 
                durationStr = str(duration)[8:]
                durationStr = durationStr[0:2] + "hr" + durationStr[3:5] + "min"

            departDateMonth =  calendar.month_abbr[departDate.month] 

            durationFormat = departDateMonth + str(departDate.day) + " " + newDepartTime + "-" + newArrivalTime + "\n" + durationStr

            if count % 2 == 0 or count == 0:
                color = "light grey"
            else:
                color = "white"
    
            if classDecision == 1:
                classPrice = class1
            if classDecision == 2:
                classPrice = class2
                
        
            ltrainNum = Label(f1, text=trainNumber, bg=color, height = 3, justify=LEFT)
            lduration = Label(f2, text=durationFormat, bg=color, height = 3, justify=LEFT)
            ldepartsFrom = Label(f3, text=departsFrom, bg=color, height = 3, justify=LEFT)
            lArrivesAt = Label(f4, text=ArrivesAt, bg=color, height = 3, justify=LEFT)
            lclassDecision = Label(f5, text=classDecision, bg=color, height = 3, justify=LEFT)
            lclassPrice = Label(f6, text="$"+str(classPrice), bg=color, height = 3, justify=LEFT)
            lbags = Label(f7, text=bags, bg=color, height = 3, justify=LEFT)
            lpassengerName = Label(f8, text=passengerName, bg=color, height = 3, justify=LEFT)
         
            ltrainNum.grid(row=count, column=0, sticky=EW)
            lduration.grid(row=count, column=0, sticky=EW)
            ldepartsFrom.grid(row=count, column=0, sticky=EW)
            lArrivesAt.grid(row=count, column=0, sticky=EW)
            lclassDecision.grid(row=count, column=0, sticky=EW)
            lclassPrice.grid(row=count, column=0, sticky=EW)
            lbags.grid(row=count, column=0, sticky=EW)
            lpassengerName.grid(row=count, column=0, sticky=EW)

            count = count + 1
        
        self.canCancel = True

        c2 = db.cursor()
        SQL2 = """SELECT Total_Cost FROM RESERVATION WHERE Reservation_ID =%s"""
        exe = c2.execute(SQL2, (reservationId))
        totalCost = c2.fetchall()
        
        totalPrice = totalCost[0][0]


        totalCostSV.set(totalPrice)
        dateOfCancel = datetime.date.today()
        dateChange = earliestDate-dateOfCancel
        dateChange = dateChange.days

        if dateChange >= 7:
            refund = int(totalPrice)*.8-50
        elif dateChange < 7 and dateChange >= 1:
            refund = int(totalPrice)*.5-50
        elif dateChange < 1:
            refund = 0
            self.canCancel=False

        self.newTotalAmt = int(totalPrice) - refund

        self.newTotalAmt = format(self.newTotalAmt, '.2f')
        
        dateOfCancel = str(dateOfCancel.month) + "-" + str(dateOfCancel.day) + "-" + str(dateOfCancel.year)
        cancelDateSV.set(dateOfCancel)
        refundAmtSV.set(format(refund, '.2f'))

        self.cancelReservationWin2.mainloop()
        
    def reserve2to1(self):
        self.cancelReservationWin2.withdraw()
        self.cancelReservationWin.deiconify()
        
    def submitCancelRes(self):
        db = self.connect()
        if self.canCancel == True:
            c = db.cursor()
            SQL = """UPDATE RESERVATION SET Is_Cancelled = 1, Total_Cost = %s WHERE Reservation_ID  = %s"""
            exe = c.execute(SQL, (self.newTotalAmt, self.cancelResEntry.get()))
            messagebox.showinfo("Reservation Canceled", "Your reservation has been canceled.")
            c.close()
        else:
            messagebox.showinfo("Reservation Error", "Unable to cancel reservation. You must /n cancel at least 1 day before departure.")
        self.cancelReservationWin2.withdraw()
        self.winChooseFunctionality.deiconify()
        db.commit()
        
#END KARA'S CANCEL RESERVATION...............................................

    def toGiveReview(self):
        self.winChooseFunctionality.withdraw()
        self.giveReviewPage()

    def giveReviewPage(self):
        self.winGiveReview = Toplevel()
        self.winGiveReview.title("Give Review")
        ltitle = Label(self.winGiveReview, text = "Give Review")
        ltitle.grid(row=0,column=0)
        f = Frame(self.winGiveReview)
        f.grid(row=1,column=0)
        l = Label(f, text="Train Number")
        l.grid(row=0,column=0)
        self.trainNumSV = StringVar()
        self.trainNumEntry = Entry(f, textvariable=self.trainNumSV)
        self.trainNumEntry.grid(row=0,column=1)
        l1 = Label(f, text="Rating")
        l1.grid(row=1,column=0)

        ratingScaleList = ["Very Good", "Good", "Neutral", "Bad", "Very Bad"]
        
        self.ratingSV = StringVar(self.winGiveReview)
        self.ratingSV.set(ratingScaleList[2])

        ratingMenu = OptionMenu(f, self.ratingSV, *ratingScaleList)
        ratingMenu.grid(row=1, column=1)

        l2 = Label(f, text="Comment")
        l2.grid(row=2,column=0)
        self.commentSV = StringVar()
        self.commentEntry = Entry(f, textvariable=self.commentSV, width=30)
        self.commentEntry.grid(row=2,column=1)

        submitB = Button(f, text="Submit", command=self.submitComment)
        submitB.grid(row=3,column=1)

        self.winGiveReview.mainloop()

    def submitComment(self):
        db = self.connect()
        c = db.cursor()
        SQL = """SELECT Train_Number FROM TRAIN_ROUTE"""
        exe = c.execute(SQL)
        trainNames = c.fetchall()

        username = self.usernameEntry.get()
        commentTrainName = self.trainNumEntry.get()
        comment = self.commentEntry.get()
        rating = self.ratingSV.get()

        trainNameExists = False
        
        for name in trainNames:
            if name[0] == commentTrainName:
                trainNameExists = True

        if trainNameExists == False:
            messagebox.showerror(title="Error", message='Must enter a valid train name.')
        else:  
            #review successful
            c2 = db.cursor()
            SQL2 = """INSERT INTO REVIEW (Comment, Rating, C_Username, Train_Number)
                      VALUES (%s, %s, %s,%s)"""
            exe2 = c2.execute(SQL2, (comment, rating, username, commentTrainName))
            messagebox.showinfo(title='Success!', message='Comment Submitted')
            self.winGiveReview.withdraw()
            self.winChooseFunctionality.deiconify()
        c.close()
        c2.close()
        db.commit()

    def toViewReview(self):
        self.winChooseFunctionality.withdraw()
        self.viewReviewPage()

    def viewReviewPage(self):
        self.winViewReview = Toplevel()
        self.winViewReview.title("View Review")
        l = Label(self.winViewReview, text="View Review")
        l.grid(row=0,column=0)
        f = Frame(self.winViewReview)
        f.grid(row=1,column=0)
        l2 = Label(f, text="Train Number")
        l2.grid(row=0,column=0)
        
        self.viewRevTrainNum = StringVar()
        self.viewRevTrainNumEntry = Entry(f, textvariable= self.viewRevTrainNum)
        self.viewRevTrainNumEntry.grid(row=0,column=1)

        back = Button(f, text = "Back", command = self.viewRevtoChooseFunc)
        back.grid(row=1, column=0)
        submit = Button(f, text = "Submit", command = self.attemptToPullReviews)
        submit.grid(row=1, column=1)

        
        self.winViewReview.mainloop()

    def viewRevtoChooseFunc(self):
        self.winViewReview.withdraw()
        self.winChooseFunctionality.deiconify()

    def attemptToPullReviews(self):
        db = self.connect()
        c = db.cursor()
        SQL = """SELECT Rating, Comment FROM REVIEW WHERE Train_Number=%s"""
        exe = c.execute(SQL, (self.viewRevTrainNumEntry.get()))
        ratings = c.fetchall()

        if len(ratings) == 0:
            messagebox.showerror("Warning", "This train has no reviews.")
        else:
            self.winViewReview.withdraw()
            self.winViewReview2 = Toplevel()
            self.winViewReview2.title("View Review")
            l = Label(self.winViewReview2, text="View Review")
            l.grid(row=0,column=0)
            ftable = Frame(self.winViewReview2)
            ftable.grid(row=1,column=0)
            f1 = Frame(ftable, bd=2, bg='black')
            f1.grid(row=1,column=0, sticky=EW)
            f2 = Frame(ftable, bd=2, bg='black')
            f2.grid(row=1,column=1, sticky=EW)
            back = Button(self.winViewReview2, text = "Back to Choose Functionality", command=self.viewRev2toChooseFunc)
            back.grid(row=2, column=0)
            l2 = Label(f1, text = "Rating", bg='dark grey')
            l2.grid(row=0, column=0, sticky=EW)
            l3 = Label(f2, text = "Comment", bg='dark grey', width=60)
            l3.grid(row=0, column=0, sticky=EW)
            count = 1
            for entry in ratings:
                rating = entry[0]
                comment = entry[1]
                if count % 2 == 0 or count == 0:
                    color = "light grey"
                else:
                    color = "white"
                l4 = Label(f1, text=rating, bg=color, justify=LEFT)
                l4.grid(row=count, column=0, sticky=EW)
                l5 = Label(f2, text=comment, bg=color, justify=LEFT)
                l5.grid(row=count, column=0, sticky=EW)
                count = count + 1
                
    def viewRev2toChooseFunc(self):
        self.winViewReview2.withdraw()
        self.winChooseFunctionality.deiconify()

    def toAddSchoolInfo(self):
        self.winChooseFunctionality.withdraw()
        self.addSchoolInfoPage()
    
        #Add School InfoT
    def addSchoolInfoPage(self):
        self.winAddSchoolInfo = Tk()
        frame = Frame(self.winAddSchoolInfo)
        frame.grid(row=0, column=0)
        
        self.winAddSchoolInfo.title("Add School Info")
        headTitle = Label(self.winAddSchoolInfo, text = "Add School Info")
        headTitle.grid(row = 0, column = 1)
        
        emailText = Label(self.winAddSchoolInfo, text = "School Email Address")
        emailText.grid(row = 1, column = 0)

        self.sEmailSV = StringVar()
        self.sEmailEntry = Entry(self.winAddSchoolInfo, textvariable=self.sEmailSV)
        self.sEmailEntry.grid(row = 1, column = 1)

        schoolEmailFrame = Frame(self.winAddSchoolInfo)
        self.schoolEmail = StringVar()
        self.schoolEmail.set("Hi")

        eduReminderTitle = Label(self.winAddSchoolInfo, text = "Your school email address should end with .edu")
        eduReminderTitle.grid(row = 2, column = 1)
        
        backButton = Button(self.winAddSchoolInfo, text="Back", command=self.schoolInfoToChooseFunc)
        submitButton = Button(self.winAddSchoolInfo, text="Submit", command = self.submitStudentID)
        
        backButton.grid(row = 3, column = 0)
        submitButton.grid(row = 3, column = 1)

        self.winAddSchoolInfo.mainloop()

    def submitStudentID(self):
        email = self.sEmailEntry.get()
        studentVal = '0' 
        if email[-3:]=="edu":
            studentVal = '1'
            db = self.connect()
            c = db.cursor()
            SQL = """UPDATE CUSTOMER SET Is_Student=%s WHERE Username = %s"""
            exe = c.execute(SQL, (studentVal, self.usernameEntry.get()))
        
            c.close()
            db.commit()
            messagebox.showinfo('Complete', 'Student status updated.')
            self.winAddSchoolInfo.withdraw()
            self.winChooseFunctionality.deiconify()
        else:
            messagebox.showerror('Invalid','Invalid student email.')

    def schoolInfoToChooseFunc(self):
        self.winAddSchoolInfo.withdraw()
        self.winChooseFunctionality.deiconify()
   
    def toChooseManagerFunctionalityPageFromRevenue(self):
        self.winViewRevenueReport.withdraw() 
        self.chooseManagerFunctionalityPage()

    def toChooseManagerFunctionalityPageFromPopular(self):
        self.winViewPopRoute.withdraw() 
        self.chooseManagerFunctionalityPage()
        
    def chooseManagerFunctionalityPage(self):
        self.winChooseManagerFunctionality = Tk()
        self.winChooseManagerFunctionality.title("Choose Functionality (manager view)")
        titleLabel = Label(self.winChooseManagerFunctionality, text = "Choose Functionality (manager view)")
        titleLabel.grid(row=0,column=0)
        viewRevenueReportButton = Button(self.winChooseManagerFunctionality, text = "View revenue report", command = self.toViewRevenueReport)
        viewRevenueReportButton.grid(row=2,column=0)
        viewPopRouteButton = Button(self.winChooseManagerFunctionality, text = "View popular route report", command = self.toViewPopRoute)
        viewPopRouteButton.grid(row=3, column=0)
        
        self.winChooseManagerFunctionality.mainloop()
        
    def toViewRevenueReport(self):
        self.winChooseManagerFunctionality.withdraw()
        self.viewRevenueReport()

    def viewRevenueReport(self):
        ## Setup window##
        self.winViewRevenueReport = Tk()
        self.winViewRevenueReport.title("View Revenue Report")
        titleL = Label(self.winViewRevenueReport, text = "View Revenue Report")
        titleL.grid(row=0, column=0)

        moreFrame = Frame(self.winViewRevenueReport)
        moreFrame.grid(row=1, column=0)
        tableFrame1 = Frame(moreFrame, bd=2, bg='black')
        tableFrame1.grid(row=0, column=0)
        tableFrame2 = Frame(moreFrame, bd=2, bg='black')
        tableFrame2.grid(row=0, column=1)

        l = Label(tableFrame1, text = "Month", bg='dark grey')
        l.grid(row=0,column=0, sticky=EW)
        l1 = Label(tableFrame2, text = "Revenue", bg='dark grey')
        l1.grid(row=0, column=0, sticky=EW)
        

        findTrainsB = Button(self.winViewRevenueReport, text = "Back", command = self.toChooseManagerFunctionalityPageFromRevenue)
        findTrainsB.grid(row=4, column=1)
        dateToday = datetime.date.today()
        monthToday = dateToday.month
        
        prev1 = monthToday - 1
        prev2 = monthToday - 2
        prev3 = monthToday - 3

        if len(str(prev1)) == 1:
            prev1 = "0" + str(prev1)
        if len(str(prev2)) == 1:
            prev2 = "0" + str(prev2)
        if len(str(prev3)) == 1:
            prev3 = "0" + str(prev3)
        if len(str(monthToday)) == 1:
            monthToday = "0"+str(monthToday)

        month1B = "2016"+str(prev1)+"01"
        month1E = "2016"+str(monthToday)+"01"
        month2B = "2016"+str(prev2)+"01"
        month2E = "2016"+str(prev1)+"01"
        month3B = "2016"+str(prev3)+"01"
        month3E = "2016"+str(prev2)+"01"

        db = self.connect()
        cursor = db.cursor();

        SQL = """(SELECT RESERVES.Departure_Date, SUM(RESERVATION.Total_Cost)
        FROM RESERVATION, RESERVES
        WHERE RESERVATION.Reservation_ID = RESERVES.Reservation_ID
        AND RESERVES.DEPARTURE_DATE >=%s
        AND RESERVES.DEPARTURE_DATE <%s)
        UNION
        (SELECT RESERVES.Departure_Date, SUM(RESERVATION.Total_Cost)
        FROM RESERVATION, RESERVES
        WHERE RESERVATION.Reservation_ID = RESERVES.Reservation_ID
        AND RESERVES.DEPARTURE_DATE >=%s
        AND RESERVES.DEPARTURE_DATE <%s)
        UNION
        (SELECT RESERVES.Departure_Date, SUM(RESERVATION.Total_Cost)
        FROM RESERVATION, RESERVES
        WHERE RESERVATION.Reservation_ID = RESERVES.Reservation_ID
        AND RESERVES.DEPARTURE_DATE >=%s
        AND RESERVES.DEPARTURE_DATE <%s)"""
        cursor.execute(SQL, (month3B, month3E, month2B, month2E, month1B, month1E))

        revenueInfo = cursor.fetchall()

        count = 1
        for revenue in revenueInfo:
            if count % 2 == 0 or count == 0:
                color = "light grey"
            else:
                color = "white"
                
            l1 = Label(tableFrame1, text=revenue[0].strftime("%B"), bg=color)
            l1.grid(row=count, column=0, sticky=EW)
            l2 = Label(tableFrame2, text="$" + str(revenue[1]), bg=color)
            l2.grid(row=count, column=0, sticky=EW)

            count+=1

    def toViewPopRoute(self):
        self.winChooseManagerFunctionality.withdraw()
        self.viewPopRoute()

    def viewPopRoute(self):
        ## Setup window##
        self.winViewPopRoute = Tk()
        self.winViewPopRoute.title("View Popular Route Report")
        titleL = Label(self.winViewPopRoute, text = "View Popular Route Report")
        titleL.grid(row=0, column=0)

        moreFrame = Frame(self.winViewPopRoute)
        moreFrame.grid(row=1, column=0)
        tableFrame1 = Frame(moreFrame, bd=2, bg='black')
        tableFrame1.grid(row=1, column=0)
        tableFrame2 = Frame(moreFrame, bd=2, bg='black')
        tableFrame2.grid(row=1, column=1)
        tableFrame3 = Frame(moreFrame, bd=2, bg='black')
        tableFrame3.grid(row=1, column=2)

        trainLabel = Label(tableFrame1, text = "Month", bg='dark grey')
        trainLabel.grid(row=0,column=0, sticky=EW)
        timeLabel = Label(tableFrame2, text = "Train Number", bg='dark grey')
        timeLabel.grid(row=0,column=0, sticky=EW)
        class1Label = Label(tableFrame3, text = "# of Reservations", bg='dark grey')
        class1Label.grid(row=0, column=0, sticky=EW)
        
        findTrainsB = Button(self.winViewPopRoute, text = "Back", command = self.toChooseManagerFunctionalityPageFromPopular)
        findTrainsB.grid(row=2, column=1)

        dateToday = datetime.date.today()
        monthToday = dateToday.month
        prev1 = monthToday - 1
        prev2 = monthToday - 2
        prev3 = monthToday - 3

        if len(str(prev1)) == 1:
            prev1 = "0" + str(prev1)
        if len(str(prev2)) == 1:
            prev2 = "0" + str(prev2)
        if len(str(prev3)) == 1:
            prev3 = "0" + str(prev3)
        if len(str(monthToday)) == 1:
            monthToday = "0"+str(monthToday)

        month1B = "2016"+str(prev1)+"01"
        month1E = "2016"+str(monthToday)+"01"
        month2B = "2016"+str(prev2)+"01"
        month2E = "2016"+str(prev1)+"01"
        month3B = "2016"+str(prev3)+"01"
        month3E = "2016"+str(prev2)+"01"

        db = self.connect()
        cursor = db.cursor();
        SQL = """(Select Departure_Date, Train_Number, COUNT(CASE WHEN Is_Cancelled = FALSE THEN 1 ELSE 0 END) FROM RESERVES
        INNER JOIN RESERVATION
        ON RESERVES.Reservation_ID = RESERVATION.Reservation_ID
        WHERE RESERVES.DEPARTURE_DATE >= %s
        AND RESERVES.DEPARTURE_DATE < %s
        AND Is_Cancelled = FALSE
        GROUP BY Train_Number 
        ORDER BY COUNT(Train_Number) DESC LIMIT 3)
        UNION
        (Select Departure_Date, Train_Number, COUNT(CASE WHEN Is_Cancelled = FALSE THEN 1 ELSE 0 END) FROM RESERVES
        INNER JOIN RESERVATION
        ON RESERVES.Reservation_ID = RESERVATION.Reservation_ID
        WHERE RESERVES.DEPARTURE_DATE >= %s
        AND RESERVES.DEPARTURE_DATE < %s
        AND Is_Cancelled = FALSE
        GROUP BY Train_Number 
        ORDER BY COUNT(Train_Number) DESC LIMIT 3)
        UNION
        (Select Departure_Date, Train_Number, COUNT(CASE WHEN Is_Cancelled = FALSE THEN 1 ELSE 0 END) FROM RESERVES
        INNER JOIN RESERVATION
        ON RESERVES.Reservation_ID = RESERVATION.Reservation_ID
        WHERE RESERVES.DEPARTURE_DATE >= %s
        AND RESERVES.DEPARTURE_DATE < %s
        AND Is_Cancelled = FALSE
        GROUP BY Train_Number 
        ORDER BY COUNT(Train_Number) DESC LIMIT 3)"""
        cursor.execute(SQL, (month3B, month3E, month2B, month2E, month1B, month1E))
        trainNamesAndReservations = cursor.fetchall()

        count = 1
        monthCount = 0
        
        for entry1 in trainNamesAndReservations:
            viewTrainList = [entry1[0], entry1[1], entry1[2]]

            if count % 2 == 0 or count == 0:
                color = "light grey"
            else:
                color = "white"

            l1 = Label(tableFrame1, text=viewTrainList[0].strftime("%B"), bg=color) #gets the month
            l2 = Label(tableFrame2, text=viewTrainList[1], bg=color)
            l3 = Label(tableFrame3, text=viewTrainList[2], bg=color)
            l1.grid(row=count, column=0, sticky=EW)
            l2.grid(row=count, column=0, sticky=EW)
            l3.grid(row=count, column=0, sticky=EW)
            count+=1

            if (count) % 3 == 0:
                monthCount+=1
            count+= 1
            
app = Trains()
	

	
