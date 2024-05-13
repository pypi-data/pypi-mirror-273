import datetime as dt
from textwrap import dedent

import numpy as np
from pydantic import BaseModel, ConfigDict, model_validator

LIMITS_401K = {2023: 22_500, 2024: 23_000}
DAY_OF_WEEK_FRI = 5

class Question(BaseModel):
    model_config = ConfigDict(validate_assignment=True)  
    question: str
    answer: float = 100_000
    default: float = 100_000
    i_question: int = None
    n_questions: int = None

    @model_validator(mode="after")
    def validate_answer(self):
        if self.answer is None:
            return self
    
    def __str__(self) -> str:
        result = f"\n{self.question}"
        result += f"\n\nEnter amount (e.g. '100_000', '100,000', 100000): """
        return result
    
    def get_readable_answer(self) -> str:
        # Offset by one since answers are between 1 and `len(self.options)`
        return self.answer

class Questionaire(BaseModel):
    questions: list[Question]

    @property
    def n_questions(self) -> int:
        return len(self.questions)


class QuestionAnswer(Question):
    model_config = ConfigDict(validate_assignment=True)  
    question: str
    options: list[str]
    answer: int = None
    default: int = 1

    @property
    def i_options(self):
        return [str(ii + 1) for ii, _ in enumerate(self.options)]

    @model_validator(mode="after")
    def validate_answer(self):
        if self.answer is None:
            return self
        elif not (1 <= self.answer <= len(self.options)):
            raise ValueError(f"Please pick an option in the range: [1, {len(self.options)}].")
    
    def __str__(self) -> str:
        result = f"\n[{self.i_question}/{self.n_questions}]{self.question}"
        for ii, option in enumerate(self.options):
            result += f"\n\t{ii + 1} - {option}"
        result += f"\n\nChoose from [{'/'.join(self.i_options)}] ({self.default}): """
        return result
    
    def get_readable_answer(self) -> str:
        # Offset by one since answers are between 1 and `len(self.options)`
        return self.options[self.answer - 1]


class QuestionAnswerFree(Question):
    model_config = ConfigDict(validate_assignment=True)  
    question: str
    answer: float = 100_000
    default: float = 100_000

    @model_validator(mode="after")
    def validate_answer(self):
        if self.answer is None:
            return self
    
    def __str__(self) -> str:
        result = f"\n{self.question}"
        result += f"\n\nEnter amount (e.g. '100_000', '100,000', 100000): """
        return result
    
    def get_readable_answer(self) -> str:
        # Offset by one since answers are between 1 and `len(self.options)`
        return self.answer
    

def get_answer(qa: QuestionAnswer) -> QuestionAnswer:
    while True:
        try:
            answer = input(f"[1/2] {qa}")
            if answer == "":
                qa.answer = qa.default
            else:
                qa.answer = answer
            print("\t", qa.get_readable_answer())
        except KeyboardInterrupt:
            print("\nAborted!")
            exit()
        except:
            print(f"\n\nPlease choose a valid option.")
        else:
            break
    
    return qa


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
            for week in range(52) if week % 2 == parity
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
    questions = {
        "cadence": QuestionAnswer(
            question="Is your paycheck bi-weekly or monthly?", 
            options=[f"Bi-Weekly"],
        ),
        "parity": QuestionAnswer(
            question="Is your paycheck this Friday or the next Friday?", 
            # options=[f"This Friday ({this_friday})", f"Next Friday ({next_friday})"]
            options=[f"{this_friday}", f"{next_friday}"]
        ),
        "salary": QuestionAnswerFree(
            question="What is your gross annual salary?",
            default=100_000,
        ),
        "contributed": QuestionAnswerFree(
            question="How much have you already contributed to your 401k?", 
            default=0,
        ),
    }

    answers = questions
    for i, (k, q) in enumerate(questions.items()):
        print(i+ 1, "/", len(questions))
        result = get_answer(q)
        answers[k] = result
        
    salary = answers["salary"].answer
    n_pay_periods = 26 if answers["cadence"].answer == 1 else 12
    next_pay_day = answers["parity"].get_readable_answer()
    
    pay_day_dates = get_payday_dates(next_pay_day)
    remaining_n_pay_days = get_remaining_n_pay_days(pay_day_dates)
    remaining_pay = get_remaining_pay(salary, remaining_n_pay_days)
    salary_per_paycheck = get_pay_per_paycheck(salary, n_pay_periods)
    
    
    limit_401k = LIMITS_401K.get(year)
    remaing_401k = max(0, limit_401k - answers["contributed"].answer)
    
    print(f"\nWith an annual salary of ${salary:,.0f}, each paycheck amount is ${salary_per_paycheck:,.2f} before any taxes or deductions.")
    if remaing_401k > 0:
        pct = get_contribution_pct_401k(remaing_401k=remaing_401k, annual_salary=remaining_pay)
        print(f"With a remaining 401k contribution of ${remaing_401k:,.0f}, to max out 401k contributions, use {pct:.2%} as your percent contribution.")
    else:
        print(f"No need to contribute to your 401k for the rest of the year -- you've already reach the {year} limit! Set your contribution percentage to 0%.")


if __name__ == "__main__":
    main()