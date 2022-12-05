from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from . import views

router = routers.DefaultRouter()
router.register(r'apprenants', views.ApprViewSet)
router.register(r'briefs', views.BriefViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('briefs/gen_groups/<int:pk>', views.GenGoupsView.as_view(), name="gen_groups"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger_ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
