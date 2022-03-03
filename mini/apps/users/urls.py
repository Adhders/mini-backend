from django.conf.urls import url

from . import views

urlpatterns = [
    # 用户注册
    url(r'^user_register$', views.RegisterView.as_view(), name='register'),
    url(r'^user_login/(?P<mode>.*)$', views.LoginView.as_view(), name='login'),
    # 发送短信验证码
    url(r'^user_sms_codes/(?P<mobile>.*)$', views.SMSCodesView.as_view()),
    # 手机号重复校验
    url(r'^user_mobiles/(?P<mobile>.*)/count$', views.MobileCountView.as_view()),
    # 修改密码
    url(r'^user_password$', views.ChangePasswordView.as_view(), name='password'),
    # 添加邮箱
    url(r'^user_emails$', views.EmailView.as_view(), name='emails'),
    # 邮箱激活
    url(r'^user_emails/verification$', views.VerifyEmailView.as_view(), name='emails'),

]
