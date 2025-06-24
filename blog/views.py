from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from .models import Post, Comment
from .forms import CommentForm
from django.shortcuts import render
from django.urls import reverse

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(status='Published').order_by('-timestamp')
    paginate_by = 3


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        comments = Comment.objects.filter(post=post, is_approved=True).order_by('-date_added')
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['comment_count'] = comments.count()

        return context

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(
            Post,
            timestamp__year = self.kwargs['year'],
            timestamp__month = self.kwargs['month'],
            timestamp__day = self.kwargs['day'],
            slug = self.kwargs['slug'],
            status='Published'
        )

        form.instance.post = post
        response = super().form_valid(form)
        return response
    
    def form_invalid(self, form):
        post = get_object_or_404(
            Post,
            timestamp__year = self.kwargs['year'],
            timestamp__month = self.kwargs['month'],
            timestamp__day = self.kwargs['day'],
            slug = self.kwargs['slug'],
            status='Published'
        )

        comments = Comment.objects.filter(
            post = post,
            is_approved=True
        ).order_by('-date_added')

        context = {
            'post': post,
            'comments': comments,
            'comment_form': form,
            'comment_count': comments.count()
        }

        return render(self.request, 'blog/post_detail.html', context)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={
            'year': self.kwargs['year'],
            'month': self.kwargs['month'],
            'day': self.kwargs['day'],
            'slug': self.kwargs['slug']
        })
    
class TaggedPostListView(ListView):
    model = Post
    template_name = 'blog/tagged_post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(
            tags__slug=tag_slug,
            status='Published'
        ).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

