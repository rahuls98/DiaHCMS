from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk,Image
import datetime
import mysql.connector
import MySQLdb
conn = mysql.connector.connect(host="localhost",user="",password="",database="")
curs = conn.cursor()

def setBackground(root):
    img = ImageTk.PhotoImage(Image.open("/Users/rahuls98/Documents/Dia_stuff/10.jpg"))
    label = ttk.Label(root,image = img)
    label.image = img
    label.grid(row=0,column=0,columnspan=20,rowspan=20)

def setStyle(root):
    style = ttk.Style(root)
    style.theme_use('aqua')
    style.configure('.',font=('Baskerville', 20,))

def BSSubWindow(num):
    BS_sub_window = Toplevel()
    BS_categories = {1:'BS_AM',2:'BS_PM'}
    BS_type = BS_categories[num]
    BS_sub_window.title(BS_type)
    BS_sub_window.geometry("630x420+450+250")

    setBackground(BS_sub_window)
    setStyle(BS_sub_window)

    topFrame = Frame(BS_sub_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(BS_sub_window)
    bottomFrame.grid(row=18,column=0)

    #taken_var = IntVar()
    bs_entry_var = StringVar()

    #taken_status = ttk.Checkbutton(topFrame, text = "Checked", variable = taken_var)
    #taken_status.grid(row=0,column=1,sticky='NSWE')
    bs_amount_label = ttk.Label(topFrame, text = "Enter BS amount: ")
    bs_amount_label.grid(row=0,column=1,sticky='NSWE')
    bs_amount_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    bs_amount_entry.grid(row=1,column=1,sticky='NSWE')

    def BS_submit():
        if bs_amount_entry.get() == '':
            tkinter.messagebox.showinfo('ERROR!','Enter valid amount')
        else:
            now = datetime.datetime.now()
            todays_date = f'{now.year}-{now.month}-{now.day}'
            bs_tab_update = f'UPDATE PATIENT SET {BS_type} = %s WHERE DATE = %s'
            input_val = (bs_amount_entry.get(),todays_date)
            curs.execute(bs_tab_update, input_val)
            conn.commit()
            tkinter.messagebox.showinfo('DONE!',"Table Updated!")
            BS_sub_window.destroy()

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:BS_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    submit = ttk.Button(bottomFrame, text="SUBMIT",command=BS_submit)
    submit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def BSMainWindow():
    BS_main_window = Toplevel()
    BS_main_window.title('Blood Sugar')
    BS_main_window.geometry("630x420+450+250")

    setStyle(BS_main_window)
    setBackground(BS_main_window)

    topFrame = Frame(BS_main_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(BS_main_window)
    bottomFrame.grid(row=18,column=0)

    BS_AM = ttk.Button(topFrame, text = "BS AM", command=lambda:BSSubWindow(1))
    BS_AM.grid(row=1,column=1,sticky='NSEW',ipady=10, ipadx=50)
    BS_PM = ttk.Button(topFrame, text = "BS PM",command=lambda:BSSubWindow(2))
    BS_PM.grid(row=2,column=1,sticky='NSEW',ipady=10, ipadx=50)

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:BS_main_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)

def foodSubWindow(num):
    food_sub_window = Toplevel()
    food_categories = {1:'BREAKFAST',2:'AM Snack',3:'Lunch',4:'PM Snack',5:'Dinner'}
    food_type = food_categories[num]
    food_sub_window.title(food_type)
    food_sub_window.geometry("630x420+450+250")

    setBackground(food_sub_window)
    setStyle(food_sub_window)

    topFrame = Frame(food_sub_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(food_sub_window)
    bottomFrame.grid(row=18,column=0)

    #taken_var = IntVar()
    #taken_status = ttk.Checkbutton(topFrame, text = "Taken", variable = taken_var)
    #taken_status.grid(row=0,column=1,sticky='NSWE')
    bs_amount_label = ttk.Label(topFrame, text = "Enter BS amount: ")
    bs_amount_label.grid(row=1,column=1,sticky='NSWE')
    bs_amount_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    bs_amount_entry.grid(row=2,column=1,sticky='NSWE')
    ins_amount_label = ttk.Label(topFrame, text = "Enter Insulin amount: ")
    ins_amount_label.grid(row=3,column=1,sticky='NSWE')
    ins_amount_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    ins_amount_entry.grid(row=4,column=1,sticky='NSWE')

    def food_submit():
        try:
            if bs_amount_entry.get() == '' or ins_amount_entry.get() == '':
                tkinter.messagebox.showinfo('ERROR!','Enter valid amount')
            else:
                last_ins_ID = "SELECT * FROM INSULIN ORDER BY I_ID DESC LIMIT 1"
                curs.execute(last_ins_ID)
                for item in curs:
                    last_two = int(item[0][2:]) + 1
                    next_id = 'IN' + str(last_two).zfill(2)

                meal_plan = "SELECT * FROM MEAL_PLAN"
                curs.execute(meal_plan)
                for item in curs:
                    if num == int(item[0][2:]):
                        mealid = item[0]

                ins_table_entry = "INSERT INTO INSULIN VALUES(%s,curdate(),curtime(),%s,%s)"
                curs.execute(ins_table_entry, (next_id,ins_amount_entry.get(),bs_amount_entry.get()))

                food_table_entry = 'INSERT INTO MEAL_TAKEN VALUES(%s,%s,%s,%s)'
                input_val = (mealid,bs_amount_entry.get(),next_id,1)
                curs.execute(food_table_entry, input_val)
                conn.commit()
                tkinter.messagebox.showinfo('DONE!',"Table Updated!")
                food_sub_window.destroy()
        except mysql.connector.Error as err:
            tkinter.messagebox.showinfo('ERROR!',"Duplicate entry!")
            food_sub_window.destroy()

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:food_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    submit = ttk.Button(bottomFrame, text="SUBMIT",command=food_submit)
    submit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def foodMainWindow():
    food_main_window = Toplevel()
    food_main_window.title('Food')
    food_main_window.geometry("630x420+450+250")

    setStyle(food_main_window)
    setBackground(food_main_window)

    topFrame = Frame(food_main_window)
    topFrame.grid(row=10,column=0)
    bottomFrame = Frame(food_main_window)
    bottomFrame.grid(row=17,column=0)

    breakfast = ttk.Button(topFrame, text = "BREAKFAST", command=lambda:foodSubWindow(1))
    breakfast.grid(row=1,column=1,sticky='NSEW',ipady=10, ipadx=50)
    snack_am = ttk.Button(topFrame, text = "AM SNACKS",command=lambda:foodSubWindow(2))
    snack_am.grid(row=2,column=1,sticky='NSEW',ipady=10, ipadx=50)
    lunch = ttk.Button(topFrame, text = "LUNCH", command=lambda:foodSubWindow(3))
    lunch.grid(row=3,column=1,sticky='NSEW',ipady=10, ipadx=50)
    snack_pm = ttk.Button(topFrame, text = "PM SNACKS",command=lambda:foodSubWindow(4))
    snack_pm.grid(row=4,column=1,sticky='NSEW',ipady=10, ipadx=50)
    dinner = ttk.Button(topFrame, text = "DINNER", command=lambda:foodSubWindow(5))
    dinner.grid(row=5,column=1,sticky='NSEW',ipady=10, ipadx=50)

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:food_main_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)

def insCalcWindow():
    ins_calc_window = Toplevel()
    ins_calc_window.title('CALCULATE')
    ins_calc_window.geometry("630x420+450+250")

    setBackground(ins_calc_window)
    setStyle(ins_calc_window)

    topFrame = Frame(ins_calc_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(ins_calc_window)
    bottomFrame.grid(row=18,column=0)

    bs_amount_label = ttk.Label(topFrame, text = "Enter BS amount: ", font=('Baskerville',20))
    bs_amount_label.grid(row=1,column=1,sticky='NSWE')
    bs_amount_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    bs_amount_entry.grid(row=2,column=1,sticky='NSWE')
    dos_amount_label = ttk.Label(topFrame, text = "Required dosage: ", font=('Baskerville',20))
    dos_amount_label.grid(row=3,column=1,sticky='NSWE')
    dos_amount_disp = ttk.Entry(topFrame, font=('Baskerville',20))
    dos_amount_disp.grid(row=4,column=1,sticky='NSWE')
    dos_amount_disp.insert(0,'Sample')

    def calDosage():
        pass

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:ins_calc_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    calculate = ttk.Button(bottomFrame, text="CALCULATE",command=calDosage)
    calculate.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def insSubWindow():
    ins_sub_window = Toplevel()
    ins_sub_window.title("Insulin")
    ins_sub_window.geometry("630x420+450+250")

    setBackground(ins_sub_window)
    setStyle(ins_sub_window)

    topFrame = Frame(ins_sub_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(ins_sub_window)
    bottomFrame.grid(row=18,column=0)

    bs_amount_label = ttk.Label(topFrame, text = "Enter BS amount: ")
    bs_amount_label.grid(row=1,column=1,sticky='NSWE')
    bs_amount_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    bs_amount_entry.grid(row=2,column=1,sticky='NSWE')
    ins_amount_label = ttk.Label(topFrame, text = "Enter Insulin amount: ")
    ins_amount_label.grid(row=3,column=1,sticky='NSWE')
    ins_amount_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    ins_amount_entry.grid(row=4,column=1,sticky='NSWE')

    def ins_submit():
        if bs_amount_entry.get() == '' or ins_amount_entry.get() == '':
            tkinter.messagebox.showinfo('ERROR!','Enter valid amount')
        else:
            last_ins_ID = "SELECT * FROM INSULIN ORDER BY I_ID DESC LIMIT 1"
            curs.execute(last_ins_ID)
            for item in curs:
                last_two = int(item[0][2:]) + 1
                next_id = 'IN' + str(last_two).zfill(2)

            ins_table_entry = "INSERT INTO INSULIN VALUES(%s,curdate(),curtime(),%s,%s)"
            curs.execute(ins_table_entry, (next_id,ins_amount_entry.get(),bs_amount_entry.get()))
            conn.commit()
            tkinter.messagebox.showinfo('DONE!',"Table Updated!")
            ins_sub_window.destroy()

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:ins_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    submit = ttk.Button(bottomFrame, text="SUBMIT",command=ins_submit)
    submit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def insMainWindow():
    ins_main_window = Toplevel()
    ins_main_window.title('INSULIN')
    ins_main_window.geometry("630x420+450+250")

    setStyle(ins_main_window)
    setBackground(ins_main_window)

    topFrame = Frame(ins_main_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(ins_main_window)
    bottomFrame.grid(row=18,column=0)

    ins_calc = ttk.Button(topFrame, text = "CALCULATE", command=insCalcWindow)
    ins_calc.grid(row=1,column=1,sticky='NSEW',ipady=10, ipadx=50)
    ins_tab_entry = ttk.Button(topFrame, text = "INSULIN ENTRY",command=insSubWindow)
    ins_tab_entry.grid(row=2,column=1,sticky='NSEW',ipady=10, ipadx=50)

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:ins_main_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)

def PESubWindow(num):
    pe_sub_window = Toplevel()
    pe_categories = {1:'Aerobics',2:'Brisk Walking',3:'Cardio',4:'Running',5:'Weights'}
    pe_type = pe_categories[num]
    pe_sub_window.title(pe_type)
    pe_sub_window.geometry("630x420+450+250")

    setBackground(pe_sub_window)
    setStyle(pe_sub_window)

    topFrame = Frame(pe_sub_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(pe_sub_window)
    bottomFrame.grid(row=18,column=0)

    #date_label = ttk.Label(topFrame, text = "Enter Date: ", font=('Baskerville',20))
    #date_label.grid(row=1,column=1,sticky='NSWE')
    #date_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    #date_entry.grid(row=2,column=1,sticky='NSWE')
    dur_label = ttk.Label(topFrame, text = "Enter Duration: ", font=('Baskerville',20))
    dur_label.grid(row=2,column=1,sticky='NSWE')
    dur_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    dur_entry.grid(row=3,column=1,sticky='NSWE')

    def pe_submit():
        pe_plan = "SELECT * FROM PE_PLAN"
        curs.execute(pe_plan)
        for item in curs:
            if pe_type.lower() == item[1].lower():
                pe_id = item[0]

        pe_tab_insert = "INSERT INTO PE_DONE VALUES(%s,curdate(),curtime(),%s)"
        curs.execute(pe_tab_insert, (pe_id,dur_entry.get()))
        conn.commit()
        tkinter.messagebox.showinfo('DONE!',"Table Updated!")
        pe_sub_window.destroy()

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:pe_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    submit = ttk.Button(bottomFrame, text="SUBMIT",command=pe_submit)
    submit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def PEMainWindow():
    pe_main_window = Toplevel()
    pe_main_window.title('PE')
    pe_main_window.geometry("630x420+450+250")

    setStyle(pe_main_window)
    setBackground(pe_main_window)

    topFrame = Frame(pe_main_window)
    topFrame.grid(row=10,column=0)
    bottomFrame = Frame(pe_main_window)
    bottomFrame.grid(row=18,column=0)

    type_label = ttk.Label(topFrame, text = "Choose type of workout: ")
    type_label.grid(row=1,column=1,sticky='NSWE')
    wo1 = ttk.Button(topFrame, text = "AEROBICS", command=lambda:PESubWindow(1))
    wo1.grid(row=1,column=1,sticky='NSEW',ipady=10, ipadx=50)
    wo2 = ttk.Button(topFrame, text = "BRISK WALKING",command=lambda:PESubWindow(2))
    wo2.grid(row=2,column=1,sticky='NSEW',ipady=10, ipadx=50)
    wo3 = ttk.Button(topFrame, text = "CARDIO", command=lambda:PESubWindow(3))
    wo3.grid(row=3,column=1,sticky='NSEW',ipady=10, ipadx=50)
    wo4 = ttk.Button(topFrame, text = "RUNNING",command=lambda:PESubWindow(4))
    wo4.grid(row=4,column=1,sticky='NSEW',ipady=10, ipadx=50)
    wo5 = ttk.Button(topFrame, text = "WEIGHTS", command=lambda:PESubWindow(5))
    wo5.grid(row=5,column=1,sticky='NSEW',ipady=10, ipadx=50)

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:pe_main_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)

def anomalyWindow():
    anomaly_window = Toplevel()
    anomaly_window.title('ANOMALY')
    anomaly_window.geometry("630x420+450+250")

    setStyle(anomaly_window)
    setBackground(anomaly_window)

    topFrame = Frame(anomaly_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(anomaly_window)
    bottomFrame.grid(row=18,column=0)

    bs_amount_label = ttk.Label(topFrame, text = "Enter BS amount: ", font=('Baskerville',20))
    bs_amount_label.grid(row=0,column=1,sticky='NSWE')
    bs_amount_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    bs_amount_entry.grid(row=1,column=1,sticky='NSWE')
    #time_label = ttk.Label(topFrame, text = "Enter time: ", font=('Baskerville',20))
    #time_label.grid(row=3,column=1,sticky='NSWE')
    #time_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    #time_entry.grid(row=4,column=1,sticky='NSWE')
    desc_label = ttk.Label(topFrame, text = "Enter description: ", font=('Baskerville',20))
    desc_label.grid(row=2,column=1,sticky='NSWE')
    desc_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    desc_entry.grid(row=3,column=1,sticky='NSWE')


    def anomaly_submit():
        if bs_amount_entry.get()=='' or desc_entry.get()=='':
            tkinter.messagebox.showinfo('ERROR!','Enter valid amount')
        else:
            last_ano_id = "SELECT * FROM ANOMALY ORDER BY A_ID DESC LIMIT 1"
            curs.execute(last_ano_id)
            for item in curs:
                last_two = int(item[0][2:]) + 1
                next_id = 'AN' + str(last_two).zfill(2)

            ano_table_entry = "INSERT INTO ANOMALY VALUES(%s,curdate(),curtime(),%s,%s)"
            curs.execute(ano_table_entry, (next_id,bs_amount_entry.get(),desc_entry.get()))
            conn.commit()
            tkinter.messagebox.showinfo('DONE!',"Table Updated!")
            anomaly_window.destroy()

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:anomaly_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    submit = ttk.Button(bottomFrame, text="SUBMIT",command=anomaly_submit)
    submit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def driveWindow():
    drive_window = Toplevel()
    drive_window.title('DRIVING')
    drive_window.geometry("630x420+450+250")

    setStyle(drive_window)
    setBackground(drive_window)

    topFrame = Frame(drive_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(drive_window)
    bottomFrame.grid(row=18,column=0)

    bs_amount_label = ttk.Label(topFrame, text = "Enter BS amount: ", font=('Baskerville',20))
    bs_amount_label.grid(row=0,column=1,sticky='NSWE')
    bs_amount_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    bs_amount_entry.grid(row=1,column=1,sticky='NSWE')
    #time_label = ttk.Label(topFrame, text = "Enter time: ", font=('Baskerville',20))
    #time_label.grid(row=3,column=1,sticky='NSWE')
    #time_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    #time_entry.grid(row=4,column=1,sticky='NSWE')
    msg_label = ttk.Label(topFrame, text = "Message: ", font=('Baskerville',20))
    msg_label.grid(row=3,column=1,sticky='NSWE')
    desc_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    desc_entry.grid(row=4,column=1,sticky='NSWE')

    def driveSubmit():
        pass

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:drive_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    submit = ttk.Button(bottomFrame, text="CHECK",command=driveSubmit)
    submit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def medWindow():
    m_main_window = Toplevel()
    m_main_window.title('MEDICATION PLAN')
    m_main_window.geometry("630x420+450+250")

    setStyle(m_main_window)
    setBackground(m_main_window)

    topFrame = Frame(m_main_window)
    topFrame.grid(row=12,column=0)
    bottomFrame = Frame(m_main_window)
    bottomFrame.grid(row=19,column=0)

    selected_med = ['def_name','def_time']

    def onselect(evt):
        w = evt.widget
        index = w.curselection()[0]
        med_name = w.get(index)
        med_time = w.get(index+1)
        result = tkinter.messagebox.askyesno("You selected ", f"{med_name}\n{med_time}\nConfirm that you haven't taken the stated medication!")
        if result == True:
            selected_med[0] = med_name
            selected_med[1] = med_time
        else:
            tkinter.messagebox.showinfo("Try again","SELECT CORRECT NAME AGAIN")

    display = Listbox(topFrame, font=('Baskerville',20))
    display.pack(fill=BOTH, expand=YES, side=LEFT)
    scroll = Scrollbar(topFrame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)

    display.bind('<<ListboxSelect>>', onselect)

    instr = ttk.Label(bottomFrame, text='Select name from list ',font=('Baskerville',20))
    instr.grid(row=0,column=1,sticky='NSEW')
    instr = ttk.Label(bottomFrame, text='if medication not taken',font=('Baskerville',20))
    instr.grid(row=0,column=2,sticky='NSEW')


    get_mp_rows = "SELECT * FROM MEDICATION"
    curs.execute(get_mp_rows)
    for item in curs:
        display.insert(END, item[1],item[2],' ')

    def onConfirm():
        if selected_med[0]=='def_name' and selected_med[1]=='def_time':
            tkinter.messagebox.showinfo("Try again","Nothing selected")
        else:
            taken_update = ("UPDATE MEDICATION SET TAKEN_STATUS = 0 WHERE NAME = %s AND TIME = %s")
            input_val = (selected_med[0],selected_med[1])
            curs.execute(taken_update, input_val)
            conn.commit()

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:m_main_window.destroy())
    back.grid(row=1,column=1,sticky='NSEW',ipady=5)
    confirm = ttk.Button(bottomFrame, text="CONFIRM CHANGES",command=onConfirm)
    confirm.grid(row=1,column=2,sticky='NSEW',ipady=5)

def foodPlanDelWindow():
    fp3_sub_window = Toplevel()
    fp3_sub_window.title('FOOD PLAN')
    fp3_sub_window.geometry("630x420+450+250")

    setStyle(fp3_sub_window)
    setBackground(fp3_sub_window)

    topFrame = Frame(fp3_sub_window)
    topFrame.grid(row=9,column=0)
    bottomFrame = Frame(fp3_sub_window)
    bottomFrame.grid(row=18,column=0)

    display = Listbox(topFrame, font=('Baskerville',20))
    display.pack(fill=BOTH, expand=YES, side=LEFT)
    scroll = Scrollbar(topFrame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)

    get_fp_rows = "SELECT * FROM MEAL_PLAN"
    curs.execute(get_fp_rows)
    for item in curs:
        display.insert(END, item[0],item[1],item[2],' ')

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:fp3_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    confirm = ttk.Button(bottomFrame, text="CONFIRM")#,command=foodPlanSubWindow)
    confirm.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def foodPlanAddWindow():
    fp2_sub_window = Toplevel()
    fp2_sub_window.title('FOOD PLAN')
    fp2_sub_window.geometry("630x420+450+250")

    setStyle(fp2_sub_window)
    setBackground(fp2_sub_window)

    topFrame = Frame(fp2_sub_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(fp2_sub_window)
    bottomFrame.grid(row=18,column=0)

    time_label = ttk.Label(topFrame, text = "Enter Time: ", font=('Baskerville',20))
    time_label.grid(row=1,column=1,sticky='NSWE')
    time_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    time_entry.grid(row=2,column=1,sticky='NSWE')
    nutr_label = ttk.Label(topFrame, text = "Enter Nutrition: ", font=('Baskerville',20))
    nutr_label.grid(row=3,column=1,sticky='NSWE')
    nutr_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    nutr_entry.grid(row=4,column=1,sticky='NSWE')

    def fp2_submit():
        pass

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:fp2_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    submit = ttk.Button(bottomFrame, text="SUBMIT",command=fp2_submit)
    submit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def foodPlanSubWindow():
    fp_sub_window = Toplevel()
    fp_sub_window.title('FOOD PLAN')
    fp_sub_window.geometry("630x420+450+250")

    setStyle(fp_sub_window)
    setBackground(fp_sub_window)

    topFrame = Frame(fp_sub_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(fp_sub_window)
    bottomFrame.grid(row=18,column=0)

    fp_add = ttk.Button(topFrame, text = "ADD", command=foodPlanAddWindow)
    fp_add.grid(row=1,column=1,sticky='NSEW',ipady=10, ipadx=50)
    fp_del = ttk.Button(topFrame, text = "DELETE",command=foodPlanDelWindow)
    fp_del.grid(row=2,column=1,sticky='NSEW',ipady=10, ipadx=50)

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:fp_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)

def foodPlanMainWindow():
    fp_main_window = Toplevel()
    fp_main_window.title('FOOD PLAN')
    fp_main_window.geometry("630x420+450+250")

    setStyle(fp_main_window)
    setBackground(fp_main_window)

    topFrame = Frame(fp_main_window)
    topFrame.grid(row=9,column=0)
    bottomFrame = Frame(fp_main_window)
    bottomFrame.grid(row=18,column=0)

    display = Listbox(topFrame, font=('Baskerville',20))
    display.pack(fill=BOTH, expand=YES, side=LEFT)
    scroll = Scrollbar(topFrame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)

    get_fp_rows = "SELECT * FROM MEAL_PLAN"
    curs.execute(get_fp_rows)
    for item in curs:
        display.insert(END, item[0],item[1],item[2],' ')

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:fp_main_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    edit = ttk.Button(bottomFrame, text="EDIT",command=foodPlanSubWindow)
    edit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def pePlanDelWindow():
    pp3_sub_window = Toplevel()
    pp3_sub_window.title('PE PLAN')
    pp3_sub_window.geometry("630x420+450+250")

    setStyle(pp3_sub_window)
    setBackground(pp3_sub_window)

    topFrame = Frame(pp3_sub_window)
    topFrame.grid(row=9,column=0)
    bottomFrame = Frame(pp3_sub_window)
    bottomFrame.grid(row=18,column=0)

    display = Listbox(topFrame, font=('Baskerville',20))
    display.pack(fill=BOTH, expand=YES, side=LEFT)
    scroll = Scrollbar(topFrame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)

    get_fp_rows = "SELECT * FROM MEAL_PLAN"
    curs.execute(get_fp_rows)
    for item in curs:
        display.insert(END, item[0],item[1],' ')

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:pp3_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    confirm = ttk.Button(bottomFrame, text="CONFIRM")#,command=pePlanSubWindow)
    confirm.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def pePlanAddWindow():
    pp2_sub_window = Toplevel()
    pp2_sub_window.title('PE PLAN')
    pp2_sub_window.geometry("630x420+450+250")

    setStyle(pp2_sub_window)
    setBackground(pp2_sub_window)

    topFrame = Frame(pp2_sub_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(pp2_sub_window)
    bottomFrame.grid(row=18,column=0)

    type_label = ttk.Label(topFrame, text = "Enter type of workout: ", font=('Baskerville',20))
    type_label.grid(row=1,column=1,sticky='NSWE')
    type_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    type_entry.grid(row=2,column=1,sticky='NSWE')

    def pp2_submit():
        pass

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:pp2_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    submit = ttk.Button(bottomFrame, text="SUBMIT",command=pp2_submit)
    submit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def pePlanSubWindow():
    pp_sub_window = Toplevel()
    pp_sub_window.title('PE PLAN')
    pp_sub_window.geometry("630x420+450+250")

    setStyle(pp_sub_window)
    setBackground(pp_sub_window)

    topFrame = Frame(pp_sub_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(pp_sub_window)
    bottomFrame.grid(row=18,column=0)

    pp_add = ttk.Button(topFrame, text = "ADD", command=pePlanAddWindow)
    pp_add.grid(row=1,column=1,sticky='NSEW',ipady=10, ipadx=50)
    pp_del = ttk.Button(topFrame, text = "DELETE", command=pePlanDelWindow)
    pp_del.grid(row=2,column=1,sticky='NSEW',ipady=10, ipadx=50)

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:pp_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)

def pePlanMainWindow():
    pp_main_window = Toplevel()
    pp_main_window.title('PE PLAN')
    pp_main_window.geometry("630x420+450+250")

    setStyle(pp_main_window)
    setBackground(pp_main_window)

    topFrame = Frame(pp_main_window)
    topFrame.grid(row=9,column=0)
    bottomFrame = Frame(pp_main_window)
    bottomFrame.grid(row=18,column=0)

    display = Listbox(topFrame, font=('Baskerville',20))
    display.pack(fill=BOTH, expand=YES, side=LEFT)
    scroll = Scrollbar(topFrame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)

    get_fp_rows = "SELECT * FROM MEAL_PLAN"
    curs.execute(get_fp_rows)
    for item in curs:
        display.insert(END, item[0],item[1],' ')

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:pp_main_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    edit = ttk.Button(bottomFrame, text="EDIT",command=pePlanSubWindow)
    edit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def medPlanDelWindow():
    mp3_sub_window = Toplevel()
    mp3_sub_window.title('MEDICATION PLAN')
    mp3_sub_window.geometry("630x420+450+250")

    setStyle(mp3_sub_window)
    setBackground(mp3_sub_window)

    topFrame = Frame(mp3_sub_window)
    topFrame.grid(row=9,column=0)
    bottomFrame = Frame(mp3_sub_window)
    bottomFrame.grid(row=18,column=0)

    selected_med = ['def_name','def_time']

    def onselect(evt):
        w = evt.widget
        index = w.curselection()[0]
        med_name = w.get(index)
        med_time = w.get(index+1)
        result = tkinter.messagebox.askyesno("You selected ", f"{med_name}\n{med_time}\nConfirm that you want to delete this entry!")
        if result == True:
            selected_med[0] = med_name
            selected_med[1] = med_time
        else:
            tkinter.messagebox.showinfo("Try again","SELECT CORRECT NAME AGAIN")

    display = Listbox(topFrame, font=('Baskerville',20))
    display.pack(fill=BOTH, expand=YES, side=LEFT)
    scroll = Scrollbar(topFrame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)

    display.bind('<<ListboxSelect>>', onselect)

    get_mp_rows = "SELECT * FROM MEDICATION"
    curs.execute(get_mp_rows)
    for item in curs:
        display.insert(END, item[1],item[2],item[3],' ')

    def delOnConfirm():
        med_del_query = ("DELETE FROM MEDICATION WHERE NAME = %s AND TIME = %s")
        input_val = (selected_med[0],selected_med[1])
        curs.execute(med_del_query, input_val)
        conn.commit()
        tkinter.messagebox.showinfo('DONE!',"Table Updated!")

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:mp3_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    confirm = ttk.Button(bottomFrame, text="CONFIRM",command=delOnConfirm)
    confirm.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def medPlanAddWindow():
    mp2_sub_window = Toplevel()
    mp2_sub_window.title('MEDICATION PLAN')
    mp2_sub_window.geometry("630x420+450+250")

    setStyle(mp2_sub_window)
    setBackground(mp2_sub_window)

    topFrame = Frame(mp2_sub_window)
    topFrame.grid(row=8,column=0)
    bottomFrame = Frame(mp2_sub_window)
    bottomFrame.grid(row=18,column=0)

    name_label = ttk.Label(topFrame, text = "Name of medication: ", font=('Baskerville',20))
    name_label.grid(row=1,column=1,sticky='NSWE')
    name_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    name_entry.grid(row=2,column=1,sticky='NSWE')
    time_label = ttk.Label(topFrame, text = "Time to be taken: ", font=('Baskerville',20))
    time_label.grid(row=3,column=1,sticky='NSWE')
    time_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    time_entry.grid(row=4,column=1,sticky='NSWE')
    quan_label = ttk.Label(topFrame, text = "Enter quantity: ", font=('Baskerville',20))
    quan_label.grid(row=5,column=1,sticky='NSWE')
    quan_entry = ttk.Entry(topFrame, font=('Baskerville',20))
    quan_entry.grid(row=6,column=1,sticky='NSWE')

    def mp2_submit():
        if name_entry.get() == '' or time_entry.get() == '' or quan_entry.get() == '':
            tkinter.messagebox.showinfo('ERROR!','Enter valid amount')
        else:
            last_med_ID = "SELECT * FROM MEDICATION ORDER BY MED_ID DESC LIMIT 1"
            curs.execute(last_med_ID)
            for item in curs:
                last_two = int(item[0][2:]) + 1
                next_id = 'ME' + str(last_two).zfill(2)

            med_table_entry = "INSERT INTO MEDICATION VALUES(%s,%s,%s,%s,%s)"
            curs.execute(med_table_entry, (next_id,name_entry.get(),time_entry.get(),quan_entry.get(),1))
            conn.commit()
            tkinter.messagebox.showinfo('DONE!',"Table Updated!")
            mp2_sub_window.destroy()

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:mp2_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    submit = ttk.Button(bottomFrame, text="SUBMIT",command=mp2_submit)
    submit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def medPlanSubWindow():
    mp_sub_window = Toplevel()
    mp_sub_window.title('MEDICATION PLAN')
    mp_sub_window.geometry("630x420+450+250")

    setStyle(mp_sub_window)
    setBackground(mp_sub_window)

    topFrame = Frame(mp_sub_window)
    topFrame.grid(row=4,column=0)
    bottomFrame = Frame(mp_sub_window)
    bottomFrame.grid(row=18,column=0)

    mp_add = ttk.Button(topFrame, text = "ADD", command=medPlanAddWindow)
    mp_add.grid(row=1,column=1,sticky='NSEW',ipady=10, ipadx=50)
    mp_del = ttk.Button(topFrame, text = "DELETE",command=medPlanDelWindow)
    mp_del.grid(row=2,column=1,sticky='NSEW',ipady=10, ipadx=50)

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:mp_sub_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)

def medPlanMainWindow():
    mp_main_window = Toplevel()
    mp_main_window.title('MEDICATION PLAN')
    mp_main_window.geometry("630x420+450+250")

    setStyle(mp_main_window)
    setBackground(mp_main_window)

    topFrame = Frame(mp_main_window)
    topFrame.grid(row=9,column=0)
    bottomFrame = Frame(mp_main_window)
    bottomFrame.grid(row=18,column=0)

    display = Listbox(topFrame, font=('Baskerville',20))
    display.pack(fill=BOTH, expand=YES, side=LEFT)
    scroll = Scrollbar(topFrame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)

    get_mp_rows = "SELECT * FROM MEDICATION"
    curs.execute(get_mp_rows)
    for item in curs:
        display.insert(END, item[1],item[2],item[3],' ')

    back = ttk.Button(bottomFrame, text="BACK",command=lambda:mp_main_window.destroy())
    back.grid(row=0,column=1,sticky='NSEW',ipady=10, ipadx=20)
    edit = ttk.Button(bottomFrame, text="EDIT",command=medPlanSubWindow)
    edit.grid(row=0,column=2,sticky='NSEW',ipady=10, ipadx=20)

def submitMain():
    upd_patient_food = "UPDATE PATIENT P, (SELECT COUNT(*) AS TOT FROM MEAL_TAKEN GROUP BY TAKEN_STATUS) MT SET P.FOOD ='Y' WHERE MT.TOT = 5 AND P.DATE = CURDATE()"
    curs.execute(upd_patient_food)
    upd_patient_med = "UPDATE PATIENT P, (SELECT SUM(TAKEN_STATUS) AS TS, COUNT(*) AS C FROM MEDICATION) MED SET P.MEDS = 'Y' WHERE MED.TS = MED.C AND P.DATE = CURDATE()"
    curs.execute(upd_patient_med)
    upd_patient_pe = "UPDATE PATIENT P, (SELECT PE.DATE,SUM(DURATION) AS TOTD FROM PE_DONE PE GROUP BY PE.DATE) T SET P.PE='Y' WHERE T.TOTD>30 AND P.DATE= T.DATE"
    curs.execute(upd_patient_pe)

    del_meal_taken = "DELETE FROM MEAL_TAKEN"
    curs.execute(del_meal_taken)
    del_pe_done = "DELETE FROM PE_DONE"
    curs.execute(del_pe_done)

    conn.commit()

def main():
    root = Tk()
    root.title("DiaHCMS")
    root.geometry("630x420+450+250")

    setStyle(root)
    setBackground(root)

    #BUTTONS FOR DYNAMIC TABLES
    BS = ttk.Button(root,text = "BLOOD SUGAR",command=BSMainWindow)
    BS.grid(row=2,column=1,sticky = "NSEW")
    FOOD = ttk.Button(root,text = "FOOD",command=foodMainWindow)
    FOOD.grid(row=3,column=1,sticky = "NSEW")
    INSULIN = ttk.Button(root,text = "INSULIN",command=insMainWindow)
    INSULIN.grid(row=4,column=1,sticky = "NSEW")
    PE = ttk.Button(root,text = "PE",command=PEMainWindow)
    PE.grid(row=5,column=1,sticky = "NSEW")
    ANOMALY = ttk.Button(root,text = "ANOMALY",command=anomalyWindow)
    ANOMALY.grid(row=6,column=1,sticky = "NSEW")
    DRIVE = ttk.Button(root,text = "DRIVING",command=driveWindow)
    DRIVE.grid(row=7,column=1,sticky = "NSEW")
    MEDS = ttk.Button(root,text = "MEDICATION",command=medWindow)
    MEDS.grid(row=8,column=1,sticky = "NSEW")

    #BUTTONS FOR STATIC TABLES
    FOOD_PLAN = ttk.Button(root,text = "FOOD PLAN",command=foodPlanMainWindow)
    FOOD_PLAN.grid(row=11,column=1,sticky = "NSEW")
    PE_PLAN = ttk.Button(root,text = "PE PLAN",command=pePlanMainWindow)
    PE_PLAN.grid(row=12,column=1,sticky = "NSEW")
    MEDICATION = ttk.Button(root,text = "MEDICATION PLAN",command=medPlanMainWindow)
    MEDICATION.grid(row=13,column=1,sticky = "NSEW")
    SUBMIT = ttk.Button(root,text = "SUBMIT",command=submitMain)
    SUBMIT.grid(row=16,column=1,sticky = "NSEW")

    root.mainloop()

if __name__ == '__main__':
    main()
