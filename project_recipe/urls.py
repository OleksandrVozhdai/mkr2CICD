from django.contrib import admin
from django.urls import path
from recipe.views import home, main, category_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
]