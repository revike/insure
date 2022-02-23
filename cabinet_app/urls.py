from django.urls import path
from cabinet_app import views as cab_app

app_name = 'cabinet_app'

urlpatterns = [
    path('', cab_app.CabinetIndexView.as_view(), name='profile'),
    path('update/<int:pk>/', cab_app.ProfileUpdateView.as_view(),
         name='profile_update'),
    path('profile_update/<int:pk>/', cab_app.ProfileUpdateView.as_view(),
         name='profile_update_data'),
    path('my_products', cab_app.MyProductListView.as_view(),
         name='my_products'),
    path('product_update/<int:pk>/', cab_app.MyProductUpdateView.as_view(),
         name='product_update'),
    path('product_update_title/<int:pk>/',
         cab_app.MyProductUpdateView.as_view(), name='product_update_title'),
    path('product_option_delete/<int:pk>/',
         cab_app.MyProductDeleteView.as_view(), name='product_option_delete'),
    path('product_delete/<int:pk>/', cab_app.MyProductDeleteView.as_view(),
         name='product_delete'),
]
