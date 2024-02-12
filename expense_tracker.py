import sqlite3
from flask import Flask
import datetime
app = Flask()
class income:
    def __init__(self, db_connect, date = '', description = '', category = '', income = '', expense = '', overall_balance = ''):
        self.db_connect = db_connect
        self.date = date 
        self.description = description
        self.category = category 
        self.income = income
        self.expense = expense 
        self.overall_balance = overall_balance 

    def new_exp_input(self, cursor):
            try:
                date = input("Enter the date of the expense (DD/MM/YY): ")
                description = input("Enter description of the expense: ")
                expense = float(input("Enter expense amounnt: "))

                new_expense_value = [(date,description,expense)]

            except ValueError:
                print("Please enter correct information")
                 
                



menu = ''
try:
    with sqlite3.connect('finance_tracker.db') as finance_db:
        cursor = finance_db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Finances(
            Date INTEGER PRIMARY KEY AUTOINCREMENT,
            Description TEXT,
            Category TEXT,
            Income INTEGER,
            Expense INTEGER,
            Overall balance INTEGER)               
        ''')
        finance_db.commit()
        
        cursor.execute("SELECT COUNNT(*) FROM Finances")
        count = cursor.fetchone()[0]
        
        if count == 0:
            example_values = [
            (2023-05-22, "monthly payment", "salary", 3000, 0)
            (2023-06-22, "monthly payment", "salary", 3000, 0)
            (2023-10-15, "holiday bookings", "personal spending", 0, 975)
            (2023-10-22, "holiday money exchange", "personal spending", 0, 300)
            (2023-11-04, "taxi", "personal spending", 0, 13)
            (2023-11-19, "freelance work", "salary", 15, 0)        
            ]
            cursor.executemany('INSERT INTO Finances(Date, Description, Category, Income, Expense) VALUES (?,?,?,?,?)', example_values)
            finance_db.commit
            print('example details added to the database.')
        else:
            print('records already exist in database.')