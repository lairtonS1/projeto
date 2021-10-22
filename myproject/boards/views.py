from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from boards.models import Board, User, Topic, Post
from django.http import Http404
from . import forms


# Create your views here.

def home (request):
    response = Board.objetos.all()
    return render(request, "home.html", {"response": response})

@login_required(login_url='login')
def board_topics(request, board_id):
    try:
        board = Board.objetos.get(id=board_id)
    except Board.DoesNotExist:
        raise Http404
    return render(request, "board_topics.html", {"board": board})

@login_required(login_url='login')
def new_topic(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = forms.NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objetos.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', board_id=board.id)  # TODO: redirect to the created topic page
    else:
        form = forms.NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

@login_required(login_url='login')
def topic_posts(request,id,topics_id):
    topic = get_object_or_404(Topic, board__id=id, id=topics_id)
    return render (request, 'topic_posts.html',{'topic':topic})
