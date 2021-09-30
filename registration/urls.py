from django.urls import path
from registration.views import RegisterView, ActivateView, LoginView, LogoutView, ForgotPasswordCompleteView, \
    ChangePasswordView, ForgotPasswordView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('activate/<str:activation_code>/',ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password/complete/', ForgotPasswordCompleteView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
]
