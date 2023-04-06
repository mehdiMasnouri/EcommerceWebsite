
from django.contrib import admin
from django.urls import path , include
from core.views import frontpage , about
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
# Order your URL patterns from most specific to least specific, 
# since Django will match the first URL pattern that matches the requested URL.

urlpatterns = [
    path('about/',about,name='about'),
    path('admin/', admin.site.urls),
    path('robots.txt',TemplateView.as_view(template_name='robots.txt',content_type='text/plain')),
    path('',include('userprofile.urls')),
    path('',frontpage,name='frontpage'),
    path('',include('store.urls')),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
