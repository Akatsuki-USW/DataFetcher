"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from getApi import views
from buzzing_admin import admin_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="🚀 Realtime Congestion Based Location Recommendation Service - 복쟉복쟉 admin_Server의 API 명세서입니다.",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('scheduler_status/', views.scheduler_status, name='scheduler_status'),
    path('auth/login/admin/', admin_views.AdminLoginView.as_view()),
    path('auth/admin/main/', admin_views.AdminMainView.as_view()),
    path('auth/admin/report/<int:report_id>/', admin_views.ReportDetailView.as_view()),
    path('auth/admin/report/<int:user_id>/unBan/', admin_views.UnbanUserView.as_view(), name='unBan'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]





