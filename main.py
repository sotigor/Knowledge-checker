import tkinter as tk
from tkinter import messagebox
import sqlite3
from csv_to_bd import *
import csv
from datetime import datetime
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog



# Create datadase and tables
con = sqlite3.connect('knowledge_checker.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Хімія
               (ID INTEGER PRIMARY KEY AUTOINCREMENT,
               questions text, 
               answers text,
               form integer
               )''')
cur.execute('''CREATE TABLE IF NOT EXISTS Математика
               (ID INTEGER PRIMARY KEY AUTOINCREMENT,
               questions text, 
               answers text,
               form integer
               )''')
cur.execute('''CREATE TABLE IF NOT EXISTS personal_data
               (ID INTEGER PRIMARY KEY AUTOINCREMENT,
               name,
               password
               )''')
cur.execute('''CREATE TABLE IF NOT EXISTS complaints
               (ID INTEGER PRIMARY KEY AUTOINCREMENT,
               question text,
               complaints text,
               subject,
               date
               )''')

con.commit()
con.close()


class StartWindow:
    def __init__(self, start_window):
        self.start_window = start_window
        start_window.title("Knowledge_checker")

        # Size of window and locate window on the screen
        start_window.resizable(False, False)
        screen_width = start_window.winfo_screenwidth()
        screen_height = start_window.winfo_screenheight()
        window_width = 440
        window_height= 480
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        start_window.geometry(f'{window_width}x{window_height}+{x_cordinate}+{y_cordinate}')

        # Making lable
        lbl_0 = tk.Label(start_window, text="Програма Knowledge checker\nдопоможе вам стати розумнішим!",
                         font="Calibri 18")
        lbl_0.grid(column=0, row=0, pady=20, padx=30)

        # Making buttons
        self.bt_1 = tk.Button(start_window, text="Увійти", font="16", width="16", height=2, cursor='hand2',
                              command=self.get_sign_in_window)
        self.bt_1.grid(column=0, row=1, pady=30)
        self.bt_1.focus()
        self.bt_1.bind('<Return>', self.enter_button_handler_for_bt_1)

        bt_2 = tk.Button(start_window, text="Зареєструватися", font="16", width="16", height=2, cursor='hand2',
                         command=self.get_sign_up_window)
        bt_2.grid(column=0, row=2)
        bt_2.bind('<Return>', self.enter_button_handler_for_bt_2)

        bt_3 = tk.Button(start_window, text="Вийти \n з програми", font="16", width="16", cursor='hand2', command=exit)
        bt_3.grid(column=0, row=3, pady=30)
        bt_3.bind('<Return>', self.enter_button_handler_for_bt_3)

        bt_4 = tk.Button(start_window, text="Панель адміністратора", font="16", width="35", cursor='hand2',
                         command=self.get_admin_window)
        bt_4.grid(column=0, row=4, pady=(65,0))
        bt_4.bind('<Return>', self.enter_button_handler_for_bt_4)

    def enter_button_handler_for_bt_1(self, event) -> None:
        self.get_sign_in_window()

    def enter_button_handler_for_bt_2(self, event) -> None:
        self.get_sign_up_window()

    def enter_button_handler_for_bt_3(self, event) -> None:
        exit()

    def enter_button_handler_for_bt_4(self, event) -> None:
        self.get_admin_window()

    def get_sign_in_window(self) -> None:
        self.start_window.withdraw()
        SignInWindow(self.start_window, self.bt_1)

    def get_sign_up_window(self) -> None:
        self.start_window.withdraw()
        SignUpWindow(self.start_window, self.bt_1)

    def get_admin_window(self):
        self.start_window.withdraw()
        AdminLoginWindow(self.start_window,self.bt_1)


class SignInWindow:
    def __init__(self, start_window, bt_1)-> None:
        self.sign_in_window = tk.Tk()
        self.sign_in_window.title('Sign in')
        self.start_window = start_window
        self.start_window_bt_1 = bt_1

        f = ('Times', 14)
        frame_1 = tk.Frame(self.sign_in_window, bd=10, bg='#CCACCC', relief='groove', padx=10, pady=10)
        lbl_30 = tk.Label(frame_1, text="Введіть ім'я:", bg='#CCACCC', font=f)
        lbl_30.grid(row=0, column=0, sticky='W', pady=10)

        lbl_31 = tk.Label(frame_1, text="Введіть пароль:", bg='#CCACCC', font=f)
        lbl_31.grid(row=1, column=0, pady=10, sticky='W')

        self.name = tk.Entry(frame_1, font=f)
        self.name.focus_force()
        self.pwd_1 = tk.Entry(frame_1, font=f, show='*')

        login_btn_1 = tk.Button(frame_1, width=10, text='Увійти', font=f, relief='solid', cursor='hand2',
                                command=lambda: self.sign_inup_checker(self.name.get(), self.pwd_1.get(), self.sign_in_window, key=True))
        login_btn_1.bind('<Return>', self.enter_button_handler_for_login_btn_1)

        login_btn_2 = tk.Button(frame_1, width=10, text='Назад', font=f, relief='solid', cursor='hand2',
                                command=lambda: [self.sign_in_window.destroy(), self.go_to_startWindow()])
        login_btn_2.bind('<Return>', self.enter_button_handler_for_login_btn_2)

        self.name.grid(row=0, column=1, pady=10, padx=20)
        self.pwd_1.grid(row=1, column=1, pady=10, padx=20)

        login_btn_1.grid(row=3, column=1, pady=10, padx=20)
        login_btn_2.grid(row=3, column=0, pady=10, padx=20)
        frame_1.pack()
        self.sign_in_window.mainloop()

    def enter_button_handler_for_login_btn_1(self,event):
        self.sign_inup_checker(self.name.get(), self.pwd_1.get(), self.sign_in_window, key=True)

    def enter_button_handler_for_login_btn_2(self, event):
        self.sign_in_window.destroy()
        self.go_to_startWindow()

    def go_to_startWindow(self):
        self.start_window.deiconify()
        self.start_window_bt_1.focus_force()

    def sign_inup_checker(self, name, psw_1, sign_in_window, psw_2="1", key=False):
        check_counter = 0
        if name == "":
            warn = "Поле для ім'я не може бути порожнім"
            messagebox.showwarning("Warning", warn)
        else:
            check_counter += 1

        if psw_1 == "":
            warn = "Поле пароля не може бути порожнім"
            messagebox.showwarning("Warning", warn)
        else:
            check_counter += 1

        if key == False:
            if psw_2 == "":
                warn = "Поле для підтвердження паролю не може бути порожнім"
                messagebox.showwarning("Warning", warn)
            else:
                check_counter += 1
            if psw_1 != psw_2:
                warn = "Паролі у двох полях не співпадають!"
                messagebox.showwarning("Warning", warn)
            else:
                check_counter += 1

            if check_counter == 4:
                con = sqlite3.connect('knowledge_checker.db')
                cur = con.cursor()

                exist_name = \
                cur.execute(f"SELECT NOT EXISTS(SELECT 1 FROM personal_data WHERE name='{name}');").fetchone()[0]
                exist_all = cur.execute(f"SELECT * FROM personal_data;").fetchall()

                if exist_name:
                    cur.execute("INSERT INTO personal_data VALUES (:name, :password)", {
                        'name': name,
                        'password': psw_1})
                    con.commit()
                    con.close()
                    messagebox.showinfo('confirmation', 'Запис зроблено')
                    sign_in_window.destroy()
                    self.back()
                else:
                    warn = "Таке ім'я вже існує. Введіть інше.\nПідказка: cпробуйте додати до ім'я рік народження."
                    messagebox.showwarning("Warning", warn)
        else:
            con = sqlite3.connect('knowledge_checker.db')
            cur = con.cursor()
            not_exist_name = \
                cur.execute(f"SELECT NOT EXISTS(SELECT 1 FROM personal_data WHERE name = '{name}');").fetchone()[0]
            if not_exist_name == 0:
                correct_psw = cur.execute(f"SELECT * FROM personal_data WHERE name = '{name}';").fetchone()[2]
                if correct_psw != psw_1:
                    not_correct_psw = True
                    messagebox.showwarning("confirmation", "Не вірно введений пароль.\nПеревірте будь-ласка.")
                else:
                    not_correct_psw = False
                    sign_in_window.destroy()
                    self.start_window.withdraw()
                    ChoiceWindow()
            else:
                messagebox.showwarning("confirmation", "Не вірно введене ім'я.\nПеревірте будь-ласка.")
            con.close()


class SignUpWindow:
    def __init__(self, start_window, bt_1):
        """Creating the new tk window for signing in

        :param start_window: for making start_window visible
        :param bt_1: for making focuse on this button after returning to start_window
        """
        self.sign_up_window = tk.Tk()
        self.sign_up_window.title('Knowledge_checker')
        self.sign_up_window.config(bg='#0B5A81')
        self.start_window = start_window
        self.start_window_bt_1 = bt_1

        f = ('Times', 14)

        frame_1 = tk.Frame(self.sign_up_window, bd=10, bg='#CCACCC', relief='groove', padx=10, pady=10)

        lbl_30 = tk.Label(frame_1, text="Введіть ім'я:", bg='#CCCCCC', font=f)
        lbl_30.grid(row=0, column=0, sticky='W', pady=10)
        lbl_30.focus_set()

        lbl_31 = tk.Label(frame_1, text="Введіть пароль:", bg='#CCCCCC', font=f)
        lbl_31.grid(row=1, column=0, pady=10, sticky='W')

        lbl_32 = tk.Label(frame_1, text="Повторіть пароль:", bg='#CCCCCC', font=f)
        lbl_32.grid(row=2, column=0, pady=10, sticky='W')

        self.name = tk.Entry(frame_1, font=f)
        self.name.focus_force()

        self.pwd_1 = tk.Entry(frame_1, font=f, show='*')
        self.pwd_2 = tk.Entry(frame_1, font=f, show='*')

        login_btn_1 = tk.Button(frame_1, width=10, text='Відправити', font=f, relief='solid', cursor='hand2',
                                command=lambda: self.sign_inup_checker(self.name.get(), self.pwd_1.get(), self.sign_up_window, psw_2=self.pwd_2.get()))
        login_btn_1.bind('<Return>', self.enter_button_handler_for_login_btn_1)
        login_btn_2 = tk.Button(frame_1, width=10, text='Назад', font=f, relief='solid', cursor='hand2',
                                command=lambda: [self.sign_up_window.destroy(), self.go_to_startWindow()])
        login_btn_2.bind('<Return>', self.enter_button_handler_for_login_btn_2)
        self.name.grid(row=0, column=1, pady=10, padx=20)
        self.pwd_1.grid(row=1, column=1, pady=10, padx=20)
        self.pwd_2.grid(row=2, column=1, pady=10, padx=20)

        login_btn_1.grid(row=3, column=1, pady=10, padx=20)
        login_btn_2.grid(row=3, column=0, pady=10, padx=20)
        frame_1.pack()
        #sign_up_window.mainloop()
    
    def enter_button_handler_for_login_btn_1(self,event):
        self.sign_inup_checker(self.name.get(), self.pwd_1.get(), self.sign_up_window, psw_2=self.pwd_2.get())

    def enter_button_handler_for_login_btn_2(self, event):
        self.sign_up_window.destroy()
        self.go_to_startWindow()

    def go_to_startWindow(self):
        self.start_window.deiconify()
        self.start_window_bt_1.focus_force()
        
    def sign_inup_checker(self, name, psw_1, sign_in_window, psw_2="1", key=False):
        check_counter = 0
        if name == "":
            warn = "Поле для ім'я не може бути порожнім"
            messagebox.showwarning("Warning", warn)
        else:
            check_counter += 1

        if psw_1 == "":
            warn = "Поле пароля не може бути порожнім"
            messagebox.showwarning("Warning", warn)
        else:
            check_counter += 1

        if key == False:
            if psw_2 == "":
                warn = "Поле для підтвердження паролю не може бути порожнім"
                messagebox.showwarning("Warning", warn)
            else:
                check_counter += 1
            if psw_1 != psw_2:
                warn = "Паролі у двох полях не співпадають!"
                messagebox.showwarning("Warning", warn)
            else:
                check_counter += 1

            if check_counter == 4:
                con = sqlite3.connect('knowledge_checker.db')
                cur = con.cursor()

                not_exist_name =\
                    cur.execute(f"SELECT NOT EXISTS(SELECT 1 FROM personal_data WHERE name='{name}');").fetchone()[0]
                exist_all = cur.execute(f"SELECT * FROM personal_data;").fetchall()

                if not_exist_name:
                    sqlite_insert_query = """INSERT INTO personal_data
                                                  (name, password) 
                                                   VALUES (?,?);"""
                    pers_data = (name, psw_1)
                    cur.execute(sqlite_insert_query, pers_data)
                    con.commit()
                    con.close()
                    messagebox.showinfo('confirmation', 'Запис зроблено')
                    sign_in_window.destroy()
                    self.go_to_startWindow()
                else:
                    warn = "Таке ім'я вже існує. Введіть інше.\nПідказка: cпробуйте додати до ім'я рік народження."
                    messagebox.showwarning("Warning", warn)
        else:
            con = sqlite3.connect('knowledge_checker.db')
            cur = con.cursor()
            not_exist_name = cur.execute(f"SELECT NOT EXISTS(SELECT 1 FROM personal_data WHERE name='{name}');").fetchone()[
                0]
            exist_psw = \
            cur.execute(f"SELECT NOT EXISTS(SELECT 1 FROM personal_data WHERE password='{psw_1}');").fetchone()[0]
            con.close()
            if not_exist_name:
                messagebox.showwarning("confirmation", "Не вірно введене ім'я.\nПеревірте будь-ласка.")
            elif exist_psw:
                messagebox.showwarning("confirmation", "Не вірно введений пароль.\nПеревірте будь-ласка.")
            else:
                sign_in_window.destroy()
                self.start_window.withdraw()
                ChoiceWindow()


class AdminLoginWindow:
    def __init__(self, start_window, bt_1)-> None:
        self.admin_login_window = tk.Tk()
        self.admin_login_window.title('Sign in for admin panel')
        self.start_window = start_window
        self.start_window_bt_1 = bt_1


        f = ('Times', 14)
        frame_1 = tk.Frame(self.admin_login_window, bd=10, bg='#CCACCC', relief='groove', padx=10, pady=10)
        lbl_30 = tk.Label(frame_1, text="Login:", bg='#CCACCC', font=f)
        lbl_30.grid(row=0, column=0, sticky='W', pady=10)

        lbl_31 = tk.Label(frame_1, text="Password:", bg='#CCACCC', font=f)
        lbl_31.grid(row=1, column=0, pady=10, sticky='W')

        placeholder = 'admin'
        def erase_name(event):
            if self.name.get() == placeholder:
                self.name.delete(0, 'end')
                self.name.config(fg = "black")
        def erase_psw(event):
            if self.psw.get() == placeholder:
                self.psw.delete(0, 'end')
                self.psw.config(fg = "black", show="*")

        def add_name(event):
            if self.name.get() == '':
                self.name.insert(0, placeholder)

        def add_psw(event):
            if self.psw.get() == '':
                self.psw.insert(0, placeholder)

        self.name = tk.Entry(frame_1, font=f, fg = "grey")
        #self.name.focus_force()
        self.psw = tk.Entry(frame_1, font=f, show='')

        self.name.insert(0, placeholder)
        self.name.bind('<FocusIn>', erase_name)
        self.name.bind('<FocusOut>', add_name)

        self.psw.insert(0, placeholder)
        self.psw.bind('<FocusIn>', erase_psw)
        self.psw.bind('<FocusOut>', add_psw)


        login_btn_1 = tk.Button(frame_1, width=10, text='Увійти', font=f, relief='solid', cursor='hand2',
                                command=lambda: self.login_checker())
        login_btn_1.bind('<Return>', self.enter_button_handler_for_login_btn_1)
        login_btn_1.focus_force()

        login_btn_2 = tk.Button(frame_1, width=10, text='Назад', font=f, relief='solid', cursor='hand2',
                                command=lambda: [self.admin_login_window.destroy(), self.go_to_startWindow()])
        login_btn_2.bind('<Return>', self.enter_button_handler_for_login_btn_2)

        self.name.grid(row=0, column=1, pady=10, padx=20)
        self.psw.grid(row=1, column=1, pady=10, padx=20)

        login_btn_1.grid(row=3, column=1, pady=10, padx=20)
        login_btn_2.grid(row=3, column=0, pady=10, padx=20)
        frame_1.pack()

    def enter_button_handler_for_login_btn_1(self,event):
        self.login_checker()

    def enter_button_handler_for_login_btn_2(self, event):
        self.admin_login_window.destroy()
        self.go_to_startWindow()

    def go_to_startWindow(self):
        self.start_window.deiconify()
        self.start_window_bt_1.focus_force()

    def login_checker(self):
        if self.name.get() == "admin" and self.psw.get() == "admin":
            self.admin_login_window.destroy()
            #self.start_window.withdraw()
            AdminPanelWindow(self.start_window, self.start_window_bt_1)
        elif self.name.get() == "" or self.psw.get() == "":
            warn = "Check! Both fields must be filled in!"
            messagebox.showwarning("Warning", warn)
        else:
            warn = "Login or password is incorrect!"
            messagebox.showwarning("Warning", warn)


class AdminPanelWindow():
    def __init__(self, start_window, bt_1)-> None:
        self.admin_panel_window = tk.Tk()
        self.admin_panel_window.title('Admin_panel')
        self.start_window = start_window
        self.start_window_bt_1 = bt_1

        lbl_del = tk.Label(self.admin_panel_window, text="Delete or change question", font="14")
        lbl_del.pack(padx=(40, 40), pady=(20, 0))

        bt_del = tk.Button(self.admin_panel_window, text="Delete/Change", font="14", width=15,
                            command= lambda: DeleteChangeQuesWindow(self.admin_panel_window))
        bt_del.pack(pady=(10, 0))
        bt_del.focus_force()
        bt_del.bind('<Return>', self.enter_button_handler_for_bt_del)

        lbl_1 = tk.Label(self.admin_panel_window, text="Add the question by hand", font="14")
        lbl_1.pack(padx=(40, 40), pady=(20,0))

        bt_add1 = tk.Button(self.admin_panel_window, text="Add", font="14", width=15,
                            command= lambda: AddQuesHandWindow(self.admin_panel_window))
        bt_add1.pack(pady=(10, 20))
        bt_add1.bind('<Return>', self.enter_button_handler_for_bt_add1)

        lbl_2 = tk.Label(self.admin_panel_window, text="Add questions from the file", font="14")
        lbl_2.pack()

        bt_add2 = tk.Button(self.admin_panel_window, text="Add",font="14", width=15,
                            command=lambda: AddQuesFileWindow(self.admin_panel_window))
        bt_add2.pack(pady=(10, 20))
        bt_add2.bind('<Return>', self.enter_button_handler_for_bt_add2)

        lbl_3 = tk.Label(self.admin_panel_window, text="Show questions with remarks", font="14")
        lbl_3.pack()

        bt_show = tk.Button(self.admin_panel_window, text="Show", font="14", width=15,
                         command = lambda: ShowRemarkedQues(self.admin_panel_window))
        bt_show.pack(pady=(10, 20))
        bt_show.bind('<Return>', self.enter_button_handler_for_bt_show)

        bt_exit = tk.Button(self.admin_panel_window, text="Exit", font="16", width="16",
                            command=lambda: self.go_to_start_window())
        bt_exit.pack(pady=(15, 20), padx=15)
        bt_exit.bind('<Return>', self.enter_button_handler_for_bt_exit)

    def enter_button_handler_for_bt_del(self, event):
        DeleteChangeQuesWindow(self.admin_panel_window)

    def enter_button_handler_for_bt_add1(self, event):
        AddQuesHandWindow(self.admin_panel_window)

    def enter_button_handler_for_bt_add2(self,event):
        AddQuesFileWindow(self.admin_panel_window)

    def enter_button_handler_for_bt_show(self, event):
        ShowRemarkedQues(self.admin_panel_window)

    def enter_button_handler_for_bt_exit(self, event):
        self.go_to_start_window()

    def go_to_start_window(self):
        self.admin_panel_window.destroy()
        self.start_window.deiconify()
        self.start_window_bt_1.focus_force()


class AddQuesHandWindow:
    def __init__(self, admin_panel_window):
        self.admin_panel_window = admin_panel_window
        admin_panel_window.withdraw()
        self.add_ques_hand = tk.Tk()
        self.add_ques_hand.title('Add file')

        lbl_1 = tk.Label(self.add_ques_hand, text="Оберіть предмет:", font="16")
        lbl_1.grid(column=0, row=1, pady=20, padx=(10, 0), sticky='W')

        self.opt_menu_var1 = tk.StringVar(self.add_ques_hand)
        self.opt_menu_var1.set("Математика")
        options_1 = [
        "Математика",
        "Хімія"]
        """
        options_1 = [
            "Географія",
            "Математика",
            "Біологія",
            "Фізика",
            "Хімія",
            "Англійська мова"]
        """
        list_of_subj = tk.OptionMenu(self.add_ques_hand, self.opt_menu_var1, *options_1)
        list_of_subj.config(width=15, font="16", bg="white", fg="black")
        list_of_subj.grid(row=1, column=1, sticky="W", padx=(0,10))
        list_of_subj.focus_force()

        lbl_2 = tk.Label(self.add_ques_hand, text="Оберіть складність:", font="16")
        lbl_2.grid(column=0, row=2, pady=20, padx=(10, 0), sticky='W')

        self.opt_menu_var2 = tk.StringVar(self.add_ques_hand)
        self.opt_menu_var2.set("5 клас")
        options_2 = [
            "5 клас",
            "6 клас"]

        """
        options_2 = [
            "5 клас",
            "6 клас",
            "7 клас",
            "8 клас",
            "9 клас"]
        """

        list_of_form = tk.OptionMenu(self.add_ques_hand, self.opt_menu_var2, *options_2)
        list_of_form.config(width=15, font="16", bg="white")
        list_of_form.grid(row=2, column=1, sticky="W")
        #list_of_form.focus_force()

        lbl_3 = tk.Label(self.add_ques_hand, text="Введіть питання:", font="16")
        lbl_3.grid(column=0, row=3, pady=20, padx=(10, 0), sticky='W')
        self.ques = tk.Entry(self.add_ques_hand, width=25, font="16")
        self.ques.grid(column=0, row=4, pady=2, columnspan=5)

        lbl_4 = tk.Label(self.add_ques_hand, text="Введіть відповідь:", font="16")
        lbl_4.grid(column=0, row=5, pady=20, padx=(10, 0), sticky='W')
        self.answ = tk.Entry(self.add_ques_hand, width=25, font="16")
        self.answ.grid(column=0, row=6, pady=2, columnspan=5)

        bt_back = tk.Button(self.add_ques_hand, text="Back", font = "16",
                         command= lambda: self.go_to_admin_panel_window())
        bt_back.grid(column=0, row=7, pady=20, padx=(0, 0))
        bt_back.bind('<Return>', self.enter_button_handler_for_bt_back)

        bt_submit = tk.Button(self.add_ques_hand, text="Submit", font = "16",
                         command=lambda: self.add_ques_to_bd())
        bt_submit.grid(column=1, row=7, pady=20, padx=(0, 0))
        bt_submit.bind('<Return>', self.enter_button_handler_for_bt_sibmit)
        #bt_1.focus_force()

    def enter_button_handler_for_bt_back(self, event):
        self.go_to_admin_panel_window()

    def enter_button_handler_for_bt_sibmit(self, event):
        self.add_ques_to_bd()

    def go_to_admin_panel_window(self):
        self.add_ques_hand.destroy()
        self.admin_panel_window.deiconify()

    def add_ques_to_bd(self):
        if self.ques.get() !="" and self.answ.get() !="":
            con = sqlite3.connect('knowledge_checker.db')
            cur = con.cursor()
            sqlite_insert_query = f"""INSERT INTO {self.opt_menu_var1.get()}
                                          (questions, answers, form) 
                                           VALUES (?,?,?);"""
            data_tuple = (self.ques.get(), self.answ.get(), self.opt_menu_var2.get()[0])
            cur.execute(sqlite_insert_query, data_tuple)
            con.commit()
            con.close()
            messagebox.showinfo('confirmation', 'Питання додано успішно!')
            self.answ.delete(0, tk.END)
            self.ques.delete(0, tk.END)
        else:
            messagebox.showwarning('Warning', 'Заповніть порожні строки!')


        #self.add_ques_hand.destroy()
        #self.admin_panel_window.deiconify()


class AddQuesFileWindow:
    def __init__(self, admin_panel_window):
        self.admin_panel_window = admin_panel_window
        self.admin_panel_window.withdraw()
        self.add_ques_file = tk.Tk()
        self.add_ques_file.title('Admin_panel')

        lbl_1 = tk.Label(self.add_ques_file, text="Оберіть предмет:", font="16")
        lbl_1.grid(column=0, row=0, pady=20, padx=(10, 0))

        self.opt_menu_var1 = tk.StringVar(self.add_ques_file)
        self.opt_menu_var1.set("Математика")
        options_1 = [
        "Математика",
        "Хімія"]
        """
        options_1 = [
            "Географія",
            "Математика",
            "Біологія",
            "Фізика",
            "Хімія",
            "Англійська мова"]
        """


        list_of_subj = tk.OptionMenu(self.add_ques_file, self.opt_menu_var1, *options_1)
        list_of_subj.config(width=15, font="16", bg="white", fg="black")
        list_of_subj.grid(row=0, column=1, sticky="W", padx=(0,10))
        list_of_subj.focus_force()

        lbl_2 = tk.Label(self.add_ques_file, text="Вибрати файл", font="16")
        lbl_2.grid(column=0, row=1, pady=20, padx=(10, 0), sticky="W")

        bt_find = tk.Button(self.add_ques_file, text="Browse", font="16",
                         command = lambda: self.open_browse_window(self.file_path))
        bt_find.grid(column=1, row=1, pady=20, padx=(0, 0), sticky="W")

        self.file_path = tk.StringVar(self.add_ques_file)
        path_field = tk.Entry(self.add_ques_file, textvariable=self.file_path, width=30, font= "11")
        #file_path.set("Шлях до файлу")
        path_field.grid(column=0, row=2, columnspan=2,  pady=20, padx=(0, 0))


        bt_back = tk.Button(self.add_ques_file, text="Back", font = "16",
                         command= lambda: self.go_to_admin_panel_window())
        bt_back.grid(column=0, row=3, pady=20, padx=(0, 0))
        bt_back.bind('<Return>', self.enter_button_handler_for_bt_back)

        bt_download = tk.Button(self.add_ques_file, text="Download", font = "16",
                         command=lambda: self.add_csv_file_to_bd(self.add_ques_file, self.file_path.get(), self.opt_menu_var1.get()))
        bt_download.grid(column=1, row=3, pady=20, padx=(0, 0))
        bt_download.bind('<Return>', self.enter_button_handler_for_bt_download)

    def enter_button_handler_for_bt_back(self, event):
        self.go_to_admin_panel_window()

    def enter_button_handler_for_bt_download(self, event):
        self.add_csv_file_to_bd(self.add_ques_file, self.file_path.get(), self.opt_menu_var1.get())

    def open_browse_window(self, path_to_file):
        path = filedialog.askopenfilename()
        path_to_file.set(f"{path}")

    def go_to_admin_panel_window(self):
        self.add_ques_file.destroy()
        self.admin_panel_window.deiconify()

    def add_csv_file_to_bd(self, add_ques_file, file_path, subject):
        print(file_path, subject)
        try:
            csv_to_bd(file_path, subject)
            messagebox.showinfo('confirmation', 'Файл завантажено успішно!')
            add_ques_file.destroy()
            self.admin_panel_window.deiconify()
        except:
            messagebox.showinfo("Check the path or file (extension or content)")


class DeleteChangeQuesWindow:
    def __init__(self, admin_panel_window):
        self.delete_change_window = tk.Tk()
        self.delete_change_window.title("Delete_Change_Question")
        self.admin_panel_window = admin_panel_window
        self.admin_panel_window.withdraw()

        lbl_massage = tk.Label(self.delete_change_window, text="Find questions by key word in", font="16", anchor="n")
        lbl_massage.grid(column=0, row=0, columnspan=1, pady=(15, 0), padx=(15, 0), sticky="w")

        self.opt_menu_var = tk.StringVar(self.delete_change_window)
        self.opt_menu_var.set("Математика")
        subjects = [
            "Математика",
            "Хімія"]

        list_of_subj = tk.OptionMenu(self.delete_change_window, self.opt_menu_var, *subjects)
        list_of_subj.config(width=15, font="16", bg="white", fg="black")
        list_of_subj.grid(column=1, row=0, pady = (15,0))

        self.search_box = tk.Entry(self.delete_change_window, width=30, font="16")
        self.search_box.grid(column=0, row=1, columnspan=2, pady=(25, 0), padx=(0, 0))

        btn_search = tk.Button(self.delete_change_window, text="Find", font="16", width=30,
                               command = lambda: self.get_data_after_search())
        btn_search.grid(column=0, row=2, columnspan=2, pady=(15, 15), padx=(40, 40))

        btn_back = tk.Button(self.delete_change_window, text="Back", font="16", width=30,
                               command = lambda: self.go_to_admin_panel_window())
        btn_back.grid(column=0, row=3, columnspan=2, pady=(0,15), padx=(40, 40))

        #self.data_for_bd = [self.search_box.get(), self.opt_menu_var.get()]
    def get_data_after_search(self):
        """
        con = sqlite3.connect('knowledge_checker.db')
        cur = con.cursor()
        data_from_bd = cur.execute(f'''SELECT * FROM {self.opt_menu_var.get()}
                                    WHERE questions LIKE '%{self.search_box.get()}%';''').fetchall()
        con.commit()
        con.close()
        """
        #self.remarks_question_window.destroy()

        ShowSearchedQues(self.admin_panel_window, self.delete_change_window, self.search_box.get(), self.opt_menu_var.get())

    def go_to_admin_panel_window(self):
        self.delete_change_window.destroy()
        self.admin_panel_window.deiconify()


class ShowSearchedQues:
    def __init__(self, admin_panel_window, delete_change_window, key_searched_word, subject):
        self.admin_panel_window = admin_panel_window
        self.delete_change_window = delete_change_window
        self.delete_change_window.withdraw()
        self.show_searched_ques_window = tk.Tk()
        self.show_searched_ques_window.title("Questions_with_remarks")
        self.data_for_bd = [key_searched_word, subject]

        con = sqlite3.connect('knowledge_checker.db')
        cur = con.cursor()
        self.data_from_bd = cur.execute(f'''SELECT * FROM {self.data_for_bd[1]} 
                                    WHERE questions LIKE '%{self.data_for_bd[0]}%';''').fetchall()
        con.commit()
        con.close()

        lbl_1 = tk.Label(self.show_searched_ques_window, text="Question", borderwidth=3, relief="raised",
                         font=("Helvetica", 8, "bold"))
        lbl_1.grid(column=0, row=0, sticky="NSEW")

        lbl_2 = tk.Label(self.show_searched_ques_window, text="Answer", borderwidth=3, relief="raised",
                         font=("Helvetica", 8, "bold"))
        lbl_2.grid(column=1, row=0, sticky="NSEW")

        lbl_3 = tk.Label(self.show_searched_ques_window, text="Complexity", borderwidth=3, relief="raised",
                         font=("Helvetica", 8, "bold"))
        lbl_3.grid(column=2, row=0, sticky="NSEW")

        """
        lbl_4 = tk.Label(self.show_searched_ques_window, text="Data", borderwidth=3, relief="raised",
                         font=("Helvetica", 8, "bold"))
        lbl_4.grid(column=3, row=0, sticky="NSEW")
        """

        rows = self.data_from_bd
        n = 0
        buttons_delete = []
        buttons_change = []
        self.remarks_dict = {}
        while n <= len(rows) - 1:
            lbl_1 = tk.Label(self.show_searched_ques_window, text=rows[n][1], borderwidth=3, relief="groove")
            lbl_1.grid(column=0, row=n + 1, sticky="NSEW")

            lbl_2 = tk.Label(self.show_searched_ques_window, text=rows[n][2], borderwidth=3, relief="groove")
            lbl_2.grid(column=1, row=n + 1, sticky="NSEW")

            lbl_3 = tk.Label(self.show_searched_ques_window, text=rows[n][3], borderwidth=3, relief="groove")
            lbl_3.grid(column=2, row=n + 1, sticky="NSEW")

            """
            lbl_4 = tk.Label(self.show_searched_ques_window, text=rows[n][4], borderwidth=3, relief="groove")
            lbl_4.grid(column=3, row=n + 1, sticky="NSEW")
            """

            btn_delete = tk.Button(self.show_searched_ques_window, text="Delete", command=lambda n=n: self.delete_row(n))
            btn_delete.grid(column=3, row=n + 1, sticky="NSEW")
            buttons_delete.append(btn_delete)

            btn_change = tk.Button(self.show_searched_ques_window, text="Change", command=lambda n=n: self.change_row(n))
            btn_change.grid(column=4, row=n + 1, sticky="NSEW")
            buttons_change.append(btn_change)

            self.remarks_dict[n] = [rows[n][1], rows[n][3]]
            n += 1

        if len(rows) == 0:
            lbl = tk.Label(self.show_searched_ques_window, text="No questions with such key words!")
            lbl.grid(column=0, row=1, columnspan=4, pady=10)

        btn_back = tk.Button(self.show_searched_ques_window, text="back", width=20,
                             command=lambda: self.go_to_delete_change_window())
        btn_back.grid(column=0, row=len(rows) + 2, columnspan=5, pady=10)
        btn_back.bind('<Return>', self.enter_button_handler_for_btn_back)
        btn_back.focus_force()

    def delete_row(self, arg):
        con = sqlite3.connect('knowledge_checker.db')
        cur = con.cursor()
        cur.execute(f'''DELETE FROM {self.data_for_bd[1]} WHERE questions = '{self.remarks_dict[arg][0]}';''')
        con.commit()
        con.close()
        self.show_searched_ques_window.destroy()
        ShowSearchedQues(self.admin_panel_window, self.delete_change_window, self.data_for_bd[0], self.data_for_bd[1])

    def change_row(self, arg):
        con = sqlite3.connect('knowledge_checker.db')
        cur = con.cursor()
        data_ques_bd = cur.execute(f'''SELECT * FROM {self.data_for_bd[1]} 
                                    WHERE questions = '{self.remarks_dict[arg][0]}';''').fetchall()
        con.commit()
        con.close()
        self.show_searched_ques_window.destroy()
        ChangeSearchedQuesWindow(self.admin_panel_window, self.delete_change_window, data_ques_bd[0], self.data_for_bd)

    def enter_button_handler_for_btn_back(self, event):
        self.go_to_delete_change_window()

    def go_to_delete_change_window(self):
        self.show_searched_ques_window.destroy()
        self.delete_change_window.deiconify()


class ChangeSearchedQuesWindow:
    def __init__(self, admin_panel_window, delete_change_window, data_ques_bd, data_for_bd):
        self.change_ques_window = tk.Tk()
        self.change_ques_window.title("Change question")
        self.admin_panel_window = admin_panel_window
        #self.admin_panel_window.withdraw()
        self.data_for_bd = data_for_bd
        self.subject = data_for_bd[1]
        self.data_ques_bd = data_ques_bd
        self.delete_change_window = delete_change_window
        #self.data_ques_bd = data_ques_bd

        lbl_ques = tk.Label(self.change_ques_window, text="Question:")
        lbl_ques.grid(column=0, row=0, padx=(5, 0), pady=(10, 0), sticky="W")
        self.text_ques = tk.Text(self.change_ques_window, width=40, height=2)
        var_text_ques =data_ques_bd[1]
        self.text_ques.insert(tk.INSERT, var_text_ques)
        self.text_ques.grid(column=0, row=1, padx=(10, 0), pady=(0, 0))

        lbl_answ = tk.Label(self.change_ques_window, text="Answer:")
        lbl_answ.grid(column=0, row=2, padx=(5, 0), pady=(10, 0), sticky="W")
        self.text_answ = tk.Text(self.change_ques_window, width=40, height=1)

        var_text_answ = data_ques_bd[2]
        self.text_answ.insert(tk.INSERT, var_text_answ)
        self.text_answ.grid(column=0, row=3, padx=(10, 0), pady=(0, 0))

        lbl_subj = tk.Label(self.change_ques_window, text="Subject:")
        lbl_subj.grid(column=0, row=4, padx=(5, 0), pady=(10, 0), sticky="W")
        self.text_subj = tk.Text(self.change_ques_window, width=40, height=1)
        subj = self.subject
        self.text_subj.insert(tk.INSERT, subj)
        self.text_subj.grid(column=0, row=5, padx=(10, 0), pady=(0, 0))

        lbl_subj = tk.Label(self.change_ques_window, text="Complexity:")
        lbl_subj.grid(column=0, row=6, padx=(5, 0), pady=(10, 0), sticky="W")
        self.text_complexity = tk.Text(self.change_ques_window, width=40, height=1)
        complexity = str(data_ques_bd[3])+" "+"клас"
        self.text_complexity.insert(tk.INSERT, complexity)
        self.text_complexity.grid(column=0, row=7, padx=(10, 0), pady=(0, 0))

        btn_change = tk.Button(self.change_ques_window, text="Change", command = lambda: self.change_ques())
        btn_change.grid(column=0, row=8, padx=(10, 60), pady=(20, 10), sticky="E")

        btn_canc = tk.Button(self.change_ques_window, text="Cancel", command = lambda: self.go_to_show_searched_ques_window())
        btn_canc.grid(column=0, row=8, padx=(60, 10), pady=(20, 10), sticky="W")

    def change_ques(self):
        con = sqlite3.connect('knowledge_checker.db')
        cur = con.cursor()
        data_ques_bd = cur.execute(f'''UPDATE {self.text_subj.get(1.0, "end")} SET questions = '{self.text_ques.get(1.0, "end")}',
                                                                 answers = '{self.text_answ.get(1.0, "end")}', 
                                                                 form = '{self.text_complexity.get(1.0, "end")[0]}'
                                                                 WHERE ID = '{self.data_ques_bd[0]}';''')
        #cur.execute(f'''DELETE FROM complaints WHERE question = '{self.data_ques_bd[1]}';''')
        con.commit()
        con.close()

        self.change_ques_window.destroy()
        ShowSearchedQues(self.admin_panel_window, self.delete_change_window, self.data_for_bd[0], self.data_for_bd[1])

    def go_to_show_searched_ques_window(self):
        self.change_ques_window.destroy()
        ShowSearchedQues(self.admin_panel_window, self.delete_change_window, self.data_for_bd[0], self.data_for_bd[1])


class ShowRemarkedQues:
    def __init__(self, admin_panel_window):
        self.admin_panel_window = admin_panel_window
        self.admin_panel_window.withdraw()
        self.remarks_question_window = tk.Tk()
        self.remarks_question_window.title("Questions_with_remarks")

        lbl_1 = tk.Label(self.remarks_question_window, text="Question", borderwidth=3, relief="raised",
                         font=("Helvetica", 8, "bold"))
        lbl_1.grid(column=0, row=0, sticky="NSEW")

        lbl_2 = tk.Label(self.remarks_question_window, text="Remark", borderwidth=3, relief="raised",
                         font=("Helvetica", 8, "bold"))
        lbl_2.grid(column=1, row=0, sticky="NSEW")

        lbl_3 = tk.Label(self.remarks_question_window, text="Subject", borderwidth=3, relief="raised",
                         font=("Helvetica", 8, "bold"))
        lbl_3.grid(column=2, row=0, sticky="NSEW")

        lbl_4 = tk.Label(self.remarks_question_window, text="Data", borderwidth=3, relief="raised",
                         font=("Helvetica", 8, "bold"))
        lbl_4.grid(column=3, row=0, sticky="NSEW")

        con = sqlite3.connect('knowledge_checker.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM complaints")
        rows = cur.fetchall()
        n=0
        buttons_delete = []
        buttons_change = []
        self.remarks_dict = {}
        while n <= len(rows)-1:
            lbl_1= tk.Label(self.remarks_question_window, text=rows[n][1], borderwidth=3, relief="groove")
            lbl_1.grid(column=0, row=n+1, sticky="NSEW")

            lbl_2 = tk.Label(self.remarks_question_window, text=rows[n][2], borderwidth=3, relief="groove")
            lbl_2.grid(column=1, row=n+1, sticky="NSEW")

            lbl_3 = tk.Label(self.remarks_question_window, text=rows[n][3], borderwidth=3, relief="groove")
            lbl_3.grid(column=2, row=n+1, sticky="NSEW")

            lbl_4 = tk.Label(self.remarks_question_window, text=rows[n][4], borderwidth=3, relief="groove")
            lbl_4.grid(column=3, row=n+1, sticky="NSEW")

            btn_delete = tk.Button(self.remarks_question_window, text = "Delete", command = lambda n=n: self.delete_row(n))
            btn_delete.grid(column=4, row=n + 1, sticky="NSEW")
            buttons_delete.append(btn_delete)

            btn_change = tk.Button(self.remarks_question_window, text = "Change", command = lambda n=n: self.change_row(n))
            btn_change.grid(column=5, row=n + 1, sticky="NSEW")
            buttons_change.append(btn_change)

            self.remarks_dict[n] = [rows[n][1], rows[n][3]]
            n += 1

        if len(rows) == 0:
            lbl = tk.Label(self.remarks_question_window, text = "No questions with remarks")
            lbl.grid(column=0, row= 1, columnspan=5, pady=10)

        btn_back = tk.Button(self.remarks_question_window, text = "back", width = 20,
                             command=lambda: self.go_to_admin_panel_window())
        btn_back.grid(column=0, row=len(rows)+2, columnspan=5, pady=10)
        btn_back.bind('<Return>', self.enter_button_handler_for_btn_back)
        btn_back.focus_force()

    def delete_row(self, arg):
        con = sqlite3.connect('knowledge_checker.db')
        cur = con.cursor()
        cur.execute(f'''DELETE FROM {self.remarks_dict[arg][1]} WHERE questions = '{self.remarks_dict[arg][0]}';''')
        cur.execute(f'''DELETE FROM complaints WHERE question = '{self.remarks_dict[arg][0]}';''')
        con.commit()
        con.close()
        self.remarks_question_window.destroy()
        ShowRemarkedQues(self.admin_panel_window)

    def change_row(self, arg):
        con = sqlite3.connect('knowledge_checker.db')
        cur = con.cursor()
        data_ques_bd = cur.execute(f'''SELECT * FROM {self.remarks_dict[arg][1]} 
                                    WHERE questions = '{self.remarks_dict[arg][0]}';''').fetchall()
        con.commit()
        con.close()
        self.remarks_question_window.destroy()
        ChangeRemarkedQuesWindow(self.admin_panel_window, data_ques_bd[0], self.remarks_dict[arg][1])

    def enter_button_handler_for_btn_back(self,event):
        self.go_to_admin_panel_window()

    def go_to_admin_panel_window(self):
        self.remarks_question_window.destroy()
        self.admin_panel_window.deiconify()


class ChangeRemarkedQuesWindow:
    def __init__(self, admin_panel_window, data_ques_bd, subject):
        self.change_ques_window = tk.Tk()
        self.change_ques_window.title("Change question")
        self.admin_panel_window = admin_panel_window
        #self.admin_panel_window.withdraw()
        self.subject = subject
        self.data_ques_bd = data_ques_bd
        #self.data_ques_bd = data_ques_bd

        lbl_ques = tk.Label(self.change_ques_window, text="Question:")
        lbl_ques.grid(column=0, row=0, padx=(5, 0), pady=(10, 0), sticky="W")
        self.text_ques = tk.Text(self.change_ques_window, width=40, height=2)
        var_text_ques =data_ques_bd[1]
        self.text_ques.insert(tk.INSERT, var_text_ques)
        self.text_ques.grid(column=0, row=1, padx=(10, 0), pady=(0, 0))

        lbl_answ = tk.Label(self.change_ques_window, text="Answer:")
        lbl_answ.grid(column=0, row=2, padx=(5, 0), pady=(10, 0), sticky="W")
        self.text_answ = tk.Text(self.change_ques_window, width=40, height=1)

        var_text_answ = data_ques_bd[2]
        self.text_answ.insert(tk.INSERT, var_text_answ)
        self.text_answ.grid(column=0, row=3, padx=(10, 0), pady=(0, 0))

        lbl_subj = tk.Label(self.change_ques_window, text="Subject:")
        lbl_subj.grid(column=0, row=4, padx=(5, 0), pady=(10, 0), sticky="W")
        self.text_subj = tk.Text(self.change_ques_window, width=40, height=1)
        subj = self.subject
        self.text_subj.insert(tk.INSERT, subj)
        self.text_subj.grid(column=0, row=5, padx=(10, 0), pady=(0, 0))

        lbl_subj = tk.Label(self.change_ques_window, text="Complexity:")
        lbl_subj.grid(column=0, row=6, padx=(5, 0), pady=(10, 0), sticky="W")
        self.text_complexity = tk.Text(self.change_ques_window, width=40, height=1)
        complexity = str(data_ques_bd[3])+" "+"клас"
        self.text_complexity.insert(tk.INSERT, complexity)
        self.text_complexity.grid(column=0, row=7, padx=(10, 0), pady=(0, 0))

        btn_change = tk.Button(self.change_ques_window, text="Change", command = lambda: self.change_row())
        btn_change.grid(column=0, row=8, padx=(10, 60), pady=(20, 10), sticky="E")

        btn_canc = tk.Button(self.change_ques_window, text="Cancel", command = lambda: self.go_to_remarks_question_window())
        btn_canc.grid(column=0, row=8, padx=(60, 10), pady=(20, 10), sticky="W")

    def change_row(self):
        con = sqlite3.connect('knowledge_checker.db')
        cur = con.cursor()
        data_ques_bd = cur.execute(f'''UPDATE {self.text_subj.get(1.0, "end")} SET questions = '{self.text_ques.get(1.0, "end")}',
                                                                 answers = '{self.text_answ.get(1.0, "end")}', 
                                                                 form = '{self.text_complexity.get(1.0, "end")[0]}'
                                                                 WHERE ID = '{self.data_ques_bd[0]}';''')
        cur.execute(f'''DELETE FROM complaints WHERE question = '{self.data_ques_bd[1]}';''')
        con.commit()
        con.close()

        self.change_ques_window.destroy()
        ShowRemarkedQues(self.admin_panel_window)

    def go_to_remarks_question_window(self):
        self.change_ques_window.destroy()
        ShowRemarkedQues(self.admin_panel_window)


class ChoiceWindow:
    def __init__(self):
        self.choice_window = tk.Tk()
        self.choice_window.title("Knowledge_checker")

        # Size of window and locate window on the screen
        self.choice_window.resizable(False, False)
        screen_width = self.choice_window.winfo_screenwidth()
        screen_height = self.choice_window.winfo_screenheight()
        window_width = 440
        window_height= 480
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.choice_window.geometry(f'{window_width}x{window_height}+{x_cordinate}+{y_cordinate}')

        lbl_0 = tk.Label(self.choice_window, text="Вітаємо у програмі knowledge checker!", font="Calibri 18")
        lbl_0.grid(column=0, row=0, columnspan=5, pady=20, padx=20)

        lbl_1 = tk.Label(self.choice_window, text="Оберіть предмет:", font="16")
        lbl_1.grid(column=0, row=1, pady=20, padx=(0, 0))

        self.opt_menu_var1 = tk.StringVar(self.choice_window)
        self.opt_menu_var1.set("Математика")
        options_1 = [
        "Математика",
        "Хімія"]
        """
        options_1 = [
            "Географія",
            "Математика",
            "Біологія",
            "Фізика",
            "Хімія",
            "Англійська мова"]
        """

        list_of_subj = tk.OptionMenu(self.choice_window, self.opt_menu_var1, *options_1)
        list_of_subj.config(width=15, font="16", bg="white", fg="black")
        list_of_subj.grid(row=1, column=1, sticky="W")
        #list_of_subj.focus_force()

        lbl_2 = tk.Label(self.choice_window, text="Оберіть складність:", font="16")
        lbl_2.grid(column=0, row=2, pady=20, padx=(0, 0))

        self.opt_menu_var2 = tk.StringVar(self.choice_window)
        self.opt_menu_var2.set("5 клас")
        options_2 = [
            "5 клас",
            "6 клас"]

        """
        options_2 = [
            "5 клас",
            "6 клас",
            "7 клас",
            "8 клас",
            "9 клас"]
        """

        list_of_form = tk.OptionMenu(self.choice_window, self.opt_menu_var2, *options_2)
        list_of_form.config(width=15, font="16", bg="white")
        list_of_form.grid(row=2, column=1, sticky="W")
        #list_of_form.focus_force()


        lbl_3 = tk.Label(self.choice_window, text="Кількість питань в тесті:", font="16")
        lbl_3.grid(column=0, row=3, pady=20, padx=(0, 0))

        self.opt_menu_var3 = tk.StringVar(self.choice_window)
        self.opt_menu_var3.set("5")
        options_3 = [
            "5",
            "10"]

        """
        options_3 = [
            "5",
            "10",
            "15",
            "20"]
        """
        list_of_numq = tk.OptionMenu(self.choice_window, self.opt_menu_var3, *options_3)
        list_of_numq.config(width=15, font="16", bg="white")
        list_of_numq.grid(row=3, column=1, sticky="W")

        lbl_4 = tk.Label(self.choice_window, text="Вид тесту:", font="16")
        lbl_4.grid(column=0, row=4, pady=20, padx=(0, 0))

        opt_menu_var4 = tk.StringVar(self.choice_window)
        opt_menu_var4.set("Звичайний")
        options_4 = [
            "Звичайний",
            "Варіанти вибору"]

        list_of_test = tk.OptionMenu(self.choice_window, opt_menu_var4, *options_4)
        list_of_test.config(width=15, font="16", bg="white")
        list_of_test.grid(row=4, column=1, sticky="W")

        bt_1 = tk.Button(self.choice_window, text="Розпочати\nтестування",
                         font="16", width="16", 
                         command=lambda: [self.choice_window.destroy(), TestWindow(self.opt_menu_var1.get(),
                                                                            self.opt_menu_var2.get(),
                                                                            self.opt_menu_var3.get())])
        bt_1.grid(column=1, row=5)
        bt_1.bind('<Return>', self.enter_button_handler_for_bt_1)
        bt_1.focus_force()

        bt_2 = tk.Button(self.choice_window, text="Вийти\nз програми", font="16", width="16", command=exit)
        bt_2.grid(column=0, row=5, pady=15)
        bt_2.bind('<Return>', self.enter_button_handler_for_bt_2)
        #choice_window.mainloop()
    def enter_button_handler_for_bt_1(self, event) -> None:
        self.choice_window.destroy()
        TestWindow(self.opt_menu_var1.get(), self.opt_menu_var2.get(), self.opt_menu_var3.get())

    def enter_button_handler_for_bt_2(self, event) -> None:
        exit()


class TestWindow:
    def __init__(self, subj, form_num_, num_of_ques):
        self.subj = subj
        self.form = form_num_
        self.num_of_ques = num_of_ques

        self.count_correct_answ = 0

        self.test_window = tk.Tk()
        self.test_window.title("Knowledge_checker")

        # Size of window and locate window on the screen
        self.test_window.resizable(False, False)
        screen_width = self.test_window.winfo_screenwidth()
        screen_height = self.test_window.winfo_screenheight()
        window_width = 440
        window_height= 530
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.test_window.geometry(f'{window_width}x{window_height}+{x_cordinate}+{y_cordinate}')

        self.ques_db, self.answ_db = self.get_data_from_bd(self.num_of_ques)

        self.text_ques = tk.StringVar(self.test_window)
        self.text_ques.set(self.ques_db.pop())

        self.answer_item = self.answ_db
        self.num_ques = tk.StringVar(self.test_window)
        self.num_ques.set(f"Залишилось питань: {len(self.ques_db) + 1} з {self.num_of_ques}")

        lbl_0 = tk.Label(self.test_window, text=f"Тест з предмету \n \"{self.subj}\"", font="Calibri 18")
        lbl_0.grid(column=1, row=0, columnspan=5, pady=(10,15))

        lbl_2 = tk.Label(self.test_window, text="Питання:", font="16")
        lbl_2.grid(column=0, row=1, padx=(10, 0))

        lbl_3 = tk.Label(self.test_window, textvariable=self.text_ques, bg="white",
                         font=("Calibri", "12"), height=3, width=34)
        lbl_3.grid(column=1, row=1, columnspan=5)

        lbl_4 = tk.Label(self.test_window, text="Відповідь:", font="16")
        lbl_4.grid(column=0, row=2, pady=20, padx=(10, 0))

        self.answ = tk.Entry(self.test_window, width=30, font="16")
        self.answ.grid(column=1, row=2, pady=20, columnspan=5)
        self.answ.focus_force()
        self.answ.bind('<Return>', self.enter_button_handler_for_bt_1)

        bt_1 = tk.Button(self.test_window, text="Оk", font="16", width="8", command=lambda: self.check_answer_isempty())
        bt_1.grid(column=2, row=3)
        bt_1.bind('<Return>', self.enter_button_handler_for_bt_1)

        bt_2 = tk.Button(self.test_window, text="Очистити", font="16", width="8", command=lambda: self.clean_field())
        bt_2.grid(column=3, row=3)
        bt_2.bind('<Return>', self.enter_button_handler_for_bt_2)

        self.lbl_4_1 = tk.Label(self.test_window, text=" ", font="16")
        self.lbl_4_1.grid(column=1, row=4, columnspan=5, pady=15)

        bt_3 = tk.Button(self.test_window, text="Поскаржитися \n на запитання", font="16", width="16",
                         command = lambda: self.go_to_complaint_window())
        bt_3.grid(column=2, row=5, columnspan=2)
        bt_3.bind('<Return>', self.enter_button_handler_for_bt_3)

        bt_4 = tk.Button(self.test_window, text="Вийти \n з програми", font="16", width="16", command=exit)
        bt_4.grid(column=2, row=6, columnspan=2, pady=15)
        bt_4.bind('<Return>', self.enter_button_handler_for_bt_4)

        lbl_5 = tk.Label(self.test_window, textvariable=self.num_ques, font="16")
        lbl_5.grid(column=1, row=7, pady=(15, 0), columnspan=5)

        self.seconds = 0
        self.lbl = tk.Label(self.test_window, text=f"Пройшло часу з початку тесту: {0}s", font="16", height=3)
        self.lbl.grid(column=1, row=8, pady=5, columnspan=5)
        self.lbl.after(1000, self.refresh_label)

    def enter_button_handler_for_bt_1(self, event):
        self.check_answer_isempty()

    def enter_button_handler_for_bt_2(self, event):
        self.clean_field()

    def enter_button_handler_for_bt_3(self, event):
        self.go_to_complaint_window()

    def enter_button_handler_for_bt_4(self, event):
        exit()

    def refresh_label(self):
        """ refresh the content of the label every second """
        self.seconds += 1
        self.lbl.configure(text=f"Пройшло часу з початку тесту: {self.seconds} s")
        self.lbl.after(1000, self.refresh_label)

    def get_data_from_bd(self, num):
        con = sqlite3.connect('knowledge_checker.db')
        cur = con.cursor()
        result = cur.execute(
            f'''SELECT questions, answers FROM {self.subj} WHERE form = '5' ORDER BY RANDOM() LIMIT {num};''')
        db_data = result.fetchall()
        con.close()
        ques_list = []
        answ_list = []
        for i in db_data:
            ques_list.append(i[0].replace('\\n', '\n'))
            answ_list.append(i[1])
        return ques_list, answ_list

    def go_to_final_window(self) -> None:
        if len(self.ques_db) < 1:
            self.test_window.destroy()
            FinalWindow(self.num_of_ques, self.count_correct_answ, self.seconds)
        else:
            self.next_ques()

    def go_to_complaint_window(self) -> None:
        self.test_window.withdraw()
        ComplaintWindow(self.test_window, self.text_ques.get(), self.answ, self.subj)

    def check_answer_isempty(self):
        if str(self.answ.get()) == "":
            warn = "Поле відповіді не може бути порожнім"
            messagebox.showwarning("Warning", warn)
        else:
            self.blink()

    def blink(self):
        if self.check_answer_iscorrect():
            self.answ.config(bg='green2')
            self.answ.after(800, lambda: self.answ.config(bg='white'))
            self.lbl_4_1.configure(text="П  Р  А  В  И  Л  Ь  Н  О ", fg="green2")
        else:
            self.answ.config(bg='red')
            self.answ.after(800, lambda: self.answ.config(bg='white'))
            self.lbl_4_1.configure(text="Н  Е  П  Р  А  В  И  Л  Ь  Н  О ", fg="red2")

        self.lbl_4_1.after(800, lambda: self.lbl_4_1.configure(text=" "))
        self.answ.after(800, self.clean_field)
        self.go_to_final_window()

    def check_answer_iscorrect(self) -> bool:
        if str(self.answ.get()) == self.answ_db[len(self.ques_db)]:
            self.count_correct_answ += 1
            return True
        return False

    def clean_field(self):
        self.answ.delete(0, tk.END)

    def next_ques(self):
        self.text_ques.set(self.ques_db.pop())
        self.num_ques.set(f"Залишилось питань: {len(self.ques_db) + 1} з {self.num_of_ques}")


class ComplaintWindow:
    def __init__(self, test_window, ques, answ, subj):
        self.complaint_window = tk.Tk()
        self.complaint_window.title("Knowledge_checker")
        self.test_window = test_window
        self.ques = ques
        self.answ = answ
        self.subj = subj

        self.var_1 = tk.StringVar(self.complaint_window)
        self.var_2 = tk.StringVar(self.complaint_window)
        self.var_3 = tk.StringVar(self.complaint_window)
        self.var_4 = tk.StringVar(self.complaint_window)

        text_for_checkbutton = ["Незрозуміле питання", "Питання містить помилки", "Питання не відповідає складності",
                                "Питання не відповідає предмету"]

        ch_but_1 = tk.Checkbutton(self.complaint_window, text=text_for_checkbutton[0], variable=self.var_1,
                                  onvalue=text_for_checkbutton[0], offvalue="", font=("Helvetica", 11))
        ch_but_1.focus_force()
        #ch_but_1.deselect()

        ch_but_2 = tk.Checkbutton(self.complaint_window, text=text_for_checkbutton[1], variable=self.var_2,
                                  onvalue=text_for_checkbutton[1], offvalue="", font=("Helvetica", 11))
        #ch_but_2.deselect()
        ch_but_3 = tk.Checkbutton(self.complaint_window, text=text_for_checkbutton[2],variable=self.var_3,
                                  onvalue=text_for_checkbutton[2], offvalue="", font=("Helvetica", 11))
        #ch_but_3.deselect()
        ch_but_4 = tk.Checkbutton(self.complaint_window, text=text_for_checkbutton[3], variable=self.var_4,
                                  onvalue=text_for_checkbutton[3], offvalue="", font=("Helvetica", 11))
        #ch_but_4.deselect()

        ch_but_1.pack(anchor="w", pady=10, padx=10)
        ch_but_2.pack(anchor="w", pady=10, padx=10)
        ch_but_3.pack(anchor="w", pady=10, padx=10)
        ch_but_4.pack(anchor="w", pady=10, padx=10)

        bt_1 = tk.Button(self.complaint_window, text="Повернутись", font="16", width="16", command=self.go_to_test_window)
        bt_1.pack(pady=(5, 0))
        bt_1.bind('<Return>', self.enter_button_handler_for_bt_1)

        bt_2 = tk.Button(self.complaint_window, text="Відправити", font="16", width="16",
                         command=lambda: self.send_to_bd())
        bt_2.pack(pady=(15, 20), padx=15)
        bt_2.bind('<Return>', self.enter_button_handler_for_bt_2)

    def enter_button_handler_for_bt_1(self, event):
        self.go_to_test_window()
        #self.start_window_bt_1.focus_force()

    def enter_button_handler_for_bt_2(self, event):
        self.send_to_bd()
        #self.start_window_bt_1.focus_force()

    def go_to_test_window(self):
        self.complaint_window.destroy()
        self.test_window.deiconify()
        self.answ.focus_force()

    def send_to_bd(self):
        compl = []
        if self.var_1.get() != "":
            compl.append(self.var_1.get())
        if self.var_2.get() != "":
            compl.append(self.var_2.get())
        if self.var_3.get() != "":
            compl.append(self.var_3.get())
        if self.var_4.get() != "":
            compl.append(self.var_4.get())
        complaints = ""

        # Elimination of adding empty rows to database
        if len(compl) != 0:
            for i in compl:
                complaints += i + "\n"
            complaints = complaints[0:len(complaints) - 1]
            con = sqlite3.connect('knowledge_checker.db')
            cur = con.cursor()
            sqlite_insert_query = """INSERT INTO complaints
                                      (question, complaints, subject, date) 
                                       VALUES (?,?,?,?);"""

            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            data_tuple = (self.ques, complaints, self.subj, dt_string)
            cur.execute(sqlite_insert_query, data_tuple)
            con.commit()
            con.close()
        self.go_to_test_window()


class FinalWindow:
    def __init__(self,num_of_ques, count_correct_answ, seconds):
        self.final_window = tk.Tk()
        self.final_window.title("Knowledge_checker")
        self.seconds = seconds

        # Size of window and locate window on the screen
        self.final_window.resizable(False, False)
        screen_width = self.final_window.winfo_screenwidth()
        screen_height = self.final_window.winfo_screenheight()
        window_width = 440
        window_height= 480
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.final_window.geometry(f'{window_width}x{window_height}+{x_cordinate}+{y_cordinate}')

        lbl_6 = tk.Label(self.final_window, text=f"\n\n ВИ  ВІДПОВИЛИ ПРАВИЛЬНО НА \n\n {count_correct_answ} з {num_of_ques} питань за {self.seconds} секунд !!! ",
        font="32")
        lbl_6.grid(column=0, row=0, columnspan=4, pady=50, padx=80)

        bt_5 = tk.Button(self.final_window, text="Продовжити \n тестування", font="16", width="16",
                         command=lambda: [self.final_window.destroy(), self.go_to_test_window()])
        bt_5.grid(column=1, row=1, columnspan=2)
        bt_5.focus_force()
        bt_5.bind('<Return>', self.enter_button_handler_for_bt_5)

        bt_6 = tk.Button(self.final_window, text="Вийти \n з програми", font="16", width="16", command=exit)
        bt_6.grid(column=1, row=2, pady=35, columnspan=2)
        bt_6.bind('<Return>', self.enter_button_handler_for_bt_6)

    def enter_button_handler_for_bt_5(self, event):
        self.final_window.destroy()
        self.go_to_test_window()

    def enter_button_handler_for_bt_6(self, event):
        exit()

    def go_to_test_window(self):
        ChoiceWindow()


start_window = tk.Tk()
start_window_inst = StartWindow(start_window)
start_window.mainloop()