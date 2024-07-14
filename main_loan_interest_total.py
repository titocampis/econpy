import matplotlib.pyplot as plt

###############################################################################
############                    Configuration                     #############
###############################################################################

loan_ammount = 100000  # total loan without interests
r = 0.03  # % of annual interest payment
N_range = range(5, 60 + 1)
# N will be the variable of study
quota_vector = []
interest_vector = []
print_data = True
plot = True
plot_data = "per"  # "per", "eur"

###############################################################################
############                         Main                         #############
###############################################################################
# Fulfilling the functions depending on N
for N in N_range:
    quota = loan_ammount * r * (1 + r) ** N / ((1 + r) ** N - 1)
    interest = quota * N - loan_ammount

    quota_vector.append(quota)
    interest_vector.append(interest)

    # Print data
    if print_data:
        print(
            f"Years: {N} | Total Interest: {round(interest, 2)}€ "
            f"({round(100 * interest / loan_ammount, 2)}%) "
            f"| Quota: {quota}(€)"
        )


# Plot €
if plot and plot_data == "eur":
    print()
    plt.title("Interest over N")
    plt.figure(1)
    plt.xlabel("N (years of loan)")
    plt.ylabel("Currency (€)")
    axis_x = N_range
    plt.plot(axis_x, interest_vector, "r", label="Interest over N")
    plt.xticks(
        axis_x
    )  # Set the tick labels to be the same as the values of axis_x
    plt.legend()  # Add a legend

    # Adjust y-axis limits and ticks
    plt.ylim(0, 10000)  # Set y-axis limits from 0 to 10000
    plt.yticks(
        range(0, 150001, 10000)
    )  # Set y-axis ticks from 0 to 10000 in steps of 1000

    # Adding horizontal lines
    thresholds = range(
        0, 150001, 10000
    )  # Example y-values where you want horizontal lines
    for threshold in thresholds:
        plt.axhline(
            y=threshold,
            color="gray",
            linestyle="-",
            linewidth=1,
            alpha=0.3,
            label=f"Threshold at {threshold}",
        )

    # Adding vertical lines with grey and soft appearance
    positions = range(
        10, 60, 10
    )  # Example x-values where you want vertical lines
    for position in positions:
        plt.axvline(
            x=position,
            color="gray",
            linestyle="-",
            linewidth=1,
            alpha=0.3,
            label=f"Position at {position}",
        )
    plt.show()

# Plot %
if plot and plot_data == "per":
    print()
    plt.figure(1)
    plt.title("Interest Over N")
    plt.xlabel("N (years of loan)")
    plt.ylabel("% interest / loan_ammount")
    axis_x = N_range
    interest_vector_per = [100 * x / loan_ammount for x in interest_vector]
    plt.plot(axis_x, interest_vector_per, "r", label="% Interest over N")
    plt.xticks(
        axis_x
    )  # Set the tick labels to be the same as the values of axis_x
    plt.legend()  # Add a legend

    # Adjust y-axis limits and ticks
    plt.ylim(0, 100 + 1)  # Set y-axis limits from 0 to 10000
    plt.yticks(
        range(0, 100 + 1, 10)
    )  # Set y-axis ticks from 0 to 10000 in steps of 1000

    # Adding horizontal lines
    thresholds = range(
        0, 100, 10
    )  # Example y-values where you want horizontal lines
    for threshold in thresholds:
        plt.axhline(
            y=threshold,
            color="gray",
            linestyle="-",
            linewidth=1,
            alpha=0.3,
            label=f"Threshold at {threshold}",
        )

    # Adding vertical lines with grey and soft appearance
    positions = range(
        10, 60, 10
    )  # Example x-values where you want vertical lines
    for position in positions:
        plt.axvline(
            x=position,
            color="gray",
            linestyle="-",
            linewidth=1,
            alpha=0.3,
            label=f"Position at {position}",
        )
    plt.show()
