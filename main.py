def initialiseState(col,row,orientation,agility,strength): #Made it two lines instead of one on return to imporve readability
  initialiseState = {'playerSquare': (col, row), 'player':{},'others': {}}
  initialiseState['player'] = {'type': 'player', 'orientation': orientation, 'agility': agility, 'strength': strength}
  return initialiseState


def addHerb(state,col,row,agility):
  return state['others'].update({(col,row):{'type':'herb','agility':agility}}) 


def addBread(state,col,row,strength):
  return state['others'].update({(col,row):{'type':'bread','strength':strength}}) 

def addBlock(state,col,row,height):
  return state['others'].update({(col,row):{'type':'block','height':height}})

def getEntityAt(state,col,row):
  if (col,row) == state['playerSquare']:
    return state['player']
  for key in state['others']:
    if key == (col,row):
      return state['others'][col,row]
  else:
      return {}


def showBoard(state,cols,rows):
  SymbolOthersDictonary = {'herb':'#','bread':'@'}
  SymbolPlayerDictonary = {'up': 0x2191, 'down':0x2193, 'left': 0x2190, 'right': 0x2192}
  LinePrint = ''
  PlayerX = state['playerSquare'][0]
  PlayerY = state['playerSquare'][1]
  
  for row in range(PlayerY-rows, PlayerY+rows+1):
    for col in range(PlayerX -cols, PlayerX+cols+1):
      TempEntity = {}
      TempEntity.update(getEntityAt(state,col,row))
      if TempEntity.get('type') == 'player': #WHY TF DOES TempEntity['type'] result in keyError?
        LinePrint += chr(SymbolPlayerDictonary[TempEntity.get('orientation')]) + ' '
    
      elif TempEntity.get('type') in SymbolOthersDictonary:
        LinePrint += SymbolOthersDictonary[TempEntity.get('type')] + ' '
        
      elif TempEntity.get('type') == 'block':
        LinePrint += str(TempEntity['height']) + ' '
      else:
        LinePrint += '. '
    print(LinePrint)
    LinePrint = '' #Empties Line print var for next cycle of x

def getPlayer(state):
  return state['player']

def turn(state, direction):
  DirectionList = ['left','right','up','down']
  if direction in DirectionList:
    state['player']['orientation'] = direction
    print('1')
    return 1 
  else:
    return -1

def step(state):
  PlayerCord = list(state['playerSquare'])
  Direction = state['player']['orientation']
  DirectionUpdates = {'left':[-1, 0], 'right': [1,0], 'up':[0,-1], 'down':[0,1]}
  PlayerCord[0] +=  DirectionUpdates[Direction][0] 
  PlayerCord[1] +=  DirectionUpdates[Direction][1]
  if tuple(PlayerCord) in state['others'].keys():
    return -1
  else: 
    state['playerSquare'] = tuple(PlayerCord)
    return 1

def showPlayer(state):
  Column = state['playerSquare'][0]
  Row = state['playerSquare'][1]
  Orientation = state['player']['orientation']
  Agility =  state['player']['agility']
  Strength = state['player']['strength']
  return print('\ncolumn: ',Column, '\nrow: ',Row, '\norientation: ',Orientation, '\nagility: ', Agility, '\nstrength: ', Strength)

def showFacing(state):
  PlayerCord = list(state['playerSquare'])
  Direction = state['player']['orientation']
  DirectionUpdates = {'left':[-1, 0], 'right': [1,0], 'up':[0,-1], 'down':[0,1]}
  PlayerCord[0] +=  DirectionUpdates[Direction][0] 
  PlayerCord[1] +=  DirectionUpdates[Direction][1]
  if tuple(PlayerCord) in state['others'].keys():
    Column = PlayerCord[0]
    Row = PlayerCord[1]
    Type = state['others'][tuple(PlayerCord)]['type']
    if Type == 'herb':
      Agility  = state['others'][tuple(PlayerCord)]['agility']
      return print('\ncolumn: ',Column, '\nrow: ',Row,'\ntype: ', Type ,'\nagility:' , Agility)
    elif Type == 'bread':
      Strength = state['others'][tuple(PlayerCord)]['strength'] 
      return print('\ncolumn: ',Column, '\nrow: ',Row, '\ntype: ',Type ,'\nstrength: ', Strength)
    elif Type == 'block':
      Height =  state['others'][tuple(PlayerCord)]['height'] 
      return print('\ncolumn: ',Column, '\nrow: ',Row, '\ntype: ',Type  ,'\nheight: ', Height )
  else: 
    print('No entity')

def eat(state):
  PlayerCord = list(state['playerSquare'])
  Direction = state['player']['orientation']
  DirectionUpdates = {'left':[-1, 0], 'right': [1,0], 'up':[0,-1], 'down':[0,1]}
  PlayerCord[0] +=  DirectionUpdates[Direction][0] 
  PlayerCord[1] +=  DirectionUpdates[Direction][1]
  if tuple(PlayerCord) in state['others']:
    Type = state['others'][tuple(PlayerCord)]['type']
    if  Type == 'herb':
      state['player']['agility'] += state['others'][tuple(PlayerCord)]['agility']
      del state['others'][tuple(PlayerCord)]
      return 1
    elif Type == 'bread':
      state['player']['strength'] += state['others'][tuple(PlayerCord)]['strength']
      del state['others'][tuple(PlayerCord)]
      return 1
    else:
      return -1
  else:
    return -1

