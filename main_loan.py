from calculators import loan_calculator as lc

# Config
loan_total_ammount = 100000  # total loan without interests
loan_years = 25
loan_r = 0.03  # % of annual interest payment

want_csv = True
CSV_FILE = "files/loan.csv"

# Main
lc.calculate_loan(
    loan_total_ammount,
    loan_years,
    loan_r,
    tocsv=want_csv,
    csv_file=CSV_FILE,
    verbose=True,
)
