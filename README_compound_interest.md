# Compound Interest Calculator

## Introduction
Loan bank calculator using the **Loan Amortization** method: https://www.investopedia.com/terms/a/amortization.asp.

Data will be calculated on an **annual basis**, as we consider:

*Number of years = Number of payments*

Monthly data can be **aproximated** dividing the anual data by 12.

> [!TIP]
> For exactly month calculation, you’ll need to divide your annual interest rate by 12, because `r` in **Loan Amortization** is always calculated annually.
>
>For example, if your annual interest rate is 3%, then your monthly interest rate will be 0.25% (0.03 annual interest rate ÷ 12 months). You'll also multiply the number of payments in your loan term by 12. For example, a four-year car loan would have 48 payments (four years × 12 months).

## Definitions
### Global
- *loan_ammount: total loan without interests.*
- *r: % of annual interest payment.*
- *N: total number of payments.*
- *quota: ammout to pay each payment.*

$$
quota = loan\_ammount \times r \times \frac{(1 + r)^N}{(1 + r)^N - 1}
$$

### Depending on payment (n)
- *total_payment(n) = quota.*
- *interest(n): ammount destined to pay interests."
- *principal(n): ammount destined to reduce the principal in payment number n.*
- *principal_balance(n): ammount of pending loan*

> [!TIP]
> `r` in **Loan Amortization** is always annually calculated.

> [!IMPORTANT]
> $n∈\mathbb{N}[{1,\space N}]$
>
> That's why in the formulas appear '*n-1*'.

$$
interest(n) = quota + (loan\_ammount \times r - quota) \times (1 + r)^{n-1}
\newline
interest(n) = loan\_ammount \times r \times (1 + r)^{n-1} - quota \times [(1 + r)^{n-1} - 1]
$$

$$ principal(n) = quota - interest(n)
\newline
principal(n) = (quota - loan\_ammount \times r) \times (1 + r)^{n-1}
\newline
principal(n) = loan\_ammount \times \frac{r \times (1 + r)^{n-1}}{(1 + r)^N - 1}
$$

$$
principal\_balance(n) = loan\_ammount - \sum_{i=1}^{n-1}{principal(i)}
\newline

principal\_balance(n) = loan\_ammount \times \frac{(1+r)^N - (1+r)^n}{(1+r)^N -1}
$$

### Total
$$
interest\_total = quota \times N - loan\_ammount
\newline
interest\_total = loan\_ammount \times (N \times r \times \frac{(1+r)^N}{(1+r)^N-1} - 1)
$$

## Usage

Configure and run the following script: [main_loan.py](main_loan.py)
