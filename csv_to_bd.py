import sqlite3
import csv

def csv_to_bd(path, subject):
    subj = subject
    con = sqlite3.connect("knowledge_checker.db")
    cur = con.cursor()
    #cur.execute(f"CREATE TABLE IF NOT EXISTS {subj} (questions, answers, form);")

    with open(path, 'r') as fin:
        dr = csv.DictReader(fin, delimiter=";")
        to_db = [(i["questions"], i["answers"], i["form"]) for i in dr]

    cur.executemany(f"INSERT INTO {subj} (questions, answers, form) VALUES (?, ?, ?);", to_db)
    con.commit()
    con.close()