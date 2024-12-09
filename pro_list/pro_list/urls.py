
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/',include('todolist.urls')),
    path('da_queen/',include("da_queen.urls")),
    path('Myblog/',include('Blog.urls')),
     path('Neoshop/',include('Neoshop.urls'))
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)