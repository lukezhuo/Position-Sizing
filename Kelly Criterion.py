import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def kelly_criterion(payout, loss, win_percentage):
    if loss == 0 or payout == 0:
        return 0
    return win_percentage / loss - (1 - win_percentage) / payout

def produce_prices(delta_arr):
    prices = [1]
    for i in range(len(delta_arr)):
        next_term = prices[-1] * (1 + delta_arr[i])
        if next_term <= 0.2:
            return [], False
        prices.append(next_term)
    return prices, prices[-1] >= 1

st.header("Kelly Criterion")
payout_str = st.text_input('Payout Percentage') 
payout  = float(payout_str) / 100 if payout_str != '' else 0
loss_str = st.text_input('Loss Percentage') 
loss  = float(loss_str) / 100 if loss_str != '' else 0
win_percentage = st.slider('Win Percentage', min_value=0, max_value=100) / 100.0


kelly = kelly_criterion(payout, loss, win_percentage)
st.write("Under the Kelly Criterion, " + str(max(0, round(kelly * 100, 2))) + " percent is optimal.")

st.header("Simulation")
trials_str = st.text_input('Trials')
trials  = int(trials_str) if trials_str != '' else 0
steps_str = st.text_input('Steps')
steps  = int(steps_str) if steps_str != '' else 0
bet = st.slider('Percentage of Portfolio', min_value=0, max_value=None) / 100

losses = 0
busts = 0
for t in range(trials):
    deltas = (np.random.binomial(1, win_percentage, steps) * (1 + payout) / 2 - 0.5) * 2 * bet
    prices, result = produce_prices(deltas)
    if not prices:
        busts += 1
    if not result:
        losses += 1
    x_vals = np.arange(len(prices))
    sim = plt.plot(x_vals, prices)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(plt.show());
st.write("Number of busts: " + str(busts) + ", Number of losses: " + str(losses) + " (in " + str(trials) + " trials)")


