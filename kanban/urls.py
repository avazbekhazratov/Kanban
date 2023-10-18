from django.urls import path
from .views import Items
from .services import TaskCondt, BoardMemberView

urlpatterns = [
    path('item/', Items.as_view()),
    path("item/<int:pk>/", Items.as_view()),

    path('item/', TaskCondt.as_view()),
    path("item/<int:pk>/", TaskCondt.as_view()),

    path('boardmem/', BoardMemberView.as_view()),
    path("boardmem/<int:pk>/", BoardMemberView.as_view()),
]
