from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db import models
from maps.models import Map
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    day = models.DateTimeField()
    time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_post"
    )
    park_address = models.ForeignKey(Map, on_delete=models.CASCADE)
    pet = models.BooleanField(default=False)
    content = models.TextField()
    TIME_CHOICES = (
        ("00:00", "00:00"),
        ("01:00", "01:00"),
        ("02:00", "02:00"),
        ("03:00", "03:00"),
        ("04:00", "04:00"),
        ("05:00", "05:00"),
        ("06:00", "06:00"),
        ("07:00", "07:00"),
        ("08:00", "08:00"),
        ("09:00", "09:00"),
        ("10:00", "10:00"),
        ("11:00", "11:00"),
        ("12:00", "12:00"),
        ("13:00", "13:00"),
        ("14:00", "14:00"),
        ("15:00", "15:00"),
        ("16:00", "16:00"),
        ("17:00", "17:00"),
        ("18:00", "18:00"),
        ("19:00", "19:00"),
        ("20:00", "20:00"),
        ("21:00", "21:00"),
        ("22:00", "22:00"),
        ("23:00", "23:00"),
        ("24:00", "24:00"),
    )
    time = models.CharField(max_length=20, choices=TIME_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participate_people = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    participate = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="participater"
    )
    hit = models.PositiveBigIntegerField(default=0)

    thumbnail = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 80},
    )

    @property
    def update_conter(self):
        self.hit = self.hit + 1
        self.save()


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Search(models.Model):
    title = models.CharField(max_length=10)
    count = models.PositiveIntegerField(default=0)
