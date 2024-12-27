from django.urls import path # 장고에서 제공하는 경로 모듈
from . import views # 현재 디렉토리의 views 모듈

app_name = 'accounts' # 앱 이름

urlpatterns = [ # 경로 패턴
    path('', views.UserDeleteView.as_view(), name='user-delete'), # 유저 삭제 경로
    path('login/', views.UserLoginView.as_view(), name='login'), # 로그인 경로
    path('logout/', views.LogoutView.as_view(), name='logout'), # 로그아웃 경로
    path('register/', views.UserRegistrationView.as_view(), name='register'), # 회원가입 경로
    path('password/', views.PasswordChangeView.as_view(), name='password-change'), # 패스워드 변경 경로
    path('<str:username>/follow/', views.UserFollowView.as_view(), name='user-follow'), # 유저 팔로우 경로
    path('<str:username>/followers/', views.FollowListView.as_view(), {'list_type': 'followers'}, name='followers-list'), # 팔로워 리스트 경로
    path('<str:username>/following/', views.FollowListView.as_view(), {'list_type': 'following'}, name='following-list'), # 팔로잉 리스트 경로
    path('<str:username>/', views.UserProfileView.as_view(), name='user-detail'), # 유저 상세 경로
    path('<str:username>/update/', views.UserUpdateView.as_view(), name='user-update'), # 유저 업데이트 경로
] 