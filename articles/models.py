from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CommonModel, User
from emoticons.models import EmoticonImage
from django.urls import reverse


class KakaoMapDataBase(CommonModel):
    """
    db저장용 모델입니다.
    """

    jibun_address = models.CharField(max_length=255)
    road_address = models.CharField(max_length=255)
    coordinate_x = models.FloatField()
    coordinate_y = models.FloatField()

    def __str__(self):
        return self.jibun_address


class Tag(CommonModel):
    """
    Tag관련 모델입니다.
    tag
    """

    tag = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.tag


class Article(CommonModel):
    """
    게시글 모델입니다.
    지도연동부분도 지도연동후에 주석을풀겠습니다.
    """

    user = models.ForeignKey(
        User, related_name="article_user", on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=256,
    )
    content = models.TextField()
    images = models.ImageField(null=True, blank=True)
    score = models.FloatField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    tags = models.ManyToManyField(Tag, through="TagList")
    location = models.ForeignKey(KakaoMapDataBase, on_delete=models.CASCADE)

    def __int__(self):
        return self.id

    def clean(self):
        if self.score >= 11:
            raise ValidationError("숫자는 10 이하로 입력해주세요.")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"article_id": self.pk})
    

    class Meta:
        db_table = "articles"


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField("이미지", upload_to="article", blank=True, null=True)


class TagList(CommonModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Comment(CommonModel):
    """
    댓글 모델입니다.
    게시글 객체와 일대다 관계를 가집니다.
    Comment객체는 게시글 객체를 의미하는 article필드, 댓글 작성자를 의미하는 writer필드,
    댓글내용의 comment필드, 사용된 이모티콘을 의미하는 use_emoticon필드로 구성됩니다.
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField("댓글 내용", blank=True)
    use_emoticon = models.ForeignKey(
        EmoticonImage, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"작성자: {self.writer} - 내용: {self.comment}"


class CommentLike(CommonModel):
    likers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_user")
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_like"
    )

    def __str__(self):
        return self.comment.comment
