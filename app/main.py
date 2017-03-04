import bottle,os,random
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
    direction = helper.handler(data.get('you'), data.get('snakes'), data.get('food'))
    end = timer()
    print "TOTAL RESPONSE TIME: %.1f" % ((end - start) * 1000)
    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
