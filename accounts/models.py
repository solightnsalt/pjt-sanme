from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from decimal import Decimal
from django import forms
from multiselectfield import MultiSelectField
import datetime

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=10)  # 별명
    contact = models.CharField(max_length=30)  # 연락처
    MBTI_CHOICES = (
        ("ISTJ", "ISTJ"),
        ("ISTP", "ISTP"),
        ("ISFJ", "ISFJ"),
        ("ISFP", "ISFP"),
        ("INTJ", "INTJ"),
        ("INTP", "INTP"),
        ("INFJ", "INFJ"),
        ("INFP", "INFP"),
        ("ESTJ", "ESTJ"),
        ("ESTP", "ESTP"),
        ("ESFJ", "ESFJ"),
        ("ESFP", "ESFP"),
        ("ENTJ", "ENTJ"),
        ("ENTP", "ENTP"),
        ("ENFJ", "ENFJ"),
        ("ENFP", "ENFP"),
    )

    mbti = models.CharField(
        max_length=10,
        choices=MBTI_CHOICES,
    )  # mbti
    address = models.CharField(max_length=50)  # 주소
    age = models.DateTimeField(default=datetime.datetime.now())  # 나이
    GENDER_CHOICES = (
        ("M", "남자"),
        ("F", "여자"),
    )
    gender = models.CharField(  # 성별
        max_length=2,
        choices=GENDER_CHOICES,
    )

    MANNER_CHOICES = (
        ("활발", "활발한"),
        ("조용", "조용한"),
        ("애교", "애교가 넘치는"),
        ("어른", "어른스러운"),
        ("열정", "열정적인"),
        ("침착", "침착한"),
        ("예의", "예의바른"),
        ("유머", "유머러스한"),
        ("진지", "진지한"),
        ("지적", "지적인"),
        ("성실", "성실한"),
        ("감성", "감성적인"),
        ("꼼꼼", "꼼꼼한"),
        ("논리", "논리적인"),
        ("즉흥", "즉흥적인"),
        ("소심", "소심한"),
        ("쿨", "쿨한"),
    )

    manner = MultiSelectField(  # 매너(성향)
        max_length=100,
        choices=MANNER_CHOICES,
    )

    SMOKING_CHOICES = (
        ("비흡연", "비흡연"),
        ("술마실때만", "술 마실 때만"),
        ("가끔", "가끔"),
        ("매일", "매일"),
        ("아이코스", "아이코스"),
        ("전자담배", "전자담배"),
    )

    smoking = models.CharField(  # 흡연여부
        max_length=10,
        choices=SMOKING_CHOICES,
    )

    pet = models.BooleanField(default=False)  # 반려동물 유무
    agree = models.BooleanField(default=False)  # 약관내용

    profile_pic = ProcessedImageField(  # 프로필사진
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(360, 360)],
        format="JPEG",
        options={"quality": 80},
    )

    followings = models.ManyToManyField(  # 팔로워
        "self", symmetrical=False, related_name="followers"
    )

    manner_point = models.DecimalField(
        max_digits=4, decimal_places=1, default=36.5
    )  # 매너점수
    date_created = models.DateTimeField(auto_now_add=True)  # 가입일
