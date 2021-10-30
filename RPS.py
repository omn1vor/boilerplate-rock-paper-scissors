# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[], my_history=[], stats=[False, False, 0]):
    
    if prev_play == "":
      opponent_history = []

    opponent_history.append(prev_play)

    strategy = guess_opponent(opponent_history, my_history)
    guess = guess_move(strategy, opponent_history, my_history, stats)    
    
    if not len(my_history):
      my_history.append("R")

    my_history.append(guess)

    stats[0] = stats[1]
    stats[1] = strategy == "abbey"

    if not (stats[0] or stats[1]):
      stats[2] = 0      
    else:
      stats[2] += 1

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

  if len(my_history) > 10 and len(opponent_history) > 10:
    maybe_its_kris = True
    last_moves = my_history[-11:-1]
    for i in range(10):
      move = last_moves[-10+i]
      if move == "":
        move = "R"
      if ideal_response[move] != opponent_history[-10+i]:
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
      most_frequent = max(base, key=base.count)      
      if ideal_response[most_frequent] != opponent_history[-i-1]:
        maybe_its_mrugesh = False
        break
    if maybe_its_mrugesh:
      return "mrugesh"

  return "abbey"
  
def guess_move(strategy, opponent_history, my_history, strat_stats):
    
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
    return ideal_response[ideal_response[most_frequent]]
  else:
    
    chain_len = 2
    source = my_history[:]
    if len(source) > 0 and source[0] == "":
      source = source[1:]
    if len(source) >= chain_len:
      legit_moves = []
      stats = {}
      for i in ["R", "P", "S"]:
        legit_moves.append("".join(source[-chain_len+1:]) + i)
      stats_base = source[-strat_stats[2]-1:]      
      for i in range(min(strat_stats[2], len(source) - chain_len+1)):
        combination = "".join(stats_base[i:i+chain_len])
        if len(combination) == chain_len:
          stats[combination] = stats.get(combination, 0) + 1
      legit_moves_probs = {x: stats[x] if x in stats else 0 for x in legit_moves }

      if len(legit_moves_probs) > 0:
        return ideal_response[ideal_response[max(legit_moves_probs, key=legit_moves_probs.get)[-1]]]
        # return min(legit_moves_probs, key=legit_moves_probs.get)[-1]        
      else:
        return  "P"

  return "R"

    