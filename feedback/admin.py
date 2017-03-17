from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django import forms
from .models import Feedback
from .forms import FeedbackForm, FeedbackAddForm
from .actions import mark_feedback_as_read


class FeedbackAdmin(ModelAdmin):
    form = FeedbackForm
    search_fields = ('name', 'category', 'email', 'subject', 'emp_no')
    list_display = ('emp_no', 'name', 'category', 'email', 'subject', 'is_read')
    list_editable = ('is_read',)
    save_on_top = True
    actions_on_bottom = False
    actions = [mark_feedback_as_read]
    ordering = ('-created_on',)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return FeedbackAddForm
        else:
            return super(FeedbackAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Feedback, FeedbackAdmin)
