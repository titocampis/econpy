import matplotlib.pyplot as plt
import pandas as pd

import utilities as ut
from calculators import loan_vs_funds as lvf

# Config
# Life
N_tot = 30
verbose = True
tocsv = True
csv_file = "files/loan_vs_funds.csv"
plot = True

# Loan
loan_total_ammount = 100000  # total loan without interests
loan_r = 0.03  # % of annual interest payment
loan_N = 29
loan_N_range = range(15, loan_N)

# Fund
rent_expected = 700
fund_init_ammount = 0  # Just the diff between rent-quota
fund_r = 0.06  # Expected interest ratio

# Calculate
balance_vec = []
full_invested_years = []
second_init = []

for n in loan_N_range:
    quota, balance, start2 = lvf.calculate_balance_loan_vs_funds_per_year(
        loan_total_ammount, N_tot, n, rent_expected, loan_r, fund_r
    )
    balance_formated = f"{balance:,.2f}€"
    # print(f"Loan years: {n} | Balance: {balance_formated}")
    balance_vec.append(balance)
    full_invested_years.append(N_tot - n)
    second_init.append(start2)

# Load a dataframe
data = {
    "Loan Years": list(loan_N_range),
    "Balance": balance_vec,
    "Full Invested": full_invested_years,
    "Second Init": second_init,
}

df = pd.DataFrame(data)
if verbose:
    print(df)

# Save the DataFrame to a CSV file
if tocsv:
    df.to_csv(csv_file, index=False)
    print(f"\n{ut.st('OK', f'{csv_file} has been saved')}.")

# Plot %
if plot:
    plt.figure(1)
    plt.title(f"Balance in {N_tot} years depending on years of loan")
    plt.xlabel("N (years of loan)")
    plt.ylabel("Euros")

    axis_x = loan_N_range
    bar_balance = plt.bar(
        axis_x, balance_vec, label="Balance over N", color="g"
    )

    plt.xticks(
        axis_x
    )  # Set the tick labels to be the same as the values of axis_x
    plt.legend()  # Add a legend

    # Add value labels on top of the bars
    for bar in bar_balance:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            f"{yval:,.0f}€",
            ha="center",
            va="bottom",
        )

    plt.show()
