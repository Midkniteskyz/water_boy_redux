from django.urls import path, include

from .views import LatestProductsList, ProductDetail, CategoryDetail 

app_name = "product_app" # for namespacing
urlpatterns = [
    path("latest-products/", LatestProductsList.as_view()),
    # path("product/search/", search),
    path("products/<slug:category_slug>/<slug:product_slug>/", ProductDetail.as_view()),
    path("products/<slug:category_slug>", CategoryDetail.as_view()),
]