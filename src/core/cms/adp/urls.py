from django.urls import (
    path
)

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from src.core.cms.adp.views import (
    UserRegistrationValidationView,
    UserRegistrationView,
    UserAuthorizationView,
    SendConfirmationCodeView,
    VerifyConfirmationCodeView,
    ProtectedView
)

urlpatterns = [
    path('validate-registration/', UserRegistrationValidationView.as_view(), name='validate_registration'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('authorization/', UserAuthorizationView.as_view(), name='authorization'),

    path('send-code/', SendConfirmationCodeView.as_view(), name="send_code"),
    path('verify-code/', VerifyConfirmationCodeView.as_view(), name="verify_code"),

    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]