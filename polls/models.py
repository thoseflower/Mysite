import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('data published')
    # 模型增加 __str__() 方法是很重要
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        # 存在bug，当pub_date为未来某天时， Question.was_published_recently()会返回True
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        # 修复上述bug
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
