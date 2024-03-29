from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import PostForm
from blog.models import Post
from blog.services import check_payment


class PostCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания поста"""
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:blog')
    extra_context = {
        'title': 'Новый пост'
    }

    def form_valid(self, form):
        """Добавляем пользователя к экземпляру поста"""
        if form.is_valid():
            self.object = form.save()
            self.object.slug = slugify(self.object.title)
            self.object.user = self.request.user
            self.object.save()
        return super().form_valid(form)


class PostListView(ListView):
    """Представление cписка постов"""
    model = Post
    extra_context = {'title': 'Блог'}
    paginate_by = 3


class PostDetailView(DetailView):
    """Представление деталей поста"""
    model = Post
    # permission_required = 'blog.view_post'

    def get_context_data(self, **kwargs):
        """Добавляем +1 просмотр"""
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post.views_count += 1
        post.save()
        context['title'] = post.title
        return context

    def dispatch(self, request, *args, **kwargs):
        """Проверка наличия подписки для платного поста"""
        obj = self.get_object()
        if obj.is_private and not request.user.is_subscribed and not request.user.is_staff and request.user != obj.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        redirect_url = reverse_lazy('blog:subscription')
        return HttpResponseRedirect(redirect_url)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Представление редактирования поста"""
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:blog')
    extra_context = {'title': 'Редактировать пост'}
    # permission_required = 'blog.change_post'

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        """Проверка права редактирования поста (только для авторов и модераторов)"""
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь автором поста или модератором")
        return self.object


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Представление удаления поста"""
    model = Post
    extra_context = {'title': 'Удалить пост'}
    success_url = reverse_lazy('blog:blog')
    permission_required = 'blog.delete_post'


class ContactsPageView(View):
    """Представление контактов и обратной связи"""
    def get(self, request):
        context = {'title': 'Контакты'}
        return render(request, 'blog/contacts.html', context)

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} ({phone}): {message}')
        context = {'title': 'Контакты'}
        return render(request, 'blog/contacts.html', context)


class SubscriptionPageView(LoginRequiredMixin, View):
    """Представление страницы с подпиской"""
    def get(self, request):
        context = {'title': 'Подписка'}
        return render(request, 'blog/subscription.html', context)


class SubscriptionSuccessPageView(LoginRequiredMixin, View):
    """Представление страницы с подпиской после оплаты"""
    def get(self, request):
        check_payment(request.user)
        context = {'title': 'Подписка'}
        return render(request, 'blog/subscription_success.html', context)
