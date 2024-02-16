import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_username = os.environ['DB_USER']
        self.database_password = os.environ['DB_PASSWORD']
        self.db_host = os.environ['DB_HOST']
        self.db_port = os.environ['DB_PORT']
        self.database_path = f"postgresql://{self.database_username}:{self.database_password}@{self.db_host}:{self.db_port}/{self.database_name}"
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
    Write at least one test for each test for successful operation and for expected errors.
    """
    # GET /categories
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["categories"], {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        })

    def test_get_categories_fail(self):
        res = self.client().get("/categories/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not found")

    # GET /questions
    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"],
            [{'answer': 'Muhammad Ali', 'category': 4, 'difficulty': 1, 'id': 9, 'question': "What boxer's original name is Cassius Clay?"}, 
             {'answer': 'Tom Cruise', 'category': 5, 'difficulty': 4, 'id': 4, 'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?'}, 
             {'answer': 'Edward Scissorhands', 'category': 5, 'difficulty': 3, 'id': 6, 'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?'}, 
             {'answer': 'Brazil', 'category': 6, 'difficulty': 3, 'id': 10, 'question': 'Which is the only team to play in every soccer World Cup tournament?'}, 
             {'answer': 'Uruguay', 'category': 6, 'difficulty': 4, 'id': 11, 'question': 'Which country won the first ever soccer World Cup in 1930?'}, 
             {'answer': 'George Washington Carver', 'category': 4, 'difficulty': 2, 'id': 12, 'question': 'Who invented Peanut Butter?'}, 
             {'answer': 'Lake Victoria', 'category': 3, 'difficulty': 2, 'id': 13, 'question': 'What is the largest lake in Africa?'}, 
             {'answer': 'The Palace of Versailles', 'category': 3, 'difficulty': 3, 'id': 14, 'question': 'In which royal palace would you find the Hall of Mirrors?'}, 
             {'answer': 'Agra', 'category': 3, 'difficulty': 2, 'id': 15, 'question': 'The Taj Mahal is located in which Indian city?'}, 
             {'answer': 'Escher', 'category': 2, 'difficulty': 1, 'id': 16, 'question': 'Which Dutch graphic artist–initials M C was a creator of optical illusions?'}])
        self.assertEqual(len(data["questions"]), 10)
        self.assertEqual(data["categories"], {
            '1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'
        })

    def test_get_questions_by_page(self):
        res = self.client().get("/questions?page=2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["categories"], {
            '1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'
        })

    def test_get_questions_fail(self):
        res = self.client().get("/questions?page=100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not found")

    # DELETE /questions/<int:question_id>
    def test_delete_question(self):
        res = self.client().delete("/questions/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_delete_question_fail(self):
        res = self.client().delete("/questions/100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable entity")


    # POST /questions
    def test_post_question(self):
        res = self.client().post("/questions", json={
            "question": "Test question",
            "answer": "Test answer",
            "difficulty": 1,
            "category": 1
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["message"], "Question successfully created")
        self.assertTrue(data["success"])
    
    def test_post_question_fail(self):
        res = self.client().post("/questions", json={
            "question": "Test question",
            "answer": "Test answer",
            "difficulty": 1,
            "category": None
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable entity")

    # POST /questions/search
    def test_search_questions(self):
        res = self.client().post("/questions/search", json={
            "searchTerm": "Test"
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
    
    def test_search_questions_fail(self):
        res = self.client().post("/questions/search", json={
            "searchTerm": "alskdjaskdjlas"
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not found")

    # GET /categories/<int:category_id>/questions
    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])

    def test_get_questions_by_category_fail(self):
        res = self.client().get("/categories/100/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not found")

    # POST /quizzes
    def test_get_quiz_question(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": {
                "id": 0,
                "type": "All"
            }
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["question"])

    def test_get_quiz_question_fail(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": {
                "id": 1000,
                "type": "All"
            }
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()