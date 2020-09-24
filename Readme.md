# Full Stack API Final Project


[Rubic](https://review.udacity.com/#!/rubrics/2634/view)

[Main github](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter)


## Tasks

Follow these steps in order to start the application:

1. Prepre the backend
    
    a. [Installe python](https://www.python.org/downloads) & [PostgreSQL](https://www.postgresql.org/download)
    
    b. go to backend folder and run `pip install -r requirements.txt` to install the required packages
    
    c. run these commands to prepare the database
    ```
    dropdb trivia
    createdb trivia
    psql -f trivia.psql trivia
    ```
    
    d. Update `USER_NAME` & `PASSWORD` in `.env` for the database `username` and `password` respectievly


2. Prepare the frontend
    
    a. [Installe Node.js and NPM](https://nodejs.com/en/download)
    
    b. go to frontend folder and run `npm install` to setup the required packages


3. Run the app
    
    a. In the backend folder run `flask run`
    
    b. In the frontend folder run `npm start`

    c. The application will be accessable from http://localhost:3000


## REVIEW_COMMENT
```
GET `/categories`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs sorted by the category name.
['2': "Art",
'5': "Entertainment",
'3': "Geography",
'4': "History",
'1': "Science",
'6': "Sports"]
```

```
GET `/questions`
- Fetches a list of question and format it in pages where each page has 10 questions
- Request Arguments: page
- Returns: a list of 10 questions ordered by id and all the categories in a dictionary
questions
    [{'id': 1, 'question': 'what's the name?', 'answer': 'identifier', 'category': 5, 'difficulty': 1}]
categories
    {'2': 'Art'}
```

```
DELETE `/questions/id`
- Fetches the question with the provided id to delete it
- Request Arguments: None
- Returns: a list of 10 questions ordered by id and the id of the deleted question
questions
    [{'id': 1, 'question': 'what's the name?', 'answer': 'identifier', 'category': 5, 'difficulty': 1}]
```

```
POST `/questions`
- Fetches: None
- Body Arguments: new question items (question, answer, category, difficulty)
- Returns: a list of 10 questions ordered by id and the id of the new question
questions
    [{'id': 1, 'question': 'what's the name?', 'answer': 'identifier', 'category': 5, 'difficulty': 1}]
```

```
POST `/questions/search`
- Fetches all questions and searches within the question element for the searchTerm after minimizing both of them
- Body Arguments: searchTerm
- Returns: a list of 10 questions with the matched criteria ordered by id and the total amount of these questions
questions
    [{'id': 1, 'question': 'what's the name?', 'answer': 'identifier', 'category': 5, 'difficulty': 1}]
```

```
GET `/categories/<id>/questions`
- Fetches all questions for a specific category <id>
- Arguments: None
- Returns: a list of 10 questions for the requested category
questions
    [{'id': 1, 'question': 'what's the name?', 'answer': 'identifier', 'category': 5, 'difficulty': 1}]
```

```
POST `/quizzes`
- Fetches all questions of required category, assuming "All" had ID 0. Then remove the previous played of the list then pick a random one to play
- Body Arguments: a list of previous questions IDs and a disctionary for quiz category to play
previous_questions
    [1, 2]
quiz_category
    {'id': 2, 'type': 'Art'}
- Returns: one question to play and indication to end the game if all questions finished
question
    {'id': 1, 'question': 'what's the name?', 'answer': 'identifier', 'category': 5, 'difficulty': 1}
forceEnd
    False
```


## Testing
To run the tests, go to the backend folder and run
```
dropdb trivia_test
createdb trivia_test
psql -f trivia.psql trivia_test
python test_flaskr.py
```

