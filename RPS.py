# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[], my_history=[], strat=[]):
    opponent_history.append(prev_play)

    # print(opponent_history)
    # print(my_history)
    strategy = guess_opponent(opponent_history, my_history)
    # if strategy != "":     
    #   if len(strat) == 0 or strategy != strat[0]:
    #     # print("its", strategy)
    #     # print(opponent_history)
    #     if len(strat) == 0:
    #       strat.append(strategy)
    #     else:
    #       strat[0] = strategy
    # else:
    #   print("cannot guess strat")
      
    guess = guess_move(strategy, opponent_history, my_history)    
    
    my_history.append(guess)

    return guess


def guess_opponent(opponent_history, my_history):
  
  ideal_response = {"P": "S", "R": "P", "S": "R"}   
  
  if len(opponent_history) > 5:
    quincy_moves_zero = ["R", "P", "P", "S", "R"]
    quincy_moves = []
    for i in range(5):
      quincy_moves.append(quincy_moves_zero[i:] + quincy_moves_zero[:i])
    if opponent_history[-5:] in quincy_moves:    
      return "quincy"

  if len(my_history) > 3:
    maybe_its_kris = True
    last_moves = my_history[-4:-1]
    for i in range(3):
      move = last_moves[-3+i]
      if move == "":
        move = "R"
      if ideal_response[move] != opponent_history[-3+i]:
        maybe_its_kris = False
        break
      if maybe_its_kris:
        return "kris"

  if len(my_history) > 4:
    maybe_its_mrugesh = True
    last_moves = my_history[-21:-1]
    for i in range(3):
      end_index = None if i == 0 else -i
      base = last_moves[-i-10:end_index]
      # print(last_moves)
      # print(base)
      most_frequent = max(base, key=base.count)      
      # print(opponent_history)
      # print("most frequent: ", most_frequent)
      # print("gonna use ", ideal_response[ideal_response[most_frequent]])
      # print("checking if he used ", ideal_response[most_frequent])
      # print("he used ", opponent_history[-i-1])
      if ideal_response[most_frequent] != opponent_history[-i-1]:
        maybe_its_mrugesh = False
        break
    if maybe_its_mrugesh:
      # print("its mrugesh")
      return "mrugesh"

  return ""
  
def guess_move(strategy, opponent_history, my_history):
    
  ideal_response = {"P": "S", "R": "P", "S": "R"}
    
  if strategy == "quincy":      
    if opponent_history[-1] == "S" or opponent_history[-2:] == ["S", "R"]:
      # expecting R
      return "P"
    elif opponent_history[-2:] == ["R", "R"] or opponent_history[-2:] == ["R", "P"]:
      # expecting P
      return "S"      
    elif opponent_history[-2:] == ["P", "P"]:
      # expecting S
      return "R"
  elif strategy == "kris":
    return ideal_response[ideal_response[my_history[-1]]]
  elif strategy == "mrugesh":
    last_ten = my_history[-10:]      
    most_frequent = max(last_ten, key=last_ten.count)
    # print(my_history[-10:])
    # print(opponent_history)
    # print("most frequent: ", most_frequent)
    # print("gonna use ", ideal_response[ideal_response[most_frequent]])
    # print("checking if he used ", ideal_response[most_frequent])
    return ideal_response[ideal_response[most_frequent]]
  else:
    if len(opponent_history) > 2:
      return opponent_history[-2]

  return "R"