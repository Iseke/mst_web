from django.urls import path

from rest_framework.routers import SimpleRouter

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.blacklist.views import BlacklistView

from apps.users import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', obtain_jwt_token),
    path('logout/', BlacklistView.as_view({"post": "create"})),
    path('forgot_password/', views.ForgotPasswordView.as_view()),
]
router = SimpleRouter()
router.register(r'password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})',
                views.PasswordResetView, basename='reset')

urlpatterns += router.urls
