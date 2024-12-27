from rest_framework import serializers # 장고에서 제공하는 시리얼라이저
from .models import CustomUser # 커스텀 유저 모델
from django.contrib.auth import authenticate # 장고에서 제공하는 인증 모듈
from django.core.exceptions import ValidationError  # 장고에서 제공하는 검증 모듈
from django.contrib.auth.password_validation import validate_password # 장고에서 제공하는 패스워드 검증 모듈

class UserRegistrationSerializer(serializers.ModelSerializer): # 유저 등록 시리얼라이저
    class Meta: # 메타 클래스
        model = CustomUser # 모델 지정
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'nickname', 'birth_date', 'gender', 'bio'] # 필드 지정
        extra_kwargs = {'password': {'write_only': True}} # 비밀번호 필드는 쓰기 전용으로 설정

    def create(self, validated_data): # 유저 생성 메서드
        user = CustomUser.objects.create_user( # 유저 생성
            username=validated_data['username'], # 유저 닉네임
            password=validated_data['password'], # 유저 비밀번호
            email=validated_data['email'], # 유저 이메일
            first_name=validated_data['first_name'], # 유저 이름
            last_name=validated_data['last_name'], # 유저 성
            nickname=validated_data['nickname'], # 유저 닉네임
            birth_date=validated_data['birth_date'], # 유저 생년월일
            gender=validated_data.get('gender', ''), # 유저 성별
            bio=validated_data.get('bio', '') # 유저 자기소개
        )
        return user # 유저 반환

class UserLoginSerializer(serializers.Serializer): # 유저 로그인 시리얼라이저
    username = serializers.CharField() # 유저 닉네임
    password = serializers.CharField(write_only=True) # 유저 비밀번호

    def validate(self, attrs): # 유저 검증 메서드
        user = authenticate(username=attrs['username'], password=attrs['password']) # 유저 인증
        if not user: # 유저가 없으면
            raise serializers.ValidationError('Invalid credentials') # 예외 발생
        return {'user': user} # 유저 반환

class UserProfileSerializer(serializers.ModelSerializer): # 유저 프로필 시리얼라이저
    class Meta: # 메타 클래스
        model = CustomUser # 모델 지정
        fields = ['username', 'email', 'first_name', 'last_name', 'nickname', 'birth_date', 'gender', 'bio'] # 필드 지��

class UserUpdateSerializer(serializers.ModelSerializer): # 유저 업데이트 시리얼라이저
    class Meta: # 메타 클래스
        model = CustomUser # 모델 지정
        fields = ('email', 'name', 'nickname', 'birth_date', 'gender', 'bio') # 필드 지정
        required_fields = ('email', 'name', 'nickname', 'birth_date') # 필수 필드 지정
        
    def validate_email(self, value): # 이메일 검증 메서드
        user = self.context['request'].user # 유저 요청
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists(): # 유저 이메일 조회
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.") # 예외 발생
        return value # 이메일 반환

    def update(self, instance, validated_data): # 유저 업데이트 메서드
        for attr, value in validated_data.items(): # 유저 데이터 업데이트
            setattr(instance, attr, value) # 유저 데이터 설정
        instance.save() # 유저 저장
        return instance # 유저 반환

class PasswordChangeSerializer(serializers.Serializer): # 패스워드 변경 시리얼라이저
    current_password = serializers.CharField(required=True) # 현재 비밀번호
    new_password = serializers.CharField(required=True) # 새 비밀번호

    def validate_current_password(self, value): # 현재 비밀번호 검증 메서드
        user = self.context['request'].user # 유저 요청
        if not user.check_password(value): # 유저 비밀번호 검증
            raise serializers.ValidationError('현재 비밀번호가 일치하지 않습니다.') # 예외 발생
        return value # 비밀번호 반환

    def validate_new_password(self, value): # 새 비밀번호 검증 메서드
        try:
            validate_password(value) # 비밀번호 검증
        except ValidationError as e: # 예외 발생
            raise serializers.ValidationError(list(e.messages)) # 예외 발생
        
        user = self.context['request'].user # 유저 요청
        if user.check_password(value): # 유저 비밀번호 검증
            raise serializers.ValidationError('새 비밀번호는 현재 비밀번호와 달라야 합니다.') # 예외 발생
        return value # 비밀번호 반환

    def save(self): # 패스워드 변경 메서드
        user = self.context['request'].user # 유저 요청
        user.set_password(self.validated_data['new_password']) # 유저 비밀번호 설정
        user.save() # 유저 저장
        return user # 유저 반환

class UserDeleteSerializer(serializers.Serializer): # 유저 삭제 시리얼라이저
    password = serializers.CharField(write_only=True, required=True) # 비밀번호

    def validate_password(self, value): # 비밀번호 검증 메서드
        user = self.context['request'].user # 유저 요청
        if not user.check_password(value): # 유저 비밀번호 검증
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.') # 예외 발생
        return value # 비밀번호 반환

class UserFollowSerializer(serializers.ModelSerializer): # 유저 팔로우 시리얼라이저
    followers_count = serializers.SerializerMethodField() # 팔로워 카운트
    following_count = serializers.SerializerMethodField() # 팔로잉 카운트
    is_following = serializers.SerializerMethodField() # 팔로잉 여부

    class Meta: # 메타 클래스
        model = CustomUser # 모델 지정
        fields = ['id', 'username', 'nickname', 'followers_count', 'following_count', 'is_following'] # 필드 지정

    def get_followers_count(self, obj): # 팔로워 카운트 메서드
        return obj.followers.count() # 팔로워 카운트 반환

    def get_following_count(self, obj): # 팔로잉 카운트 메서드
        return obj.following.count() # 팔로잉 카운트 반환

    def get_is_following(self, obj): # 팔로잉 여부 메서드
        request = self.context.get('request') # 요청
        if request and request.user.is_authenticated: # 요청이 있고 유저가 인증되었을 때
            return request.user.is_following(obj) # 팔로잉 여부 반환
        return False # 팔로잉 여부 반환