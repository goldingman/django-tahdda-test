import logging
from django.contrib.auth.models import User
from .models import Book
from .serializers import (
    BookSerializer, 
    RegisterSerializer, 
    MyTokenObtainPairSerializer
)
from rest_framework import (
    generics, 
    status, 
    serializers
)
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view, schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger('django')

# Create your views here.
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'Login [POST]': 'api/login',
        'Register [POST]': 'api/register',
        'Get All Books [GET]': 'api/books',
        'Search by Title [GET]': 'api/books?title__contains=title',
        'Search by Author [GET]': 'api/books?author__contains=author',
        'Get a Book [GET]': 'api/books/:id',
        'Add a Book [POST]': 'api/books',
        'Update a Book [PUT]': 'api/books/:id',
        'Delete a Book [DELETE]': 'api/books/:id'
    }
 
    return Response(api_urls)

@swagger_auto_schema(methods=['post'], request_body=BookSerializer)
@api_view(['GET', 'POST'])
def add_or_get_book(request):
    if request.method == 'GET':

        if request.query_params:
                books = Book.objects.filter(**request.query_params.dict())
        else:
            books = Book.objects.all()
        
        # if there is something in items else raise error
        if books:
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'POST':

        book = BookSerializer(data=request.data)
        # validating for already existing data
        if Book.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')
    
        if book.is_valid():
            book.save()
            return Response(book.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(methods=['put'], request_body=BookSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
def action_book(request, id):

    try:
        book = Book.objects.get(pk=id)

        if request.method == 'GET':

            data = BookSerializer(book)
            return Response(data.data, status=status.HTTP_202_ACCEPTED)
        
        elif request.method == 'PUT':

            valid_fields = [field.name for field in Book._meta.get_fields()]
            for field in request.data.keys():
                if field not in valid_fields:
                    return Response({"message": f"Invalid field: {field}"}, status=status.HTTP_400_BAD_REQUEST)
                
            data = BookSerializer(book, data=request.data, partial=True)
            if data.is_valid():
                data.save()
                return Response(data.data)
            else:
                return Response({"message": "Book validation error."}, status=status.HTTP_404_NOT_FOUND)
   
        elif request.method == 'DELETE':
            
            book.delete()
            return Response({"message": "Book deleted successfully."})
            
    except Book.DoesNotExist:
            return Response({"message": "Book not found."}, status=status.HTTP_404_NOT_FOUND)