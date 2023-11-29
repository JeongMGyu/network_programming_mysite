from django.shortcuts import get_object_or_404, render
from polls.models import Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
# Create your views here.

class IndexView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class VoteView(DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(DetailView):
    model = Question
    template_name = 'polls/results.html'



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 설문 투표 폼을 다시 보여 준다
        return render(request, 'polls/detail.html',{'question': question,
                                                    'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # POST 데이터를 정상적으로 처리하였으면, 항상 HttpResponseRedirect를 반환하여 리다이렉션 처리함
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
