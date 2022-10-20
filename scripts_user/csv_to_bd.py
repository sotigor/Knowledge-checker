import sqlite3
import csv


def csv_to_bd(path, subject) -> None:
    """
    Transfer data from csv file to database
    :param path: path to csv file
    :param subject: subject name (table name in database)
    :return: None
    """

    # Connect to database
    con = sqlite3.connect("knowledge_checker.db")
    cur = con.cursor()

    # open csv file and upload data to a list
    with open(path, 'r') as fin:
        dr = csv.DictReader(fin, delimiter=";")
        to_db = [(i["questions"], i["answers"], i["form"]) for i in dr]

    # insert data to database
    cur.executemany(f"INSERT INTO {subject} (questions, answers, form) VALUES (?, ?, ?);", to_db)
    con.commit()
    con.close()
