from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.stockin_list, name="home"),
    path("stockin/", views.stockin_list, name="stockin_list"),
    path("stockin/<int:pk>/edit/",   views.stockin_edit,   name="stockin_edit"),
    path("stockin/<int:pk>/delete/", views.stockin_delete, name="stockin_delete"),
    path("items/quick-add/",         views.item_quick_add, name="item_quick_add"),
    path("stockin/report/",          views.stockin_report, name="stockin_report"),
]
