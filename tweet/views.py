from django.shortcuts import render, redirect
from .models import TweetModel
from django.contrib.auth.decorators import login_required
from .models import TweetComment
from django.views.generic import ListView, TemplateView


# Create your views here.
def home(request):
    user = request.user.is_authenticated
    # 유저가 로그인되어있는지 확인
    if user:  # 로그인 되어있으면 /tweet이라는 url로 연결
        return redirect("/tweet")
    else:  # 로그인 안되어있으면 로그인 url로 연결
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

    elif request.method == "POST":
        user = request.user
        content = request.POST.get("my-content", '')
        tags = request.POST.get("tag", '').split(",")
        if content == '':
            all_tweet = TweetModel.objects.all().order_by("-created_at")
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    my_tweet.tags.add(tag)
            # my_tweet = TweetModel()
            # my_tweet.author=user
            # my_tweet.content = request.POST.get("my-content", "")
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
def write_comment(request, id):
    if request.method == "POST":
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect("/tweet/" + str(id))


@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect("/tweet/" + str(current_tweet))

# 장고 taggit 공식웹사이트에서 제공하는 공식문서대로 작성
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
