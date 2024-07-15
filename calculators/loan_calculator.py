# Suppress specific warning for matplotlib with WSL
import warnings

warnings.filterwarnings(
    "ignore", message="Unable to import Axes3D", category=UserWarning
)

import matplotlib.pyplot as plt
import pandas as pd

import utilities as ut


def calculate_quota(loan_ammount: float, N: int, r: float = 0.03):
    """
    Method to calculate the fixed quota of a loan based on:

    Parameters:
    loan_ammount (float): total loan without interests.
    N (int): total number of payments.
    r (float): % of annual interest payment.

    Returns:
    quota (double)
    """
    # Calculate Quota, interest_total and diff_rent_quota
    quota = loan_ammount * r * (1 + r) ** N / ((1 + r) ** N - 1)

    return quota


def calculate_interest_n(loan_ammount: float, N: int, n: int, r: float = 0.03):
    """
    Method to calculate the interest of a year n

    Parameters:
    loan_ammount (float): total loan without interests.
    N (int): total number of payments.
    n (int): year to calculate.
    r (float): % of annual interest payment.

    Returns:
    interest_n (double)
    """
    quota = calculate_quota(loan_ammount, N, r)
    interest_n = loan_ammount * r * (1 + r) ** (n - 1) - quota * (
        (1 + r) ** (n - 1) - 1
    )

    return interest_n


def calculate_principal_n(loan_ammount: float, N: int, n: int, r: float = 0.03):
    """
    Method to calculate the principal payment of a year n

    Parameters:
    loan_ammount (float): total loan without interests.
    N (int): total number of payments.
    n (int): year to calculate.
    r (float): % of annual interest payment.

    Returns:
    principal_n (double)
    """
    principal_n = loan_ammount * r * (1 + r) ** (n - 1) / ((1 + r) ** N - 1)

    return principal_n


def calculate_principal_balance_n(
    loan_ammount: float, N: int, n: int, r: float = 0.03
):
    """
    Method to calculate the principal balance of a year n

    Parameters:
    loan_ammount (float): total loan without interests.
    N (int): total number of payments.
    n (int): year to calculate.
    r (float): % of annual interest payment.

    Returns:
    principal_balance_n (double)
    """
    principal_balance_n = loan_ammount * (
        ((1 + r) ** N - (1 + r) ** (n - 1)) / ((1 + r) ** N - 1)
    )

    return principal_balance_n


def check_calculations_interest_principal(
    quota: float, interest_n: float, principal_n: float
):
    """
    Method to check that the loan calculations have been done correctly

    Parameters:
    quota (float): quota to pay annually.
    interest_n (float): interest paid in the year.
    principal_n (float): principal paid in the year.

    Returns:
    None
    """
    if abs(quota - interest_n - principal_n) > 1e-9:
        error_msg = (
            "Something went wrong validating the calculations, "
            "quota != interest + principal, please check the script.\n"
            f"{quota} != {interest_n} + {principal_n}"
        )
        print(ut.st("error", error_msg))
        exit(1)


def check_calculations_interest_total(interest: list, interest_total: float):
    """
    Method to check that the loan calculations have been done correctly

    Parameters:
    interest (list): interest paid every year.
    interest_total (float): total interest paid.

    Returns:
    None
    """
    if abs(sum(interest) - interest_total) > 1e-7:
        error_msg = (
            "Something went wrong validating the calculations, "
            "sum(interests) != interest_total, "
            "please check the script."
        )
        print(ut.st("error", error_msg))
        exit(1)
    else:
        print(f"{ut.st('OK', 'Validation successfully passed.')}\n")


def calculate_loan(
    loan_ammount: int,
    N: int,
    r: float = 0.03,
    tocsv: bool = True,
    csv_file: str = "files/loan.csv",
    verbose: bool = False,
    plot: bool = False,
):
    """
    Method to calculate and print (if desired) data from a loan

    Parameters:
    loan_ammount (int): total loan without interests.
    N (int): total number of payments.
    r (float): % of annual interest payment.
    tocsv (bool): if results want to be exported to a csv.
    csv_file (str): name of the csv file.
    verbose (bool)
    plot (bool)

    Returns:
    None
    """
    # Calculate Quota and interest_total
    quota = calculate_quota(loan_ammount, N, r)
    interest_total = quota * N - loan_ammount

    # Print Values
    if verbose:
        interest_total_formated = f"{interest_total:,.2f}"
        quota_formated = f"{quota:,.2f}"
        quota_month_formated = f"{quota / 12:,.2f}"
        print(
            "*******************************************\n"
            f"r                           = {100 * r}%\n"
            f"Payment fixed annual quota  = {quota_formated}€\n"
            f"Payment fixed mensual quota = {quota_month_formated}€\n"
            f"Total Interests             = {interest_total_formated}€ "
            f"({round(100 * interest_total / loan_ammount, 2)}%)\n"
            "*******************************************\n"
        )

    # Annual calculations
    interest = []
    principal = []
    principal_balance = []
    interest_validation = []

    for n in range(1, N + 1):
        interest_n = calculate_interest_n(loan_ammount, N, n, r)
        principal_n = calculate_principal_n(loan_ammount, N, n, r)
        principal_balance_n = calculate_principal_balance_n(
            loan_ammount, N, n, r
        )

        check_calculations_interest_principal(quota, interest_n, principal_n)

        interest.append(round(interest_n, 2))
        principal.append(round(principal_n, 2))
        principal_balance.append(round(principal_balance_n, 2))
        interest_validation.append(interest_n)

    check_calculations_interest_total(interest_validation, interest_total)

    # Load a dataframe
    data = {
        "Payment": list(range(1, N + 1)),
        "Quota": [quota] * N,
        "Interest": interest,
        "Principal": principal,
        "Principal Balance": principal_balance,
    }

    df = pd.DataFrame(data)
    if verbose:
        print(df)

    # Save the DataFrame to a CSV file
    if tocsv:
        df.to_csv(csv_file, index=False)
        print(f"\n{ut.st('OK', f'{csv_file} has been saved')}.")

    # Plot
    if plot:
        plt.figure(1)
        plt.title("Loan Evolution")
        plt.xlabel("N (years of loan)")
        plt.ylabel("Eur(€)")
        axis_x = range(1, N + 1)

        quota_bar = plt.bar(axis_x, quota, label="Principal", color="g")
        interest_bar = plt.bar(
            axis_x, interest, label="Interest", color="orange"
        )

        plt.xticks(
            axis_x
        )  # Set the tick labels to be the same as the values of axis_x

        plt.legend()  # Add a legend

        # Add value labels on top of the bars
        for bar in quota_bar:
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval,
                f"{yval:,.0f}€",
                ha="center",
                va="bottom",
            )

        for bar in interest_bar:
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval,
                f"{yval:,.0f}€",
                ha="center",
                va="bottom",
            )

        plt.show()
