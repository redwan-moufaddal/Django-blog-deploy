from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404
urlpatterns = [
    path('', include("base.urls")),
    path("admin/", admin.site.urls),
    path('password_reset/', auth_views.PasswordResetView.as_view(), 
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), 
        name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'),    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), 
        name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = 'base.views.error'