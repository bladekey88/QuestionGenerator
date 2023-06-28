from django.contrib import admin
from .models import Subject, Level, Topic, Question, Profile, Document, ProcessDocument

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.conf.locale.es import formats as es_formats


es_formats.DATETIME_FORMAT = "d M Y H:i:s"


# Set all blank values
admin.site.empty_value_display = "(None)"


class SubjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Subject Information",
            {
                "fields": ["subjectname"],
            },
        ),
    ]
    list_display = ("subjectname",)
    search_fields = ["subjectname"]
    list_filter = ["subjectname"]
    readonly_fields = ("subjectid",)
    ordering = ["subjectname"]


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    max_num = 1


class DocumentAdmin(admin.ModelAdmin):
    list_display = ["get_file_name", "subject", "uploaded_by", "uploaded_at"]
    readonly_fields = [
        "uploaded_by",
        "uploaded_at",
        "subject",
        "get_file_path",
        "get_file_name",
        "document_id",
    ]
    exclude = ("document",)


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    can_delete = False
    verbose_name_ = "Uploaded File"
    fk_name = "uploaded_by"
    readonly_fields = [
        "uploaded_by",
        "uploaded_at",
        "subject",
        "get_file_name",
        "get_file_path",
        "description",
    ]
    exclude = ("document",)

    def has_add_permission(self, request, obj=None):
        return False


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Question Information", {"fields": ["questiontext", "questionanswer"]}),
        ("Subject Information", {"fields": ["topicid", "subjectid"]}),
    ]
    list_display = (
        "questionid",
        "questiontext",
        "questionanswer",
        "subjectid",
        "topicid",
    )
    search_fields = [
        "questiontext",
        "questionanswer",
        "topicid__topicname",
        "subjectid__subjectname",
    ]
    list_filter = ["subjectid", "topicid"]
    readonly_fields = ("questionid",)
    ordering = ["questionid"]


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, DocumentInline)
    list_display = (
        "username",
        "email",
        "first_name",
        "get_middlename",
        "last_name",
        "is_active",
        "is_staff",
        "last_login",
    )
    list_select_related = ("profile",)
    # readonly_fields = ("username",)
    ordering = ["username"]
    search_fields = ["username", "first_name", "last_name", "email"]
    list_filter = ["last_login", "groups", "is_staff", "is_active"]
    list_display_links = list_display
    # list_max_show_all = 50
    list_select_related = True
    save_on_top = True
    show_full_result_count = True

    def get_middlename(self, instance):
        return instance.profile.middlename

    get_middlename.short_description = "Middle Name"


class ProcessDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "processed_id",
        "document_id",
        "processed_by",
        "processed_at",
    ]
    search_fields = ["document_id", "processed_by"]
    ordering = ["-processed_at"]
    readonly_fields = ("document_id",)
    list_display_links = list_display
    list_select_related = ("processed_by",)
    list_filter = ["processed_by", "processed_at"]
    list_select_related = True
    save_on_top = True
    show_full_result_count = True

    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(Document, DocumentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Level)
admin.site.register(Topic)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(ProcessDocument, ProcessDocumentAdmin)
