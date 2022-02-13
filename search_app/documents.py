from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from auth_app.models import CompanyUserProfile, CompanyUser
from main_app.models import ProductOption, Product, ProductCategory


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

        related_models = [
            Product, ProductCategory, CompanyUserProfile, CompanyUser
        ]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Product):
            return related_instance.productoption_set.all()
        elif isinstance(related_instance, ProductCategory):
            return related_instance.product_set.all()
        elif isinstance(related_instance, CompanyUserProfile):
            return related_instance.product_set.all()
