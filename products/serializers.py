from rest_framework import serializers # 장고에서 제공하는 시리얼라이저 모듈
from .models import Product, Tag # 현재 디렉토리의 models 모듈

class TagSerializer(serializers.ModelSerializer): # 태그 시리얼라이저
    class Meta: # 태그 메타 클래스
        model = Tag # 태그 모델
        fields = ('id', 'name') # 태그 필드

class ProductSerializer(serializers.ModelSerializer): # 상품 시리얼라이저
    author = serializers.ReadOnlyField(source='author.username') # 상품 작성자
    likes_count = serializers.SerializerMethodField() # 좋아요 카운트
    is_liked = serializers.SerializerMethodField() # 좋아요 여부
    tags = TagSerializer(many=True, read_only=True) # 태그 정보
    tag_names = serializers.ListField( # 태그 이름
        child=serializers.CharField(max_length=50), # 태그 이름
        write_only=True, # 쓰기 전용
        required=False # 필수 아님
    )
    
    class Meta: # 상품 메타 클래스
        model = Product # 상품 모델
        fields = ('id', 'title', 'content', 'image', 'author', 'created_at', 'updated_at', 'likes_count', 'is_liked', 'tags', 'tag_names') # 상품 필드
        read_only_fields = ('author', 'created_at', 'updated_at', 'likes_count', 'is_liked', 'tags') # 상품 읽기 전용 필드

    def get_likes_count(self, obj): # 좋아요 카운트 메서드
        return obj.like_count() # 좋아요 카운트 반환

    def get_is_liked(self, obj): # 좋아요 여부 메서드
        request = self.context.get('request') # 요청
        if request and request.user.is_authenticated: # 요청이 있고 유저가 인증되었을 때
            return obj.is_liked_by(request.user) # 좋아요 여부 반환
        return False # 좋아요 여부 반환

    def create(self, validated_data): # 상품 생성 메서드
        tag_names = validated_data.pop('tag_names', []) # 태그 이름
        product = super().create(validated_data) # 상품 생성
        product.add_tags(tag_names) # 태그 추가
        return product # 상품 반환

    def update(self, instance, validated_data): # 상품 업데이트 메서드
        tag_names = validated_data.pop('tag_names', []) # 태그 이름
        product = super().update(instance, validated_data) # 상품 업데이트
        if tag_names: # 태그 이름이 있을 때
            product.tags.clear() # 태그 초기화
            product.add_tags(tag_names) # 태그 추가
        return product # 상품 반환