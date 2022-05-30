from django.contrib import admin  # 장고에서 admin툴을 사용하겠다!
from .models import UserModel     # 우리가 생성한 모델 가져옴
# .models 현재 위치와 동일한 models.py에서 그 중 UserModel 모델을 가져오겠다

# Register your models here.
admin.site.register(UserModel)
# 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다
# = 우리가 가져온 UserModel을 관리자 계정에 넣어주겠다
# = Admin페이지에서 우리의 UserModel 확인 가능
