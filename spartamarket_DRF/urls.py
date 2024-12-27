"""
URL configuration for spartamarket_DRF project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin # 장고 관리자
from django.urls import path, include # 장고 URL 패턴
from django.conf import settings # 장고 설정
from django.conf.urls.static import static # 장고 정적 파일 설정

urlpatterns = [ # URL 패턴
    path('admin/', admin.site.urls), # 관리자 URL
    path('api/accounts/', include('accounts.urls')), # 계정 URL
    path('api/products/', include('products.urls')), # 상품 URL
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 미디어 파일 경로 설정
