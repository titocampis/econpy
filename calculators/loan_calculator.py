import pandas as pd

import utilities as ut


def calculate_loan(
    loan_ammount: int,
    N: int,
    r: float = 0.06,
    tocsv: bool = True,
    csv_file: str = "files/loan.csv",
    verbose: bool = False,
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

    Returns:
    None
    """
    # Calculate Quota and interest_total
    quota = loan_ammount * r * (1 + r) ** N / ((1 + r) ** N - 1)
    interest_total = quota * N - loan_ammount

    # Print Values
    if verbose:
        interest_total_formated = f"{interest_total:,.2f}"
        quota_formated = f"{quota:,.2f}"
        quota_month_formated = f"{quota / 12:,.2f}"
        print(
            "*******************************************\n"
            f"Payment fixed annual quota: {quota_formated}€\n"
            f"Payment fixed mensual quota: {quota_month_formated}€\n"
            f"Total Interests: {interest_total_formated}€ "
            f"({round(100 * interest_total / loan_ammount, 2)}%)\n"
            "*******************************************\n"
        )

    # Annual calculations
    interest = []
    principal = []
    principal_balance = []
    interest_validation = []

    for n in range(1, N + 1):
        interest_n = loan_ammount * r * (1 + r) ** (n - 1) - quota * (
            (1 + r) ** (n - 1) - 1
        )

        principal_n = loan_ammount * r * (1 + r) ** (n - 1) / ((1 + r) ** N - 1)
        principal_balance_n = loan_ammount * (
            ((1 + r) ** N - (1 + r) ** (n - 1)) / ((1 + r) ** N - 1)
        )

        interest.append(round(interest_n, 2))
        principal.append(round(principal_n, 2))
        principal_balance.append(round(principal_balance_n, 2))
        interest_validation.append(interest_n)

        if abs(quota - interest_n - principal_n) > 1e-9:
            error_msg = (
                "Something went wrong validating the calculations, "
                "quota != interest - principal, please check the script."
            )
            print(ut.st("error", error_msg))
            exit(1)

        if abs(sum(interest_validation) - interest_total) > 1e-7:
            error_msg = (
                "Something went wrong validating the calculations, "
                "sum(interests) != interest_total (calculated with formula), "
                "please check the script."
            )
        else:
            print(f"{ut.st('OK', 'Validation successfully passed.')}\n")

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
