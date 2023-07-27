from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from identifier.models import Book,Classes,School,SuggestedBooks
from identifier.serializers import BookSerializer,ClassesSerializer,SchoolSerializer,SuggestedBookSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from user.permission import IsAdminUser, IsLoggedInUserOrSuperAdmin, IsAdminOrAnonymousUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ObjectDoesNotExist
class SuggestedBooksList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAnonymousUser]
    def get(self,request,format=None):
        try:
        
            books = SuggestedBooks.objects.all()
            print(books)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SuggestedBookSerializer(books, many=True)
        return Response(serializer.data, status=200)

class SuggestedBooksDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAnonymousUser]
    def get(self,request,format=None):
        try:
            username =self.request.GET.get('username')
            books = SuggestedBooks.objects.filter(suggester__username=username)
        
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SuggestedBookSerializer(books)
        return Response(serializer.data)


class BookList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAnonymousUser]
    
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    #test
    def post(self, request, format=None):
        
        #data = JSONParser().parse(request)
        data = {
            "product_code": request.POST.get('product_code', None),
            "price": request.POST.get('price', None),
            "tax": request.POST.get('tax', None),

            "pdf": request.FILES.get('pdf', None),
            }
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class BookDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAnonymousUser]
    
    
    def get(self,request,format=None):
        try:
            pk =self.request.GET.get('pk')
            books = Book.objects.get(pk=pk)
        
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(books)
        return Response(serializer.data)

class Classes(APIView):
    """
    List all classes , or create a new class.
    """
    def get(self,request,format=None):
        try:        
            siniflar = Classes.objects.all()
            serializer = ClassesSerializer(siniflar, many=True)
            return JsonResponse(serializer.data, safe=False)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        try:
            data = JSONParser().parse(request)
            serializer = ClassesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except:
            return JsonResponse("An error occured", status=400)
class ClassesDetail(APIView):
    """
    Retrieve, update or delete a code snippet.
    """
    
    def get(self,request,format=None):
        try:
            pk =self.request.GET.get('pk')
            siniflar = Classes.objects.get(pk=pk)
        
            serializer = ClassesSerializer(siniflar)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
            
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SchoolList(APIView):
    """
    List all schools , or create a new school.
    """
    def get(self,request,format=None):
        try:
            school = School.objects.all()
            serializer = SchoolSerializer(school, many=True)
            
#                serializer.save()
            return Response(serializer.data, status=200)
            #return JsonResponse(serializer.errors, status=400)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request,format=None):
        try:        
            data = JSONParser().parse(request)
            serializer = SchoolSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SchoolDetail(APIView):
    """
    Retrieve, update or delete a code snippet.
    """
    def get(self,request,format=None):
        try:
            pk =self.request.GET.get('pk')
            school = School.objects.get(pk=pk)
        
        
            serializer = SchoolSerializer(school)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
