from warnings import catch_warnings

from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
#from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from logg.models import User, Advertisement, Profile
from logg.permissions import CustomReadOnly
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
import json
from django.shortcuts import render

from django.shortcuts import render
from .models import Advertisement
from selenium import webdriver

def ad_list_view_inf(request):
    ads = Advertisement.objects.all()  # Advertisement 테이블의 모든 데이터를 가져옴
    context = {'ads': ads}
    return render(request, 'logg/inf.html', context)
def filter_ads(request):
    # # JSON 요청을 받기
    # if request.method == 'POST':
    #     data = json.loads(request.body)
    #     selected_prices = data.get('selected_prices', [])
        # URL 파라미터로 전달된 'price' 값을 받아옵니다.
        selected_prices = request.GET.getlist('price')  # ['1', '2', '3'] 형식으로 받아옴
        selected_categories = request.GET.getlist('category')  # ['cosmetic', 'fashion', 'food'] 형식으로 받아옴
        selected_sns = request.GET.getlist('sns')  # ['instagram', 'youtube'] 형식으로 받아옴

# 가격 범위 조건을 담을 리스트
        price_filters = []
        if '1' in selected_prices:
            price_filters.append(0)  # ~10만 원
        if '2' in selected_prices:
            price_filters.append(10)  # 10만 원 이상
        if '3' in selected_prices:
            price_filters.append(20)  # 20만 원 이상
        if '4' in selected_prices:
            price_filters.append(30)  # 30만 원 이상
        if '5' in selected_prices:
            price_filters.append(40)  # 40만 원 이상
        if '6' in selected_prices:
            price_filters.append(50)  # 50만 원 이상


        ads = Advertisement.objects.all()

        if price_filters:
            # price_filters에 포함된 최소 예산 값 중 하나라도 만족하는 광고만 가져오기
            ads = ads.filter(min_budget__gte=min(price_filters))

        # 카테고리 필터 적용
        if selected_categories:
            ads = ads.filter(category__in=selected_categories)

        # SNS 필터 적용
        if selected_sns:
            ads = ads.filter(sns__in=selected_sns)

        # 광고 목록을 JSON 형태로 반환

        ads_data = [{
            "pk": ad.pk,  # 광고의 primary key
            "title": ad.title,
            "product_name": ad.product_name,
            "thumbnail": ad.thumbnail.url if ad.thumbnail else None,  # 썸네일 URL
            "category": ad.category,
            "sns": ad.sns,
            "min_budget": ad.min_budget,
            "max_budget": ad.max_budget
        } for ad in ads]
        return JsonResponse({'ads': ads_data})

#수정해야하는 부분
def ad_list_view_adv(request):
    profs = Profile.objects.all()
    context = {'profs': profs}
    return render(request, 'logg/adv.html', context)

class StartView(TemplateView):
    template_name = 'logg/hello.html'
    def get(self,request,*args, **kwargs):
        print("hello")
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)

class InfluenceView(TemplateView):
    template_name = 'logg/inf.html'
    def get(self,request,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)

class AdvertiseView(TemplateView):
    template_name = 'logg/adv.html'
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)

class PostingView(TemplateView):
    template_name = 'logg/postform.html'
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)
    def post(self, request, *args, **kwargs):
        try:
            thumbnail = request.FILES.get('thumbnail')
            ad_title = request.POST.get('ad-title')
            product_name = request.POST.get('ad-product')
            category = request.POST.get('category')
            sns = request.POST.get('sns')
            min_budget = request.POST.get('min_budget')
            max_amount = request.POST.get('max_budget')
            details = request.POST.get('details')
            product_image = request.FILES.get('details_image')

            ad = Advertisement.objects.create(
                user = request.user,
                thumbnail=thumbnail,
                title=ad_title,
                sns = sns,
                category = category,
                product_name=product_name,
                description=details,
                min_budget=min_budget,
                max_budget=max_amount,
                product_image=product_image
            )

            ad.save()
            return render(request, 'logg/postform.html')
        except Exception as e:
            print(f"Error occurred: {e}")  # 오류 내용 출력
            return render(request, 'logg/postform.html', {'error': 'An error occurred while saving the advertisement.'})

        return redirect('/login/adv/')

