class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}
        #dict is {Book(object): rating}
        
    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        #takes in a new email and changes the email associated with the user
        return "The email address of {name} has been updated to {address}".format(name=self.name, address=self.email)

    def __repr__(self):
        return "Username: {name}, email: {address}, books read: {number}".format(name=self.name, address=self.email, number=len(self.books))
        
    def __eq__(self, other_user):
        return (self.name == other_user.name) and (self.email == other_user.email)
        
    def read_book(self, book, rating=None):
        self.books[book] = rating
        return self.books
    
    #This method is for the get_n_most_prolific_reader function. 
    def get_book_count(self):
        return len(self.books)
    
    def __hash__(self):
        return hash((self.name, self.email))
        
    def get_average_rating(self):
        return sum([rating for rating in self.books.values() if rating is not None]) / len(self.books)

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        self.isbn_list = []
        
    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self, new_isbn):
        self.new_isbn = new_isbn
        return "The isbn of {title} has been updated to {new_isbn}".format(title=self.title, new_isbn=self.new_isbn)

    def add_rating(self, rating):
        if (rating is None) or (0 <= rating <=4):
        #Kept getting a TypeError: 'NoneType' and 'int'
            self.ratings.append(rating)
        else:
            print("Invalid Rating")
    
    def __eq__(self, other_book):
        return (self.title == other_book.title) and (self.isbn == other_book.isbn)
    
    def get_average_rating(self):
        return sum([rating for rating in self.ratings if rating is not None]) / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))
    
    def __repr__(self):
        return "{title} with isbn number {isbn}".format(title=self.title, isbn=self.isbn)

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author
    
    def get_author(self):
        return self.author
    
    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level
    
    def get_subject(self):
        return self.subject
    
    def get_level(self):
        return self.level
    
    def __repr__(self):
        return "{title}, a(n) {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)
    
class TomeRater:
    def __init__(self):
        self.users = {}
        #will map a user's email to the corresponding User object
        self.books = {}
        #will map a Book object to the number of Users that have read it
    
    def create_book(self, title, isbn):
        return Book(title, isbn)
    
    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)
    
    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)
    
    def add_book_to_user(self, book, email, rating=None):
        if email in self.users.keys():
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("No user with email {}".format(email))

    def valid_email(self, email):
        if email.find("@") >= 0 and (email[-4:] == ".com") or (email[-4:] == ".edu") or (email[-4:] == ".org"):
            return True
        else: 
            print("{email} is not a valid email address".format(email=email))
        #I know I've taken the instructions to the letter here and in reality you'd need to be able to accept .co.uk 
        #email addresses and so forth. 
        
    def add_user(self, name, email, user_books=None):
        if self.valid_email(email): 
            if email in self.users.keys():
                print("A user with email address {email} already exists. Please use another email address.".format(email=email))
            else:
                new_user = User(name, email)
                self.users[email] = new_user
                if user_books != None:
                    for book in user_books:
                        self.add_book_to_user(book, email)
    
    def print_catalog(self):
        for book in self.books.keys():
            print(book)
    
    def print_users(self):
        for user in self.users.values():
            print(user)
            
    def most_read_book(self):
        max_read = 0
        most_popular_book = ""
        for book, read in self.books.items():
            if read >= max_read:
                max_read = read
                most_popular_book = book
        return most_popular_book
    
    def highest_rated_book(self):
        highest_rating = 0
        highest_rated_book_title = ""
        for book in self.books.keys():
            av_rating = book.get_average_rating()
            if av_rating >= highest_rating:
                highest_rating = av_rating 
                highest_rated_book_title = book
        return highest_rated_book_title

    def most_positive_user(self):
        most_positive_user_name = ""
        highest_user_rating = 0
        for user in self.users.values():
            if user.get_average_rating() >= highest_user_rating:
                most_positive_user_name = user
                highest_user_rating = user.get_average_rating()
        return most_positive_user_name

    #idea is to get the top n books. i.e. if n is 3, return the top 3 most read books, in descending order.
    def get_n_most_read_books(self, n):
        n_most_read_books = sorted(self.books, key=self.books.get, reverse=True)
        #I confess I didn't know how to write this function, so I found the answer on stackoverflow. 
        #Using sorted() seemed to be the best way without importing any additional classes such as Counter.  
        #I already have a dictionary with the books as keys, and the number of users who have read the book as 
        #the values - i.e. self.books. This is then sorted by key (i.e. by book name). It is automatically set
        #to be sorted in ascending order - i.e. to False, so I have reversed this using True. 
        
        #Have added in what happens if n=0 or n is greater than the number of different books read. 
        if n <= 0:
            return "Error: please input a positive number to find the most read books."
        elif n > len(n_most_read_books):
            n2 = len(n_most_read_books)
            top_n2 = n_most_read_books[:n2]
            return "There are less than {n} books in the list. These are the top {n2} books in descending order: {top_n2}".format(n=n, n2=n2, top_n2=top_n2)
        else:   
            top_n = n_most_read_books[:n]
            return "The top {n} most read books in descending order are: {top_n}".format(n=n, top_n=top_n)
        
    def get_n_most_prolific_readers(self, n):
        #I need to make a dictionary with keys being users, and number of books read being the values.
        #self.books in User class has this information.....I don't know how to access it from here....so I've 
        #put in a new method in the User class to count the number of books read per user instance. 
        #I kept getting an error saying 'User' wasn't hashable so I've added __hash__ to the User class. 
        #I looked up how to use lambda in a sorted() function. 
        
        prolific_readers = {}
        for reader in self.users.values():
            prolific_readers[reader] = reader.get_book_count()
        n_most_prolific_readers = sorted(prolific_readers.items(), key=lambda reader:reader[1], reverse=True)
        
        #Again, I've included what happens if n<0 or no of users is less than n. 
        if n<=0: 
            return "Error: please input a positive number to find the most prolific readers."
        elif n > len(n_most_prolific_readers):
            n2 = len(n_most_prolific_readers)
            top_n2 = n_most_prolific_readers[:n2]
            return "There are less than {n} readers in our database. These are the top {n2} most prolific readers in descending order: {top_n2}".format(n=n, n2=n2, top_n2=top_n2)
        else:   
            most_prolific = n_most_prolific_readers[:n]
            return "The top {n} most prolific readers in descending order are: {most_prolific}".format(n=n, most_prolific=most_prolific)


        