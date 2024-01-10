"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings      ## 5일차 작성
from django.conf.urls.static import static     ## 5일차 작성

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("single_pages.urls")),
    path("blog/", include("blog.urls")),
    path('markdownx/', include('markdownx.urls')),
    path('blog1/', include('blog1.urls')),
    path('accounts/', include('allauth.urls')),  # Allauth의 URL을 추가
]

urlpatterns += static(   
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT         ## 5일차 작성
)    # 미디어 파일을 서빙 할 수 있도록 urlpatterns에 추가
