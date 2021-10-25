# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.


def player(prev_play, opponent_history=[], my_history=[], stats=[False, False, 0], int_stats=[{}]):
    opponent_history.append(prev_play)

    # print(opponent_history)
    # print(my_history)
    strategy = guess_opponent(opponent_history, my_history)
    # print(strategy)

    # if strategy != "abbey":
    #   for key in stats[0]:
    #     stats[0][key] = 0

    guess = guess_move(strategy, opponent_history, my_history, stats)    
    
    if not len(my_history):
      my_history.append("R")

    my_history.append(guess)
    # if len(my_history) >= 2:
    #   last_two = "".join(my_history[-2:])
    #   stats[0][last_two] = stats[0].get(last_two, 0) + 1

    stats[0] = stats[1]
    stats[1] = strategy == "abbey"

    if not (stats[0] or stats[1]):
      # pass
      # if stats[2] > 0:
      #   print("not abbey anymore")
      stats[2] = 0      
    else:
      stats[2] += 1


    # strat_name = "none" if strategy == "" else strategy
    # int_stats[0][strat_name] = int_stats[0].get(strat_name, 0) + 1
    # if len(my_history) % 1000 == 0:
    #   # print(int_stats)
    #   for key in int_stats[0]:
    #     int_stats[0][key] = 0

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

  if len(my_history) > 10:
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
    # print(my_history[-10:])
    # print(opponent_history)
    # print("most frequent: ", most_frequent)
    # print("gonna use ", ideal_response[ideal_response[most_frequent]])
    # print("checking if he used ", ideal_response[most_frequent])
    return ideal_response[ideal_response[most_frequent]]
  else:

    return ideal_response[ideal_response[opponent_history[-1]]] if len(opponent_history[-1]) else "S"

    if len(my_history) >= 2:      
      my_last = my_history[-1]
      for i in range(min(len(my_history) - 1, 20)):
        last_picked = my_history[-i-2]
        if last_picked == my_last:
          # print("last one was " + my_last + my_history[-i-1] + " so I go " + ideal_response[ideal_response[my_history[-i-1]]])
          # print(my_history)
          return ideal_response[ideal_response[my_history[-i-1]]]
    # print("general order")
    general_order = "SRP"
    current_index = len(my_history) % 3
    return general_order[current_index]


    if len(my_history) > 1:
      legit_moves = []
      stats = {}
      for i in ["R", "P", "S"]:
        legit_moves.append(my_history[-1] + i)
      stats_base = my_history[-strat_stats[2]-1:]
      for i in range(min(strat_stats[2], len(my_history) - 1)):
        combination = "".join(stats_base[i:i+2])
        if len(combination) == 2:
          stats[combination] = stats.get(combination, 0) + 1
      legit_moves_probs = {x: stats[x] if x in stats else 0 for x in legit_moves }
      # print(legit_moves)
      # print(legit_moves_probs)
      # print(stats)
      # print(my_history)
      if len(legit_moves_probs) > 0:
        # print(legit_moves)
        # print(legit_moves_probs)
        # print(stats)
        # print(my_history)
        # print(opponent_history)
        return ideal_response[ideal_response[max(legit_moves_probs, key=legit_moves_probs.get)[-1]]]
        # return min(legit_moves_probs, key=legit_moves_probs.get)[-1]        
      else:
        return  "P"

  return "R"

# def first_won(list1, list2):
#   return (list1[-1] + list2[-1] in ["RS", "PR", "SP"])
    