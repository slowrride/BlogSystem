from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    文章表单
    """
    VISIBILITY_CHOICES = [
        (True, '公开'),
        (False, '仅个人可见'),
    ]

    is_public = forms.ChoiceField(
        choices=VISIBILITY_CHOICES,
        label='文章可见性',
        initial=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'cover_image', 'attachment1', 'attachment2', 'attachment3', 'is_public')
        labels = {
            'title': '标题',
            'content': '内容',
            'cover_image': '封面图片（可选）',
            'attachment1': '附件1（可选）',
            'attachment2': '附件2（可选）',
            'attachment3': '附件3（可选）',
            'is_public': '文章可见性',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'id': 'content-editor'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'attachment1': forms.FileInput(attrs={'class': 'form-control'}),
            'attachment2': forms.FileInput(attrs={'class': 'form-control'}),
            'attachment3': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['is_public'].initial = self.instance.is_public


class CommentForm(forms.ModelForm):
    """
    评论表单
    """
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': '评论内容',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
