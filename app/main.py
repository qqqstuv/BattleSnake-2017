import bottle,os
from timeit import default_timer as timer
import helper,settings

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']
    settings.initializeMap(board_width, board_height) #set global map size
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'Desafinado'
    }


@bottle.post('/move')
def move():
    start = timer()
    data = bottle.request.json
    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']
    helper.possibleMove(None, data.get('snakes'))

    end = timer()
    print "TIME TO RESPONSE: %.6f" % (end - start)
    return {
        'move': 'up',
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
