from django.urls import path
from .views import Items
from .services import TaskCondt, BoardMemberView, TaskItemView, SubTaskView
from .services.auth import AuthorizationView, LoginView, AuthOne, AuthTwo

urlpatterns = [
    path('item/', Items.as_view()),
    path("item/<int:pk>/", Items.as_view()),

    path('task/', TaskCondt.as_view()),
    path("task/<int:pk>/", TaskCondt.as_view()),

    path('task-item/', TaskItemView.as_view()),
    path("task-item/<int:pk>/", TaskItemView.as_view()),

    path('sub-task/', SubTaskView.as_view()),
    path("sub-task/<int:pk>/", SubTaskView.as_view()),

    path('boardmem/', BoardMemberView.as_view()),
    path("boardmem/<int:pk>/", BoardMemberView.as_view()),

    path('regis/', AuthorizationView.as_view()),
    path("login/", LoginView.as_view()),

    path('otp/', AuthOne.as_view()),
    path("otp2/", AuthTwo.as_view()),
]
