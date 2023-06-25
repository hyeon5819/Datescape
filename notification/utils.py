from notification.models import Notification
from emoticons.models import Emoticon
from articles.models import Article, Comment, Reply


def get_instances_data():
    # Example query to retrieve instances from the database
    instances = Notification.objects.all().order_by("-created_at")
    instances_data = []
    article = None
    comment = None
    emoticon = None

    for instance in instances:
        if instance.type == "comment":
            article = Comment.objects.get(id=instance.type_id).article.title
        elif instance.type == "reply":
            article = Reply.objects.get(id=instance.type_id).comment.article.title
            # comment = Reply.objects.get(id=instance.type_id).comment
        elif instance.type == "emoticon":
            emoticon = Emoticon.objects.get(id=instance.type_id).title

        instance_data = {
            "id": instance.pk,
            "type": instance.type,
            "type_id": instance.type_id,
            "db_status": instance.db_status,
            "article": article,
            "comment": comment,
            "emoticon": emoticon,
        }
        instances_data.append(instance_data)

    return instances_data
