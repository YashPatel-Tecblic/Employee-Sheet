from django.urls import path
from . import views

urlpatterns = [
    path('details/',views.DetailsAPI.as_view()),
    path('details/<int:pk>/',views.DetailsAPI.as_view()),
    path('adduser/',views.AddInfoAPI.as_view()),
    path('adduser/<int:pk>/',views.AddInfoAPI.as_view())
    # path('gsheet/<int:pk>/',views.DetailsAPI.as_view()),
]