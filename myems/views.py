from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import EmployeeForm
from .models import Employee, Salary, generate_next_emp_no


def index(request):
    if request.method.upper() == 'GET':
        return render(request, 'index.html', {})


def my_profile(request, pk):
    profile = get_object_or_404(Employee, pk=pk)
    if request.method.upper() == 'POST':
        form = EmployeeForm(request.POST, request, instance=profile)
        if form.is_valid():
            # Process form cleaned data
            form.save()
            return redirect('my_profile', pk=pk)
    form = EmployeeForm(instance=profile)
    return render(request, 'profile.html', {'form': form})


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {})

    def post(self, request, *args, **kwargs):
        return render(request, 'index.html', {})


class IndexGenericView(TemplateView):
    template_name = 'index.html'

class ProfileView(View):
    form_class = EmployeeForm
    template_name = 'my_profile_detail.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_context_data().get('profile'))
        return render(request, self.get_template_name(), {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success/')
        return render(request, self.template_name, {'form': form})

    def get_template_name(self):
        return self.template_name

    def get_context_data(self):
        return {
            'profile': self.get_object(),
        }

    def get_object(self):
        return get_object_or_404(Employee, pk=self.kwargs.get('pk'))


class ProfileListView(ListView):
    model = Employee
    template_name = 'profile_list.html'
    paginate_by = 100

    def get_queryset(self):
        order_by_field = self.request.GET.get('order-by') or '-hire_date'
        queryset = super(ProfileListView, self).get_queryset()
        return queryset.order_by(order_by_field)


class ProfileDetailView(DetailView):
    template_name = 'my_profile_detail.html'
    model = Employee

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['salary_entries'] = Salary.objects.filter(emp_no__exact=self.object.emp_no)
        return context


class ProfileCreateView(CreateView):
    template_name = 'my_profile_create.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('profile_list')

    def get_initial(self):
        initial =super(ProfileCreateView, self).get_initial()
        initial['emp_no'] = generate_next_emp_no()
        return initial


class ProfileUpdateView(UpdateView):
    template_name = 'my_profile_update.html'
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('profile_list')


class ProfileDeleteView(DeleteView):
    model = Employee
    success_url = reverse_lazy('profile_list')

    def get(self, request, *args, **kwargs):
        """
        Note: This is a hack as we don't want to show a confirmation page before deleting.
        Django will default to objectname__confirm_delete.html.
        """
        return self.post(request, *args, **kwargs)