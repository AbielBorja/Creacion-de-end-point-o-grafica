from django.urls import path
from .views import getInfo, loginView, signUpView, logout_user, private_page

urlpatterns = [
    path('', loginView, name="login"),
    path('signup/', signUpView, name="signup"),
    path('logout/', logout_user, name="logout"),
    path('APIs/', private_page, name="APIs_pages"),
    path('getInfo/', getInfo, name="GET"),
]