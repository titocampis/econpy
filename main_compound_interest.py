from calculators import compound_interest_calculator as cic

# Config
init_ammount = 1000
monthly_cont = 700
years_fund = 25  # Number of years
r_fund = 0.06  # Expected interest ratio

want_csv = True
CSV_FILE = "files/compound_interest.csv"

plot = True

cic.calculate_compound(
    years_fund,
    monthly_cont,
    r_fund,
    init_ammount,
    want_csv,
    verbose=True,
    plot=True,
)
