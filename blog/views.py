from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    """
    文章列表
    """
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # 每页显示10篇文章
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


def post_detail(request, pk):
    """
    文章详情
    """
    post = get_object_or_404(Post, pk=pk)
    
    # 增加浏览量
    post.views += 1
    post.save(update_fields=['views'])
    
    # 处理评论
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, '请先登录才能评论！')
            return redirect('login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '评论发表成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,
        'comments': post.comments.all()
    })


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    创建文章
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '文章发布成功！')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    更新文章
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, '文章更新成功！')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    删除文章
    """
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'blog/post_confirm_delete.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, '文章删除成功！')
        return super().delete(request, *args, **kwargs)


def hot_posts(request):
    """
    热度排行榜
    """
    posts = Post.objects.annotate(
        comment_count=Count('comments')
    ).order_by('-heat', '-views')[:20]  # 显示热度最高的20篇文章
    
    return render(request, 'blog/hot_posts.html', {'posts': posts})


def delete_comment(request, pk):
    """
    删除评论
    """
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.author != request.user:
        messages.error(request, '您没有权限删除此评论！')
        return redirect('post_detail', pk=comment.post.pk)
    
    post = comment.post
    comment.delete()
    # 删除评论后重新计算热度
    post.calculate_heat()
    messages.success(request, '评论删除成功！')
    return redirect('post_detail', pk=post.pk)
