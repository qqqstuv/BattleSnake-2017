# battlesnake-python

A simple [BattleSnake AI](http://battlesnake.io) written in Python. 

Visit [battlesnake.io/readme](http://battlesnake.io/readme) for API documentation and instructions for running your AI.

This AI client uses the [bottle web framework](http://bottlepy.org/docs/dev/index.html) to serve requests and the [gunicorn web server](http://gunicorn.org/) for running bottle on Heroku. Dependencies are listed in [requirements.txt](requirements.txt).

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

This idea is inspired from [Game Programming](http://theory.stanford.edu/~amitp/GameProgramming/)

#### Algorithms used:
* BFS: calculate if the snake is likely to be cornered in x move
* Dijkstra: calculate if the snake is likely to be cornered, taken surrounding weights into consideration
* A*: calculate the shortest path to a point, taken surrounding weights into consideration

#### The approach: The snake will make a move based on the intention: get food, trap a snake, or safe move
* Get food gets the closest food and run A* to find a path to get there
* Trap a snake runs BFS and Dijkstra to see if a snake is trapped then find a path to get there to block their exit
* Safe move: do Dijkstra from our head, approximate a safe point and navigate there

The kind of moves the snake will make take into account the number of snakes on the board and levels of food

#### You will need...

* a working Python 2.7 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
* experience [deploying Python apps to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies

## Running the Snake Locally

1) [Fork this repo](https://github.com/sendwithus/battlesnake-python/fork).

2) Clone repo to your development environment:
```
git clone git@github.com:username/battlesnake-python.git
```

3) Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html):
```
pip install -r requirements.txt
```

4) Run local server:
```
python app/main.py
```

5) Test client in your browser: [http://localhost:8080](http://localhost:8080).

## Deploying to Heroku

1) Create a new Heroku app:
```
heroku create [APP_NAME]
```

2) Deploy code to Heroku servers:
```
git push heroku master
```

3) Open Heroku app in browser:
```
heroku open
```
or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4) View server logs with the `heroku logs` command:
```
heroku logs --tail
```

## Questions?

Email [battlesnake@sendwithus.com](mailto:battlesnake@sendwithus.com), or tweet [@send_with_us](http://twitter.com/send_with_us).
