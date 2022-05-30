from django.shortcuts import render, redirect
# render를 통해 html 파일을 화면에 보여줌
from .models import UserModel
from django.http import HttpResponse

from django.contrib.auth import get_user_model
# 사용자가 데이터베이스 안에 있는지 검사하는 함수

from django.contrib import auth

from django.contrib.auth.decorators import login_required


# Create your views here.
# 각각에 맞는 html 파일을 연결해주는 함수 생성
def sign_up_view(request):
    if request.method == "GET":
        user = request.user.is_authenticated
        if user:
            return redirect("/")
        else:
            return render(request, 'user/signup.html')

    elif request.method == "POST":
        username = request.POST.get('username', None)
        # request.POST : POST로 온 데이터를 받는 방식
        # .get('username', None) : 그 중 username으로 되어있는 데이터 가져와
        # 데이터가 없다면 None(빈칸)으로 처리
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        bio = request.POST.get('bio', None)


        if password != password2:
            return render(request, 'user/signup.html')
        else:
            exist_user = get_user_model().objects.filter(username=username)
            # exist_user = UserModel.objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html')
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                # 아래 다섯줄 코드를 위의 한줄로!
                # new_user = UserModel()
                # new_user.username = username
                # new_user.password = password
                # new_user.bio = bio
                # new_user.save()

        return redirect('/sign-in')



def sign_in_view(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        me = auth.authenticate(request, username=username, password=password)
        # me = UserModel.objects.get(username = username)
        # 우리가 작성했던 유저모델은 이미 데이터베이스와 연결되어 있는 객체
        # (username = username) 왼쪽의 username : 유저모델 안에 있던 username

        # if me.password == password:
        if me is not None:
            # request.session['user'] = me.username
            auth.login(request, me)
            return redirect("/")
        else:
            return redirect("/sign-in")

    elif request.method == "GET":
        user = request.user.is_authenticated
        if user:
            return redirect("/")
        else:
            return render(request, 'user/signin.html')

@login_required # 사용자가 로그인이 되어있어야만 접근이 가능한 함수
def logout(request):
    auth.logout(request)
    return redirect("/")


# user/views.py
@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')