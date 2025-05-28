from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mcp_interface.protocol_server import ProtocolServer
import os


class HealthAuthorityAgent:
    def __init__(self, llm_model="gpt-4o"):
        """
        Initializes the HealthAuthorityAgent with an LLM and a specific prompt.
        """
        self.llm = ChatOpenAI(model=llm_model, temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_template = PromptTemplate(
            template="""
            You are a Health Authority/Regulatory Compliance Agent reviewing a clinical trial protocol.
            Your focus is on adherence to regulatory guidelines (ICH-GCP, FDA, EMA as applicable), ethical considerations, and data integrity.
            Identify any potential issues that could lead to amendments, suggest improvements, and provide a clear rationale.
            Provide your feedback as a section-level summary for each area of concern.

            Review the following protocol content:
            ---
            {protocol_content}
            ---

            Provide your feedback in a structured format, highlighting concerns and recommendations.
            Focus on these key areas, and for each, provide a summary of potential issues and regulatory-compliant recommendations for improvement.
            If a section has no major concerns from your perspective, state "No major concerns for this section."

            **1. Compliance with Regulatory Guidelines (ICH-GCP, FDA, EMA):**
            [Assess if all relevant sections conform to international and regional regulatory requirements.]

            **2. Adequacy of Informed Consent Process:**
            [Review whether the informed consent process is clearly defined, addresses all necessary elements, and ensures patient understanding and voluntary participation.]

            **3. Data Management and Quality Assurance Procedures:**
            [Evaluate the robustness of data collection, handling, validation, and storage procedures to ensure data integrity and traceability.]

            **4. Statistical Analysis Plan Rigor and Appropriateness:**
            [Assess if the statistical methods are appropriate for the study objectives and endpoints, and if the sample size justification is sound from a regulatory perspective.]

            **5. Safety Reporting Mechanisms and Adverse Event Definitions:**
            [Verify that AE/SAE definitions, reporting timelines, and follow-up procedures are clear, compliant with regulations, and ensure patient safety monitoring.]

            **6. Overall Ethical Soundness:**
            [Review the ethical aspects of the study design, including patient welfare, risks vs. benefits, vulnerable populations, and privacy safeguards.]

            **7. Any Ambiguities in Regulatory Phrasing:**
            [Identify any language that could be interpreted differently or is not precise enough for regulatory clarity.]

            Example output format for a concern:
            **1. Compliance with Regulatory Guidelines (ICH-GCP, FDA, EMA):**
            Concern: The protocol does not explicitly state adherence to ICH-GCP principles in the ethical considerations section, which is a standard regulatory expectation.
            Recommendation: Add a statement affirming compliance with ICH Harmonised Tripartite Guideline for Good Clinical Practice (ICH-GCP).

            Now provide your full review based on the protocol:
            """,
            input_variables=["protocol_content"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def review_protocol(self, protocol_server: ProtocolServer) -> str:
        """
        Reviews the clinical protocol from a Health Authority/Regulatory Compliance perspective.
        Args:
            protocol_server: An instance of ProtocolServer to access protocol content.
        Returns:
            A string containing the health authority's feedback and recommendations.
        """
        # For section-level summary, we still give the full protocol context for now
        # but the agent is prompted to focus on certain aspects.
        full_protocol = protocol_server.get_all_content()
        response = self.chain.run(protocol_content=full_protocol)
        return response