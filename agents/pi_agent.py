from langchain.chat_models import ChatOpenAI
from mcp_interface.protocol_server import ProtocolServer
import os

class PIAgent:
    def __init__(self, llm_model="gpt-4o"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_template = PromptTemplate(
            template="""
            You are a Principal Investigator reviewing a clinical trial protocol.
            Your focus is on the feasibility of the study, the scientific rigor, and patient safety from a research leadership perspective.
            Identify any potential issues that could lead to amendments, suggest improvements, and provide a clear rationale.

            Review the following protocol content:
            {protocol_content}

            Provide your feedback in a structured format, highlighting concerns and recommendations.
            Focus on:
            - Overall scientific soundness and relevance.
            - Feasibility of patient recruitment and retention.
            - Adequacy of safety monitoring and adverse event reporting.
            - Clarity and completeness of study objectives and endpoints.
            - Potential for bias or ethical concerns.
            - Any sections that are unclear or contradictory.
            """,
            input_variables=["protocol_content"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def review_protocol(self, protocol_server: ProtocolServer) -> str:
        full_protocol = protocol_server.get_all_content()
        response = self.chain.run(protocol_content=full_protocol)
        return response

# agents/site_physician_agent.py (similar structure)
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mcp_interface.protocol_server import ProtocolServer
import os

class SitePhysicianAgent:
    def __init__(self, llm_model="gpt-4o"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_template = PromptTemplate(
            template="""
            You are a Site Physician reviewing a clinical trial protocol.
            Your focus is on the practical implementation at a clinical site, patient management, and operational challenges.
            Identify any potential issues that could lead to amendments, suggest improvements, and provide a clear rationale.

            Review the following protocol content:
            {protocol_content}

            Provide your feedback in a structured format, highlighting concerns and recommendations.
            Focus on:
            - Practicality of inclusion/exclusion criteria for site staff.
            - Feasibility of study procedures and visit schedules in a clinical setting.
            - Resource requirements (staff, equipment, time).
            - Patient burden and adherence.
            - Clarity of dosing, administration, and monitoring instructions.
            - Logistics of drug supply and accountability.
            """,
            input_variables=["protocol_content"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def review_protocol(self, protocol_server: ProtocolServer) -> str:
        full_protocol = protocol_server.get_all_content()
        response = self.chain.run(protocol_content=full_protocol)
        return response

# agents/health_authority_agent.py (similar structure)
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mcp_interface.protocol_server import ProtocolServer
import os

class HealthAuthorityAgent:
    def __init__(self, llm_model="gpt-4o"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_template = PromptTemplate(
            template="""
            You are a Health Authority/Regulatory Compliance Agent reviewing a clinical trial protocol.
            Your focus is on adherence to regulatory guidelines (ICH-GCP, FDA, EMA), ethical considerations, and data integrity.
            Identify any potential issues that could lead to amendments, suggest improvements, and provide a clear rationale.

            Review the following protocol content:
            {protocol_content}

            Provide your feedback in a structured format, highlighting concerns and recommendations.
            Focus on:
            - Compliance with relevant regulatory guidelines (ICH-GCP, FDA, EMA).
            - Adequacy of informed consent process.
            - Data management and quality assurance procedures.
            - Statistical analysis plan rigor and appropriateness.
            - Safety reporting mechanisms and adverse event definitions.
            - Overall ethical soundness of the study design.
            - Any ambiguities in regulatory phrasing.
            """,
            input_variables=["protocol_content"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def review_protocol(self, protocol_server: ProtocolServer) -> str:
        full_protocol = protocol_server.get_all_content()
        response = self.chain.run(protocol_content=full_protocol)
        return response