from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("accounts.urls")),
    path("", include("core.urls")),
    path("profile/", include("profiles.urls")),
    path("chat/", include("chat.urls")),
]
