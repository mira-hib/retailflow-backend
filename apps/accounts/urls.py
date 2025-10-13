from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .View.auth_views import RegisterView
from .View.auth_views import LoginView
from .View.user_views import ChangePasswordView
from .View.user_views import PasswordResetRequestView
from .View.user_views import PasswordResetConfirmView
from .View.auth_views import TokenRefreshView
from .View.auth_views import LogoutView
from .View.user_views import UserUpdateView
from .View.user_views import UserSoftDeleteView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('changePassword/', ChangePasswordView.as_view(), name='changePassword'),
    path("password_reset/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('<uuid:public_id>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<uuid:public_id>/delete/', UserSoftDeleteView.as_view(), name='user_soft_delete'),

]