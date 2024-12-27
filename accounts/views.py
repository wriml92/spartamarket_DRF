from django.shortcuts import render, get_object_or_404 # 장고에서 제공하는 렌더링 함수
from rest_framework import generics, permissions, filters # 장고에서 제공하는 제네릭 뷰 모듈
from .models import CustomUser # 현재 디렉토리의 models 모듈
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserUpdateSerializer, PasswordChangeSerializer, UserDeleteSerializer, UserFollowSerializer # 현재 디렉토리의 serializers 모듈
from rest_framework.authtoken.models import Token # 장고에서 제공하는 토큰 모듈
from rest_framework.response import Response # 장고에서 제공하는 응답 모듈
from rest_framework import status, views # 장고에서 제공하는 상태 모듈
from django.contrib.auth import authenticate # 장고에서 제공하는 인증 모듈
from rest_framework.permissions import IsAuthenticated # 장고에서 제공하는 인증 모듈
from rest_framework.authentication import TokenAuthentication # 장고에서 제공하는 인증 모듈
from rest_framework import permissions # 장고에서 제공하는 권한 모듈

class IsOwnerOnly(permissions.BasePermission): # 장고에서 제공하는 권한 모듈
    def has_object_permission(self, request, view, obj): # 장고에서 제공하는 권한 모듈
        return obj == request.user # 장고에서 제공하는 권한 모듈

class UserRegistrationView(generics.CreateAPIView): # 회원가입 뷰
    queryset = CustomUser.objects.all() # 모든 유저 쿼리셋
    serializer_class = UserRegistrationSerializer # 유저 등록 시리얼라이저

class UserLoginView(views.APIView): # 로그인 뷰
    def post(self, request, *args, **kwargs): # 로그인 메서드
        serializer = UserLoginSerializer(data=request.data) # 유저 로그인 시리얼라이저
        if serializer.is_valid(): # 유저 로그인 시리얼라이저 유효성 검사
            user = authenticate( # 유저 인증
                username=serializer.validated_data['username'], # 유저 이름
                password=serializer.validated_data['password'] # 유저 비밀번호
            )
            if user is not None: # 유저 인증
                token, created = Token.objects.get_or_create(user=user) # 토큰 생성
                return Response({'token': token.key}, status=status.HTTP_200_OK) # 토큰 응답
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED) # 유저 인증 실패
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 유저 인증 실패

class UserProfileView(generics.RetrieveAPIView): # 유저 프로필 뷰
    queryset = CustomUser.objects.all() # 모든 유저 쿼리셋
    serializer_class = UserProfileSerializer # 유저 프로필 시리얼라이저
    permission_classes = [IsAuthenticated] # 인증 권한
    lookup_field = 'username' # 유저 이름

class UserUpdateView(generics.UpdateAPIView): # 유저 업데이트 뷰
    queryset = CustomUser.objects.all() # 모든 유저 쿼리셋
    serializer_class = UserUpdateSerializer # 유저 업데이트 시리얼라이저
    permission_classes = [IsAuthenticated, IsOwnerOnly] # 인증 권한
    lookup_field = 'username' # 유저 이름

    def get_object(self): # 유저 객체 가져오기
        username = self.kwargs.get('username') # 유저 이름
        return CustomUser.objects.get(username=username) # 유저 객체

class LogoutView(views.APIView): # 로그아웃 뷰
    authentication_classes = [TokenAuthentication] # 인증 클래스
    permission_classes = [IsAuthenticated] # 인증 권한

    def post(self, request): # 로그아웃 메서드
        request.user.auth_token.delete() # 토큰 삭제
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK) # 응답

class PasswordChangeView(generics.UpdateAPIView): # 패스워드 변경 뷰
    serializer_class = PasswordChangeSerializer # 패스워드 변경 시리얼라이저
    permission_classes = [IsAuthenticated] # 인증 권한

    def get_object(self): # 유저 객체 가져오기
        return self.request.user # 유저 요청

    def update(self, request, *args, **kwargs): # 패스워드 변경 메서드
        serializer = self.get_serializer(data=request.data) # 패스워드 변경 시리얼라이저
        if serializer.is_valid(): # 패스워드 변경 시리얼라이저 유효성 검사
            serializer.save() # 패스워드 변경
            # 비밀번호가 변경되면 기존 토큰을 삭제하고 새 토큰을 발급
            request.user.auth_token.delete() # 토큰 삭제
            token = Token.objects.create(user=request.user) # 토큰 생성
            return Response({ # 응답
                'message': '비밀번호가 성공적으로 변경되었습니다.', # 메시지
                'new_token': token.key # 새 토큰
            }, status=status.HTTP_200_OK) # 응답
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 응답

class UserDeleteView(views.APIView): # 유저 삭제 뷰
    permission_classes = [IsAuthenticated] # 인증 권한
    serializer_class = UserDeleteSerializer # 유저 삭제 시리얼라이저

    def delete(self, request): # 유저 삭제 메서드
        serializer = self.serializer_class(data=request.data, context={'request': request}) # 유저 삭제 시리얼라이저
        if serializer.is_valid(): # 유저 삭제 시리얼라이저 유효성 검사
            user = request.user # 유저 요청
            user.auth_token.delete() # 토큰 삭제
            user.delete() # 사용자 계정 삭제
            return Response({"message": "계정이 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT) # 응답
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 응답

class UserFollowView(views.APIView): # 유저 팔로우 뷰
    permission_classes = [IsAuthenticated] # 인증 권한

    def post(self, request, username): # 팔로우 메서드
        user_to_follow = get_object_or_404(CustomUser, username=username) # 유저 팔로우
        if request.user == user_to_follow: # 유저가 자기 자신일 때
            return Response( # 응답
                {"error": "자기 자신을 팔로우할 수 없습니다."}, # 에러 메시지
                status=status.HTTP_400_BAD_REQUEST # 상태 코드
            )

        request.user.follow(user_to_follow) # 유저 팔로우
        serializer = UserFollowSerializer( # 유저 팔로우 시리얼라이저
            user_to_follow, # 유저 팔로우
            context={'request': request} # 요청
        )
        return Response(serializer.data) # 응답

    def delete(self, request, username): # 언팔로우 메서드
        user_to_unfollow = get_object_or_404(CustomUser, username=username) # 유저 언팔로우
        request.user.unfollow(user_to_unfollow) # 유저 언팔로우
        serializer = UserFollowSerializer( # 유저 팔로우 시리얼라이저
            user_to_unfollow, # 유저 언팔로우
            context={'request': request} # 요청
        )
        return Response(serializer.data) # 응답

class FollowListView(views.APIView): # 팔로우 리스트 뷰
    permission_classes = [IsAuthenticated] # 인증 권한
    
    def get(self, request, username, list_type): # 팔로우 리스트 메서드
        user = get_object_or_404(CustomUser, username=username) # 유저 객체
        if list_type == 'followers': # 팔로워 리스트
            users = user.followers.all() # 팔로워 리스트
        else: # 팔로잉 리스트
            users = user.following.all() # 팔로잉 리스트

        serializer = UserFollowSerializer( # 유저 팔로우 시리얼라이저
            users, # 유저 팔로우
            many=True, # 여러 개
            context={'request': request} # 요청
        )
        return Response(serializer.data) # 응답