def batter(state):
  PlayerCord = list(state['playerSquare'])
  Direction = state['player']['orientation']
  DirectionUpdates = {'left':[-1, 0], 'right': [1,0], 'up':[0,-1], 'down':[0,1]}
  PlayerCord[0] +=  DirectionUpdates[Direction][0] 
  PlayerCord[1] +=  DirectionUpdates[Direction][1]

  if tuple(PlayerCord) in state['others']:
    Type = state['others'][tuple(PlayerCord)]['type']
    if Type == 'block':
      if state['others'][tuple(PlayerCord)]['height'] <= 2: 
        del state['others'][tuple(PlayerCord)]
        state['player']['strength'] -= 1
        return 1
      elif  state['others'][tuple(PlayerCord)]['height'] > 2:
        state['player']['strength'] -= 1 #Check if I need to swap line 16 and 17?
        state['others'][tuple(PlayerCord)]['height'] -= state['player']['strength']
        if  state['others'][tuple(PlayerCord)]['height'] <= 0:
          del state['others'][tuple(PlayerCord)]
        return 1
      else:
        return -1
    else:
      return -1
  else:
    return -1

def jump(state):
  PlayerCord = list(state['playerSquare'])
  PlayerJumpLocation = list(state['playerSquare'])
  Direction = state['player']['orientation']
  DirectionUpdates = {'left':[-1, 0], 'right': [1,0], 'up':[0,-1], 'down':[0,1]}
  DirectionJumpUpdates = {'left':[-2, 0], 'right': [2,0], 'up':[0,-2], 'down':[0,2]}
  PlayerCord[0] +=  DirectionUpdates[Direction][0] 
  PlayerCord[1] +=  DirectionUpdates[Direction][1]
  PlayerJumpLocation[0] +=  DirectionJumpUpdates[Direction][0]
  PlayerJumpLocation[1] +=  DirectionJumpUpdates[Direction][1]
  
  if tuple(PlayerCord) in state['others'].keys() and tuple(PlayerJumpLocation) not in state['others'].keys():
    Type = state['others'][tuple(PlayerCord)]['type']
    if Type == 'block':
      state['player']['agility'] -= 1
      state['playerSquare'] = tuple(PlayerJumpLocation)
      return 1
    else:
      state['playerSquare'] = tuple(PlayerJumpLocation)
      return 1
  else:
    return -1 

def readState(file):
  state = {'playerSquare':(),'player':{'type':'', 'orientation':'','agility':'','strength':'' },'others':{}}
  GameSave = open(file)
  for eachLine in GameSave:
    LinesSplit = eachLine.split()
    if LinesSplit[0] == 'player':
      state.update(initialiseState(int(LinesSplit[1]),int(LinesSplit[2]),LinesSplit[5],int(LinesSplit[3]),int(LinesSplit[4])))
    elif LinesSplit[0] == 'herb':
      addHerb(state,int(LinesSplit[1]),int(LinesSplit[2]),int(LinesSplit[3]))
    elif LinesSplit[0] == 'bread':
      addBread(state,int(LinesSplit[1]),int(LinesSplit[2]),int(LinesSplit[3]))
    elif LinesSplit[0] == 'block':
      addBlock(state,int(LinesSplit[1]),int(LinesSplit[2]),int(LinesSplit[3]))
  return state


def playConsole(file):
  state = readState(file)
  GAME = True
  while GAME == True: #Game = False is within the if Quit statment
    GameInput = input('>')
    GameInputSplit = GameInput.split()
    if not GameInputSplit:
      pass
    elif GameInputSplit[0] == 'turn' and len(GameInputSplit) == 2:
      if (GameInputSplit[0] == 'turn' and (GameInputSplit[1] == 'left' or 'right' or 'up' or 'down')):
        turn(state,GameInputSplit[1])
      else:
        pass
    elif (GameInputSplit[0] == 'show' and len(GameInputSplit) == 2):
      if (GameInputSplit[0] == 'show' and GameInputSplit[1] == 'board'):
        showBoard(state, 7,7)
      elif (GameInputSplit[0] == 'show' and GameInputSplit[1] == 'player'):
        showPlayer(state)
      elif (GameInputSplit[0] == 'show' and GameInputSplit[1] == 'facing'):
        showFacing(state)
      else:
        pass
    elif GameInputSplit[0] == 'step':
      step(state)
    elif GameInputSplit[0] == 'jump':
      jump(state)
    elif GameInputSplit[0] == 'eat':
      eat(state)
    elif GameInputSplit[0] == 'batter':
      batter(state)
    elif GameInputSplit[0] == 'quit':
      GAME = False
    else:
      pass

if __name__ == "__main__":
  playConsole('example.txt')
