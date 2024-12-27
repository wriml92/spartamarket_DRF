from django.apps import AppConfig


class ProductsConfig(AppConfig): # 상품 앱 설정
    default_auto_field = 'django.db.models.BigAutoField' # 장고에서 제공하는 빅 오토 필드
    name = 'products' # 앱 이름