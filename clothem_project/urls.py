# clothem_project/urls.py
from django.contrib import admin
from django.urls import path
from clothem import views
from clothem_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),
    path('about_as/', views.main_page, name='about_as'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
