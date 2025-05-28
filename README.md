# Clinical Protocol Draft Assistant

## Overview

This project implements an Agents-powered system for drafting and reviewing clinical trial protocols. Leveraging Large Language Models (LLMs) via LangChain, it facilitates the generation of new protocol drafts and employs a multi-agent review system to identify potential amendment triggers before implementation. The system is designed to provide a structured review process, culminating in a protocol score and actionable recommendations.

The core idea is inspired by the Model Context Protocol (MCP) to enable structured interaction between AI agents and the protocol content, mimicking the collaborative review process of human experts.

## How It Works

The system comprises the following key modules:

1.  **Protocol Generator (`agents/protocol_generator.py`):**
    * Generates initial clinical protocol drafts based on user-defined parameters and predefined templates (e.g., ICH, FDA guidelines).
    * Acts as the initial "Draft Assist" component.

2.  **Model Context Protocol (MCP) Interface (`mcp_interface/protocol_server.py`):**
    * A standardized interface that exposes protocol content in a structured manner to the review agents.
    * Enables agents to access specific sections of the protocol (e.g., "Study Objectives," "Inclusion Criteria") for targeted review, simulating a more realistic interaction than providing the full text at once.
    * (Future enhancement: This will be developed to a deeper, more realistic MCP implementation, potentially involving a structured data model for protocols).

3.  **Multi-Agent Review System (`agents/*.py`):**
    * **Specialized AI Agents:** Multiple agents, each representing a subject matter expert (SME) with a unique perspective, evaluate the protocol.
        * **Principal Investigator (PI) Agent (`agents/pi_agent.py`):** Reviews for scientific rigor, study feasibility, and patient safety from a research leadership perspective.
        * **Site Physician Agent (`agents/site_physician_agent.py`):** Focuses on practical implementation at a clinical site, patient management, and operational challenges.
        * **Health Authority Agent (`agents/health_authority_agent.py`):** Assesses adherence to regulatory guidelines (ICH-GCP, FDA), ethical considerations, and data integrity.
    * **Agentic AI Framework (LangChain):** Utilizes LangChain for defining agent behavior, enabling multi-step reasoning, planning, and contextual understanding. (Future enhancement: Incorporate Chain-of-Thought, Reflection, and Self-correction for more sophisticated review).

4.  **Amendment Risk Detection & Recommendation (`utils/risk_assessor.py`):**
    * Analyzes consolidated feedback from all specialized agents.
    * Identifies potential issues that could lead to protocol amendments.
    * Provides a severity assessment (Low, Medium, High), rationale, and specific recommendations for improvement.

5.  **Scoring Engine (`utils/scoring_engine.py`):**
    * Assigns a numerical score to the protocol based on the identified risks and their severity. A higher score indicates fewer or less severe issues.

6.  **Document Processor (`utils/document_processor.py`):**
    * Handles the extraction of text content from various document formats (e.g., PDF, TXT, MD) uploaded by the user.

7.  **Streamlit Application (`streamlit_app.py`):**
    * The user-friendly interface for interacting with the system.
    * Allows users to generate new protocol drafts, upload existing protocols, trigger the multi-agent review, and view the consolidated feedback, risk assessment, and score.


## Setup and Installation

Follow these steps to set up and run the project locally.

### Prerequisites

* Python 3.8+
* An OpenAI API Key

### 1. Clone the Repository

```bash
git clone [https://github.com/pooja-k-swamy/clinical-protocol-review.git](https://github.com/pooja-k-swamy/clinical-protocol-review.git)
cd clinical-protocol-review
```

### 2. Create and Activate a Virtual Environment
Use a virtual environment to manage dependencies

```bash
python -m venv venv
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the root directory of your project and add your OpenAI API key:
```python
OPENAI_API_KEY="OPENAI_API_KEY_HERE"
```

### 5. Add Protocol Templates
The templates/ directory is structured for different guideline types. Populate templates/ich_templates/ich_template_v1.md with a basic ICH-compliant markdown protocol structure.

### 6. Run the Application
Once all setup steps are complete, run the Streamlit application from the root directory of your project:

```bash
streamlit run streamlit_app.py
```


#### Usage
1. Generate Protocol Draft: Use the "Protocol Generation" section to input basic study parameters and generate a new protocol draft using an LLM.
2. Upload Existing Protocol: Upload a protocol file (PDF, TXT, or MD) to be reviewed. The system will extract its text content.
3. Start Multi-Agent Review: Once a protocol is displayed, click "Start Multi-Agent Review". The specialized AI agents will then process the protocol, provide their feedback, and the system will present an amendment risk assessment, recommendations, and an overall score.
