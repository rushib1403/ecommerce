from django.urls import path
from shop import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('tables2',views.tables2),
    path('checkmail',views.checkmail),
    path('adminpanel',views.adminpanel),
    path('sendcoupon',views.sendcoupon),
    path('checkcoupon',views.checkcoupon),
    path('exam',views.exam),
    path('userinfo',views.userinfo),
    path('track',views.track),
     path('categorywise_all',views.categorywise_all),
    path('handlerequest/',views.handlerequest),
    path('chatjava',views.chatjava),
   path('category',views.category),
  path("sendstatus",views.sendstatus),
    path('viewprod',views.viewprod),
    path("postComment",views.postComment),
    path("", views.store),
     path('prevorder2',views.prevorder),
    path("cart",views.cart),
    path("search",views.search),
    path("checkout",views.checkout),
    path("updateitem",views.updateitem),
    path("processorder",views.processorder),
    path("processorder2",views.processorder2),
    path("contact", views.contact),
    path("contact2", views.contact2),
    path("signup",views.handlesignup),
    path("login",views.handlelogin),
    path("logout",views.handlelogout),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="shop/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="shop/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="shop/password_reset_form.html"),
     name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="shop/password_reset_done.html"),
        name="password_reset_complete"),
]
