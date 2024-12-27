from django.contrib.auth.models import AbstractUser # 장고에서 제공하는 기본 유저 모델
from django.db import models # 장고에서 제공하는 데이터베이스 모델

class CustomUser(AbstractUser): # 장고에서 제공하는 기본 유저 모델을 상속받아 커스텀 유저 모델을 만든다.
    nickname = models.CharField(max_length=50) # 닉네임 필드 추가
    birth_date = models.DateField(null=True) # 생년월일 필드 추가
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')], blank=True) # 성별 필드 추가
    bio = models.TextField(blank=True) # 자기소개 필드 추가
    following = models.ManyToManyField( # 팔로잉 필드 추가
        'self', # 자기 자신
        related_name='followers', # 팔로워 관계
        symmetrical=False, # 대칭 관계 여부
        blank=True # 비어있을 수 있음
    )

    def __str__(self): # 유저 모델을 문자열로 표현하는 메서드
        return self.username # 유저 모델의 username을 반환

    def follow(self, user): # 팔로우 메서드
        if user != self: # 유저가 자기 자신이 아닐 때
            self.following.add(user) # 팔로잉 추가

    def unfollow(self, user): # 언팔로우 메서드
        self.following.remove(user) # 팔로잉 삭제

    def is_following(self, user): # 팔로잉 여부 확인 메서드
        return self.following.filter(id=user.id).exists() # 팔로잉 필터링