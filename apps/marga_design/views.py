from django.urls import reverse_lazy
from slugify import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from apps.marga_design.forms import AuthorForm
from apps.marga_design.models import Project, Application, BlogPost


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
        queryset = queryset.filter(top_rating=True).order_by('?')[:4]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_posts'] = BlogPost.objects.all().order_by('-created')[:4]
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

    # def form_invalid(self, form):
    #     print("Форма не прошла валидацию:", form.errors)
    #     return super().form_invalid(form)


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


class BlogListView(ListView):
    """Список всех постов блога"""
    model = BlogPost
    template_name = "marga_design/blog_list.html"
    context_object_name = "blog_posts"
    ordering = ["-created"]


class BlogPostDetailView(DetailView):
    """Просмотр поста блога"""
    model = BlogPost
    template_name = "marga_design/blog_post.html"
    context_object_name = "blog_post"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class BlogPostEditView(UpdateView):
    """Редактирование поста блога"""
    model = BlogPost
    template_name = "marga_design/blog_edit.html"
    fields = ["title", "content"]

    def get_success_url(self):
        return self.object.get_absolute_url()  # Перенаправление после сохранения


class CreateBlogPost(CreateView):
    """Создание нового поста"""
    model = BlogPost
    template_name = "marga_design/blog_form.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)  # Генерация слага перед сохранением
        return super().form_valid(form)
