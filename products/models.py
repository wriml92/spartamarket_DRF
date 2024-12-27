from django.db import models # 장고에서 제공하는 모델 모듈
from django.conf import settings # 장고에서 제공하는 설정 모듈

class Tag(models.Model): # 태그 모델
    name = models.CharField(max_length=50, unique=True) # 태그 이름
    created_at = models.DateTimeField(auto_now_add=True) # 태그 생성 시간

    def __str__(self): # 태그 문자열 표현
        return self.name # 태그 이름

    def save(self, *args, **kwargs): # 태그 저장
        self.name = self.name.lower()  # 태그 이름을 소문자로 저장
        super().save(*args, **kwargs) # 태그 저장

class Product(models.Model): # 상품 모델
    title = models.CharField(max_length=200) # 상품 제목
    content = models.TextField() # 상품 내용
    image = models.ImageField(upload_to='products/') # 상품 이미지
    created_at = models.DateTimeField(auto_now_add=True) # 상품 생성 시간
    updated_at = models.DateTimeField(auto_now=True) # 상품 업데이트 시간
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products') # 상품 작성자
    likes = models.ManyToManyField( # 좋아요 모델
        settings.AUTH_USER_MODEL, # 유저 모델
        related_name='liked_products', # 관계 이름
        blank=True # 비어있을 수 있음
    )
    tags = models.ManyToManyField(Tag, related_name='products', blank=True) # 태그 모델

    def __str__(self): # 상품 문자열 표현
        return self.title # 상품 제목

    def like_count(self): # 좋아요 카운트 메서드
        return self.likes.count() # 좋아요 카운트 반환

    def is_liked_by(self, user): # 좋아요 여부 메서드
        return self.likes.filter(id=user.id).exists() # 좋아요 여부 반환

    def add_tags(self, tag_names): # 태그 추가 메서드
        for tag_name in tag_names: # 태그 이름
            tag_name = tag_name.lower().strip() # 태그 이름 소문자로 변환
            if tag_name: # 태그 이름이 있을 때
                tag, _ = Tag.objects.get_or_create(name=tag_name) # 태그 조회 또는 생성
                self.tags.add(tag) # 태그 추가