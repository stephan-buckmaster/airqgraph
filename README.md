Known for its ease of use and simplicity, Python is one of the most beloved general-purpose programming languages. And GraphQL, a declarative query language for APIs and server runtimes, pairs quite nicely with Python. Unfortunately, there are very few comprehensive learning materials out there that give you a step-by-step breakdown of how to use GraphQL with Python.

This repo has the code of [this article](https://www.apollographql.com/blog/complete-api-guide) which goes over everything you need to know to get up and running with GraphQL API using Python, Flask, and Ariadne.

Here we use .env for managing database credentials (which is git-ignored). Create an entry in file called .env
 in the root directory as below. Of course, change localhost and port as needed.

```
DATABASE_URI='postgresql://sample_user:samplepwd@localhost:5432/sample_db'
```

# Additional Installation Steps

This repo has a requirements.txt. As usual, install packages with

```
pip install -r requirements.txt
```

For psycop2 (python driver for PostgreSQL), may need to first install :

```
sudo apt install libpq-dev python3-dev
```

# Differences to the tutorial

To create all tables (which is the post table), run this command in shell

```
python create_db_tables.py
```
