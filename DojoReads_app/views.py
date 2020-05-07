from django.shortcuts import render, redirect, HttpResponse
from .models import User, UserManager, Book, Review, Author
from django.contrib import messages
import bcrypt


# Create your views here.

def index(request):
    users = User.objects.all()
    context = {
        "all_users": users
    }
    return render(request, "index.html", context)

# Successful login page
def successDisplay(request, user_Val):
    users = User.objects.get(id = user_Val)
    books = Book.objects.all()
    filter_books = Book.objects.filter().order_by('-id')[:3]
    reviews = Review.objects.all()
    all_users = User.objects.all()
    
    if "user" not in request.session:
        return redirect("/")
    context = {
        "create_user": users,
        "these_books": books,
        "all_reviews": reviews,
        "the_users": all_users,
        "three_books": filter_books,

    }
    return render(request, "BookPage.html", context)

# Create a new user
def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    password = request.POST['type_password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
    print(pw_hash) 
    
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        # print("*"*50, "\n", errors)
        return redirect("/")
    else:
        newUser = User.objects.create(name = request.POST["type_name"], 
        alias = request.POST["type_alias"], email = request.POST["type_email"],
        password = pw_hash)

        request.session['user'] = newUser.id
        return redirect(f"/success/{newUser.id}")
    
# Checks if their is a user that exist in the database
def validate_login(request):
    user = User.objects.filter(email=request.POST['type_login_email']) 
    print(user)
    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['type_login_password'].encode(), logged_user.password.encode()):
            request.session["user"] = logged_user.id
            print("password match")
            return redirect("/success/{}".format(logged_user.id))
        else:
            print("failed password")
            messages.error(request, "Invalid password")
            return redirect("/")
    messages.error(request, "No account associated to email")
    print ("No account associated to email")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")


# Show adding/creating a book/author
def AddBook (request):
    all_authors = Author.objects.all()
    the_ratings = Review.objects.all()
    active_user = User.objects.get(id=request.session['user'])
    context = {
        "user": active_user,
        "authors": all_authors,
        "these_ratings": the_ratings
    }
    return render (request, 'AddorReview.html', context)

# logic in creating the book/author
def CreateBook(request):
    #check if there is a new author
        #if there is, create that author and set it as the variable "use this author"
        #if not, grab the existing author from the database and set it as the variable "use this author"
    #create the book with the author "use this author" 

    if len(request.POST['get_author_name']) > 0:
        myAuthor = Author.objects.create(name=request.POST['get_author_name'])
    else:
        myAuthor = Author.objects.get(id=request.POST['existing_author'])
    this_user_id = User.objects.get(id=request.session['user'])
    newBook = Book.objects.create(title = request.POST['get_title'], author = myAuthor, uploaded_by = this_user_id)
    this_book_id = newBook
    newReview = Review.objects.create(written_review = request.POST['get_reviews'], ratings = request.POST['my_ratings'], books = this_book_id, user_reviewer = this_user_id)
    
    myBook_ID = newBook.id

    return redirect(f"/books/{myBook_ID}")

# View the book page and able to review it 
def view_book_page(request, myBook_ID):
    my_Book = Book.objects.get(id=myBook_ID)

    current_user_id = request.session['user']
   
    this_book_authors = my_Book.author
    
    my_user_reviewers = Review.objects.all()

    context = {
        "the_book": my_Book,
        "this_book_author": this_book_authors,
        "the_other_review": my_user_reviewers,
        "this_user": current_user_id,
    }

    return render(request, "view_book_review.html", context)

# Delete the review
def delete_review(request, get_id):
    del_review = Review.objects.get(id=get_id)
    del_review.delete()
    book_page_id = Book.objects.get(id=request.session['book'])
    return redirect(f"/books/{user_page_id}") 

# Viewing the user's page
def view_this_user(request, user_val):
    ok_user = User.objects.get(id = user_val)
    reviews = Review.objects.filter(user_reviewer= ok_user)
    int_reviews = Review
    context = {
        "this_user": ok_user,
        "book_I_review": reviews
    } 
    return render(request, "viewUser.html", context)
    
