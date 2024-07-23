# Suppress specific warning for matplotlib with WSL
import warnings

warnings.filterwarnings(
    "ignore", message="Unable to import Axes3D", category=UserWarning
)

import matplotlib.pyplot as plt
import pandas as pd

import utilities as ut
from calculators import compound_interest_calculator as cic
from calculators import loan_vs_funds as lvf

###############################################################################
############                    Configuration                     #############
###############################################################################
# Life
N_tot = 40
verbose = True
wantcsv = True
CSV_FILE = "files/example_loan_vs_funds.csv"
plot = True

# Loan
loan_principal = 100000  # total loan without interests
loan_r = 3  # annual interest rate (in %)
loan_N = 30

# Fund
rent_expected = 700
fund_init_ammount = 0  # Just the diff between rent-quota
fund_r = 6  # Expected interest ratio

###############################################################################
############                       Init Vars                      #############
###############################################################################
# Correct r's
loan_r = loan_r / 100
fund_r = fund_r / 100

interest = []
amortization = []
amortization_balance = []

CSV_FILE = "files/loan_rent.csv"

###############################################################################
############                         Main                         #############
###############################################################################
# Calculate Quota, interest_total and diff_rent_quota
quota, balance, start2 = lvf.calculate_balance_loan_vs_funds_per_year(
    loan_principal, N_tot, loan_N, rent_expected, loan_r, fund_r
)
quota_monthly = quota / 12
interest_total = quota * loan_N - loan_principal
diff_rent_quota = rent_expected - quota_monthly

# Check that rent is always bigger than quota
if quota_monthly >= rent_expected:
    msg = (
        "Rent Expected in a month is smaller than quota in a month: "
        f"{rent_expected} <= {round(quota_monthly, 2)}"
    )
    print(ut.st("error", msg))
    exit(1)

# Printing sum up data of the first period =< loan_years
print(
    "*******************************************\n"
    f"r: {100 * loan_r}%\n"
    f"Annual fixed quota: {round(quota, 2)}€\n"
    f"Monthly fixed quota: {round(quota_monthly, 2)}€\n"
    f"Number of years: {loan_N}\n"
    f"Total Interests: {round(interest_total, 2)}€ "
    f"({round(100 * interest_total / loan_principal, 2)}%)\n"
    f"Expected monthly rent: {round(rent_expected, 2)}€\n"
    f"Monthly diff rent-quota: {round(diff_rent_quota, 2)}€\n"
    "*******************************************\n"
)

start2_formated = f"{start2:,.2f}"
balance_formated = f"{balance:,.2f}"

# Printing sum up data of the first period > loan_years
print(
    "\n*******************************************\n"
    f"Investing {loan_N} years:\n"
    f"  * r                    = {100 * fund_r}%\n"
    f"  * initial_contribution = 0€\n"
    f"  * monthly              = {round(diff_rent_quota, 2)}€\n"
    f"  * final_balance        = {start2_formated}€\n\n"
    f"Investing {N_tot - loan_N} years:\n"
    f"  * r                    = {100 * fund_r}%\n"
    f"  * initial_contribution = {start2_formated}€\n"
    f"  * monthly              = {round(rent_expected, 2)}€\n"
    f"  * final_balance        = {balance_formated}€\n"
    "*******************************************\n"
)

# Load a dataframe
## Getting data from first period
first_period_data = cic.calculate_compound(
    loan_N,
    diff_rent_quota,
    fund_r,
    0,
    False,
    CSV_FILE,
    verbose=False,
    plot=False,
)

## Getting data from first period
second_period_data = cic.calculate_compound(
    N_tot - loan_N,
    rent_expected,
    fund_r,
    start2,
    False,
    CSV_FILE,
    verbose=False,
    plot=False,
)

## Gather data
full_data = {}

for key in first_period_data.keys():
    # Transform second_period_data for contributed to make it
    # linear
    if key == "Contributed":
        adj = (
            first_period_data["Contributed"][-1]
            - first_period_data["Balance"][-1]
        )
        second_period_data[key] = [x + adj for x in second_period_data[key]]

    # Combine the lists for each key
    full_data[key] = first_period_data[key] + second_period_data[key]

df = pd.DataFrame(full_data)
if verbose:
    print(df)

# Plot
if plot:
    plt.figure(1)
    plt.title(f"Compound interest in {N_tot} years")
    plt.xlabel("N (years)")
    plt.ylabel("Euros")

    axis_x = range(1, N_tot + 1)
    balance_bar = plt.bar(
        axis_x, full_data["Balance"], label="Benefit", color="g"
    )
    contributed_bar = plt.bar(
        axis_x, full_data["Contributed"], label="Contributed", color="b"
    )

    plt.xticks(
        axis_x
    )  # Set the tick labels to be the same as the values of axis_x
    plt.legend()  # Add a legend

    # Add value labels on top of the bars
    for bar in balance_bar:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            f"{yval:,.0f}€",
            ha="center",
            va="bottom",
        )

    for bar in contributed_bar:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            f"{yval:,.0f}€",
            ha="center",
            va="bottom",
        )

    # Vertical line in the change
    plt.axvline(
        x=loan_N,
        color="red",
        linestyle="-",
        linewidth=1,
        alpha=0.5,
        label="Loan finish",
    )

    plt.show()
