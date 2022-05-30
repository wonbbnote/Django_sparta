from django.shortcuts import render, redirect
from .models import TweetModel
from django.contrib.auth.decorators import login_required
from .models import TweetComment

# Create your views here.
def home(request):
    user = request.user.is_authenticated
    # 유저가 로그인되어있는지 확인
    if user:  # 로그인 되어있으면 /tweet이라는 url로 연결
        return redirect("/tweet")
    else:     # 로그인 안되어있으면 로그인 url로 연결
        return redirect("/sign-in")


# tweet/home.html 화면을 보여주는 함수
# render() : html를 보여주는 함수
def tweet(request):
    if request.method == "GET":
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by("-created_at")
            # TweetModel에 저장한 모든 데이터를 불러오겠다 (최신순으로!)
            return render(request, "tweet/home.html", {"tweet": all_tweet})
        else:
            return redirect("/sign-in")

    elif request.method =="POST":
        user = request.user
        my_tweet = TweetModel()
        my_tweet.author=user
        my_tweet.content = request.POST.get("my-content", "")
        my_tweet.save()
        return redirect("/tweet")


@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect("/tweet")


@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, "tweet/tweet_detail.html", {'tweet': my_tweet, 'comment': tweet_comment})


@login_required
def write_comment(request,id):
    if request.method=="POST":
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect("/tweet/"+str(id))

@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id = id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect("/tweet/"+str(current_tweet))






