import streamlit as st
from dotenv import load_dotenv
import os

# Assuming you have these modules implemented
from agents.protocol_generator import ProtocolGenerator
from mcp_interface.protocol_server import ProtocolServer
from agents.pi_agent import PIAgent
from agents.site_physician_agent import SitePhysicianAgent
from agents.health_authority_agent import HealthAuthorityAgent
from utils.risk_assessor import RiskAssessor
from utils.scoring_engine import ScoringEngine
from utils.document_processor import DocumentProcessor

load_dotenv() # Load environment variables

st.set_page_config(layout="wide", page_title="Clinical Protocol AI Review")

st.title("Clinical Protocol AI Review System")

# --- Protocol Generation Section ---
st.header("1. Protocol Generation")
with st.expander("Generate a New Protocol Draft"):
    st.write("Input parameters to generate a new clinical protocol draft.")
    study_title = st.text_input("Study Title", "A Phase III Study of Novel Drug X for Disease Y")
    indication = st.text_area("Indication", "Advanced metastatic solid tumors resistant to standard therapies.")
    objectives = st.text_area("Objectives", "Primary: Overall Response Rate. Secondary: Progression-Free Survival, Safety.")
    # Add more parameters as needed based on your templates

    if st.button("Generate Protocol Draft"):
        with st.spinner("Generating protocol draft..."):
            protocol_generator = ProtocolGenerator(llm_model="gpt-4o") # or your preferred model
            generated_protocol_content = protocol_generator.generate_protocol_draft(
                study_title=study_title,
                indication=indication,
                objectives=objectives,
                template_path="templates/ich_templates/ich_template_v1.md" # Placeholder
            )
            st.session_state["current_protocol"] = generated_protocol_content
            st.success("Protocol draft generated!")
            st.subheader("Generated Protocol Draft:")
            st.text_area("Protocol Content", generated_protocol_content, height=400)


# --- Protocol Upload Section ---
st.header("2. Upload Existing Protocol")
uploaded_file = st.file_uploader("Upload a clinical protocol (PDF, TXT, MD)", type=["pdf", "txt", "md"])
if uploaded_file is not None:
    with st.spinner("Processing uploaded protocol..."):
        doc_processor = DocumentProcessor()
        if uploaded_file.type == "application/pdf":
            st.session_state["current_protocol"] = doc_processor.extract_text_from_pdf(uploaded_file)
        else: # Assuming txt or md
            st.session_state["current_protocol"] = uploaded_file.read().decode("utf-8")
        st.success("Protocol uploaded and processed!")
        st.subheader("Uploaded Protocol Content:")
        st.text_area("Protocol Content", st.session_state["current_protocol"], height=400)


# --- Protocol Review Section ---
st.header("3. Multi-Agent Protocol Review")
if "current_protocol" in st.session_state and st.session_state["current_protocol"]:
    if st.button("Start Multi-Agent Review"):
        with st.spinner("Agents are reviewing the protocol..."):
            # Initialize MCP Server (to simulate structured access for agents)
            protocol_server = ProtocolServer(st.session_state["current_protocol"])

            # Initialize Agents
            pi_agent = PIAgent(llm_model="gpt-4o")
            site_physician_agent = SitePhysicianAgent(llm_model="gpt-4o")
            health_authority_agent = HealthAuthorityAgent(llm_model="gpt-4o")

            # Perform Reviews
            st.subheader("Agent Review Feedback:")
            pi_feedback = pi_agent.review_protocol(protocol_server)
            st.write(f"**Principal Investigator Agent Feedback:**\n{pi_feedback}")

            site_physician_feedback = site_physician_agent.review_protocol(protocol_server)
            st.write(f"**Site Physician Agent Feedback:**\n{site_physician_feedback}")

            health_authority_feedback = health_authority_agent.review_protocol(protocol_server)
            st.write(f"**Health Authority Agent Feedback:**\n{health_authority_feedback}")

            # Consolidate feedback (this can be done by a meta-agent or a utility)
            all_feedback = {
                "pi": pi_feedback,
                "site_physician": site_physician_feedback,
                "health_authority": health_authority_feedback
            }
            st.session_state["all_feedback"] = all_feedback

            # Risk Assessment and Scoring
            risk_assessor = RiskAssessor()
            amendment_risks = risk_assessor.assess_risks(all_feedback)
            st.subheader("Amendment Risk Assessment:")
            for risk in amendment_risks:
                st.write(f"- **Risk:** {risk['description']} (Severity: {risk['severity']})")
                st.write(f"  **Rationale:** {risk['rationale']}")
                st.write(f"  **Recommendation:** {risk['recommendation']}")

            scoring_engine = ScoringEngine()
            protocol_score = scoring_engine.score_protocol(amendment_risks)
            st.subheader("Overall Protocol Score:")
            st.success(f"The protocol scored: {protocol_score}/100")

else:
    st.info("Please generate or upload a protocol to proceed with the review.")

# --- Future Enhancements (Mentions) ---
st.sidebar.header("About This System")
st.sidebar.info(
    "This is a prototype for an AI-powered clinical protocol generation and multi-agent review system. "
    "It leverages LangChain for agentic behavior and the Model Context Protocol (MCP) for structured "
    "protocol interaction."
)