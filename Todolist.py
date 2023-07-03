from tkinter import font
from tkinter import messagebox
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import *
import time


# Register Page
def register_page():
    register_page = tk.Toplevel()
    register_page.title("JCO Register Page")
    register_page.geometry("600x400")
    register_page.iconbitmap("JCO.ico")
    register_page.configure(bg="#7EB2DD"'')

    registerframe = tk.Frame(register_page, bg="#7EB2DD")
    registerframe.pack()

    # check the data that user input for register
    def check_everything():
        if len(Username_entry.get()) != 0:
            email_confirm1 = "@"
            email_confirm2 = ".com"
            if email_confirm1 in Email_Entry.get() and email_confirm2 in Email_Entry.get():
                password = Password_Entry.get()
                confirm_password = Confirm_Password_Entry.get()
                if len(password) != 0 or len(confirm_password) != 0:
                    if password == confirm_password:
                        register()
                    else:
                        messagebox.showerror("ERROR!", "Two password are not the same!", icon="error")
                else:
                    messagebox.showerror("ERROR!", "Please fill up password and confirm password boxes!", icon="error")
            else:
                tk.messagebox.showerror("INVALID EMAIL", "this is not a valid email!", icon="error")
        else:
            tk.messagebox.showerror("ERROR", "Please type username!", icon="error")

    def show_password():

        if Password_Entry.cget("show"):
            Password_Entry.config(show="")
        else:
            Password_Entry.config(show="*")

        if Confirm_Password_Entry.cget("show"):
            Confirm_Password_Entry.config(show="")
        else:
            Confirm_Password_Entry.config(show="*")

    def register():
        username = Username_entry.get()
        password = Password_Entry.get()
        email = Email_Entry.get()

        # database
        conn = sqlite3.connect('todolist.db')
        create_table = '''
               CREATE TABLE IF NOT EXISTS Task_Information
               (USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,username TEXT , password TEXT , email TEXT )
               '''
        conn.execute(create_table)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM User_Information WHERE username=? OR email=?''', (username, email,))
        check_user_input = cursor.fetchone()
        if check_user_input is not None:
            tk.messagebox.showinfo("USED ERROR", "This username or email already used!")
        else:
            insert_table = '''
                    INSERT INTO User_Information 
                    (username , password , email) 
                    VALUES 
                    (? , ? , ?);
                    '''

            insert_tuple = (username, password, email)
            cursor.execute(insert_table, insert_tuple)
            tk.messagebox.showinfo("REGISTERED", "Register complete,thank you!")
            register_page.destroy()

        conn.commit()
        conn.close()

    welcome = tk.Label(registerframe, text="Register Page", font=("8514oem", 50), bg="#7EB2DD", fg="Lightcyan")
    welcome.grid(row=1, column=1, pady=40, columnspan=2)

    Register_entry = Frame(registerframe, bg="#7EB2DD")
    Register_entry.grid(row=2, column=1)

    word = tk.Label(Register_entry, text="             Username:", font=("8514oem", 12), bg="#7EB2DD", fg="Lightcyan")
    word.grid(row=2, column=1, padx=10, pady=10)
    Username_entry = tk.Entry(Register_entry, bg="#e5eff8", bd=3)
    Username_entry.grid(row=2, column=2, padx=10, pady=10)

    word2 = tk.Label(Register_entry, text="                Email:", font=("8514oem", 12), bg="#7EB2DD", fg="Lightcyan")
    word2.grid(row=3, column=1, padx=10, pady=10)
    Email_Entry = tk.Entry(Register_entry, bg="#e5eff8", bd=3)
    Email_Entry.grid(row=3, column=2, padx=10, pady=10)

    word3 = tk.Label(Register_entry, text="         New password:", font=("8514oem", 12), bg="#7EB2DD", fg="Lightcyan")
    word3.grid(row=4, column=1, padx=10, pady=10)
    Password_Entry = tk.Entry(Register_entry, show="*", bg="#e5eff8", bd=3)
    Password_Entry.grid(row=4, column=2, padx=10, pady=10)

    word4 = tk.Label(Register_entry, text="Confirm your password:", font=("8514oem", 12), bg="#7EB2DD", fg="Lightcyan")
    word4.grid(row=5, column=1, padx=10, pady=10)
    Confirm_Password_Entry = tk.Entry(Register_entry, show="*", bg="#e5eff8", bd=3)
    Confirm_Password_Entry.grid(row=5, column=2, padx=10, pady=10)

    Register_Button_Frame = Frame(registerframe, bg="#7EB2DD")
    Register_Button_Frame.grid(row=3, column=1)

    cbutton = Checkbutton(Register_Button_Frame, text="show password", font=button_font, bg="#7EB2DD", fg="Lightcyan",
                          command=show_password, activebackground="#7EB2DD", selectcolor="lightblue3")
    cbutton.grid(row=1, column=3, padx=10, pady=10)

    space = tk.Label(Register_Button_Frame, text="                  ", bg="#7EB2DD")
    space.grid(row=1, column=2)

    button = tk.Button(Register_Button_Frame, text="Submit", bg="#71a0c6", font=("8514oem", 12, 'bold'), fg="Lightcyan",
                       command=check_everything, padx=30, pady=10, activebackground="#71a0c6")
    button.grid(row=1, column=1)


# Main Page
n = 0


def main_page(USER_ID):
    root = tk.Tk()
    root.title('Welcome to JCO Todoapp-version0.9alpha')
    root.geometry('1050x400')
    root.iconbitmap("JCO.ico")
    root.configure(bg="#7EB2DD")

    # connect to the database
    conn = sqlite3.connect('todolist.db')
    cursor = conn.cursor()

    # create the Task_Information table if it doesn't exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Task_Information"
        "(Task_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,Task_name TEXT, "
        "Due_date TEXT,Task_state TEXT,Days_left TEXT,USER_ID INTEGER)")
    conn.commit()

    # calendar and getting the date
    def calendar():
        calendar_page = tk.Toplevel(root, bg="#7EB2DD")
        cal = Calendar(calendar_page, selectmode='day', date_pattern='y-mm-dd')
        cal.pack()

        def get_date():
            due_date = cal.get_date()
            show_due_date.config(text=due_date)
            print(due_date)
            calendar_page.destroy()

        button = tk.Button(calendar_page, text="Choose this date", command=get_date, fg="Lightcyan", bg="#71a0c6",
                           activebackground="#71a0c6", font=("8514oem"))
        button.pack()

    # add task into treeview and database
    def add():
        due_date = show_due_date.cget("text")
        task_name = task_name_enter.get()
        if task_name == "":
            tk.messagebox.showerror("ERROR", "Please fill up the task name!", icon="error")
        else:
            # connect to the database and retrieve the maximum task ID
            cursor.execute("SELECT MAX(Task_ID) FROM Task_Information")
            result = cursor.fetchone()
            n = result[0] if result[0] else 0
            task_state = "processing"
            task_name_enter.delete(0, END)
            if due_date == "":
                due_date = "NO DUE DATE"
                tree.insert("", 'end', iid=n, values=(n, task_name, due_date, 'Processing'))
                cursor.execute("INSERT INTO Task_Information (Task_name,Due_date,Task_state,USER_ID)"
                               "VALUES ( ? , ? , ? , ? )", (task_name, due_date, task_state, USER_ID))
            else:
                tree.insert("", 'end', iid=n, values=(n, task_name, due_date, 'Processing'))
                cursor.execute("INSERT INTO Task_Information (Task_name,Due_date,Task_state,USER_ID)"
                               "VALUES ( ? , ? , ? , ? )", (task_name, due_date, task_state, USER_ID))
            update_days_left()

    # calculate days left and update it
    def update_days_left():
        cursor.execute("SELECT * FROM Task_Information")
        rows = cursor.fetchall()

        # update the days left for every row inside database
        for row in rows:
            get_time = row[2]
            print(get_time)
            if get_time == "NO DUE DATE":
                no_days_left = "NONE"
                cursor.execute("UPDATE Task_Information SET Days_left = ? WHERE Due_date = ?", (no_days_left, row[2]))
            else:
                new_time = datetime.strptime(get_time, "%Y-%m-%d")
                current_date = datetime.now().date()
                remaining_days = (new_time.date() - current_date).days

                if remaining_days < 0:
                    late_text = "LATE"
                else:
                    late_text = str(remaining_days)

                cursor.execute("UPDATE Task_Information SET Days_left = ? WHERE Due_date = ?", (late_text, row[2]))

            for row in tree.get_children():
                tree.delete(row)

            cursor.execute("SELECT * FROM Task_Information WHERE USER_ID = ?", (USER_ID,))
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", 'end', values=row)
            conn.commit()

    def delete():
        selected_items = tree.selection()
        if selected_items:
            for item in selected_items:
                item_name = tree.item(item)['values'][1]
                tree.delete(item)
                # delete data from the database
                cursor.execute("DELETE FROM Task_Information WHERE Task_name = ?", (item_name,))
                conn.commit()
        else:
            tk.messagebox.showerror("ERROR", "You cannot delete the air!", icon='error')

    def finish_task():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            values = item['values']

            Task_name_get = values[1]
            Due_date_get = values[2]
            tree.set(selected_item, 'Process', 'Finished')
            cursor.execute("UPDATE Task_Information SET Task_state = 'Finished' "
                           "WHERE Task_name = ? AND Due_date = ?", (Task_name_get, Due_date_get))
            conn.commit()
        else:
            tk.messagebox.showerror("ERROR", "You cannot finish NOTHING!", icon='error')

    def edit_task_details():
        # fetch the selected row of data
        selected_item = tree.focus()
        if selected_item != "":
            item_id = tree.item(selected_item)['values'][0]
            task_name = tree.item(selected_item)['values'][1]
            due_date = tree.item(selected_item)['values'][2]

            # Create a new window for editing the task details
            edit_window = tk.Toplevel(root)
            edit_window.title("Edit Task Details")
            edit_window.geometry('600x200')
            edit_window.configure(bg="#7EB2DD")

            # Create labels and entry fields for task name and due date in the edit window
            task_box = tk.Frame(edit_window, bg="#7EB2DD")
            task_box.grid(row=0, column=0)
            tk.Label(task_box, text="Task Name:", bg="#7EB2DD", fg="Lightcyan", font=("8514oem")).grid(row=0, column=0)
            task_name_entry = Entry(task_box,width=35)
            task_name_entry.insert(END, task_name)
            task_name_entry.grid(row=0, column=1)

            tk.Label(task_box, text=" Due Date:", bg="#7EB2DD", fg="Lightcyan", font=("8514oem")).grid(row=1, column=0)
            due_date_entry = tk.Label(task_box, text=due_date, bg="#7EB2DD", font=("8514oem"), fg="Lightcyan")
            due_date_entry.grid(row=1, column=1)

            cal2 = Calendar(edit_window, selectmode='day', date_pattern='y-mm-dd')
            cal2.grid(row=0, column=1)

            def choose_date():
                selected_date = cal2.get_date()
                due_date_entry.config(text=str(selected_date))

            # Add a button to open the calendar widget for selecting a date
            calendar_button = tk.Button(task_box, text="Select Date", command=choose_date, fg="Lightcyan", bg="#71a0c6",
                                        activebackground="#71a0c6", font=("8514oem"))
            calendar_button.grid(row=2, column=0)

            # Function to save the edited task details
            def save_edited_details():
                edited_task_name = task_name_entry.get()
                selected_date = due_date_entry.cget("text")

                # Update the task details in the treeview
                tree.item(selected_item, values=(item_id, edited_task_name, selected_date, 'processing'))

                # Update the task details in the database
                cursor.execute("UPDATE Task_Information SET Task_name = ?, Due_date = ? WHERE Task_ID = ?",
                               (edited_task_name, selected_date, item_id))
                conn.commit()

                # Close the edit window
                edit_window.destroy()

                update_days_left()

            # Create a save button to update the task details
            save_button = tk.Button(task_box, text="Save", command=save_edited_details, padx=20, fg="Lightcyan",
                                    bg="#71a0c6",
                                    activebackground="#71a0c6", font=("8514oem"))
            save_button.grid(row=2, column=1)
        else:
            tk.messagebox.showerror("ERROR", "You must choose a task to edit!", icon='error')

    # set a reminder that remind user
    def set_reminder():
        cursor.execute("SELECT * FROM Task_Information WHERE USER_ID = ?", (USER_ID,))
        rows = cursor.fetchall()
        for row in rows:
            get_days_left = row[4]
            get_task_name = row[1]
            progress = row[3]
            if progress == "processing":
                print(get_days_left)
                if get_days_left == "NONE":
                    continue
                elif get_days_left == "LATE":
                    message = "You are LATE to do this task the due date is over:\n " + get_task_name
                    tk.messagebox.showwarning("Attention", message, icon='warning')
                else:
                    get_days_left = int(get_days_left)
                    if get_days_left == 3:
                        message = "you only have 3 DAYS left to do this task:\n " + get_task_name
                        tk.messagebox.showwarning("Attention", message, icon='warning')
                    elif get_days_left == 2:
                        message = "you only have 2 DAYS left to do this task:\n " + get_task_name
                        tk.messagebox.showwarning("Attention", message, icon='warning')
                    elif get_days_left == 1:
                        message = "you only have 1 DAY left to do this task:\n " + get_task_name
                        tk.messagebox.showwarning("Attention", message, icon='warning')
                    elif get_days_left == 0:
                        message = "TODAY is the due date to do this task:\n " + get_task_name
                        tk.messagebox.showwarning("Attention", message, icon='warning')
                    else:
                        continue
            else:
                continue
        conn.commit()

    # looper
    def check_time():
        current_time = time.strftime("%H:%M:%S")
        print("current time：", current_time)
        # execute reminder for every loop
        set_reminder()
        # loop every 10 minutes
        root.after(600000, check_time)

    # start the looper
    check_time()

    # entry_frame
    entry_frame = tk.LabelFrame(root, text="Entries", bg="#7EB2DD", fg="Lightcyan", font=("8514oem"))
    entry_frame.grid(row=0, column=0, columnspan=3, sticky="news")
    task_name = tk.Label(entry_frame, text="Task Name", fg="Lightcyan", bg="#7EB2DD", font=("8514oem"))
    task_name.grid(row=0, column=0)
    task_name_enter = Entry(entry_frame, bg="#e5eff8",width=45)
    task_name_enter.grid(row=0, column=1)
    blank = tk.Label(entry_frame, text=" ", font=("Cambria", 12), bg="#7EB2DD")
    blank.grid(row=0, column=2)
    calendar_task = tk.Button(entry_frame, text="Choose Date", command=calendar, fg="Lightcyan", bg="#71a0c6",
                              activebackground="#71a0c6", font=("8514oem"))
    calendar_task.grid(row=0, column=3)
    show_due_date = tk.Label(entry_frame, text="", font=("Cambria", 12), bg="#7EB2DD")
    show_due_date.grid(row=0, column=4)

    # task_frame
    Task_frame = tk.LabelFrame(root, text="Tasks", bg="#7EB2DD", fg="Lightcyan", font=("8514oem"))
    Task_frame.grid(row=2, column=0, columnspan=3, sticky="news")
    columns = ('Task_ID', 'Task_name', 'Due_date', 'Process', 'Days Left')
    tree = ttk.Treeview(Task_frame, columns=columns, show='headings')
    tree.column('Task_ID', width=50)
    tree.column('Task_name', width=700)
    tree.column('Due_date', width=100)
    tree.column('Process', width=100)
    tree.column('Days Left', width=60)

    # add columns to the treeview
    for col in columns:
        tree.heading(col, text=col)

    # configure scrollbar for the treeview
    scrollbar = ttk.Scrollbar(Task_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    update_days_left()
    # update the days left for every task when it is midnight
    while True:
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        time_to_midnight = (midnight - now).total_seconds()

        # check if is midnight
        if time_to_midnight <= 0:
            update_days_left()
            break

        # wait until midnight
        time.sleep(time_to_midnight)

    # pack the treeview
    tree.pack()

    # function_frame
    Function_frame = tk.LabelFrame(root, text='Functions', bg="#7EB2DD", fg="Lightcyan", font=("8514oem"))
    Function_frame.grid(row=1, column=0, columnspan=3, sticky="news")
    add_task = tk.Button(Function_frame, text="ADD TASK", padx=10, command=add, fg="Lightcyan", bg="#71a0c6",
                         activebackground="#71a0c6", font=("8514oem"))
    add_task.grid(row=1, column=0)
    delete_task = tk.Button(Function_frame, text="DELETE TASK", padx=10, command=delete, fg="Lightcyan", bg="#71a0c6",
                            activebackground="#71a0c6", font=("8514oem"))
    delete_task.grid(row=1, column=1)
    finish_task = tk.Button(Function_frame, text="FINISH TASK", padx=10, command=finish_task, fg="Lightcyan",
                            bg="#71a0c6", activebackground="#71a0c6", font=("8514oem"))
    finish_task.grid(row=1, column=2)
    edit_task = tk.Button(Function_frame, text="EDIT TASK", padx=10, command=edit_task_details, fg="Lightcyan",
                          bg="#71a0c6", activebackground="#71a0c6", font=("8514oem"))
    edit_task.grid(row=1, column=3)

    root.mainloop()


# Login Page
# region
login = tk.Tk()
login.title("JCO TodoApp,your life task manager")
login.geometry("600x400")
login.iconbitmap("JCO.ico")
login.configure(bg="#7EB2DD")


def logining():
    # database
    conn = sqlite3.connect('todolist.db')
    create_table = '''
         CREATE TABLE IF NOT EXISTS User_Information
         (USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,username TEXT , password TEXT , email TEXT )
         '''
    conn.execute(create_table)
    conn.commit()
    conn.close()


def loging():
    username = entry.get()
    email = entry2.get()
    password = entry3.get()

    conn = sqlite3.connect('todolist.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM User_Information WHERE username=? AND password=? AND email =?''',
                   (username, password, email))
    row = cursor.fetchone()

    conn.close()
    email_confirm = "@"
    email_confirm2 = ".com"
    if email_confirm in email and email_confirm2 in email:
        if row is not None:
            USER_ID = row[0]
            tk.messagebox.showinfo("Login", "Login Successful !")
            main_page(USER_ID)
        else:
            tk.messagebox.showerror("Login", "Invalid username or password.", icon='error')
    else:
        tk.messagebox.showerror("invalid email", "this is not a valid email!", icon="error")


