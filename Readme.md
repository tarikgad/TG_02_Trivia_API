# Full Stack API Final Project


[Rubic](https://review.udacity.com/#!/rubrics/2634/view)

[Main github](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter)


## Tasks

Follow these steps in order to start the application:

1. Prepre the backend
    
    a. [Installe python](https://www.python.org/downloads) & [install PostgreSQL](https://www.postgresql.org/download)
    
    b. go to backend folder and run `pip install -r requirements.txt` to install the required packages
    
    c. run these commands to prepare the database
    ```
    dropdb trivia
    createdb trivia
    psql -f trivia.psql trivia
    ```
    
    d. run `flask run` to start the frontend page
    
    e. access it from http://localhost:5000. You can change it in `.flaskenv` for flask options


2. Prepare the frontend
    
    a. [Installe Node and NPM](https://nodejs.com/en/download)
    
    b. go to frontend folder and run `npm install` to setup the required packages
    
    c. run `npm start` to start the frontend page
    
    d. access it from http://localhost:5000, as indicated in `package.json`



## REVIEW_COMMENT
```
Example for endpoint to get all categories:

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql -f trivia.psql trivia_test
python test_flaskr.py
```

