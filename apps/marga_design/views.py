from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from slugify import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from apps.marga_design.forms import AuthorForm, CreateBlogPostForm
from apps.marga_design.models import Project, Application, BlogPost
from django.db.models.functions import Random


# макет https://preview.colorlib.com/#marga
# https://colorlib.com/wp/templates/

class MargaHome(ListView):
    """
    Главная страница сайта
    """
    model = Project
    template_name = 'marga_design/home.html'
    context_object_name = 'projects_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(top_rating=True).order_by(Random())[:4]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_posts'] = BlogPost.objects.filter(published=True).order_by('-created')[:4]
        return context


class MargaProject(DetailView):
    """
    Страница проекта
    """
    model = Project
    template_name = 'marga_design/project.html'
    context_object_name = 'project'


class MargaProjectsList(ListView):
    """
    Страница со всеми проектами
    """
    model = Project
    template_name = 'marga_design/projects_list.html'
    context_object_name = 'projects_list'
    paginate_by = 6
    queryset = Project.objects.filter(published=True)


class MargaProjectsApplicationCreateView(CreateView):
    """
    Форма для создания заявки на проект
    """
    model = Application
    template_name = 'marga_design/application_form.html'
    form_class = AuthorForm
    success_url = reverse_lazy('marga_design:thanks')

    def form_valid(self, form):
        form.instance.answer = Application.NEW
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # if not self.request.user.is_staff:  # Проверяем, сотрудник ли это
        del form.fields["note"]  # Удаляем поле для клиентов
        del form.fields["answer"]  # Удаляем поле для клиентов
        return form


class MargaContactCreateView(CreateView):
    """
    Страница с формой обратной связи
    """
    model = Application
    template_name = 'marga_design/contact.html'
    form_class = AuthorForm
    success_url = reverse_lazy('marga_design:thanks')

    def form_valid(self, form):
        form.instance.answer = Application.NEW
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if "note" in form.fields:
            del form.fields["note"]
        if "answer" in form.fields:
            del form.fields["answer"]
        return form

class BlogListView(ListView):
    """Список всех постов блога"""
    model = BlogPost
    template_name = "marga_design/blog_list.html"
    context_object_name = "blog_posts"
    ordering = ["-created"]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published=True)
        return queryset


class BlogPostDetailView(DetailView):
    """Просмотр поста блога"""
    model = BlogPost
    template_name = "marga_design/blog_post.html"
    context_object_name = "blog_post"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class BlogPostEditView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """Редактирование поста блога"""
    model = BlogPost
    template_name = "marga_design/blog_edit.html"
    form_class = CreateBlogPostForm
    permission_required = "marga_design.change_blogpost"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class CreateBlogPost(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """Создание нового поста"""
    model = BlogPost
    template_name = "marga_design/blog_form.html"
    form_class = CreateBlogPostForm
    permission_required = "marga_design.add_blogpost"

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)

        if BlogPost.objects.filter(slug=form.instance.slug).exists():
            return self.render_to_response(self.get_context_data(
                form=form,
                error_message="Пост с таким названием уже существует. Выберите уникальное название."
            ))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(request=request, template_name='errors/error_page.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': 'К сожалению такая страница была не найдена, или перемещена',
    })


def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    return render(request=request, template_name='errors/error_page.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message': 'Внутренняя ошибка сайта, вернитесь на главную страницу, отчёт об ошибке мы направим администрации сайта',
    })


def tr_handler403(request, exception):
    """
    Обработка ошибки 403
    """
    return render(request=request, template_name='errors/error_page.html', status=403, context={
        'title': 'Ошибка доступа: 403',
        'error_message': 'Доступ к этой странице ограничен',
    })
