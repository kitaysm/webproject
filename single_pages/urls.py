# urls.py
from django.urls import path
from . import views
from .views import CustomLoginView

# 로그인구현
from .views import CustomLoginView, home, main, music_recommendations, my_music, realtime_chart, maker, CustomSignupView, CustomLogoutView
from allauth.account.views import SignupView  # 추가

urlpatterns = [
    path('', views.home),
    path('main/', views.main),
    path('music_recommendations/', views.music_recommendations),
    path('my_music/', views.my_music),
    path('realtime_chart/', views.realtime_chart),
    path('maker/', views.maker),
    path('login/', CustomLoginView.as_view(), name='login'),

    # 멜론 차트 페이지 경로
    path('realtime_chart/', views.realtime_chart, name='realtime_chart'),
    path('123/', views.realtime_chart123, name='realtime_chart123'),

    path("landing/", views.landing),

    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('signup/', CustomSignupView.as_view(), name='signup'),  
    path('logout/', CustomLogoutView.as_view(), name='account_logout'),

]


