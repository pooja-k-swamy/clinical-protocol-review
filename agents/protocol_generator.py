from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os


class ProtocolGenerator:
    def __init__(self, llm_model="gpt-4o"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))
        # Placeholder for dynamic template loading
        self.base_template = """
        You are an AI assistant specialized in drafting clinical trial protocols.
        Generate a clinical protocol based on the following details and follow ICH/FDA guidelines implicitly.

        Study Title: {study_title}
        Indication: {indication}
        Objectives: {objectives}

        ---
        **1. Introduction**
        [Elaborate on the disease background, unmet medical need, and rationale for the study.]

        **2. Study Objectives**
        [Expand on the primary and secondary objectives.]

        **3. Study Design**
        [Describe the study type (e.g., randomized, double-blind, placebo-controlled), phases, duration, and patient population.]

        **4. Study Population**
        [Inclusion and Exclusion Criteria.]

        **5. Study Procedures**
        [Outline visits, assessments, interventions, and data collection.]

        **6. Statistical Considerations**
        [Sample size, endpoints, statistical methods.]

        **7. Safety Reporting**
        [Adverse events, serious adverse events, reporting procedures.]

        **8. Ethical Considerations**
        [Informed consent, IRB/IEC approval.]

        **9. Data Management and Quality Control**
        [Data capture, quality assurance.]

        **10. References**
        [Placeholder for references.]
        ---
        """

    def load_template(self, template_path: str):
        """Loads a template from a specified path."""
        try:
            with open(template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: Template not found at {template_path}. Using default base template.")
            return self.base_template

    def generate_protocol_draft(self, study_title: str, indication: str, objectives: str, template_path: str = None) -> str:
        if template_path:
            template = self.load_template(template_path)
        else:
            template = self.base_template

        prompt = PromptTemplate(
            template=template,
            input_variables=["study_title", "indication", "objectives"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(
            study_title=study_title,
            indication=indication,
            objectives=objectives
        )
        return response