from django.urls import path
from .views import RegisterView,LoginView,barrrowView,bokkslistView

urlpatterns = [
    path('register',RegisterView.as_view(),name='register'),
    path('loginuser',LoginView.as_view(),name='loginuser'),
    path('barrrow',barrrowView.as_view(),name='barrrow'),
    path('userbarrrow',bokkslistView.as_view(),name='userbarrrow'),
]