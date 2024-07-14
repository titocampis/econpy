import utilities as ut
from calculators import compound_interest_calculator as cic


def calculate_balance_loan_vs_funds_per_year(
    ammount_loan: int,
    total_years: int,
    loan_years: int,
    rent_expected: int,
    r_loan: float = 0.03,
    r_fund: float = 0.06,
):
    # Calculate Quota, interest_total and diff_rent_quota
    quota = (
        ammount_loan
        * r_loan
        * (1 + r_loan) ** loan_years
        / ((1 + r_loan) ** loan_years - 1)
    )
    quota_monthly = quota / 12
    # interest_total = quota * loan_years - ammount_loan
    diff_rent_quota = rent_expected - quota_monthly

    # Check that rent is always bigger than quota
    if quota_monthly >= rent_expected:
        msg = (
            "Rent Expected in a month is smaller than quota in a month: "
            f"{rent_expected} <= {round(quota_monthly, 2)}"
        )
        print(ut.st("error", msg))
        exit(1)

    # Check that N_tot > N
    if total_years < loan_years:
        msg = (
            "Total years must be bigger than loan years: "
            f"{total_years} > {loan_years}"
        )
        print(ut.st("error", msg))
        exit(1)

    # Calculate the benefits during the loan (N years)
    balance = cic.calculate_balance(loan_years, diff_rent_quota, r_fund, 0)
    total_balance = cic.calculate_balance(
        total_years - loan_years, rent_expected, r_fund, balance
    )
    return [quota, total_balance, balance]
