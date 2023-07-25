from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('books/<int:pk>/', views.BookDetail.as_view()),
    path('schools/', views.SchoolList.as_view()),
    path('schools/<int:pk>/', views.SchoolDetail.as_view()),
    path('classes/', views.Classes.as_view()),
    path('classes/<int:pk>/', views.ClassesDetail.as_view()),
    path('suggestedbooks/',views.SuggestedBooksList.as_view()),
    path('suggestedbooks/<str:username>/',views.SuggestedBooksDetail.as_view()),
]