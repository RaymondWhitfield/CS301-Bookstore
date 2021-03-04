from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Genre)
admin.site.register(Language)
#admin.site.register(Customer)
#admin.site.register(Order)
#admin.site.register(ShippingAddress)

class AuthorInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer','order','address', 'city','state','zip')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer','id','date_ordered','submitted', 'confirmation_num')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name',  ('date_of_birth', 'date_of_death'),]
    


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language', 'image' )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ( 'book','order', 'quantity', 'date_added')
    list_filter = ()