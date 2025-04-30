from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login),
    path('state/', views.change_system_state),
    path('items/', views.handle_items),
    path('items/<str:item_id>/state', views.change_item_state),
    path('user/', views.update_user),
    path('item-control/', views.item_control_access),
]