class LoginView(TemplateView):
    template_name = 'logg/login.html'
    def get(self,request,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self,request,*args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        position = request.POST['user_type']
        print(username, password, position)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if (user.position != position):
                return render(request, 'logg/login.html')
            messages.success(request, 'You are now logged in')
            login(request, user)
            if (position == "influencer"):
                return redirect('inf/')
            else:
                return redirect('adv/')
        else:
            print("********************************")
            messages.error(request, 'Username or password is incorrect')
            return render(request, 'logg/login.html')

class SignupView(TemplateView):
    template_name = 'logg/sign_up.html'
    def get(self,request,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)
    def post(self,request,*args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email', ' ')
        nickname = request.POST.get('nickname')
        field = request.POST.get('field')
        position = request.POST.get('user_type')
        if password != confirm_password:
            return render(request, 'logg/sign_up.html')
        user = User.objects.create_user(
            username=username,
            position=position,
            password = password
            )
        user.save()
        return redirect('/login/')
#인플루언서
class MypageView(TemplateView):
    template_name = 'logg/mypage.html'
    def get(self,request,*args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)  # Profile 객체 가져오기
        except Profile.DoesNotExist:
            profile = None
        context = super().get_context_data(**kwargs)
        context['profile'] = profile
        return self.render_to_response(context)
    def post(self,request,*args, **kwargs):
        user = request.user
        profile = request.FILES.get('profile')
        content = request.POST.get('category')
        platform = request.POST.get('sns')
        urls = request.POST.get('link')
        min_budget = request.POST.get('min-budget')
        max_budget = request.POST.get('max-budget')
        text_box = request.POST.get('text-box')

        prof, created = Profile.objects.get_or_create(
            user=user,  # user를 기준으로 프로필 조회
            defaults={
                'img': profile,
                'content': content,
                'platform': platform,
                'urls': urls,
                'min_budget': min_budget,
                'max_budget': max_budget,
                'text_box': text_box,
            }
        )
        #UPDATE
        if not created:
            if profile:
                prof.img = profile
            prof.content = content
            prof.platform = platform
            prof.urls = urls
            prof.min_budget = min_budget
            prof.max_budget = max_budget
            prof.text_box = text_box
            prof.save()


        return redirect("/login/inf/")


#광고주 마이페이지
class MypageViewAdv(TemplateView):
    template_name = 'logg/mypage_adv.html'
    def get(self,request,*args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)  # Profile 객체 가져오기
        except Profile.DoesNotExist:
            profile = None
        context = super().get_context_data(**kwargs)
        context['profile'] = profile
        return self.render_to_response(context)
    def post(self,request,*args, **kwargs):
        user = request.user
        profile = request.FILES.get('profile')
        content = request.POST.get('category')
        platform = request.POST.get('sns')
        min_budget = request.POST.get('min-budget')
        max_budget = request.POST.get('max-budget')
        text_box = request.POST.get('text-box')

        prof, created = Profile.objects.get_or_create(
            user=user,  # user를 기준으로 프로필 조회
            defaults={
                'img': profile,
                'content': content,
                'platform': platform,
                'min_budget': min_budget,
                'max_budget': max_budget,
                'text_box': text_box,
            }
        )
        #UPDATE
        if not created:
            if profile:
                prof.img = profile
            prof.content = content
            prof.platform = platform
            prof.urls = ''
            prof.min_budget = min_budget
            prof.max_budget = max_budget
            prof.text_box = text_box
            prof.save()


        return redirect("/login/adv/")
#인플루언서 상세페이지
def detailInf(request,id):
    adv = get_object_or_404(Advertisement,id = id)

    #channel_data = get_channel_statistics(request, adv.get("platform"), adv.data.get("urls"))
    context = {
        'ad_data':adv,
        #'channel_data': channel_data
    }
    return render(request,'logg/detail.html',context)

#인플루언서 상세페이지
def detailAdv(request,id):
    inf = get_object_or_404(Profile,id = id)
        # 필요한 데이터 직접 추출
    platform = getattr(inf, 'platform', None)  # 'platform' 필드
    urls = getattr(inf, 'urls', None)  # 'urls' 필드
    print(urls)
    # `get_channel_statistics` 함수 호출
    if platform and urls:
        channel_data = get_channel_statistics(request, platform, urls)
    else:
        channel_data = {}  # 기본값: 데이터가 없을 경우 빈 딕셔너리 반환

    # 템플릿에 전달할 컨텍스트
    context = {
        'inf_data': inf,
        'channel_data': channel_data,
    }
    return render(request, 'logg/detail_adv.html', context)


# # 로그인
# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         token = serializer.validated_data
#         return Response({"token": token.key}, status=status.HTTP_200_OK)


# 프로필
# class ProfileView(generics.RetrieveUpdateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     # permission_classes = [IsAuthenticatedOrReadOnly, CustomReadOnly]

# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
'''API 처리 함수'''
import re

from django.http import JsonResponse
from googleapiclient.discovery import build
from django.conf import settings
from django.shortcuts import render
from googleapiclient.errors import HttpError
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_SERVICE_VERSION = 'v3'
# YouTube API 클라이언트 생성
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_SERVICE_VERSION, developerKey=settings.API_KEY)


# video_json_data ={NULL_MASK}

# 유튜브 링크에서 비디오 ID를 추출하는 함수
def extract_video_id(url):
    video_id_pattern = r'(?:youtube\.com\/(?:[^\/\n\s]*\/\S*\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(video_id_pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("유효한 YouTube URL이 아닙니다.")


# Django 뷰: YouTube 동영상 데이터 가져오기
'''def youtube_statistics(request):
    # 요청에서 URL 가져오기#다운그레이드 하자

    youtube_url = 'https://www.youtube.com/watch?v=D2rYY8w2BAQ'
    if not youtube_url:
        return JsonResponse({'error': 'YouTube URL이 필요합니다.'}, status=400)

    # 비디오 ID 추출
    video_id = extract_video_id(youtube_url)

    # YouTube API로 데이터 요청
    response = youtube.videos().list(
        part='statistics',
        id=video_id
    ).execute()
    video_data = response['items'][0]['statistics']
    view_count = video_data.get('viewCount', '정보 없음')
    like_count = video_data.get('likeCount', '정보 없음')
    comment_count = video_data.get('commentCount', '정보 없음')
    # 데이터 추출
    video_dict_data = {
        'video_id': video_id,
        'view_count': view_count,
        'like_count': like_count,
        'comment_count': comment_count
    }
    # JSON 응답 반환
    return video_dict_data'''


'''이거는 이제 한 인플루언서의 유튜브 정보를 나타내는 코드(인플루언서 마이페이지에 뜰 통계) '''

def get_channel_statistics(request,platform,urls):

    try:
        # 요청에서 채널 ID 가져오기
        if (platform.lower()=='youtube'):
            if '@' in urls:
                match = re.search(r"youtube\.com/@([a-zA-Z0-9_-]+)", urls)
                if match:
                    handle = match.group(1)
                else:
                    print("nohandle")
            else:
                match = re.search(r"youtube\.com/([a-zA-Z0-9_-]+)", urls)
                if match:
                    handle = match.group(1)
                else:
                    print("nohandle")

            response = youtube.channels().list(
                part="id",
                forHandle=handle
            ).execute()

            if "items" in response and len(response["items"]) > 0:
               channel_id = response["items"][0]["id"]
            else:
                print("No channel ID found for the given handle.")

            print(channel_id)

            # 채널의 동영상 검색
            search_response = youtube.search().list(
                channelId=channel_id,
                part='id',
                maxResults=50,  # 한 번에 가져올 동영상 수 (최대 50개)
                type='video',
                order = 'date'
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response['items']]
            if not video_ids:
                return JsonResponse({'error': '채널에 동영상이 없습니다.'}, status=404)

            videos_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids)  # 동영상 ID를 쉼표로 구분하여 전달
            ).execute()
            # 채널의 통계 데이터 가져오기
            channel_response = youtube.channels().list(
                part='statistics',
                id=channel_id
            ).execute()

            channel_statistics = channel_response['items'][0]['statistics']
            subscribers_count = channel_statistics.get('subscriberCount', '0')

            results = []
            total_view_count = 0
            total_like_count = 0
            total_comment_count=0
            rateoflikes=0;
            for item in videos_response['items']:
                statistics = item['statistics']
                results.append({
                    'video_id': item['id'],
                    'view_count': statistics.get('viewCount', '0'),
                    'like_count': statistics.get('likeCount', '0'),
                    'comment_count': statistics.get('commentCount', '0'),
                    # 'subscribers_count': statistics.get('subscriberCount', '0')
                })
                total_view_count += int(statistics.get('viewCount', '0'))

                total_comment_count+= int(statistics.get('commentCount', '0'))
                rateoflikes+=int(statistics.get('likeCount', '0'))/int(statistics.get('viewCount', '0'))*100
            totalrate_view_count=total_view_count
            totalrate_view_count/=50
            rateoflikes=round(rateoflikes/50,2)
            total_comment_count/=50
            influencers_dict_data = {
                'channel_id': channel_id,
                'subscribers_count': subscribers_count,
                'total_view_count': total_view_count,
                'totalrate_view_count': str(totalrate_view_count),
                'rateoflikes': str(rateoflikes),
                'totalrate_comment_count':str(total_comment_count)
            }
        # JSON 응답 반환
            return influencers_dict_data
        else:
            influencers_dict_data = {
                'channel_id': '-',
                'subscribers_count': '-',
                'total_view_count': '-',
                'totalrate_view_count': '-',
                'rateoflikes': '-',
                'totalrate_comment_count': '-'
            }
            return influencers_dict_data

    except HttpError as e:
        return JsonResponse({'error': 'YouTube API 호출 실패', 'details': str(e)}, status=500)

    except Exception as e:
        return JsonResponse({'error': '서버 오류', 'details': str(e)}, status=500)


