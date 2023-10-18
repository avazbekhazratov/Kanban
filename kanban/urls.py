from django.urls import path
from .views import Items

urlpatterns = [
    path('item/', Items.as_view()),
    path("item/<int:pk>/", Items.as_view()),
]
