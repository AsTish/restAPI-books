"""
URL configuration for restAPIbooks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from myapp.views import \
    AuthorCreateView, \
    AuthorsListView, \
    BookCreateView, \
    BooksListView, \
    AuthorDetailView, \
    BookDetailView, \
    BookDeleteView, \
    AuthorDeleteView, \
    BookUpdateView


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation",
        # terms_of_service="https://www.example.com/terms/",
        # contact=openapi.Contact(email="support@example.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authors/create', AuthorCreateView.as_view(), name='create-author'),
    path('authors/', AuthorsListView.as_view(), name='list-authors'),
    path('books/create', BookCreateView.as_view(), name='create-book'),
    path('books/', BooksListView.as_view(), name='list-books'),
    path('authors/<uuid:id>/', AuthorDetailView.as_view(), name='author-detail'),
    path('books/<uuid:id>/', BookDetailView.as_view(), name='book_detail'),
    path('books/delete/<uuid:id>/', BookDeleteView.as_view(), name='book-delete'),
    path('authors/delete/<uuid:id>/', AuthorDeleteView.as_view(), name='author-delete'),
    path('books/update/<uuid:id>/', BookUpdateView.as_view(), name='book-update'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('openapi/', schema_view.without_ui(cache_timeout=0), name='schema-openapi-json'),
]
