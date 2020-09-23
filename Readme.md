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
- Send all available categories in which the keys are the ids and the value is the corresponding string of the category
- It returns the available categories sorted by category name
```

```
GET `/questions`
- Send all questions ordered by id
- Returned questions are limited to 10 questions per page
- `page` is a url argument to determine the required page, i.e. `/questions?page=2` returns the second page of questions (Q11-Q20)
```

```
DELETE `/questions/id`
- Delete question with its id
- Retreive all remaining questions and send back first page of questions
```

```
POST `/questions`
- Add a new question to the list including its answer, difficulty, and category
```

```
POST `/questions/search`
- It searchs within the questions for specific keyword and case insinsitive
- It uses `searchTerm` from the main page
```

```
GET `/categories/id/questions`
- Retreive all questions for a specific category based on category id
```

```
POST `/quizzes`
- It's used to pick a random question and send for the play
- It receive in the message body a list of previous questions and the selected category
- Category will be 0 if required to play all categories
- It filters the question by the category then filter out the previous ones. After that it pick a random question and send it back
- If all questions in the selected category finished, then ends the game
```


## Testing
To run the tests, go to the backend folder and run
```
dropdb trivia_test
createdb trivia_test
psql -f trivia.psql trivia_test
python test_flaskr.py
```

