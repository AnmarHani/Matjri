from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="product_index"),
    path("productGet/<int:id>/", views.productGetPage, name="productGet"),
    path("productCreate/", views.productCreatePage, name="productCreate"),
    path("productUpdate/<int:id>/", views.productUpdatePage, name="productUpdate"),
    path("productDelete/<int:id>/", views.productDeletePage, name="productDelete"),
    path("notYet/", views.notYet, name="notYet"),
    path("Like/<int:id>/", views.productLikes, name="Like"),
]
