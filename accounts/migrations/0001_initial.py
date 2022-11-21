
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import imagekit.models.fields
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("nickname", models.CharField(max_length=10)),
                (
                    "mbti",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=10,
                    ),
                ),
                ("address", models.CharField(max_length=50)),
                ("address_detail", models.CharField(max_length=40, null=True)),
                ("birth", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "gender",
                    models.CharField(choices=[("M", "남자"), ("F", "여자")], max_length=2),
                ),
                (
                    "manner",
                    multiselectfield.db.fields.MultiSelectField(
                        choices=[
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
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "smoking",
                    models.CharField(
                        choices=[
                            ("비흡연", "비흡연"),
                            ("술마실때만", "술 마실 때만"),
                            ("가끔", "가끔"),
                            ("매일", "매일"),
                            ("아이코스", "아이코스"),
                            ("전자담배", "전자담배"),
                        ],
                        max_length=10,
                    ),
                ),
                ("pet", models.BooleanField(default=False)),
                ("agree", models.BooleanField(default=False)),
                (
                    "profile_pic",
                    imagekit.models.fields.ProcessedImageField(
                        blank=True,
                        default="../static/images/profile_default.png",
                        upload_to="profile/%Y%m%d/",
                    ),
                ),
                ("manner_point", models.FloatField(default=36.5)),
                (
                    "blocking",
                    models.ManyToManyField(
                        related_name="blockers", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "followings",
                    models.ManyToManyField(
                        related_name="followers", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]

