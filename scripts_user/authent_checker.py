from tkinter import messagebox
import sqlite3


def sign_inup_checker(name: str, psw_1: str, psw_2="1", key=False) -> bool:
    """
    Check the password and name fields during sign in and sign up
    :param name: username
    :param psw_1: entered password
    :param psw_2: repeat password psw_1, during registration
    :param key: key = True for sign in window; key = False for sign up window
    :return: bool
    """
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
        if check_counter == 2:
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

                    not_exist_name = \
                        cur.execute(f"SELECT NOT EXISTS(SELECT 1 FROM personal_data WHERE name='{name}');").fetchone()[
                            0]

                    if not_exist_name:
                        sqlite_insert_query = """INSERT INTO personal_data
                                                      (name, password) 
                                                       VALUES (?,?);"""
                        pers_data = (name, psw_1)
                        cur.execute(sqlite_insert_query, pers_data)
                        con.commit()
                        con.close()
                        messagebox.showinfo('confirmation', 'Запис зроблено')
                        return True
                    else:
                        warn = "Таке ім'я вже існує. Введіть інше.\nПідказка: cпробуйте додати до ім'я рік народження."
                        messagebox.showwarning("Warning", warn)
            else:
                con = sqlite3.connect('knowledge_checker.db')
                cur = con.cursor()
                exist_name = \
                    cur.execute(f"SELECT EXISTS(SELECT 1 FROM personal_data WHERE name = '{name}');").fetchone()[0]
                if exist_name:
                    correct_psw = cur.execute(f"SELECT * FROM personal_data WHERE name = '{name}';").fetchone()[2]
                    if correct_psw == psw_1:
                        return True
                    else:
                        messagebox.showwarning("confirmation", "Не вірно введений пароль.\nПеревірте будь-ласка.")

                else:
                    messagebox.showwarning("confirmation", "Не вірно введене ім'я.\nПеревірте будь-ласка.")
                con.close()


