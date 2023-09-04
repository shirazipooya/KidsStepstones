from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from posts.models import Post, Category

class FieldsMixin():
    
    def dispatch(self, request, *args, **kwargs):
        
        self.fields = [
            "title",
            "slug",
            "category",
            "body",
            "thumbnail",
            "publish",
            'is_special',
            "status"
        ]
        
        if request.user.is_superuser:
            self.fields.append("author")

        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            print("--------------------------------------------------------")
            print("--------------------------------------------------------")
            print(self.obj.status)
            if not (self.obj.status == 'i'):
                self.obj.status = 'd'
        
        return super().form_valid(form)



class AuthorAccessMixin():    
    def dispatch(self, request, pk, *args, **kwargs):        
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user and post.status in ["d", "b"] or\
            request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("شما اجازه دسترسی به این صفحه را ندارید.")


class AuthorsAccessMixin():    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:      
            if request.user.is_author or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("dashboard:profile")
        else:
            return redirect("account:login")
            


class SuperuserAccessMixin():    
    def dispatch(self, request, *args, **kwargs):        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("شما اجازه دسترسی به این صفحه را ندارید.")