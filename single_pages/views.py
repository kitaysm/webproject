# \single_pages\views.py
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render


# 로그인 구현
from allauth.account.views import SignupView  
from .forms import CustomSignupForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from .forms import CustomLogoutForm


class CustomLoginView(LoginView):
    template_name = 'single_pages/login.html'
    # success_url = reverse_lazy('main')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'  # 해당 템플릿으로 설정

class CustomLogoutView(LogoutView):
    template_name = 'account/logout.html'
    form_class = CustomLogoutForm











def home(request):
    return render(request, "single_pages/home.html")

def main(request):
    chart_data = get_melon_chart()
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(
        request,
        "single_pages/main.html",
        {
            'chart_data': chart_data,
            'recent_posts': recent_posts,
        }
    )


def music_recommendations(request):
    return render(request, "single_pages/music_recommendations.html")

def my_music(request):
    return render(request, "single_pages/my_music.html")

def realtime_chart(request):
    return render(request, "single_pages/realtime_chart.html")

def maker(request):
    return render(request, "single_pages/maker.html")

# 웹크롤링
from django.shortcuts import render
from .melon_scraper import get_melon_chart
from .bugs_scraper import get_bugs_chart
from .flo_scraper import get_flo_chart
# from .models import Song

def realtime_chart(request):
    chart_data = get_melon_chart()
    chart_data1 = get_bugs_chart()
    chart_data2 = get_flo_chart()
    # print(chart_data2)  # 이 부분을 추가하여 데이터 확인
    return render(request, 'single_pages/realtime_chart.html', {'chart_data': chart_data,'chart_data1': chart_data1,'chart_data2': chart_data2})

def realtime_chart123(request):
    chart_data = get_melon_chart()
    chart_data1 = get_bugs_chart()
    chart_data2 = get_flo_chart()
    print('asdsadsadsaasdasda', chart_data, chart_data1, chart_data2,)  # 이 부분을 추가하여 데이터 확인
    return render(request, 'single_pages/123.html', {'chart_data': chart_data, 'chart_data1': chart_data1, 'chart_data2': chart_data2})


# 0105 추가 내용 : 메인페이지에 최신글 띄우고 링크
from blog.models import Post

def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(
        request,
        "single_pages/main.html",
        {
            'recent_posts':recent_posts,
        }
        
    )