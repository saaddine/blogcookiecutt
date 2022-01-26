from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm, FeedbackForm
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail


class PostListView(generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')


class PostDetailView(generic.DetailView):
    # pk_url_kwarg='pkpk'
    model = Post
    template_name = 'blog/post_detail.html'


# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(
#                 commit=False)  # commit=False means that we don't want to save the Post model yet – we want to add the author first. Most of the time you will use form.save() without commit=False
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})
class CreatePost(generic.CreateView):

    # model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)


class PostEditView(generic.UpdateView):

    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm
    # success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_list')


class CreatefeedView(generic.FormView):
    form_class = FeedbackForm
    success_url = '/'
    template_name = 'blog/feedback.html'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        feedbackmsg = form.cleaned_data['feedbackmsg']
        email = form.cleaned_data['email']
        recipients = ['saad.saadeddine@softcatalyst.com']
        send_mail(name, feedbackmsg, email, recipients)
        return super().form_valid(form)
