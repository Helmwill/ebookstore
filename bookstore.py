#Create program:
#menu to:
#    1.Enter book
#    2.update book
#    3.search book
#    4.delete book
#    0.exit
#create database:
#    enter existing data into dbms 
#    allow access to alter existing data 
#    allow access to add data 
#    create table to show users the data in a clear way.
#auto-increment
#delete books
#view all books
import sqlite3
class Book:

    #constructor method with instances 
    def __init__(self,db_connection,id='',title='',author='',qty=0):
        self.id = id
        self.title = title
        self.author = author
        self.qty = qty
        self.db_connection = db_connection


    #class variable 
    stock_par_lvl = 5

    #method for class variable
    def stock_lpar_lvl(self):

        if self.qty < self.stock_par_lvl:
            return f"{self.title} need to be ordered"
        else:
            return f"{self.title} stock is good"



    #method for recieving data from user to add to database
    def new_book_input(self, cursor):
        try:
            title = input("Enter book title: ")
            author = input("Enter Author's name: ")
            qty = int(input("Enter quantity avilable: "))

            new_book_values = [(title, author, qty)]
            self.add_books(cursor, new_book_values)
            self.db_connection.commit()
        except ValueError:
            print("invalid input. Please enter valid value")
    

    #method for adding new_book_input vakues into database 
    def add_books (self, cursor, new_book_values):
        try:
            bookdb_input ='''INSERT OR IGNORE INTO book(title, author, qty)
                            VALUES(?,?,?)''' 
            cursor.executemany(bookdb_input, new_book_values)
            self.db_connection.commit() 
            print("Book details added to the bookstore")
        except Exception as e:
            print(f"an error occured: {e}")


    #method to update existing books stored in the database
    def update_book(self, cursor):
        try:
            print("To update book please enter the title and author of the book")
            current_title = input("Enter book title to search: ")
            current_author = input("Please enter authors name: ")
            print(f"You would like to update {current_title} written by {current_author}?")
            change_book_confirm= input("if correct please confirm (Y/N): ").upper()
            
            search_query = '''
                SELECT * FROM book
                WHERE title=? AND author=?
            '''

            cursor.execute(search_query, (current_title, current_author))
            books_found = cursor.fetchall()

            if not books_found:
                print("No books found with the given title or author.")
            else:
                if change_book_confirm == "Y" or change_book_confirm == "Yes":
                    new_title = input("Enter updated book title: ")
                    new_author = input("Enter updated Author's name: ")
                    new_qty = int(input("Enter updated quantity avilable: "))

                    update_query = '''
                    UPDATE book
                    SET title=?, author=?, qty=?
                    WHERE title=? AND author=?
                    ''' 
                    new_book_values = (new_title, new_author, new_qty, current_title, current_author)
                    cursor.execute(update_query, new_book_values)
                    self.db_connection.commit()

                    print("Book added succesfully!")
                elif change_book_confirm == "N" or change_book_confirm == "No": 
                    print("Update canceled. Please try again.")
                else:
                    print(f"Please enter Y/N: ")
        except ValueError:
            print("Invalid input. Please re-enter correct information: ")
            pass
        except Exception as e:
                print(f"An error occurred: {e}")
            


    #method for the user to search for a specific book in database
    def search_book(self, cursor):
        try:
            search_book = input("Enter book title to search: ")
            search_author = input("Please enter Authors name: ")
            search_query = '''
                SELECT * FROM book
                WHERE title=? AND author=?
            '''

            cursor.execute(search_query, (search_book, search_author))
            books_found = cursor.fetchall()
            self.db_connection.commit()

            if not books_found:
                print("No books found with the given title or author.")
            else:
                print("Books found:")
                for book in books_found:
                    print(f"Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")
                    stock_par_lvl = 5
                    if book[3] < stock_par_lvl:
                            print(f"{book[1]} need to be ordered")
                    else:
                            print(f"{book[1]}: stock is good")
        except Exception as e:
                print(f"An error occurred: {e}")


    #method to delete a book from database
    def delete_book(self, cursor):
        try:
            delete_title = input("Enter the title of the book to delete: ")
            delete_author = input("Enter the author of the book to delete: ")
            delete_query = '''
            DELETE FROM book
            WHERE title=? AND author=?
            '''
            cursor.execute(delete_query, (delete_title, delete_author))
            self.db_connection.commit()
            print("Book deleted successfully!")
        except Exception as e:
           print(f"An error occurred: {e}")

    #method to view all books in database
    def view_all(self,cursor):
        try:
            cursor.execute('SELECT * FROM book')
            all_books = cursor.fetchall()
            self.db_connection.commit()
            print("all books stored: ")
            for table in all_books:                
                print(str(table)[1:-1])  
        except Exception as e:
           print(f"An error occurred: {e}")


menu = ''
try:
    with sqlite3.connect('ebookstore.db') as bs_db:
        # database initialization and table creation
        cursor = bs_db.cursor()
        #creating table and incremental id number automatically incremenets the id by +1
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                title TEXT,
                author TEXT, 
                qty INTEGER)
            ''')
        bs_db.commit()

        cursor.execute("SELECT COUNT(*) FROM book")
        count = cursor.fetchone()[0]
        # Checking if records exist in the table

        if count == 0:
            # Inserting initial book values if the table is empty
            book_values = [
                (3001, "A Tale of Two Cities", "Charles Dickens", 30),
                (3002, "Harry Potter and the Philosophers Stone", "J.K Rowling", 40),
                (3003, "The Lion, the Witch and the Wardrobe", "C.S Lewis", 25),
                (3004, "The Lord of the Rings", "J.R.R Tolkein", 37),
                (3005, "Alice in Wonderland", "Lewis Carroll", 12),
            ]
            cursor.executemany('INSERT INTO book(id, title, author, qty) VALUES (?,?, ?, ?)', book_values)
            bs_db.commit()
            print('Book details added to the bookstore')
        else:
            print("Records already exist in the database.")


        while True:
            menu = input('''
Welcome to the bookstore, 
please choose one of the following options:
1.Enter book
2.Update book
3.Search book
4.Delete book
5.View all
0.exit \n
: ''')      
            #calling add book function
            if menu == '1':
                try:
                    book = Book(db_connection=bs_db, id='', title='', author='', qty=0)
                    book.new_book_input(cursor)
                    pass
                except Exception as e:
                    print(f"An error occurred: {e}") 

            #calling update book function
            elif menu == '2':
                try: 
                    book = Book(db_connection=bs_db, id='', title='', author='', qty=0)
                    book.update_book(cursor)
                    pass                     
                except Exception as e:
                    print(f"An error occurred: {e}")

            #calling search book function
            elif menu == '3':
                try:
                    book = Book(db_connection=bs_db, id='', title='', author='', qty=0)
                    book.search_book(cursor)
                    pass
                except Exception as e:
                    print(f"An error occurred: {e}")

            #calling delete book function
            elif menu == '4':
                try:
                    book = Book(db_connection=bs_db, id='', title='', author='', qty=0)
                    book.delete_book(cursor)
                    pass
                except Exception as e:
                    print(f"An error occurred: {e}")
            #calling view all function
            elif menu == '5':
                try: 
                    book=Book(db_connection=bs_db, id='', title='', author='', qty=0)
                    book.view_all(cursor)
                    pass
                    
                except Exception as e:
                    print(f"An error occured: {e}")
            #exit menu
            elif menu == '0':
                print("Exiting the bookstore. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a valid option.")
except Exception as e:   
        print(f"An error occurred: {e}")