from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import magic
from identifier.models import Book,Classes,School,SuggestedBooks
from identifier.serializers import BookSerializer,ClassesSerializer,SchoolSerializer,SuggestedBookSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from user.permission import IsAdminUser, IsLoggedInUserOrSuperAdmin, IsAdminOrAnonymousUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ObjectDoesNotExist
from .documents import BookDocument,SuggestedBookDocument
import abc
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination


from user.serializers import UserSerializer



class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)



class SearchBooks(PaginatedElasticSearchAPIView):
    serializer_class = BookSerializer
    document_class = BookDocument

    def generate_q_expression(self, query):
        return Q(
     'multi_match',
     query=query,
     fields=[
         'product_code'
     ])


class SearchSuggesteddBooks(PaginatedElasticSearchAPIView):
    serializer_class = SuggestedBookSerializer
    document_class = SuggestedBookDocument

    def generate_q_expression(self, query):
        return Q(
                'multi_match', query=query,
                fields=[
                    'suggester',
                    'advisory',
                    'type',
                    ], fuzziness='auto')
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

def check_in_memory_mime(in_memory_file):
        mime = magic.from_buffer(in_memory_file.read(), mime=True)
        return mime
class BookList(APIView):
#    authentication_classes = [JWTAuthentication]
 #   permission_classes = [IsAdminOrAnonymousUser]
    
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
        if check_in_memory_mime(request.FILES.get('pdf', None)) == 'application/pdf':
            extension = "pdf"
            book = request.FILES.get('pdf', None)
            if book.name.endswith(extension):
                serializer = BookSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                return JsonResponse(serializer.errors, status=400)
            else:
                return Response("error:Wrong extension")
        else:
            return Response("error:Wrong mime type")
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
