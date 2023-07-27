
from rest_framework import serializers
from identifier.models import Book,Classes,School,SuggestedBooks
from user.models import User
from user.serializers import UserSerializer




class BookSerializer(serializers.Serializer):
    
    product_code = serializers.CharField(required=True,allow_blank=True)
    price = serializers.CharField(required=True,allow_blank=True)
    tax = serializers.CharField(required=True,allow_blank=True)
    pdf = serializers.FileField(allow_empty_file=False)
    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.product_code = validated_data.get('product_code', instance.product_code)
        instance.price = validated_data.get('price', instance.fiyat)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.pdf = validated_data.get('pdf', instance.pdf)
        
        instance.save()
        return instance
class SuggestedBookSerializer(serializers.Serializer):
    suggester = UserSerializer()
    books = BookSerializer(many=True)
    advisory = serializers.CharField(required=True,allow_blank=True)
    class Meta:
        model = SuggestedBooks
       # fields = ('id','suggester','advisory','books')
    def create(self, validated_data):
        return SuggestedBooks.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.suggester = validated_data.get('suggester', instance.suggester).lower()
        instance.books = validated_data.get('books', instance.books).lower()
        instance.advisory = validated_data.get('advisory', instance.advisory).lower()
        instance.save()
        return instance


class ClassesSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    class Meta:
        model = Classes
        fields = ('id','class_name', 'class_number','keycode','books',)
    
    def create(self, validated_data):
        return Classes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.class_number = validated_data.get('class_number', instance.Classes_NUMARASI)
        instance.keycode = validated_data.get('keycode', instance.sube)
        instance.books = validated_data.get('books', instance.books)
        instance.save()
        return instance
class SchoolSerializer(serializers.ModelSerializer):
    classesq = ClassesSerializer(many=True)
    class Meta:
        model = School
        fields = ('id', 'logo','name','city','country','classesq',)
        depth = 1 
    
    def create(self, validated_data):
        
        return School.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.logo = validated_data.get('logo', instance.logo)
        instance.name = validated_data.get('name', instance.name)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.classesq = validated_data.get('classesq', instance.classesq)
        instance.save()
        return instance
 
 
