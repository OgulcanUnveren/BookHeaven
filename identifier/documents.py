from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import SuggestedBooks, Book




@registry.register_document
class BookDocument(Document):
    id = fields.IntegerField()


    class Index:
        name = 'books'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Book
        fields = [
            'price',
            'tax',
            'pdf'
        ]


@registry.register_document
class SuggestedBookDocument(Document):
    suggester = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(),
        'last_name': fields.TextField(),
        'username': fields.TextField(),
    })
    books = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'product_code': fields.TextField(),
        'price': fields.IntegerField(),
        'tax': fields.IntegerField(),
        'pdf':fields.FileField(),
    
    })
    type = fields.TextField(attr='type_to_string')
    advisory = fields.TextField()
    class Index:
        name = 'suggestedbooks'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = SuggestedBooks
        fields = [
            'id',
        ]