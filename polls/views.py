from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from django.db.models import F


from django.http import Http404
#from django.template import loader

from .models import Question, Choice


# Using generic views for index, detail and results
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions. Excluding future one and questions without choices"""
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
        ).exclude(choice=None).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).exclude(choice=None)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).exclude(choice=None)


'''
# Using our own code views
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    #return HttpResponse(render(context, request))
    return render(request,'polls/index.html',context)

def detail(request, question_id):
    #try:
    #    question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question': question})
'''


def vote(request, question_id):
    #question = get_object_or_404(Question, pk=question_id)
    question = get_object_or_404(Question, pk=question_id, pub_date__lte=timezone.now())
    if question.choice_set.count() == 0:
        raise Http404("Question does not have choices")
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        #Potential race condition
        #selected_choice.votes += 1
        #selected_choice.save()

        #Votes updated avoiding race condition using F()
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        #or selected_choice.update(votes=F('votes') + 1)

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