loginframe = tk.Frame(login, bg="#7EB2DD")
loginframe.pack()

welcome = tk.Label(loginframe, text="Login Page", font=("8514oem", 50), bg="#7EB2DD", fg="Lightcyan")
welcome.grid(row=1, column=1, pady=50, columnspan=2)

login_frame = Frame(loginframe, width=500, height=300, bg="#7EB2DD")
login_frame.grid(row=2, column=1)
word = tk.Label(login_frame, text="      Username:", font=("8514oem", 12), bg="#7EB2DD", fg="Lightcyan")
word.grid(row=2, column=1)
entry = tk.Entry(login_frame, bd=3, bg="#e5eff8")
entry.grid(row=2, column=2, pady=10)

word2 = tk.Label(login_frame, text="         Email:", font=("8514oem", 12), bg="#7EB2DD", fg="Lightcyan")
word2.grid(row=3, column=1)
entry2 = tk.Entry(login_frame, width=20, bd=3, bg="#e5eff8")
entry2.grid(row=3, column=2, pady=10)

word3 = tk.Label(login_frame, text="      Password:", font=("8514oem", 12), bg="#7EB2DD", fg="Lightcyan")
word3.grid(row=4, column=1)
entry3 = tk.Entry(login_frame, width=20, bd=3, bg="#e5eff8")
entry3.grid(row=4, column=2, pady=10)

button_font = font.Font(family="8514oem", size=10, weight='bold')
button = tk.Button(login_frame, text="Login", font=button_font, bg="#71a0c6", fg="Lightcyan", command=loging,
                   activebackground="#71a0c6")
button.grid(row=5, column=2, columnspan=2, pady=10)

word3 = tk.Label(loginframe, text="Don't have an account? Register here >> ", font=("8514oem", 1), bg="#7EB2DD",
                 fg="Lightcyan")
word3.grid(row=10, column=1)

button_font2 = font.Font(family="8514oem", size=10, weight='bold')
button2 = tk.Button(loginframe, text="Register", command=register_page, font=button_font2, fg="Lightcyan", bg="#71a0c6",
                    activebackground="#71a0c6")
button2.grid(row=10, column=2)

login.mainloop()
# endregion
