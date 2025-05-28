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

## Project Structure
clinical-protocol-ai-review/ \
├── README.md                
├── requirements.txt         
├── streamlit_app.py          
├── agents/                    \
│   ├── protocol_generator.py \
│   ├── pi_agent.py           \
│   ├── site_physician_agent.py \
│   └── health_authority_agent.py \
├── mcp_interface/            
│   ├── protocol_server.py   
│   └── review_tools.py     
├── templates/                
│   ├── ich_templates/        
│   └── fda_templates/        
├── utils/                    
│   ├── document_processor.py \
│   ├── risk_assessor.py     
│   └── scoring_engine.py     
├── data/                     
│   └── sample_protocols/     
├── tests/                    #to be added\
├── .env                      
└── .gitignore                


## Setup and Installation

Follow these steps to set up and run the project locally.

### Prerequisites

* Python 3.8+
* An OpenAI API Key

### 1. Clone the Repository

```bash
git clone [https://github.com/pooja-k-swamy/clinical-protocol-review.git](https://github.com/pooja-k-swamy/clinical-protocol-review.git)
cd clinical-protocol-review
