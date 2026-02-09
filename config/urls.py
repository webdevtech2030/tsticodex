from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/listings/", include("listings.urls")),
    path("api/v1/bookings/", include("bookings.urls")),
    path("api/v1/payments/", include("payments.urls")),
    path("api/v1/blogs/", include("blogs.urls")),
    path("", include("users.urls")),
]
