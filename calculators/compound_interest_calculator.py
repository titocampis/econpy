# Suppress specific warning for matplotlib with WSL
import warnings

warnings.filterwarnings(
    "ignore", message="Unable to import Axes3D", category=UserWarning
)

import matplotlib.pyplot as plt
import pandas as pd

import utilities as ut


def calculate_balance(
    N: int,
    monthly_contribution: int,
    r: float = 0.06,
    init_contribution: int = 0,
):
    """
    Method to calculate balance in compound interest

    Parameters:
    N (int): balance at month N.
    monthly_contribution (int).
    r (float): expected benefit ratio.
    init_contribution (int).
    """
    balance = init_contribution * (1 + r / 12) ** (
        12 * N
    ) + monthly_contribution * ((1 + r / 12) ** (12 * N) - 1) / (r / 12) * (
        1 + r / 12
    )

    return balance


def calculate_compound(
    N: int,
    monthly_contribution: int,
    r: float = 0.06,
    init_contribution: int = 0,
    tocsv: bool = True,
    csv_file: str = "files/compound_interest.csv",
    verbose: bool = False,
    plot: bool = False,
):
    """
    Method to calculate compound interest when investing

    Parameters:
    N (int): number of years investing.
    r (float): average % of annual benefit.
    init_contribution (int): initial contribution.
    tocsv (bool): if results want to be exported to a csv.
    csv_file (str): name of the csv file.
    verbose (bool)
    plot (bool)

    Return:
    data (dict)
    """
    # Vars
    N_range = range(1, N + 1)
    year_contribution = 12 * monthly_contribution

    total_contributed = []
    annual_benefit = []
    annual_balance = []

    # Calculate
    for n in range(1, N + 1):
        total_contributed.append(init_contribution + year_contribution * n)
        balance = calculate_balance(
            n, monthly_contribution, r, init_contribution
        )
        annual_balance.append(round(balance, 2))
        annual_benefit.append(
            round(balance - init_contribution - year_contribution * n, 2)
        )

    # Load a dataframe
    data = {
        "Year": list(range(1, N + 1)),
        "Contribution": [year_contribution] * N,
        "Contributed": total_contributed,
        "Balance": annual_balance,
        "Benefit": annual_benefit,
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
        plt.title(f"Compound interest in {N} years")
        plt.xlabel("N (years)")
        plt.ylabel("Euros")

        axis_x = N_range
        balance_bar = plt.bar(
            axis_x, annual_balance, label="Benefit", color="g"
        )
        contributed_bar = plt.bar(
            axis_x, total_contributed, label="Contributed", color="b"
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

        plt.show()

    return data
