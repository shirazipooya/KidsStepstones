from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, CreateView
from .models import User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy, reverse

@login_required
def home(request):
    return render(request, "account/home.html")


class Login(LoginView):    
    template_name = "account/login.html" 
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy("dashboard:home")
        else:
            return reverse_lazy("dashboard:profile")


class PasswordChange(PasswordChangeView):
    template_name = "account/password_change_form.html"  
    success_url = reverse_lazy("account:password_change_done")


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = "account/password_change_done.html"  


class PasswordReset(PasswordResetView):
    template_name = "account/password_reset_form.html"  
    success_url = reverse_lazy("account:password_reset_done")
    email_template_name = "account/password_reset_email.html"


class PasswordResetDone(PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"  
    success_url = reverse_lazy("account:password_reset_complete")


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"




from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

class Register(CreateView):
	form_class = SignupForm
	template_name = "account/register.html"

	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_active = False
		user.save()
		current_site = get_current_site(self.request)
		mail_subject = 'فعال سازی حساب کاربری'
		message = render_to_string('account/activate_account.html', {
			'user': user,
			'domain': current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':account_activation_token.make_token(user),
		})
		to_email = form.cleaned_data.get('email')
		email = EmailMessage(
					mail_subject, message, to=[to_email]
		)
		email.send()
		return render(self.request, "account/send_activation_email.html")


def activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		return render(request, "account/active_account_success.html")
	else:
		return render(request, "account/active_account_failed.html")
