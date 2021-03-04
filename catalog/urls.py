from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    #path('book/<int:pk>', views.index, name = 'book-detail'),
    path('authors/', views.AuthorListView.as_view(), name = 'author'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name = 'author-detail'),
    path('records', views.records, name='records'),
    path('cart', views.order, name='order'),
    path('checkout', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='loginUser'),
    path('login/',views.logout_view, name='logout_view'),
    

]