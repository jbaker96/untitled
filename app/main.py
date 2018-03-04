import bottle
import os
import random
import json

@bottle.route('/')
def static():
    return "we in this"

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.post('/start')
def start():
    return {
        'color': 'black',
        'head_url': 'https://upload.wikimedia.org/wikipedia/en/3/31/BruceBorn1984.JPG',
        'head_type': 'tongue',
        'tail_type': 'curled',
        'taunt': 'Who wants to stare at a computer for the rest of their lives?',
    }

def FindTail(a, walls, checked, tail):
    
    if a == tail:
        return True
    if a in walls:
        return False
    if a in checked:
        return False
    checked.extend([a])

    tailX = tail[0] - a[0]
    tailY = tail[1] - a[1]
    headU = [0, -1]
    headD = [0, 1]
    headL = [-1, 0]
    headR = [1, 0]

    if abs(tailX) >= abs(tailY):
        if tailX > 0:
            first = headR
            if tailY >= 0:
                second = headD
                third = headU
                last = headL
            else:
                second = headU
                third = headD
                last = headL
        else:
            first = headL
            if tailY >= 0:
                second = headD
                third = headU
                last = headR
            else:
                second = headU
                third = headD
                last = headR
    else:
        if tailY > 0:
            first = headD
            if tailX >= 0:
                second = headR
                third = headL
                last = headU
            else:
                second = headL
                third = headR
                last = headU
        else:
            first = headU
            if tailX >= 0:
                second = headR
                third = headL
                last = headD
            else:
                second = headL
                third = headR
                last = headD

    if (FindTail([a[0] + first[0], a[1] + first[1]], walls, checked, tail)) == True:
        return True
    if (FindTail([a[0] + second[0], a[1] + second[1]], walls, checked, tail)) == True:
        return True
    if (FindTail([a[0] + third[0], a[1] + third[1]], walls, checked, tail)) == True:
        return True
    if (FindTail([a[0] + last[0], a[1] + last[1]], walls, checked, tail)) == True:
        return True
    return False



