from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mcp_interface.protocol_server import ProtocolServer
import os

class SitePhysicianAgent:
    def __init__(self, llm_model="gpt-4o"):
        """
        Initializes the SitePhysicianAgent with an LLM and a specific prompt.
        """
        self.llm = ChatOpenAI(model=llm_model, temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_template = PromptTemplate(
            template="""
            You are a Site Physician reviewing a clinical trial protocol.
            Your focus is on the practical implementation at a clinical site, patient management, and operational challenges.
            Identify any potential issues that could lead to amendments, suggest improvements, and provide a clear rationale.
            Provide your feedback as a section-level summary for each area of concern.

            Review the following protocol content:
            ---
            {protocol_content}
            ---

            Provide your feedback in a structured format, highlighting concerns and recommendations.
            Focus on these key areas, and for each, provide a summary of potential issues and practical recommendations for improvement.
            If a section has no major concerns from your perspective, state "No major concerns for this section."

            **1. Practicality of Inclusion/Exclusion Criteria:**
            [Assess if criteria are easily verifiable and don't overly restrict recruitment or burden staff.]

            **2. Feasibility of Study Procedures and Visit Schedules:**
            [Evaluate if the required procedures (e.g., lab tests, imaging, specific assessments) and their frequency are realistic for a busy clinical setting and manageable for patients.]

            **3. Resource Requirements:**
            [Consider demands on site staff (nurses, coordinators), equipment availability, and clinic space/time.]

            **4. Patient Burden and Adherence:**
            [Assess the overall burden on patients (e.g., number of visits, invasiveness of procedures, duration of study) and potential impact on adherence.]

            **5. Clarity of Dosing, Administration, and Monitoring Instructions:**
            [Ensure drug administration details, concomitant medication rules, and safety monitoring instructions are unambiguous for site staff.]

            **6. Logistics of Drug Supply and Accountability:**
            [Review procedures for receiving, storing, dispensing, and returning investigational product, as well as accountability requirements.]

            **7. Overall Operational Workflow:**
            [Any other operational challenges or potential bottlenecks in the study flow.]

            Example output format for a concern:
            **1. Practicality of Inclusion/Exclusion Criteria:**
            Concern: The exclusion criteria regarding "history of any psychiatric disorder" is too broad and could exclude many otherwise eligible patients, impacting recruitment.
            Recommendation: Specify which psychiatric disorders are relevant (e.g., unstable, severe psychiatric disorders requiring hospitalization within 6 months).

            Now provide your full review based on the protocol:
            """,
            input_variables=["protocol_content"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def review_protocol(self, protocol_server: ProtocolServer) -> str:
        """
        Reviews the clinical protocol from a Site Physician's perspective.
        Args:
            protocol_server: An instance of ProtocolServer to access protocol content.
        Returns:
            A string containing the site physician's feedback and recommendations.
        """
        # For section-level summary, we still give the full protocol context for now
        # but the agent is prompted to focus on certain aspects.
        full_protocol = protocol_server.get_all_content()
        response = self.chain.run(protocol_content=full_protocol)
        return response