from django.urls import path
from .views import RegisterView,LoginView,UserView,UserLogout,Addnote,Updatenote,Deletenote,test
urlpatterns = [

    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('get/',UserView.as_view()),
    path('logout/',UserLogout.as_view()),
    path('add/',Addnote.as_view()),
    path('update/<int:pk>/',Updatenote.as_view()),
    path('delete/<int:pk>/',Deletenote.as_view()),
    path('test/',test.as_view())
]
