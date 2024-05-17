import datetime as dt
from textwrap import dedent

import numpy as np
from pydantic import BaseModel, ConfigDict, model_validator
from questionaire import Questionaire, PromptWithFloats, PromptWithOptions

LIMITS_401K = {2023: 22_500, 2024: 23_000}
DAY_OF_WEEK_FRI = 5


def get_pay_per_period(annual_salary: float, n_pay_periods: float) -> float:
    result = annual_salary / n_pay_periods

    return result


def get_remaining_n_pay_days(pay_periods: np.ndarray) -> int:
    today = dt.date.today()
    result = (pay_periods > today).sum()

    return result


def get_pay_per_paycheck(annual_salary: float, n_pay_periods: int) -> float:
    result = annual_salary / n_pay_periods

    return result


def get_remaining_pay(annual_salary: float, remaining_n_pay_days: int) -> float:
    result = annual_salary * remaining_n_pay_days / 26.0

    return result


def get_payday_dates(dt_next_pay: str | dt.date) -> np.ndarray:
    if isinstance(dt_next_pay, str):
        dt_next_pay = dt.datetime.strptime(dt_next_pay, "%Y-%m-%d")
    parity = dt_next_pay.isocalendar().week % 2
    year = dt_next_pay.year
    
    result = np.array(
        [
            dt.date.fromisocalendar(year, week, DAY_OF_WEEK_FRI) 
            for week in range(1, 53) if week % 2 == parity
        ],
        dtype="datetime64[D]"
    )

    return result


def get_contribution_pct_401k(
    remaing_401k: float, annual_salary: float
) -> float:
    result = remaing_401k / annual_salary

    return result


def main():
    # Get next paycheck date to see if paychecks come on odd or even weeks
    today = dt.datetime.today()
    year = today.year
    week = today.isocalendar().week
    
    this_friday = dt.date.fromisocalendar(year, week, DAY_OF_WEEK_FRI)
    next_friday = this_friday + dt.timedelta(weeks=1)

    # Set up questions and options
    prompts = [
        PromptWithOptions(
            name="cadence",
            question="Is your paycheck bi-weekly or monthly?", 
            options=[f"Bi-Weekly"],
        ),
        PromptWithOptions(
            name="parity",
            question="Is your paycheck this Friday or the next Friday?", 
            options=[f"{this_friday}", f"{next_friday}"]
        ),
        PromptWithFloats(
            name="salary",
            question="What is your gross annual salary?",
            default=100_000,
        ),
        PromptWithFloats(
            name="contributed",
            question="How much have you already contributed to your 401k?", 
            default=0,
        ),
    ]

    # Run questionaire; retrieve answers
    questionaire = Questionaire(prompts=prompts)
    questionaire.run()
    
    # Extract raw answers
    salary = questionaire.get_answer("salary")
    cadence = questionaire.get_answer("cadence")
    contributed = questionaire.get_answer("contributed")
    
    # Get formatted answer (otherwise in [1, n_options])
    next_pay_day = questionaire.get_prompt("parity").get_readable_answer()


    # Calculate helpers
    n_pay_periods = 26 if cadence == 1 else 12
    pay_day_dates = get_payday_dates(next_pay_day)
    remaining_n_pay_days = get_remaining_n_pay_days(pay_day_dates)
    remaining_pay = get_remaining_pay(salary, remaining_n_pay_days)
    salary_per_paycheck = get_pay_per_paycheck(salary, n_pay_periods)
    
    # Calculate 401k contribution
    limit_401k = LIMITS_401K.get(year)
    remaing_401k = max(0, limit_401k - contributed)
    
    # Write to output
    print(
        f"\nWith an annual salary of ${salary:,.0f}, each paycheck amount is "
        f"${salary_per_paycheck:,.2f} before any taxes or deductions."
    )
    if remaing_401k > 0:
        pct = get_contribution_pct_401k(
            remaing_401k, annual_salary=remaining_pay
        )
        print(
            f"With a remaining 401k contribution of ${remaing_401k:,.0f}, to "
            f"max out 401k contributions, use {pct:.2%} as your percent "
            "contribution."
        )
    else:
        print(
            f"No need to contribute to your 401k for the rest of the year -- "
            f"you've already reach the {year} limit! Set your contribution "
            "percentage to 0%."
        )


if __name__ == "__main__":
    main()