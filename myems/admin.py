from django.contrib import admin
# from django.contrib.admin import AdminSite
# from django.utils.translation import ugettext_lazy
from .models import (Employee, Department, DeptEmp, DeptManager, Salary, Titles)
from .forms import EmployeeForm, SalaryForm
from django.utils.safestring import mark_safe


# class MyEmsAdminSite(AdminSite):
#     # Text to put at each page's <title>.
#     site_title = ugettext_lazy('My EMS Site Admin')
#
#     # The text to put at the top of each admin page, as an <h1>
#     site_header = ugettext_lazy('EMS Administration')
#
#     # The text to put at the top of the admin index page
#     index_title = ugettext_lazy('EMS Admin Index')
#
# myems_admin_site = MyEmsAdminSite()


class SalaryTableInline(admin.TabularInline):
    form = SalaryForm
    model = Salary
    fk_name = 'emp_no'
    extra = 1


class DepartmentFilter(admin.SimpleListFilter):
    title = 'Department'
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        departments = set([d for d in Department.objects.all()])
        return [(d.dept_no, d.dept_name) for d in departments]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(departments__dept_no__exact=self.value())
        else:
            return queryset


class GenderFilter(admin.SimpleListFilter):
    title = 'Gender'
    parameter_name = 'gender'

    def lookups(self, request, model_admin):
        return (
            ('M', 'Dicks'),
            ('F', 'Bitches'),
        )

    def queryset(self, request, queryset):
        return queryset.filter(gender__exact=self.value()) if self.value() else queryset


class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    search_fields = ('emp_no', 'first_name', 'last_name', 'hire_date', 'gender')
    list_display = ('image_thumbnail', 'emp_no', 'first_name', 'last_name', 'gender', 'hire_date')
    list_display_links = ('emp_no',)
    list_filter = ('hire_date', GenderFilter, DepartmentFilter)
    save_on_top = True
    inlines = [SalaryTableInline]
    actions_on_bottom = False
    ordering = ('-hire_date',)
    placeholder = '/images/profile/placeholder.thumbnail.png'
    list_per_page = 5

    def image_thumbnail(self, obj):
        return mark_safe('<img src="%s" />' % (obj.image.thumbnail.url if obj.image else self.placeholder))

    image_thumbnail.short_description = 'Profile Image'


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(DeptEmp)
admin.site.register(DeptManager)
admin.site.register(Salary)
admin.site.register(Titles)
