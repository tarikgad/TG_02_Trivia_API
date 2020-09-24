import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.user_name = os.environ.get('USER_NAME')
        self.admin_pass = os.environ.get('PASSWORD')
        self.database_path = "postgres://{}:{}@{}/{}".format(self.user_name, self.admin_pass, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertEqual(len(data['categories']),data['total_categories'])


    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['questions']),10)

        
    def test_get_error_paginated_questions(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')
    

    def test_delete_questions(self):
        id = Question.query.first().id
        res = self.client().delete('/questions/'+str(id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'],id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])


    def test_delete_error_questions(self):
        res = self.client().delete('/questions/0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')


    def test_post_add_questions(self):
        res = self.client().post('/questions', json={'question': 'a new question', 'answer': 'its answer', 'difficulty': 1, 'category': 3})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])


    def test_post_error_add_questions(self):
        res = self.client().post('/questions', json={'question': 'a new question', 'answer': 'its answer', 'difficulty': 1, 'category': 10})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')


    def test_post_search_questions(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'a'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])


    def test_post_error_search_questions(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'car'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['total_questions'])


    def test_get_categorized_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])


    def test_get_error_categorized_questions(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')


    def test_post_play(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['forceEnd'])
        self.assertTrue(data['question'])


    def test_post_error_play(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 10}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()