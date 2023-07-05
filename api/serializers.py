from django.contrib.auth import authenticate
from upload.models import Question, Topic, Subject, User
from django.contrib.auth.models import Group
from rest_framework import serializers


class QuestionSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "questionid",
            "questiontext",
            "questionanswer",
            "topicid",
            "subjectid",
        ]
        depth = 1


class TopicSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["topicid", "topicname"]


class SubjectSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["subjectid", "subjectname"]


class QuestionBasicSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "questionid",
            "questiontext",
            "topicid",
            "subjectid",
        ]
        depth = 1


class UserSerialiser(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        ]
        depth = 1

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]

    def get_user_permissions(self, obj):
        return [permission.name for permission in obj.user_permissions.all()]


class GroupSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]
        depth = 1


class LoginSerialiser(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            if User.objects.filter(username=username).exists():
                user = authenticate(
                    request=self.context.get("request"),
                    username=username,
                    password=password,
                )
            else:
                msg = {
                    "detail": "Invalid Username and Password Combination. Login Failed. Access Denied.",
                    "status": False,
                }
                raise serializers.ValidationError(msg, code="authorization")

            if not user:
                msg = {
                    "detail": "Invalid Username and Password Combination. Login Failed. Access Denied.",
                    "status": False,
                }
                raise serializers.ValidationError(msg, code="authorization")

        else:
            msg = {
                "detail": "Authentication Information has not been provided.",
                "status": False,
            }
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data
