from django.shortcuts import render, get_object_or_404
from boards.models import Board
from django.http import  Http404
# Create your views here.


def home(request):
    response = Board.objetos.all()
    return render(request, "home.html", {"response": response})
    
def board_topics(request, board_id):
    try:
        board = Board.objetos.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404
    return render(request, "board_topics.html", {"board":board})

def new_topic (request, board_id):
    board = get_object_or_404(Board, id=board_id)
    return render(request, "new_topic.html", {'board' : board    })
    