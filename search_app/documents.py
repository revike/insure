from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from main_app.models import ProductOption


@registry.register_document
class ProductOptionDocument(Document):
    """New Document Products"""
    product = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'category': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'description': fields.TextField(),
            'is_active': fields.BooleanField()
        }),
        'company': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'company': fields.ObjectField(properties={
                'is_active': fields.BooleanField()
            }),
            'name': fields.TextField(),
            'about_company': fields.TextField(),
            'label': fields.FileField(),
            'is_active': fields.BooleanField()
        }),
        'name': fields.TextField(),
        'short_desc': fields.TextField(),
        'description': fields.TextField(),
        'is_active': fields.BooleanField()
    })

    class Index:
        name = 'products'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = ProductOption
        fields = [
            'id',
            'price',
            'term',
            'rate',
            'is_active'
        ]
