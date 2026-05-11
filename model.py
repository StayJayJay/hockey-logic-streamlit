import math

def logistic(x):
    return 1 / (1 + math.exp(-x))

def predict(match, coef):
    log_odds = (
        coef["intercept"]
        + coef["home"] * match["home"]
        + coef["xg_diff"] * match["xg_diff"]
        + coef["pp_diff"] * match["pp_diff"]
        + coef["goalie"] * match["goalie_diff"]
    )
    return log_odds, logistic(log_odds)
