from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="DOCUMENTAÇÃO API PROUNI",
        default_version='v1',
        description="Esta API oferece funcionalidades de CRUD (Create, Read, Update, Delete) para gerenciar recursos específicos, requerendo autenticação para operações sensíveis. Os métodos disponíveis permitem interações seguras com os dados por meio de endpoints bem definidos. Para acessar endpoints protegidos, é necessário autenticar-se utilizando um token de autenticação válido.",
        terms_of_service="https://www.seusite.com/terms/",
        contact=openapi.Contact(email="contato@seusite.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('user/', views.get_users, name='get_all_users'),
    path('user/<int:id>', views.get_by_id),
    path('user/create', views.post_create_user),
    path('user/update/<int:id>', views.put_edit_user),
    path('user/delete/<int:id>', views.delete_user),
    path('login/', views.LoginView.as_view()),
    path('user/resultado/<int:id>', views.get_result_ia_by_id),
    path('user/create/resultado/<int:id>', views.post_resultado_ia),
    path('consultar_cep/<str:cep>/', views.consultar_cep),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]