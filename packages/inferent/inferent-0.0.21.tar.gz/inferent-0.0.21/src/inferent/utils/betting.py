"""Betting utilities"""

import itertools
from math import log

def convert_odds_to_percent(odd, fro="percent"):
    if fro == "percent":
        return odd
    elif fro == "american":
        return 100.0 / (odd + 100.0) if odd >= 0 else (-odd) / (-odd + 100.0)
    elif fro == "decimal":
        return 1 / odd
    else:
        raise


def convert_odds_from_percent(odd, to="decimal"):
    if to == "percent":
        return odd
    elif to == "american":
        return (
            100.0 / odd - 100.0 if odd >= 0.5 else (-100.0 * odd) / (1.0 - odd)
        )
    elif to == "decimal":
        return 1.0 / odd
    else:
        raise


def convert_odds(odd, to="percent", fro="american"):
    return convert_odds_from_percent(convert_odds_to_percent(odd, fro), to)

def exp_log_wealth(probabilities,  # probability
                   ptl,            # profit to loss; (payout - 1)
                   weights):       # weights
  res = 0.0
  grad = np.zeros(len(probabilities))
  # All combinationations of 0 and 1s in a n-dimensional array, e.g. for n=3,
  # 000,001,010,011,100, ...
  for indices in itertools.product([0, 1], repeat=len(probabilities)):
      prob = 1.0
      wealth = 1.0
      local_grad = np.zeros(len(probabilities))
      # (0,1,2) x (each combination for all combinations)
      for i, j in enumerate(indices):
        if j == 0:
          prob *= probabilities[i]
          wealth += weights[i] * ptl[i]
          local_grad[i] += ptl[i]
        else:
          prob *= 1 - probabilities[i]
          wealth -= weights[i]
          local_grad[i] -= 1
      wealth = wealth + 0.000001  # Handle 0 and <0 errors
      res += prob * log(wealth)
      grad += prob * local_grad / wealth
  return res, grad

def optimal_kelly(probabilities,   # predicted probability of winning
                  payoffs,         # how much won if wagering $1
                  alpha=0.001,      # learning rate
                  eps=0.000000001):# epsilon for stopping point
  ptl = [ payoff - 1.0 for payoff in payoffs ]
  #initial_weights = [1.0 / len(probabilities)] * len(probabilities)
  initial_weights = [0.0] * len(probabilities)
  res = None
  weights = initial_weights.copy()
  #print("TRY", probabilities, ptl)
  while True:
    newres, grad = exp_log_wealth(probabilities, ptl, weights)

    # apply alpha, check that weights sum to < 1.
    alpha2 = alpha
    while True:
      weights2 = weights + grad * alpha2
      weights2 = [ 0.0 if weight < 0.0 else 1.0 if weight > 1.0 else weight for weight in weights2]
      if sum(weights2) <= 1.0:
        weights = weights2
        break
      else:
        print("halving alpha: ")
        print(weights2)
        alpha2 = alpha2 / 2
    if not res:
      res = newres
    else:
      #print("EPS: ", abs(newres - res))
      if abs(newres - res) < eps:
        res = newres
        break
      res = newres
  return res, weights
