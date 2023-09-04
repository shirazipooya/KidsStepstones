from django.contrib.auth import views
from django.urls import path, include, re_path
from .views import home, Login, PasswordChange, PasswordChangeDone, PasswordReset, PasswordResetDone, PasswordResetConfirm, PasswordResetComplete, Register, activate

app_name = "account"
urlpatterns = [
    path("reset/<uidb64>/<token>/", PasswordResetConfirm.as_view(),name="password_reset_confirm"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("password_change/", PasswordChange.as_view(), name="password_change"),
    path("password_change/done/", PasswordChangeDone.as_view(), name="password_change_done"),
    path("password_reset/", PasswordReset.as_view(), name="password_reset"),
    path("password_reset/done/", PasswordResetDone.as_view(), name="password_reset_done"),
    path("reset/done/", PasswordResetComplete.as_view(), name="password_reset_complete"),
    path('register/', Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),

]

urlpatterns += [
    path("", home, name="home"),
]
