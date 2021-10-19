from django.test import TestCase
from django.urls import reverse, resolve
from .views import home,board_topics
from .models import  Board

class HomeTest(TestCase):
    
    def setUp(self):
        self.board = Board.objetos.create(name="Django", description="Apredendo django")
        url = reverse('home')
        self.response = self.client.get(url)
        
    def test_home_view_status_code(self):
        url = reverse ('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def test_home_view_contain_link_topic_page(self):
        board_topics_url = reverse('board_topics', kwargs={'board_id' : self.board.id})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
        
    def test_home_url_resolves_home_view(self):
        View = resolve("/")
        self.assertEquals(View.func, home)


class BoardTopicsTest(TestCase):
    #instanciado Board para usar no teste
    def setUp (self):
        Board.objetos.create(name='Java Script',  description = 'Aprendendo java Script')
    #teste para verificar o status do metodo get realizado pelo usuario com valor True
    def test_board_topics_sucess_status_code(self):
        url = reverse ("board_topics", kwargs={'board_id':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code,  200)
     #teste para verificar o status do metodo get para resultado 404
    def test_board_topics_view_not_found_status_code(self):
        url = reverse ("board_topics", kwargs={'board_id':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
   #teste para verificar se a url esta direcionando para a view certa
    def test_board_topics_url_resolves_board_topics_view(self):
        View = resolve('/board/1/')
        self.assertEquals(View.func, board_topics)
    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'board_id': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))