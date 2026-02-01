from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    return redirect("mauribus_app:login")

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', root_redirect),                  # ✅ / redirige vers login admin
    path('', include('mauribus_app.urls')),   # toutes les autres URLs
]
