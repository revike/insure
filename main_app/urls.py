from django.urls import path
from main_app import views as main_app

app_name = 'main_app'

urlpatterns = [
    path('', main_app.IndexView.as_view(), name='index'),
    path('category/<int:pk>/', main_app.ProductForCategoryDetailView.as_view(),
         name='category'),
    path('product/', main_app.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', main_app.ProductDetailView.as_view(),
         name='product'),
    path('response-valid/<int:pk>', main_app.ResponseValidView.as_view(),
         name='valid'),
]
