# Compound Interest Calculator

## Introduction
Compound interest calculator taking into account monthly periodical contributions.

## Definitions
- *init_contribution*
- *r: % of annual interest.*
- *n: number of years investing.*
- *monthly_contribution*
- *contributed: total money you have invest*
- *balance: total money you will have*
- *benefits: total money you earned investing*

$$
contributed(n) = init\_contribution + 12 \times n  \times monthly\_contribution
$$

$$
benefit(n) = balance(n) - contributed(n)
$$

#### Contributions at the Beginning of the Month:
$$
balance(n) = init\_contribution \times (1 + \frac{r}{12})^{12t}
+ monthly\_contribution \times \frac{(1 + \frac{r}{12})^{12t} - 1}{\frac{r}{12}}
\times (1 + \frac{r}{12})
$$

#### Contributions at the End of the Month:
$$
balance(n) = init\_contribution \times (1 + \frac{r}{12})^{12t}
+ monthly\_contribution \times \frac{(1 + \frac{r}{12})^{12t} - 1}{\frac{r}{12}}
$$


> ![NOTE]
> We are taking into account the **Contributions at the Beginning of the Month**

## Usage
Configure and run the following script: [main_compound_interest.py](main_compound_interest.py)
