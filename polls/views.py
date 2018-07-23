from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.

"""
# 被通用视图替代
def index(request):
    # return HttpResponse("Hello world! You are at the polls index")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    # 载入 polls/index.html 模板文件，并且向它传递一个上下文(context)
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))

    # 快捷函数：render()，不再需要导入 loader 和 HttpResponse
    '''The render() function takes the request object as its first argument, 
    a template name as its second argument 
    and a dictionary as its optional third argument. 
    It returns an HttpResponse object of the given template 
    rendered with the given context.'''
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# 投票详情视图
def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id)
    # 抛出 404 错误
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})

    # 快捷函数： get_object_or_404()
    '''The get_object_or_404() function takes a Django model as its first argument
    and an arbitrary number of keyword arguments, which it passes to
    the get() function of the model's manager.
    It raises Http404 if the object doesn't exist.'''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)

    # 处理投票
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice'] 以字符串形式返回选择的 Choice 的 ID,request.POST的值永远是字符串
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # HttpResponseRedirect 只接收一个参数：用户将要被重定向的 URL
        # 使用reverse() 函数避免了在视图函数中硬编码 URL
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
"""


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]

        # 改进 get_queryset() 方法，
        # 通过将Question的pub_data属性与timezone.now()相比较来判断是否应该显示未来的Question
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        '''
        Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset 
        containing Questions whose pub_date is less than or 
        equal to - that is, earlier than or equal to - timezone.now.
        '''
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    # 问题详情页增加对问题发布时间的约束
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)

    # 处理投票
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice'] 以字符串形式返回选择的 Choice 的 ID,request.POST的值永远是字符串
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # HttpResponseRedirect 只接收一个参数：用户将要被重定向的 URL
        # 使用reverse() 函数避免了在视图函数中硬编码 URL
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))