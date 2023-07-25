from django.contrib import admin
from identifier.models import School, Classes, Book,SuggestedBooks
# Register your models here.
class SchoolPage(admin.ModelAdmin):
    list_display = ('id','name','city')
    list_display_links = ('name','city')
    list_filter = ('city',)
    
    search_fields = ('name',)
       
    

admin.site.register(School, SchoolPage)

class SuggestedBPage(admin.ModelAdmin):
    list_display= ('id','suggester')
    search_fields = ('suggester',)
admin.site.register(SuggestedBooks, SuggestedBPage)
class ClassesPage(admin.ModelAdmin):
    
    
    
    list_display = ('id','class_name','keycode')
    list_display_links = ('id','class_name','keycode')
    list_filter = ('class_name',)
    
    search_fields = ('class_name',)
    
    

admin.site.register(Classes, ClassesPage)
class BookPage(admin.ModelAdmin):
    
    list_display = ('id','product_code')
    list_display_links = ('id','product_code')
    list_filter = ('id','product_code',)
    
    search_fields = ('product_code',)
    
admin.site.register(Book, BookPage)

