from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from tasks.models import Task, User
from .forms import TaskCreationForm
from django.contrib.auth.mixins import AccessMixin
from .forms import SuperAdminUserCreationForm, UserUpdateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import Group
from django.views.generic import DetailView


class SuperAdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.is_superuser:
            return ['superadmin.html']
        elif self.request.user.groups.filter(name='Admin').exists():
            return ['admin.html']
        else:
            return ['admin.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Pass the user into the form instance
        context['form'] = TaskCreationForm(user=user)

        if user.is_superuser:
            all_users = User.objects.all().prefetch_related('groups')
            for u in all_users:
                u.is_admin = u.groups.filter(name='Admin').exists()
            context['all_users'] = all_users
            context['all_tasks'] = Task.objects.all().order_by('-id')
        
        elif user.groups.filter(name='Admin').exists():
            # Get only the users managed by this Admin
            managed_users = User.objects.filter(profile__managed_by=user)
            # Get only the tasks assigned to those managed users
            context['assigned_tasks'] = Task.objects.filter(assigned_to__in=managed_users).order_by('-id')

        return context

    def post(self, request, *args, **kwargs):
        # Pass the user into the form instance on POST as well
        form = TaskCreationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        
        return render(request, self.get_template_names()[0], self.get_context_data(form=form))
    
    
class UserCreateView(SuperAdminRequiredMixin, CreateView):
    model = User
    form_class = SuperAdminUserCreationForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('dashboard')

class UserUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('dashboard')

class UserDeleteView(SuperAdminRequiredMixin, DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    
    
@user_passes_test(lambda u: u.is_superuser)
def toggle_admin_status(request, pk):
    user_to_toggle = get_object_or_404(User, pk=pk)
    admin_group, created = Group.objects.get_or_create(name='Admin')

    if admin_group in user_to_toggle.groups.all():
        user_to_toggle.groups.remove(admin_group)
    else:
        user_to_toggle.groups.add(admin_group)

    return redirect('dashboard')

class AdminSuperAdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
class TaskReportDetailView(AdminSuperAdminRequiredMixin, DetailView):
    model = Task
    template_name = 'task_report_detail.html'
    context_object_name = 'task'
