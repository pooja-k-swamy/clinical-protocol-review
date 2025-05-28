from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import json

class RiskAssessor:
    def __init__(self, llm_model="gpt-4o"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_template = PromptTemplate(
            template="""
            Analyze the following agent feedback on a clinical trial protocol.
            Identify potential amendment triggers, categorize their severity (Low, Medium, High),
            provide a concise rationale, and suggest a specific recommendation to address the issue.
            Structure your output as a JSON array of objects.

            Agent Feedback:
            {agent_feedback_json}

            Output JSON format example:
            [
                {{
                    "description": "Risk description",
                    "severity": "Low|Medium|High",
                    "rationale": "Reason for the risk",
                    "recommendation": "Suggested change or action"
                }},
                ...
            ]
            """,
            input_variables=["agent_feedback_json"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def assess_risks(self, all_feedback: dict) -> list[dict]:
        """
        Assesses amendment risks based on consolidated agent feedback.
        """
        agent_feedback_str = json.dumps(all_feedback, indent=2)
        try:
            response = self.chain.run(agent_feedback_json=agent_feedback_str)
            risks = json.loads(response)
            return risks
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from LLM response: {e}")
            print(f"LLM Response was: {response}")
            return [{"description": "Error in risk assessment format.", "severity": "High", "rationale": "LLM output not valid JSON.", "recommendation": "Check LLM prompt."}]
        except Exception as e:
            print(f"An unexpected error occurred during risk assessment: {e}")
            return [{"description": "Unexpected error during risk assessment.", "severity": "High", "rationale": str(e), "recommendation": "Review logs."}]