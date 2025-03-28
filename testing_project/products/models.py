from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='이름')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='가격')
    stock_count = models.IntegerField(default=0, verbose_name='재고')

    @property
    def is_stock(self) -> bool: # 당연히 속성이니까 매개변수 x
        return self.stock_count > 0

    class Meta:
        constraints = [ # 이거 수정하고 반드시 migrations 해줘야 한다: Create constraint price__gt_0 on model product
            models.CheckConstraint(
                check=models.Q(price__gt=0),
                name='price__gt_0'
            ),
            models.CheckConstraint(
                check=models.Q(stock_count__gt=0),
                name='stock_count__gt_0'
            ),
        ] # 음수로 설정하고 .save()하면 django.db.utils.IntegrityError: CHECK constraint failed: stock_count__gt_0 나옴

    def get_discounted_price(self, discount_pecentage):
        """할인된 가격을 계산하여 반환"""
        return self.price * (1 - discount_pecentage / 100)
    
    # def clean(self): # form에서 각 필드 유효성 검사 하기 때문에 이제 필요x
    #     """가격, 재고 유효성 검사"""
    #     if self.price < 0:
    #         raise ValidationError('Price cannot be negative')
    #     if self.stock_count < 0:
    #         raise ValidationError('stock_count cannot be negative')
    
    """
    def clean(self)
    - 모든 필드에 대해 self.clean_fields가 호출된 후, 추가적인 *모델 전체에 대한 추가적인 검증*을 수행하는 훅(hook)
    - 이 메서드에서 발생한 ValidationError는 특정 필드와 연결되지 않으며, 특별한 경우로 NON_FIELD_ERRORS에 할당됨
    - clean()에서 ValidationError를 발생시키면,이 오류를 개별 필드가 아닌 NON_FIELD_ERRORS라는 키에 저장함
        이는 {{ form.non_field_errors }}로 확인 가능
    """