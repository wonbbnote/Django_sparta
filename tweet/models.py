# tweet/models.py
from django.db import models
from user.models import UserModel  # 다른모델을 불러옴
# user앱에 있는 모델에서 UserModel 가져올 것


# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    # ForeignKey : 다른 데이터베이스에서 내용을 가져오겠다 (다른 모델을 가져오는 것?)
    content = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TweetComment(models.Model):
    class Meta:
        db_table = "comment"
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)