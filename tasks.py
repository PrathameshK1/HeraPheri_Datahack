from crewai import Task
from agents import (
    research_analyst_agent,
    portfolio_manager_agent,
    risk_manager_agent,
)

research_task = Task(
    description="""
    Conduct in-depth analysis of company infrastructure and security practices. This includes:
    - Utilizing NLP techniques to analyze infrastructure documentation and identify potential security gaps.
    - Generating detailed security reports including risk assessments, vulnerability analyses, and compliance checks.
    - Delivering comprehensive insights to the Security Manager for strategy development.
    - Generating follow-up questions to probe areas needing clarification in security practices.
    Provide a detailed research report with your findings and analysis.
    """,
    expected_output="""
    A comprehensive research report on the company's infrastructure and security practices including:
    - Analysis of infrastructure documentation
    - Identification of potential security gaps
    - Risk assessments and vulnerability analyses
    - Compliance checks
    - Follow-up questions for further clarification
    """,
    agent=research_analyst_agent,
)

portfolio_management_task = Task(
    description="""
    Based on the research report provided, develop and implement security strategies. Your task includes:
    - Assessing security conditions, risk levels, and overall threat landscape.
    - Making decisions on security resource allocation and implementation of security measures.
    - Adjusting strategies for both immediate and long-term security goals.
    - Communicating with the Risk Manager to ensure all risk factors are adequately considered.
    - Calculating real-time risk scores for each security decision, providing an immediate snapshot of the organization's security profile.
    - Generating comprehensive reports with actionable recommendations, prioritizing high-risk areas for immediate attention.
    - Conducting dynamic and context-aware questioning to identify potential vulnerabilities in security strategies.
    - Verifying security practices against relevant industry standards and compliance requirements.
    Prepare a detailed security strategy proposal.
    """,
    expected_output="""
    A security strategy proposal including:
    - Security condition assessment
    - Risk level and threat landscape analysis
    - Resource allocation and implementation plans
    - Real-time risk scores
    - Actionable recommendations
    - Dynamic questioning results
    - Compliance verification
    """,
    agent=portfolio_manager_agent,
)

risk_assessment_task = Task(
    description="""
    Evaluate the risks associated with the proposed security measures. Your assessment should include:
    - Analyzing organizational exposure and conducting threat assessments.
    - Ensuring the organization stays within defined risk thresholds.
    - Monitoring ongoing risks after security measure implementation.
    - Adjusting risk thresholds based on threat landscape changes.
    - Reporting potential issues to the Security Manager that might require security posture adjustments.
    - Minimizing security risks while maximizing operational efficiency.
    - Performing dynamic and context-aware questioning to identify potential vulnerabilities or gaps in risk management.
    - Assessing infrastructure documentation to identify security gaps and generate follow-up questions.
    - Calculating a total risk score based on the sum of all risk scores across different security domains.
    - Verifying the organization's security practices against common compliance standards like GDPR or HIPAA.
    - Generating a comprehensive security report with actionable recommendations after 10-15 questions.
    Prepare a comprehensive risk assessment report.
    """,
    expected_output="""
    A comprehensive risk assessment report including:
    - Organizational exposure analysis
    - Threat assessment results
    - Ongoing risk monitoring
    - Risk threshold adjustments
    - Identified potential issues
    - Risk minimization strategies
    - Dynamic questioning results
    - Infrastructure documentation assessment
    - Total risk score calculation
    - Compliance verification
    - Actionable recommendations
    """,
    agent=risk_manager_agent,
    output_file="investment_risk_analysis.md",
)
