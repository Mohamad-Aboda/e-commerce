from django.urls import path
from .apis import CategoryListCreateView, CategoryRetriveUpdateDestroyView

app_name = 'categories'

urlpatterns = [
    path('category/list-create/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('category/retrive-update-delete/<int:pk>/', CategoryRetriveUpdateDestroyView.as_view(), name='category-retrive-update-delete'),
]



