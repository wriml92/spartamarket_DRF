from django.urls import path # 장고에서 제공하는 경로 모듈
from . import views # 현재 디렉토리의 views 모듈

app_name = 'products' # 앱 이름

urlpatterns = [ # 경로 패턴
    path('', views.ProductListView.as_view(), name='product-list'), # 상품 목록 경로
    path('create/', views.ProductCreateView.as_view(), name='product-create'), # 상품 생성 경로
    path('tags/', views.TagListView.as_view(), name='tag-list'), # 태그 목록 경로
    path('<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'), # 상품 업데이트 경로
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'), # 상품 삭제 경로
    path('<int:pk>/like/', views.ProductLikeView.as_view(), name='product-like'), # 상품 좋아요 경로
] 