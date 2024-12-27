from django.shortcuts import get_object_or_404 # 장고에서 제공하는 뷰 함수
from rest_framework import generics, permissions, filters # 장고에서 제공하는 뷰 함수
from django.db.models import Count # 장고에서 제공하는 모델 함수
from .models import Product, Tag # 현재 디렉토리의 models 모듈
from .serializers import ProductSerializer, TagSerializer # 현재 디렉토리의 serializers 모듈
from rest_framework.pagination import PageNumberPagination # 장고에서 제공하는 페이지네이션 함수
from rest_framework.response import Response # 장고에서 제공하는 응답 함수
from rest_framework.views import APIView # 장고에서 제공하는 뷰 함수
from rest_framework import status

class ProductPagination(PageNumberPagination): # 상품 페이지네이션
    page_size = 10 # 페이지 크기
    page_size_query_param = 'page_size' # 페이지 크기 쿼리 매개변수
    max_page_size = 100 # 최대 페이지 크기

class ProductCreateView(generics.CreateAPIView): # 상품 생성 뷰
    queryset = Product.objects.all() # 상품 쿼리셋
    serializer_class = ProductSerializer # 상품 시리얼라이저
    permission_classes = [permissions.IsAuthenticated] # 권한 클래스

    def perform_create(self, serializer): # 상품 생성 메서드
        serializer.save(author=self.request.user) # 상품 저장

class ProductListView(generics.ListAPIView): # 상품 리스트 뷰
    serializer_class = ProductSerializer # 상품 시리얼라이저
    permission_classes = [permissions.AllowAny] # 권한 클래스
    pagination_class = ProductPagination # 페이지네이션 클래스
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] # 필터 백엔드
    search_fields = ['title', 'content', 'author__username', 'tags__name'] # 검색 필드
    ordering_fields = ['created_at', 'likes'] # 정렬 필드
    ordering = ['-created_at'] # 정렬

    def get_queryset(self): # 상품 쿼리셋 메서드
        queryset = Product.objects.annotate( # 상품 쿼리셋 주석
            likes_count=Count('likes') # 좋아요 카운트
        ).all() # 상품 쿼리셋 주석
        
        # 태그 필터링
        tag = self.request.query_params.get('tag', None) # 태그
        if tag: # 태그가 있을 때
            queryset = queryset.filter(tags__name__iexact=tag.lower()) # 태그 필터링
        
        # 정렬 옵션 처리
        ordering = self.request.query_params.get('ordering', '-created_at') # 정렬 옵션
        if ordering == 'likes': # 좋아요 순
            queryset = queryset.order_by('-likes_count', '-created_at') # 좋아요 순 정렬
        elif ordering == '-likes': # 좋아요 순
            queryset = queryset.order_by('-likes_count', '-created_at') # 좋아요 순 정렬
        else: # 생성 시간 순
            queryset = queryset.order_by(ordering) # 생성 시간 순 정렬
            
        return queryset # 상품 쿼리셋 반환

class IsAuthorOrReadOnly(permissions.BasePermission): # 상품 권한 클래스
    def has_object_permission(self, request, view, obj): # 상품 권한 메서드
        if request.method in permissions.SAFE_METHODS: # 안전한 메서드일 때
            return True # 권한 허용
        return obj.author == request.user # 상품 작성자와 요청자가 같을 때

class ProductUpdateView(generics.UpdateAPIView): # 상품 업데이트 뷰
    queryset = Product.objects.all() # 상품 쿼리셋
    serializer_class = ProductSerializer # 상품 시리얼라이저
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly] # 권한 클래스
    lookup_field = 'pk' # 상품 키

class ProductDeleteView(generics.DestroyAPIView): # 상품 삭제 뷰
    queryset = Product.objects.all() # 상품 쿼리셋
    serializer_class = ProductSerializer # 상품 시리얼라이저
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly] # 권한 클래스
    lookup_field = 'pk' # 상품 키

class ProductLikeView(APIView): # 상품 좋아요 뷰
    permission_classes = [permissions.IsAuthenticated] # 권한 클래스

    def post(self, request, pk): # 상품 좋아요 메서드
        product = get_object_or_404(Product, pk=pk) # 상품 조회
        if product.is_liked_by(request.user): # 상품 좋아요 여부
            product.likes.remove(request.user) # 상품 좋아요 삭제
            return Response({"message": "좋아요가 취소되었습니다."}) # 응답
        else: # 상품 좋아요 여부가 아닐 때
            product.likes.add(request.user) # 상품 좋아요 추가
            return Response({"message": "좋아요가 추가되었습니다."}) # 응답

class TagListView(generics.ListAPIView): # 태그 리스트 뷰
    queryset = Tag.objects.all().order_by('name') # 태그 쿼리셋
    serializer_class = TagSerializer # 태그 시리얼라이저
    permission_classes = [permissions.AllowAny] # 권한 클래스
