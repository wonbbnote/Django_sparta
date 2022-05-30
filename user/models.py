#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
# AbstractUser: 장고가 제공하는 기본적인 auth_user 테이블과 연동되는 클래스
from django.conf import settings


# Create your models here.
class UserModel(AbstractUser):  # 생성한 클래스 이름 # 괄호안에 넣어줌 (상속)
    class Meta:                 # DB에 정보를 넣어주는 역할을 함
        db_table = "my_user"

    # username = models.CharField(max_length=20, null=False)   # 사용자 이름
    # password = models.CharField(max_length=256, null=False)  # 패스워드
    bio = models.CharField(max_length=256, default='')       # 상태메시지
    # created_at = models.DateTimeField(auto_now_add=True)     # 생성일
    # updated_at = models.DateTimeField(auto_now=True)         # 수정일

    # CharField, DateTimeField -> 각각의 정보들이 어떠한 형태로 DB에 저장될 것인지 설정
    # 장고 모델 필드의 종류 노션참고

    # 장고에 없는 bio만 남기고 지우기
    # -> 장고에 알려주기: mySpartaSns/settings.py에 AUTH_USER_MODEL = 'user.UserModel'추가

    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followee")
    # 팔로우 필드의 정보는 사용자 정보임