@bottle.post('/move')
def move():
    data = bottle.request.json
    snakes = bottle.request.json[u'snakes']
    height = data['height'] - 1
    width = data['width'] - 1
    
    player_body = data['you']['body']['data']
    my_size = len(player_body)
    numenemy = len(data['snakes']['data'])
    if numenemy == 2:
        cutoff = 105
    elif numenemy == 3:
        cutoff = 75
    elif numenemy == 4:
        cutoff = 50
    else:
        cutoff = (height + width)

    boardsize = (height+1)*(width+1)
    invperctosafe = 2
    optisize = boardsize/invperctosafe
    walls = []                                                                                 #CREATING WALLS ARRAY
    
    h = 0
    w = 0
    h1 = 0
    w1 = 0
    q = 1
    p = 1
    
    while (h < data['height']):
        a = [[-1, h]]
        walls.extend(a)
        h = h + 1
    
    while (w < data['width']):
        a = [[w, -1]]
        walls.extend(a)
        w = w + 1
    
    while (h1 < data['height']):
        a = [[data['width'], h1]]
        walls.extend(a)
        h1 = h1 + 1
    
    while (w1 < data['width']):
        a = [[w1, data['height']]]
        walls.extend(a)
        w1 = w1 + 1

    playerLocation = data['you']['body']['data']
    if data['you']['health'] == 100:
        q = 0
    for i in range(len(playerLocation)-q):
        a = [[playerLocation[i]['x'], playerLocation[i]['y']]]
        walls.extend(a)


    enemiesLocation = data['snakes']['data']
    for i in range(len(enemiesLocation)):
        snake = data['snakes']['data'][i]['body']['data']
        if data['snakes']['data'][i]['health'] == 100:
            p = 0
        for j in range(len(snake) - p):
            
            a = [[snake[j]['x'], snake[j]['y']]]
            walls.extend(a)
            p = 1

    tail = [playerLocation[len(playerLocation)-1]['x'], playerLocation[len(playerLocation)-1]['y']]
    head = [data['you']['body']['data'][0]['x'], data['you']['body']['data'][0]['y']]

    if my_size < 4:
        i = 0
        j = 0
        a = []
        checked = []
        
        while (i < len(data['food']['data'])):
            b = [[abs(data['food']['data'][i]['x'] - head[0]) + abs(data['food']['data'][i]['y'] - head[1]) , i]]
            a.extend(b)
            i = i + 1
        
        while (j < len(data['food']['data'])):
            minval = min(a)
            a.remove(minval)
            foodnum = minval[1]
            FoodX = data['food']['data'][foodnum]['x']
            FoodY = data['food']['data'][foodnum]['y']
            
            goalX = FoodX - head[0]
            goalY = FoodY - head[1]
            checked = []

            headU = [0, -1]
            headD = [0, 1]
            headL = [-1, 0]
            headR = [1, 0]

            if abs(goalX) >= abs(goalY):
                if goalX > 0:
                    first = headR
                    if goalY >= 0:
                        second = headD
                        third = headU
                        last = headL
                    else:
                        second = headU
                        third = headD
                        last = headL
                else:
                    first = headL
                    if goalY >= 0:
                        second = headD
                        third = headU
                        last = headR
                    else:
                        second = headU
                        third = headD
                        last = headR
            else:
                if goalY > 0:
                    first = headD
                    if goalX >= 0:
                        second = headR
                        third = headL
                        last = headU
                    else:
                        second = headL
                        third = headR
                        last = headU
                else:
                    first = headU
                    if goalX >= 0:
                        second = headR
                        third = headL
                        last = headD
                    else:
                        second = headL
                        third = headR
                        last = headD

            if FindTail([head[0] + first[0], head[1] + first[1]], walls, checked, tail) == True:
                if first == headU:
                    return {
                        'move': 'up'
                }
                if first == headD:
                    return {
                        'move': 'down'
                }
                if first == headL:
                    return {
                        'move': 'left'
                }
                if first == headR:
                    return {
                        'move': 'right'
                }

            if FindTail([head[0] + second[0], head[1] + second[1]], walls, checked, tail) == True:
                if second == headU:
                    return {
                        'move': 'up'
                }
                if second == headD:
                    return {
                        'move': 'down'
                }
                if second == headL:
                    return {
                        'move': 'left'
                }
                if second == headR:
                    return {
                        'move': 'right'
                }

            if FindTail([head[0] + third[0], head[1] + third[1]], walls, checked, tail) == True:
                if third == headU:
                    return {
                        'move': 'up'
                }
                if third == headD:
                    return {
                        'move': 'down'
                }
                if third == headL:
                    return {
                        'move': 'left'
                }
                if third == headR:
                    return {
                        'move': 'right'
                }

            if FindTail([head[0] + last[0], head[1] + last[1]], walls, checked, tail) == True:
                if last == headU:
                    return {
                        'move': 'up'
                }
                if last == headD:
                    return {
                        'move': 'down'
                }
                if last == headL:
                    return {
                        'move': 'left'
                }
                if last == headR:
                    return {
                        'move': 'right'
                }

            j = j + 1



    if data['you']['health'] >= cutoff:
        tailX = tail[0] - head[0]
        tailY = tail[1] - head[1]
        checked = []

        headU = [0, -1]
        headD = [0, 1]
        headL = [-1, 0]
        headR = [1, 0]

        if abs(tailX) >= abs(tailY):
            if tailX > 0:
                first = headR
                if tailY >= 0:
                    second = headD
                    third = headU
                    last = headL
                else:
                    second = headU
                    third = headD
                    last = headL
            else:
                first = headL
                if tailY >= 0:
                    second = headD
                    third = headU
                    last = headR
                else:
                    second = headU
                    third = headD
                    last = headR
        else:
            if tailY > 0:
                first = headD
                if tailX >= 0:
                    second = headR
                    third = headL
                    last = headU
                else:
                    second = headL
                    third = headR
                    last = headU
            else:
                first = headU
                if tailX >= 0:
                    second = headR
                    third = headL
                    last = headD
                else:
                    second = headL
                    third = headR
                    last = headD

        if FindTail([head[0] + first[0], head[1] + first[1]], walls, checked, tail) == True:
            if first == headU:
                return {
                    'move': 'up'
            }
            if first == headD:
                return {
                    'move': 'down'
            }
            if first == headL:
                return {
                    'move': 'left'
            }
            if first == headR:
                return {
                    'move': 'right'
            }

        if FindTail([head[0] + second[0], head[1] + second[1]], walls, checked, tail) == True:
            if second == headU:
                return {
                    'move': 'up'
            }
            if second == headD:
                return {
                    'move': 'down'
            }
            if second == headL:
                return {
                    'move': 'left'
            }
            if second == headR:
                return {
                    'move': 'right'
            }

        if FindTail([head[0] + third[0], head[1] + third[1]], walls, checked, tail) == True:
            if third == headU:
                return {
                    'move': 'up'
            }
            if third == headD:
                return {
                    'move': 'down'
            }
            if third == headL:
                return {
                    'move': 'left'
            }
            if third == headR:
                return {
                    'move': 'right'
            }

        if FindTail([head[0] + last[0], head[1] + last[1]], walls, checked, tail) == True:
            if last == headU:
                return {
                    'move': 'up'
            }
            if last == headD:
                return {
                    'move': 'down'
            }
            if last == headL:
                return {
                    'move': 'left'
            }
            if last == headR:
                return {
                    'move': 'right'
            }

    if data['you']['health'] < cutoff:        
        i = 0
        j = 0
        a = []
        checked = []
        
        while (i < len(data['food']['data'])):
            b = [[abs(data['food']['data'][i]['x'] - head[0]) + abs(data['food']['data'][i]['y'] - head[1]) , i]]
            a.extend(b)
            i = i + 1
        
        while (j < len(data['food']['data'])):
            minval = min(a)
            a.remove(minval)
            foodnum = minval[1]
            FoodX = data['food']['data'][foodnum]['x']
            FoodY = data['food']['data'][foodnum]['y']
            
            goalX = FoodX - head[0]
            goalY = FoodY - head[1]
            checked = []

            headU = [0, -1]
            headD = [0, 1]
            headL = [-1, 0]
            headR = [1, 0]

            if abs(goalX) >= abs(goalY):
                if goalX > 0:
                    first = headR
                    if goalY >= 0:
                        second = headD
                        third = headU
                        last = headL
                    else:
                        second = headU
                        third = headD
                        last = headL
                else:
                    first = headL
                    if goalY >= 0:
                        second = headD
                        third = headU
                        last = headR
                    else:
                        second = headU
                        third = headD
                        last = headR
            else:
                if goalY > 0:
                    first = headD
                    if goalX >= 0:
                        second = headR
                        third = headL
                        last = headU
                    else:
                        second = headL
                        third = headR
                        last = headU
                else:
                    first = headU
                    if goalX >= 0:
                        second = headR
                        third = headL
                        last = headD
                    else:
                        second = headL
                        third = headR
                        last = headD

            if FindTail([head[0] + first[0], head[1] + first[1]], walls, checked, tail) == True:
                if first == headU:
                    return {
                        'move': 'up'
                }
                if first == headD:
                    return {
                        'move': 'down'
                }
                if first == headL:
                    return {
                        'move': 'left'
                }
                if first == headR:
                    return {
                        'move': 'right'
                }

            if FindTail([head[0] + second[0], head[1] + second[1]], walls, checked, tail) == True:
                if second == headU:
                    return {
                        'move': 'up'
                }
                if second == headD:
                    return {
                        'move': 'down'
                }
                if second == headL:
                    return {
                        'move': 'left'
                }
                if second == headR:
                    return {
                        'move': 'right'
                }

            if FindTail([head[0] + third[0], head[1] + third[1]], walls, checked, tail) == True:
                if third == headU:
                    return {
                        'move': 'up'
                }
                if third == headD:
                    return {
                        'move': 'down'
                }
                if third == headL:
                    return {
                        'move': 'left'
                }
                if third == headR:
                    return {
                        'move': 'right'
                }

            if FindTail([head[0] + last[0], head[1] + last[1]], walls, checked, tail) == True:
                if last == headU:
                    return {
                        'move': 'up'
                }
                if last == headD:
                    return {
                        'move': 'down'
                }
                if last == headL:
                    return {
                        'move': 'left'
                }
                if last == headR:
                    return {
                        'move': 'right'
                }

            j = j + 1

    i = 0
    j = 0
    a = []
    checked = []
    
    while (i < len(data['food']['data'])):
        b = [[abs(data['food']['data'][i]['x'] - head[0]) + abs(data['food']['data'][i]['y'] - head[1]) , i]]
        a.extend(b)
        i = i + 1
    
    while (j < len(data['food']['data'])):
        minval = min(a)
        a.remove(minval)
        foodnum = minval[1]
        FoodX = data['food']['data'][foodnum]['x']
        FoodY = data['food']['data'][foodnum]['y']
        
        goalX = FoodX - head[0]
        goalY = FoodY - head[1]
        checked = []

        headU = [0, -1]
        headD = [0, 1]
        headL = [-1, 0]
        headR = [1, 0]

        if abs(goalX) >= abs(goalY):
            if goalX > 0:
                first = headR
                if goalY >= 0:
                    second = headD
                    third = headU
                    last = headL
                else:
                    second = headU
                    third = headD
                    last = headL
            else:
                first = headL
                if goalY >= 0:
                    second = headD
                    third = headU
                    last = headR
                else:
                    second = headU
                    third = headD
                    last = headR
        else:
            if goalY > 0:
                first = headD
                if goalX >= 0:
                    second = headR
                    third = headL
                    last = headU
                else:
                    second = headL
                    third = headR
                    last = headU
            else:
                first = headU
                if goalX >= 0:
                    second = headR
                    third = headL
                    last = headD
                else:
                    second = headL
                    third = headR
                    last = headD

        if FindTail([head[0] + first[0], head[1] + first[1]], walls, checked, tail) == True:
            if first == headU:
                return {
                    'move': 'up'
            }
            if first == headD:
                return {
                    'move': 'down'
            }
            if first == headL:
                return {
                    'move': 'left'
            }
            if first == headR:
                return {
                    'move': 'right'
            }

        if FindTail([head[0] + second[0], head[1] + second[1]], walls, checked, tail) == True:
            if second == headU:
                return {
                    'move': 'up'
            }
            if second == headD:
                return {
                    'move': 'down'
            }
            if second == headL:
                return {
                    'move': 'left'
            }
            if second == headR:
                return {
                    'move': 'right'
            }

        if FindTail([head[0] + third[0], head[1] + third[1]], walls, checked, tail) == True:
            if third == headU:
                return {
                    'move': 'up'
            }
            if third == headD:
                return {
                    'move': 'down'
            }
            if third == headL:
                return {
                    'move': 'left'
            }
            if third == headR:
                return {
                    'move': 'right'
            }

        if FindTail([head[0] + last[0], head[1] + last[1]], walls, checked, tail) == True:
            if last == headU:
                return {
                    'move': 'up'
            }
            if last == headD:
                return {
                    'move': 'down'
            }
            if last == headL:
                return {
                    'move': 'left'
            }
            if last == headR:
                return {
                    'move': 'right'
            }

        j = j + 1
    
    
    tailX = tail[0] - head[0]
    tailY = tail[1] - head[1]
    checked = []

    headU = [0, -1]
    headD = [0, 1]
    headL = [-1, 0]
    headR = [1, 0]

    if abs(tailX) >= abs(tailY):
        if tailX > 0:
            first = headR
            if tailY >= 0:
                second = headD
                third = headU
                last = headL
            else:
                second = headU
                third = headD
                last = headL
        else:
            first = headL
            if tailY >= 0:
                second = headD
                third = headU
                last = headR
            else:
                second = headU
                third = headD
                last = headR
    else:
        if tailY > 0:
            first = headD
            if tailX >= 0:
                second = headR
                third = headL
                last = headU
            else:
                second = headL
                third = headR
                last = headU
        else:
            first = headU
            if tailX >= 0:
                second = headR
                third = headL
                last = headD
            else:
                second = headL
                third = headR
                last = headD

    if FindTail([head[0] + first[0], head[1] + first[1]], walls, checked, tail) == True:
        if first == headU:
            return {
                'move': 'up'
        }
        if first == headD:
            return {
                'move': 'down'
        }
        if first == headL:
            return {
                'move': 'left'
        }
        if first == headR:
            return {
                'move': 'right'
        }

    if FindTail([head[0] + second[0], head[1] + second[1]], walls, checked, tail) == True:
        if second == headU:
            return {
                'move': 'up'
        }
        if second == headD:
            return {
                'move': 'down'
        }
        if second == headL:
            return {
                'move': 'left'
        }
        if second == headR:
            return {
                'move': 'right'
        }

    if FindTail([head[0] + third[0], head[1] + third[1]], walls, checked, tail) == True:
        if third == headU:
            return {
                'move': 'up'
        }
        if third == headD:
            return {
                'move': 'down'
        }
        if third == headL:
            return {
                'move': 'left'
        }
        if third == headR:
            return {
                'move': 'right'
        }

    if FindTail([head[0] + last[0], head[1] + last[1]], walls, checked, tail) == True:
        if last == headU:
            return {
                'move': 'up'
        }
        if last == headD:
            return {
                'move': 'down'
        }
        if last == headL:
            return {
                'move': 'left'
        }
        if last == headR:
            return {
                'move': 'right'
        }


    if([head[0], head[1]+1] not in walls):
        return {
            'move': 'down'
    }

    if([head[0], head[1]-1] not in walls):
        return {
            'move': 'up'
    }

    if([head[0] - 1, head[1]] not in walls):
        return {
            'move': 'left'
    }

    if([head[0] + 1, head[1]] not in walls):
        return {
            'move': 'right'
    }

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '192.168.96.121'),
        port=os.getenv('PORT', '8080'),
        debug = True)
