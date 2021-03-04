from django.shortcuts import render, redirect
from catalog.models import *
from django.http import JsonResponse
import json, datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm
from django.contrib import messages
# Create your views here.

#Render login page
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
    context = {}

    return render(request, 'login.html', context=context)

#View to logout user
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('loginUser')

#Render registration page
def register(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account Created for '+ user)
            
            return redirect('loginUser')

    context= {'form':form,}

    return render(request,'register.html', context=context)

#Render home page
def index(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, submitted=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,}
        cartItems = order['get_cart_items']

    books = Book.objects.all()
    context={'items':items,'books':books,'order':order, 'cartItems':cartItems,}
    return render(request, 'index.html', context=context)

#Render cart data
def order(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, submitted=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,}
        cartItems = order['get_cart_items']

    books = Book.objects.all()
    context={'items':items,'books':books,'order':order, 'cartItems':cartItems,}
    return render(request, 'cart.html', context=context)

#If user logged in, add items to cart. If none logged in, set cart to empty. Render.
def checkout(request):
    books = Book.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, submitted=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,}
        cartItems = order['get_cart_items']

    context={'items':items,'books':books,'order':order,'cartItems':cartItems}
    return render(request, 'checkout.html', context=context)

#JS view function update cart items
def updateItem(request):
    data = json.loads(request.body)
    bookId = data['bookId']
    action = data['action']
    print('Action:', action)
    print('bookId:', bookId)

    customer = request.user.customer
    book = Book.objects.get(id=bookId)
    order, created = Order.objects.get_or_create(customer=customer, submitted=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, book=book)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added to cart', safe=False)

def processOrder(request):
    confirmation_num = datetime.datetime.now()
    data = json.loads(request.body)
    if request.user.is_authenticated:

        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, submitted=False)
        total = float(data['form']['total'])
        order.confirmation_num = confirmation_num
        
        if total == order.get_cart_total:
            order.submitted = True
        order.save()

        if order.submitted == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zip = data['shipping']['zip'],
                
                )
    else:
        print('No user logged in')

    print('Data:', request.body)
    return JsonResponse('Payment complete', safe=False )

#query data for records
def records(request):
    num_books = Book.objects.all().count()
    num_order = Order.objects.all().count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_books_fiction = Book.objects.filter(genre__name__icontains='fiction').count()
    num_books_children = Book.objects.filter(genre__name__icontains='children').count()
    num_books_classics = Book.objects.filter(genre__name__icontains='classic').count()
    context = {
        'num_books': num_books,
        'num_order': num_order,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_fiction': num_books_fiction,
        'num_books_children': num_books_children,
        'num_books_classics': num_books_classics,
    }
    return render(request, 'records.html', context=context)

from django.views import generic

#generic Book List of Books in DB
class BookListView(generic.ListView):
    model = Book
    paginate_by = 20
    template_name = 'book_list.html'

#generic Book Details of Books in DB
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'

#List of all Authors in DB
class AuthorListView(generic.ListView):
    model = Author
    template_name = 'author_list.html'

#Author detail
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'
    