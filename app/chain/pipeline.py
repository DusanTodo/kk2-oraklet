from app.chain.steps import PromptBuilder, LLMRunner, ResponseParser

# sammansätter hela kedjan med | operatorn
ask_pipeline = PromptBuilder() | LLMRunner() | ResponseParser()