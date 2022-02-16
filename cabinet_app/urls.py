from django.urls import path
from cabinet_app import views as cab_app

app_name = 'cabinet_app'

urlpatterns = [
    path('', cab_app.CabinetIndexView.as_view(), name='profile'),
    path('update/<int:pk>/', cab_app.ProfileUpdateView.as_view(),
         name='profile_update'),
    path('profile-update/<int:pk>/', cab_app.ProfileUpdateView.as_view(),
         name='profile_update_data'),
]
