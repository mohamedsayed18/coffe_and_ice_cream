from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login),
    path('state/', views.change_system_state),
    path('items/', views.handle_items),
    path('items/<str:item_id>/run/', views.run_item_view),
]