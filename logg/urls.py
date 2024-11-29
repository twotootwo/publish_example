# logg/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from logg import views


urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),  # /login/ 경로에 CustomLoginView 연결
    path('sign-up/',views.SignupView.as_view(),name="sign_up"),
    path('inf/',views.ad_list_view_inf,name="inf"),
    path('filter-ads/', views.filter_ads, name='filter_ads'),
    path('adv/',views.ad_list_view_adv,name="adv"),
    path('postform/',views.PostingView.as_view(),name="post_form"),
    path('details/<int:id>/', views.detailInf, name="detailView"),
    path('details_adv/<int:id>/', views.detailAdv, name="detailAdv"),
    path('mypage/',views.MypageView.as_view(),name="mypage"),
    path('mypage_adv/',views.MypageViewAdv.as_view(),name="mypageAdv"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
