from django.test import TestCase
from django.urls import reverse, resolve
from ..views import home,board_topics, new_topic
from django.contrib.auth.models import User
from ..models import  Board, Topic, Post
from ..forms import NewTopicForm

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
    def test_board_topics_view_contains_links_navigation(self):
        board_topics_url = reverse('board_topics', kwargs={'board_id': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'board_id':1})
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response,'href="{0}"'.format(new_topic_url))

class NewTopicsTest(TestCase):
    def setUp(self):
        Board.objetos.create(name='Django', description="Apredendo Django")
        User.objects.create_user(username="Lairton", email="lairtons2000@gmail.com", password="123")
    def test_new_topic_sucess_status_code(self):
        new_topic_url = reverse('new_topic', kwargs={'board_id':1})
        response = self.client.get(new_topic_url)
        self.assertEquals(response.status_code, 200)
    def test_new_topic_view_not_found_status_code(self):
        new_topic_url = reverse('new_topic', kwargs={'board_id':99})
        response = self.client.get(new_topic_url)
        self.assertEquals(response.status_code, 404)
 
    def test_new_topic_url_resolves_new_topic_view(self):
        View = resolve('/board/1/new/')
        self.assertEquals(View.func, new_topic)
    def test_new_topic_view_contain_link_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'board_id':1})
        board_topics_url = reverse('board_topics', kwargs={'board_id':1})
        response = self.client.get(new_topic_url)
        self.assertContains(response,'href="{0}"'.format(board_topics_url))
      
    def test_csrf(self):
        url = reverse('new_topic', kwargs={'board_id':1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'board_id':1})
        data = {
            'subject': "Test title",
            'message': "testando titulo",
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objetos.exists())
        self.assertTrue(Post.objetos.exists())
    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('new_topic', kwargs={'board_id':1})
        data= {'subject':"", 'message':"" }
        response = self.client.post(url,data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objetos.exists())
        self.assertFalse(Post.objetos.exists())
       
    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'board_id':1})
        response= self.client.post(url,{})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
    def test_contains_form(self):  # <- new test
        url = reverse('new_topic', kwargs={'board_id':1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)
