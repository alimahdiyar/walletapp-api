from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view

from walletapp.views import SendVerificationCodeView

schema_view = get_schema_view(
   openapi.Info(
      title="WalletApp API",
      default_version='development version',
      description="CafePay API Documentation",
      contact=openapi.Contact(email="alimahdiyar77@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('user-profile/send-code/', SendVerificationCodeView.as_view()),

   # docs
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
