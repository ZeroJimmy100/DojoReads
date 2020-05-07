from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #index page (login/register)
    path('success/<int:user_Val>', views.successDisplay), # create user success
    path('success/create', views.create_user), # go to the create page
    path('login/display', views.validate_login), # validate if the user exist
    path('logoutUser', views.logout), # successful logout
    path('notlogin', views.index), # checks if the user is login if not GETOUT 
    path('books/add', views.AddBook), # adding/creating new book
    path('books/create', views.CreateBook), # process the book and go to the page
    path('users/<int:user_val>', views.view_this_user), # viewing the user page
    path('books/<int:myBook_ID>', views.view_book_page), # viewing the book page
    path('books/<int:get_id>/delete', views.delete_review)

]