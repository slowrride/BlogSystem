from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.db.models import Count
from .models import Post, Comment, Notification, Message
from users.models import User, Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# 必须登录之后才能点赞
@login_required
def like_post(request, pk):
    """
    点赞/取消点赞
    :param request:
    :param pk:
    :return:
    """
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        # 创建点赞通知（不给自己发通知）
        if request.user != post.author:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='like',
                post=post
            )

    post.calculate_heat()

    return JsonResponse({'liked': liked, 'like_count': post.like_count})

    # return JsonResponse({'likes': post.likes.count()})

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
            # 创建评论通知（不给自己发通知）
            if request.user != post.author:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )
            messages.success(request, '评论发表成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,
        'comments': post.comments.all(),
        'common_emojis': ['😊', '😂', '🥰', '😍', '🤔', '😢', '😡', '👍', '👎', '🎉', '💪', '🙏', '✨', '❤️', '🔥'],
        'gesture_emojis': ['👋', '🤝', '👆', '👇', '👉', '👈', '✌️', '🤞', '👏', '🙌', '👐', '🤙', '👋', '💅', '👄']
    })


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    创建文章
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 添加表情包数据
        context['common_emojis'] = ['😊', '😂', '🥰', '😍', '🤔', '😢', '😡', '👍', '👎', '🎉', '💪', '🙏', '✨', '❤️', '🔥']
        context['gesture_emojis'] = ['👋', '🤝', '👆', '👇', '👉', '👈', '✌️', '🤞', '👏', '🙌', '👐', '🤙', '👋', '💅', '👄']
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # 给所有粉丝发送新文章通知
        from users.models import Follow
        follower_relations = Follow.objects.filter(following=self.request.user)
        for relation in follower_relations:
            Notification.objects.create(
                recipient=relation.follower,
                sender=self.request.user,
                notification_type='new_post',
                post=form.instance,
                comment=None
            )

        messages.success(self.request, '文章发布成功！')
        return response


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    更新文章
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 添加表情包数据
        context['common_emojis'] = ['😊', '😂', '🥰', '😍', '🤔', '😢', '😡', '👍', '👎', '🎉', '💪', '🙏', '✨', '❤️', '🔥']
        context['gesture_emojis'] = ['👋', '🤝', '👆', '👇', '👉', '👈', '✌️', '🤞', '👏', '🙌', '👐', '🤙', '👋', '💅', '👄']
        return context

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


@login_required
def notification_list(request):
    """
    通知列表
    """
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'blog/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


@login_required
def mark_notification_read(request, pk):
    """
    标记通知为已读
    """
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()

    # 根据通知类型跳转到不同页面
    if notification.notification_type == 'message':
        # 私信通知，跳转到聊天界面
        return redirect('chat_with', username=notification.sender.username)
    elif notification.notification_type == 'follow':
        # 关注通知，跳转到发送者主页
        return redirect('profile', username=notification.sender.username)
    elif notification.notification_type in ['like', 'comment', 'new_post']:
        # 文章相关通知，跳转到相关文章
        if notification.post:
            return redirect('post_detail', pk=notification.post.pk)
        else:
            return redirect('notification_list')
    else:
        # 其他情况，跳转到通知列表
        return redirect('notification_list')


@login_required
def mark_all_read(request):
    """
    标记所有通知为已读
    """
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('notification_list')


@login_required
def message_list(request):
    """
    消息列表 - 显示所有聊天会话
    """
    # 获取当前用户所有涉及的消息（发送或接收）
    sent_messages = request.user.sent_messages.all()
    received_messages = request.user.received_messages.all()

    # 合并消息并按时间倒序排列
    all_messages = list(sent_messages) + list(received_messages)
    all_messages.sort(key=lambda x: x.created_at, reverse=True)

    # 获取唯一的对话伙伴
    conversations = {}
    total_unread = 0
    for msg in all_messages:
        other_user = msg.recipient if msg.sender == request.user else msg.sender
        if other_user not in conversations:
            unread_count = request.user.received_messages.filter(
                sender=other_user,
                is_read=False
            ).count()
            total_unread += unread_count
            conversations[other_user] = {
                'user': other_user,
                'last_message': msg,
                'unread_count': unread_count
            }

    # 按最后消息时间排序
    conversations = sorted(
        conversations.values(),
        key=lambda x: x['last_message'].created_at,
        reverse=True
    )

    return render(request, 'blog/message_list.html', {
        'conversations': conversations,
        'total_unread': total_unread
    })


