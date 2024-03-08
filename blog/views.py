from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import PostForm, PaymentForm
from blog.models import Post, Payment
from blog.services import check_payment


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:blog')
    extra_context = {
        'title': 'Новый пост'
    }

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.slug = slugify(self.object.title)
            self.object.user = self.request.user
            self.object.save()
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    extra_context = {'title': 'Блог'}
    paginate_by = 3


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    # permission_required = 'blog.view_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # if not self.request.user.is_subscribed and post.is_private
        post.views_count += 1
        post.save()
        context['title'] = post.title
        return context

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.is_private and not self.request.user.is_subscribed:
    #         raise Http404("Для просмотра данного поста необходима подписка")
    #     return self.object

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_private and not request.user.is_subscribed:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        redirect_url = reverse_lazy('blog:subscription')
        return HttpResponseRedirect(redirect_url)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:blog')
    extra_context = {'title': 'Редактировать пост'}
    permission_required = 'blog.change_post'

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    extra_context = {'title': 'Удалить пост'}
    success_url = reverse_lazy('blog:blog')
    permission_required = 'blog.delete_post'


class ContactsPageView(View):
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

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            self.object.save()
        return super().form_valid(form)


class SubscriptionPageView(LoginRequiredMixin, View):
    def get(self, request):
        context = {'title': 'Подписка'}
        return render(request, 'blog/subscription.html', context)


class SubscriptionSuccessPageView(LoginRequiredMixin, View):
    def get(self, request):
        check_payment(request.user)
        context = {'title': 'Подписка'}
        return render(request, 'blog/subscription_success.html', context)