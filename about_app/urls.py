from django.urls import path
from about_app import views as about_app

app_name = 'about_app'

urlpatterns = [
    path('contacts/', about_app.ContactView.as_view(), name='contacts'),
    path('feedback/', about_app.FeedbackView.as_view(), name='feedback'),
    path('information/', about_app.InformationView.as_view(),
         name='information'),
    path('politics/', about_app.PoliticsView.as_view(), name='politics'),
    path('cookies/', about_app.CookieView.as_view(), name='cookie'),
]
