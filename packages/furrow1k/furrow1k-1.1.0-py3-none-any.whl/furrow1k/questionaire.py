from pydantic import BaseModel, ConfigDict, model_validator


class Prompt(BaseModel):
    model_config = ConfigDict(validate_assignment=True)  
    name: str
    question: str
    answer: float = 100_000
    default: float = 100_000

    @model_validator(mode="after")
    def validate_answer(self):
        if self.answer is None:
            return self
    
    def __str__(self) -> str:
        pass
    
    def format_question(self, **kwargs) -> str:
        pass
    
    def get_readable_answer(self) -> str:
        pass


class PromptWithOptions(Prompt):
    model_config = ConfigDict(validate_assignment=True)  
    name: str
    question: str
    options: list[str]
    answer: int = None
    default: int = 1

    @model_validator(mode="after")
    def validate_answer(self):
        if self.answer is None:
            return self
        elif not (1 <= self.answer <= len(self.options)):
            raise ValueError(f"Please pick an option in the range: [1, {self.n_options}].")

    @property
    def n_options(self):
        return len(self.options)
    
    def __str__(self) -> str:
        result = f"{self.question}"
        for ii, option in enumerate(self.options):
            result += f"\n\t{ii + 1} - {option}"
        result += f"\nChoose from [{'/'.join(str(x) for x in range(1, self.n_options + 1))}] ({self.default}): """
        return result
    
    def format_question(self, progress: str = "") -> str:
        result = f"\n{progress}{self.question}"
        for ii, option in enumerate(self.options):
            result += f"\n\t{ii + 1} - {option}"
        result += f"\nChoose from [{'/'.join(str(x) for x in range(1, self.n_options + 1))}] ({self.default}): """
        return result
    
    def get_readable_answer(self) -> str:
        # Offset by one since answers are between 1 and `len(self.options)`
        return self.options[self.answer - 1]


class PromptWithFloats(Prompt):
    model_config = ConfigDict(validate_assignment=True)  
    name: str
    question: str
    answer: float = None
    default: float = 100_000
    format_: str = "${x:,.2f}"

    @model_validator(mode="after")
    def validate_answer(self):
        if self.answer is None:
            return self
    
    def __str__(self) -> str:
        result = f"\n{self.question}"
        result += f"\n\nEnter amount (e.g. '100_000', '100,000', 100000): """
        return result

    def format_question(self, progress: str = "") -> str:
        result = f"\n{progress}{self.question}"
        result += f"\n\nEnter amount (e.g. '100_000', '100,000', 100000): """
        return result
    
    def get_readable_answer(self) -> str:
        # Offset by one since answers are between 1 and `len(self.options)`
        return self.format_.format(x=self.answer)

class Questionaire(BaseModel):
    prompts: list[Prompt]
    answers: dict[str, Prompt] = None

    @property
    def n_prompts(self) -> int:
        return len(self.prompts)
    
    def run(self) -> None:
        answers = {}
        for ii, question in enumerate(self.prompts):
            progress = f"[{ii + 1}/{self.n_prompts}] " 
            name = question.name
            answer = self.ask_question(question, progress)
            answers[name] = answer
        self.answers = answers

    def get_prompt(self, name: str) -> str:
        if self.answers is None:
            raise ValueError("Run questionaire to get answers.")
        prompt = self.answers.get(name)
        return prompt

    def get_answer(self, name: str) -> str:
        prompt = self.get_prompt(name)
        return prompt.answer
        
    def ask_question(self, prompt: Prompt, progress: str) -> Prompt:
        while True:
            try:
                formatted_question = prompt.format_question(progress)
                
                answer = input(formatted_question)
                if answer == "":
                    prompt.answer = prompt.default
                else:
                    prompt.answer = answer
                print("\t", prompt.get_readable_answer())
            except KeyboardInterrupt:
                print("\nAborted!")
                exit()
            except:
                print(f"\n\nPlease choose a valid option.")
            else:
                break
        
        return prompt