@login_required
def chat_with(request, username):
    """
    与特定用户聊天
    """
    other_user = get_object_or_404(User, username=username)

    # 获取两个用户之间的所有消息
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(recipient=other_user)) |
        (models.Q(sender=other_user) & models.Q(recipient=request.user))
    ).order_by('created_at')

    # 标记对方发来的消息为已读
    Message.objects.filter(
        sender=other_user,
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                recipient=other_user,
                content=content
            )
            return redirect('chat_with', username=username)

    return render(request, 'blog/chat.html', {
        'other_user': other_user,
        'messages': messages,
        'common_emojis': ['😊', '😂', '🥰', '😍', '🤔', '😢', '😡', '👍', '👎', '🎉', '💪', '🙏', '✨', '❤️', '🔥'],
        'gesture_emojis': ['👋', '🤝', '👆', '👇', '👉', '👈', '✌️', '🤞', '👏', '🙌', '👐', '🤙', '👋', '💅', '👄']
    })


@login_required
def get_new_messages(request, username):
    """
    AJAX接口：获取新消息
    """
    other_user = get_object_or_404(User, username=username)

    # 获取最后一条消息的时间戳
    last_message_time = request.GET.get('last_time')

    # 获取新消息
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(recipient=other_user)) |
        (models.Q(sender=other_user) & models.Q(recipient=request.user))
    ).order_by('created_at')

    if last_message_time:
        from datetime import datetime
        try:
            last_time = datetime.fromisoformat(last_message_time)
            messages = messages.filter(created_at__gt=last_time)
        except:
            pass

    # 标记对方发来的新消息为已读
    Message.objects.filter(
        sender=other_user,
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    # 返回JSON格式的新消息
    messages_data = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'recipient': msg.recipient.username,
        'content': msg.content,
        'created_at': msg.created_at.isoformat(),
        'is_me': msg.sender == request.user
    } for msg in messages]

    return JsonResponse({'messages': messages_data})


@login_required
def follow_user(request, username):
    """
    关注用户
    """
    user_to_follow = get_object_or_404(User, username=username)

    if user_to_follow == request.user:
        messages.error(request, '不能关注自己！')
        # 重定向到上一页，如果没有则跳转到用户主页
        next_url = request.META.get('HTTP_REFERER')
        if next_url:
            return redirect(next_url)
        return redirect('profile', username=username)

    # 检查是否已经关注
    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)

        # 发送关注通知
        Notification.objects.create(
            recipient=user_to_follow,
            sender=request.user,
            notification_type='follow',
            post=None,
            comment=None
        )

        messages.success(request, f'已关注 {user_to_follow.username}！')
    else:
        messages.info(request, f'你已经关注了 {user_to_follow.username}')

    # 重定向到上一页，如果没有则跳转到用户主页
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('profile', username=username)


@login_required
def unfollow_user(request, username):
    """
    取消关注用户
    """
    user_to_unfollow = get_object_or_404(User, username=username)

    # 删除关注关系
    follow_relation = Follow.objects.filter(
        follower=request.user,
        following=user_to_unfollow
    ).first()

    if follow_relation:
        follow_relation.delete()
        messages.success(request, f'已取消关注 {user_to_unfollow.username}！')
    else:
        messages.info(request, f'你没有关注 {user_to_unfollow.username}')

    # 重定向到上一页，如果没有则跳转到用户主页
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('profile', username=username)


@login_required
def followers_list(request, username):
    """
    粉丝列表
    """
    user = get_object_or_404(User, username=username)
    from users.models import Follow
    follower_relations = Follow.objects.filter(following=user)

    return render(request, 'blog/followers_list.html', {
        'user': user,
        'followers': follower_relations
    })


@login_required
def following_list(request, username):
    """
    关注列表
    """
    user = get_object_or_404(User, username=username)
    from users.models import Follow
    following_relations = Follow.objects.filter(follower=user)

    return render(request, 'blog/following_list.html', {
        'user': user,
        'following': following_relations
    })
