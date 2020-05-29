from django.shortcuts import render, redirect
from .models import DiaryPost
from .forms import DiaryPostForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import markdown
# Create your views here.



@login_required(login_url='/accounts/login/')
def diary_list(request):
    superuser = User.objects.get(is_superuser=True)
    if request.user != superuser:
        return HttpResponse("抱歉，权限不够。")
    search = request.GET.get('search')
    diary_list = DiaryPost.objects.all()

    # # 搜索查询集
    if search:
        diary_list = diary_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    paginator = Paginator(diary_list, 10)
    page = request.GET.get('page')
    diaries = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'diaries': diaries,
        'search': search,
    }

    return render(request, 'diary/list.html', context)


@login_required(login_url='/accounts/login/')
def diary_detail(request, id):
    superuser = User.objects.get(is_superuser=True)
    if request.user != superuser:
        return HttpResponse("抱歉，权限不够。")
    diary = DiaryPost.objects.get(id=id)
    diary.body = markdown.markdown(diary.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])

    context = {'diary': diary }
    return render(request, 'diary/detail.html', context)


@login_required(login_url='/accounts/login/')
def diary_create(request):
    superuser = User.objects.get(is_superuser=True)
    if request.user != superuser:
        return HttpResponse("抱歉，权限不够。")
    if request.method == "POST":
        diary_post_form = DiaryPostForm(data=request.POST)
        if diary_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_diary = diary_post_form.save(commit=False)
            new_diary.author = User.objects.get(id=request.user.id)
            new_diary.save()
            return redirect("diary:diary_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        diary_post_form = DiaryPostForm()
        context = {'diary_post_form': diary_post_form}
        return render(request, 'diary/create.html', context)


@login_required(login_url='/accounts/login/')
def diary_safe_delete(request, id):
    if request.method == 'POST':
        diary = DiaryPost.objects.get(id=id)
        # 过滤非作者的用户
        if request.user != diary.author:
            return HttpResponse("抱歉，你无权修改。")
        diary.delete()
        return redirect("diary:diary_list")
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/accounts/login/')
def diary_update(request, id):
    diary = DiaryPost.objects.get(id=id)
    if request.user != diary.author:
        return HttpResponse("抱歉，你无权修改。")
    if request.method == "POST":
        diary_post_form = DiaryPostForm(data=request.POST)
        if diary_post_form.is_valid():

            diary.title = request.POST['title']
            diary.body = request.POST['body']
            if request.POST['created']:
                diary.created = request.POST['created']
            diary.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("diary:diary_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        context = {'diary': diary}
        return render(request, 'diary/update.html', context)