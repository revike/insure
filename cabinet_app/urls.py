from django.urls import path
from cabinet_app import views as cab_app

app_name = 'cabinet_app'

urlpatterns = [
    path('', cab_app.CabinetIndexView.as_view(), name='index_cab'),
]
