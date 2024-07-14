import utilities as ut
from calculators import loan_vs_funds as lvf

###############################################################################
############                    Configuration                     #############
###############################################################################
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

# Fund
rent_expected = 700
fund_init_ammount = 0  # Just the diff between rent-quota
fund_r = 0.06  # Expected interest ratio

###############################################################################
############                       Init Vars                      #############
###############################################################################
interest = []
principal = []
principal_balance = []

CSV_FILE = "loan_rent.csv"

###############################################################################
############                         Main                         #############
###############################################################################
# Calculate Quota, interest_total and diff_rent_quota
quota, balance, start2 = lvf.calculate_balance_loan_vs_funds_per_year(
    loan_total_ammount, N_tot, loan_N, rent_expected, loan_r, fund_r
)
quota_monthly = quota / 12
interest_total = quota * loan_N - loan_total_ammount
diff_rent_quota = rent_expected - quota_monthly

# Check that rent is always bigger than quota
if quota_monthly >= rent_expected:
    msg = (
        "Rent Expected in a month is smaller than quota in a month: "
        f"{rent_expected} <= {round(quota_monthly, 2)}"
    )
    print(ut.st("error", msg))
    exit(1)

print(
    "*******************************************\n"
    f"Annual Payment fixed quota: {round(quota, 2)}€\n"
    f"Monthly Payment fixed quota: {round(quota_monthly, 2)}€\n"
    f"Number of years paying loan: {loan_N}\n"
    f"Total Interests: {round(interest_total, 2)}€ "
    f"({round(100 * interest_total / loan_total_ammount, 2)}%)\n"
    f"Expected monthly rent: {round(rent_expected, 2)}€\n"
    f"Monthly diff rent-quota: {round(diff_rent_quota, 2)}€\n\n"
    "*******************************************\n"
)

start2_formated = f"{start2:,.2f}"
balance_formated = f"{balance:,.2f}"


print(
    "*******************************************\n"
    f"Investing {loan_N} years:\n"
    f"  * initial_contribution = 0€\n"
    f"  * monthly              = {round(diff_rent_quota, 2)}€\n"
    f"  * final_balance        = {start2_formated}€\n\n"
    f"Investing {N_tot - loan_N} years:\n"
    f"  * initial_contribution = {start2_formated}€\n"
    f"  * monthly              = {round(rent_expected, 2)}€\n"
    f"  * final_balance        = {balance_formated}€\n"
    "*******************************************"
)
