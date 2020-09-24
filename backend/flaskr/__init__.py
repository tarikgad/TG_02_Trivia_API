import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,text
from flask_cors import CORS
import random

from models import *

QUESTIONS_PER_PAGE = 10

def paginate(request, selection):
  category = request.args.get('page', 1, type=int)
  start =  (category - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  categories = [category.format() for category in selection]
  current_categories = categories[start:end]

  return current_categories

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  # GET /categories used to list all available categories
  @app.route('/categories')
  def retrieve_categories():
    selection = Category.query.order_by(Category.type).all()
    current_selections = [category.format() for category in selection]

    if len(current_selections) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': current_selections,
      'total_categories': len(Category.query.all()),
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  # GET /questions?page=2 retreive questions in page 2
  @app.route('/questions')
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_qustions = paginate(request, selection)

    if len(current_qustions) == 0:
      abort(404)
      
    data = Category.query.order_by(Category.type).all()
    d = {x.id:x.type for x in data}
    
    return jsonify({
      'success': True,
      'questions': current_qustions,
      'total_questions': len(Question.query.all()),
      'categories': d
    })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  # DELETE /questions/1 used to delete question with id_1
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      # if no question with this id, then abort
      if question is None:
        abort(404)

      question.delete()
      
      # after deleting the question, retreive all remaining questions and send page-1
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  # POST /questions used to add a new question
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate(request, selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # POST /questions/search used to search with the questions for specific keyword and case insinsitive
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    x = request.get_json('searchTerm')['searchTerm']
    # search within the question field for the searchTerm in lowercase to make sure both in same ascii level
    Q_search = Question.query.filter(func.lower(Question.question).contains(func.lower(x))).all()
    
    Qs = [q.format() for q in Q_search]
    
    return jsonify({
      'questions': Qs,
      'total_questions': len(Qs)
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  # GET /categories/id/questions used to retreive all questions for a specific category
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category(category_id):
    selection = Question.query.filter_by(category=category_id).order_by(Question.id).all()
    current_qustions = paginate(request, selection)

    if len(current_qustions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_qustions,
      'current_category': [],
      'total_questions': len(Question.query.filter_by(category=category_id).all())
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  # POST /quizzes used to pick a random question of specific category, or all categories, and not picked before
  @app.route('/quizzes', methods=['POST'])
  def play_quizzes():
    pre_Questions = request.get_json('previous_questions')['previous_questions'] #list of last questions
    Q_category = request.get_json('quiz_category')['quiz_category']['id'] #category id. It will be 0 for all categories
    
    # retrieve all questions in the selected category
    if Q_category == 0:
      all_Q = Question.query.all()
    else:
      all_Q = Question.query.filter_by(category=Q_category).all()
    
    # list of all questions' IDs in the selected category
    data=[x.id for x in all_Q]
    
    # remove the previous questions' IDs from the in-scope IDs
    for x in pre_Questions:
      data.remove(x)
    
    # if all questions in the selected category finished, then force ending
    if len(data) > 0:
      new_Q = random.choice(data)
      question = Question.query.filter_by(id=new_Q).first().format()
      forceEnd = False
    else:
      question = True
      forceEnd = True
    
    return jsonify({
      'question': question,
      'forceEnd': forceEnd
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not Found"
        }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method Not Allowed"
        }), 405

  @app.errorhandler(406)
  def not_acceptable(error):
    return jsonify({
        "success": False, 
        "error": 406,
        "message": "Not Acceptable"
        }), 406
  @app.errorhandler(408)
  def request_timeout(error):
    return jsonify({
        "success": False, 
        "error": 408,
        "message": "Request Timeout"
        }), 408

  @app.errorhandler(414)
  def request_uri_too_long(error):
    return jsonify({
        "success": False, 
        "error": 414,
        "message": "Request URI Too Long"
        }), 414

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal Server Error"
        }), 500

  @app.errorhandler(503)
  def service_unavailable_error(error):
      return jsonify({
        "success": False, 
        "error": 503,
        "message": "Service Unavailable Error"
        }), 503


  return app
