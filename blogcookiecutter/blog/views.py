import json

from crispy_forms.utils import render_crispy_form
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Post
from .forms import PostForm, FeedbackForm
from django.views import generic
from django.views.generic.edit import DeleteView
from django.views.generic import View
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.forms.models import model_to_dict


class PostListView(generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')


class PostDetailView(generic.DetailView):
    # pk_url_kwarg='pkpk'

    model = Post
    template_name = 'blog/post_detail.html'

    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context['form']=PostForm(instance=self.object)
    #     print(context)
    #     return context


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


#
# def blog_update(request, pk):
#     context = dict()
#     if request.method == 'GET' and request.is_ajax():
#         print(request.GET)
#        # ID = request.GET.get('id')
#         post = Post.objects.filter(id=pk).first()
#         form=PostForm(instance=post)
#         title = post.title
#         text = post.text
#         context['title'] = title
#         context['text'] = text
#         context['form'] = form
#         return HttpResponse(json.dumps(context, default=str), content_type="application/json")
#
#     if request.method == 'POST' and request.is_ajax():
#         new_data = json.loads(request.POST.get('formm', None))
#         #Id = request.POST.get('id')
#         post = Post.objects.get(id=pk)
#         post.title = new_data['title']
#         post.text = new_data['text']
#         post.save()
#         print("hhhhhhh******")
#         context['title'] = post.title
#         context['text'] = post.text
#         return HttpResponse(json.dumps(context), content_type="application/json", status=201)

class PostUpdate(View):

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        form = PostForm(instance=post)
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        data = {'form': form_html}
        return JsonResponse(data)

    def post(self, request, pk):
        data = dict()
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post, data=request.POST)
        print(form)
        if form.is_valid():
            print('valid')
            post = form.save()
            data['post'] = model_to_dict(post)
            data['title'] = post.title
            data['text'] = post.text
            data['success'] = True

        else:
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            data['form'] = form_html
            data['error'] = "form not valid!"
        return JsonResponse(data)


# def blog_delete(request, pk):
#
#     context = dict()
#     if request.method == 'POST'and request.is_ajax():
#         post = get_object_or_404(Post, pk=pk)
#         post.delete()
#         posts = Post.objects.all()
#         context['item'] =pk
#         return HttpResponse(json.dumps(context), content_type="application/json", status=201)


class PostDelete(DeleteView):
    model = Post
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {}
        # if self.get_object():
        #     data['message'] = "Blog Post deleted!"
        # else:
        #     data['message'] = "Error!"
        return JsonResponse({'message': "Blog Post deleted!"})

        # data = dict()
        # post = Post.objects.get(pk=pk)
        # if post:
        #     post.delete()
        #     data['message'] =  "Blog Post deleted!"
        # else:
        #     data['message'] =  "Error!"
        # return JsonResponse(data)
