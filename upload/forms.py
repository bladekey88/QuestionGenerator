from django import forms
from .models import Document, ProcessDocument, Question, Subject, Topic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ("document", "description", "subject", "document_id")


class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["subjectname"]


class AddTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["topicname"]


class EditSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["subjectname"]


class EditTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["topicname"]


# Form to Process Document to extract Questions and Topics
class ProcessDocumentForm(forms.ModelForm):
    class Meta:
        model = ProcessDocument
        fields = ("processed_id",)


# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text="Required")
    middle_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=True, help_text="Required   ")
    email = forms.EmailField(max_length=255, help_text="Enter a valid email address")

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]


##########################AJAX SHIT########################
from django import forms
from .models import Person, City


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ("name", "birthdate", "country", "city")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.none()

        if "country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["city"].queryset = City.objects.filter(
                    country_id=country_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields["city"].queryset = self.instance.country.city_set.order_by(
                "name"
            )


class SubjectForm(forms.ModelForm):
    CHOICES = [
        ("1", "1 Question From Each Selected Topic"),
        ("2", "Questions from Any Selected Topic"),
    ]
    choice_field = forms.ChoiceField(
        widget=forms.RadioSelect, choices=CHOICES, label="Question Preference:"
    )
    number_of_questions = forms.IntegerField(
        min_value=1,
        max_value=10,
        required=True,
        label="How many questions should be generated from all selected topics (max 10): ",
    )

    class Meta:
        model = Question
        fields = ("subjectid", "topicid", "number_of_questions", "choice_field")

        widgets = {
            "topicid": forms.CheckboxSelectMultiple(attrs={"id": "topics"}),
        }

    field_order = ["subjectid", "topicid", "choice_field", "number_of_questions"]

    # Override params by cleaning it up :)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["topicid"].queryset = Question.objects.none()
        self.fields["topicid"].empty_label = None


class SubjectFormBeta(forms.ModelForm):
    CHOICES = [
        ("1", "1 Question From Each Selected Topic"),
        ("2", "Questions from Any Selected Topic"),
    ]
    number_of_questions = forms.IntegerField(
        min_value=1,
        max_value=10,
        required=True,
        label="How many questions should be generated from all selected topics (max 10): ",
    )

    class Meta:
        model = Question
        fields = ("subjectid", "topicid", "number_of_questions")

        widgets = {
            "topicid": forms.CheckboxSelectMultiple(attrs={"id": "topics"}),
        }

    field_order = ["subjectid", "topicid", "number_of_questions"]

    # Override params by cleaning it up :)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["topicid"].queryset = Question.objects.none()
        self.fields["topicid"].empty_label = None
