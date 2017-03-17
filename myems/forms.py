from django.utils import timezone
from django import forms
from django.utils.safestring import mark_safe

from .models import Employee, Salary


class AdminImageFieldWidget(forms.widgets.FileInput):
    def __init__(self, placeholder='/images/profile/placeholder.thumbnail.png'):
        self.placeholder = placeholder
        super(AdminImageFieldWidget, self).__init__({})

    def render(self, name, image, attrs=None):
        render_html = '<img src="%s" />' % (image.thumbnail.url) if image and hasattr(image, "url") else '<img src="%s" />' % (self.placeholder)
        return mark_safe("%s%s" % (render_html, super(AdminImageFieldWidget, self).render(name, image, attrs)))


class EmployeeForm(forms.ModelForm):
    hire_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1980, 2025)), initial=timezone.now)
    birth_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    image = forms.ImageField(label='Profile Image', widget=AdminImageFieldWidget(), required=False)

    class Meta:
        model = Employee
        fields = ('image', 'emp_no', 'birth_date', 'first_name', 'last_name', 'gender', 'hire_date')


class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        fields = '__all__'
