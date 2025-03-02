from django.urls import path

from users.views import auth_views

urlpatterns = [
    path('signup/', auth_views.SignupView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('test/', auth_views.TestView.as_view(), name='test'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('details/', auth_views.UserDetails.as_view(), name='details'),

]