'''인스타그램 광고 현황'''


def get_instagram_channel_details(request):
    username = settings.INSTAGRAM_USERNAME
    password = settings.INSTAGRAM_PASSWORD

    # Chrome WebDriver 설정
    driver = webdriver.Chrome()
    post_url = "본래 게시물 url"
    if not post_url:
        return JsonResponse({'error': '게시물 URL이 필요합니다'})
    # Instagram 로그인 페이지 열기
    driver.get('https://www.instagram.com/accounts/login/')

    # 로그인 (계정 정보 입력)
    time.sleep(2)  # 페이지 로딩 시간
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')

    username_input.send_keys(username)
    password_input.send_keys(password)

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(5)  # 로그인 후 페이지 로딩 대기'''

    # 개인 계정의 특정 게시물 URL로 이동

    driver.get(post_url)
    # time.sleep(3)

    try:
        likes = driver.find_element(By.XPATH,
                                    "//span[contains(@class, 'html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs')]").text
        comments = driver.find_element(By.XPATH, "//span[@class='C4VMK']").text  # 댓글 수 추출 방법은 게시물 구조에 따라 다를 수 있음
        instagram_dict_data = {
            'post_url': post_url,
            'likes': likes,
            'comments': comments  # 필요 시 추가
        }
        return instagram_dict_data
    except Exception as e:
        print("정보를 추출할 수 없습니다.", e)
    finally:
        driver.quit()





