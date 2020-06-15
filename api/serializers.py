from django.contrib.auth import authenticate
from upload.models import Question,Topic,Subject,User
from django.contrib.auth.models import Group
from rest_framework import serializers




class QuestionSerialiser(serializers.ModelSerializer):
        
    class Meta:
        model = Question
        fields = ['questionid','questiontext','questionanswer','topicid','subjectid'] 
        depth = 1

        
class QuestionBasicSerialiser(serializers.ModelSerializer):
        
    class Meta:
        model = Question
        fields = ['questionid','questiontext', 'topicid','subjectid'] 
        depth = 1


class TopicSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Topic
        fields = ['topicid','topicname']

class SubjectSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Subject
        fields = ['subjectid','subjectname']        



class UserSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

class GroupSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = ['id','name']
        depth = 1         



class LoginSerialiser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        
        style = { 'input_type' : 'password' }, trim_whitespace = False

    )

    def validate(self,data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            if User.objects.filter(username=username).exists():
                user = authenticate(request = self.context.get('request'), username=username,password=password )
            else: 
                msg = {
                    "detail" : "Invalid Username and Password Combination. Login Failed. Access Denied.",
                    "status": False,
                }
                raise serializers.ValidationError(msg, code = 'authorization')

            if not user:
                msg = {
                    "detail" : "Invalid Username and Password Combination. Login Failed. Access Denied.",
                    "status" : False,
                }
                raise serializers.ValidationError(msg, code = 'authorization')

        else: 
            msg = {
                "detail": "Authentication Information has not been provided.",
                "status": False,
            }
            raise serializers.ValidationError(msg, code = 'authorization')

        data['user'] = user
        return data
