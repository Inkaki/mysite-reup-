from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm
)

from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views.decorators.http import require_POST


User = get_user_model()


class Top(generic.TemplateView):
    template_name = 'accounts/top.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'accounts/top.html'


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'accounts/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject_template = get_template('accounts/mail_template/create/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('accounts/mail_template/create/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('accounts:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'accounts/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'accounts/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoenNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # まだ仮登録で、他に問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()



class OnlyYouMixin(UserPassesTestMixin):
    """本人か、スーパーユーザーだけユーザーページアクセスを許可する"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    """ユーザーの詳細ページ"""
    model = User
    template_name = 'accounts/user_detail.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    """ユーザー情報更新ページ"""
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く

    def get_success_url(self):
        return resolve_url('accounts:user_detail', pk=self.kwargs['pk'])


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'accounts/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'accounts/mail_template/reset/subject.txt'
    email_template_name = 'accounts/mail_template/reset/message.txt'
    template_name = 'accounts/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
template_name = 'accounts/password_reset_complete.html'

class chart(generic.TemplateView):
	"""グラフ、インフォグラフィック建設"""	
	template_name = 'accounts/chart.html'

class money_literacy(generic.TemplateView):
	"""マネーリテラシー（収支の概念、クレジットカード、投資、節約術）ソースのリンクを張る。"""	
	template_name = 'accounts/literacy.html'

def mail1(request):
    subject = "題名"
    message = "本文\\nです"
    from_email = "inukaielms181@eis.hokudai.ac.jp"
    # 宛先を変えたい場合は、このリストの中を変更しましょう。このアドレスは私のアドレスです。
    # たまにメールが届きます。ちょっとほんわかします。
    recipient_list = [
        "inukaielms181@eis.hokudai.ac.jp"
    ]
 
    send_mail(subject, message, from_email, recipient_list)
    return render(request, 'accounts/base.html')
 
 
def mail2(request):
    subject = "題名"
    message = "本文\\nです"
    # ログインユーザーなら、request.userでUserモデルインスタンスが取得できます
    user = User.objects.get(email="toritoritorina@gmail.com")
    user.email_user(subject, message)  # メールの送信
 
    from_email = "inukaielms181@eis.hokudai.ac.jp"
    user.email_user(subject, message, from_email)  # メールの送信
    return render(request, 'accounts/base.html')
 
 
def mail3(request):
    subject = "題名"
    message = "本文\\nです"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [
        "inukaielms181@eis.hokudai.ac.jp"
    ]
    send_mail(subject, message, from_email, recipient_list)
    return render(request, 'accounts/base.html')
 
 
def mail4(request):
    subject = "題名"
    message = "本文\\nです"
    from_email = settings.EMAIL_HOST_USER
    to = ["inukaielms181@eis.hokudai.ac.jp"]
    bcc = ["inukaielms181@eis.hokudai.ac.jp"]
    email = EmailMessage(subject, message, from_email, to, bcc)
    email.send()
    return render(request, 'accounts/base.html')
 
 
def mail5(request):
    subject = "題名"
 
    mail_template = get_template('accounts/mailtemplate/mail.txt')
    user = User.objects.get(pk=1)  # is_superuser=True 等もよく使う
    context = {
        "user": user,
    }
    message = mail_template.render(context)
 
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [
        "inukaielms181@eis.hokudai.ac.jp"
    ]
    send_mail(subject, message, from_email, recipient_list)
    return render(request, 'accounts/base.html')
