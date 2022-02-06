from django.urls import path
from search_app import views as search_app

app_name = 'search_app'

urlpatterns = [
    path('', search_app.SearchView.as_view(), name='search'),
]
