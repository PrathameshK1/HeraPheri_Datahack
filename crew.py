from deep_translator import GoogleTranslator
from crewai import Process, Crew
from agents import (
    research_analyst_agent,
    portfolio_manager_agent,
    risk_manager_agent,
)
from tasks import research_task, portfolio_management_task, risk_assessment_task
import os

# Update the agents with the new roles and goals
research_analyst_agent.role = "Cybersecurity Analyst"
research_analyst_agent.goal = """
    - Conduct in-depth analysis of company infrastructure and security practices.
    - Utilize NLP techniques to analyze infrastructure documentation and identify potential security gaps.
    - Generate detailed security reports including risk assessments, vulnerability analyses, and compliance checks.
    - Deliver comprehensive insights to the Security Manager for strategy development.
    - Generate follow-up questions to probe areas needing clarification in security practices.
"""

portfolio_manager_agent.role = "Security Manager"
portfolio_manager_agent.goal = """
    - Develop and implement security strategies based on analysis provided by the Cybersecurity Analyst.
    - Assess security conditions, risk levels, and overall threat landscape.
    - Make decisions on security resource allocation and implementation of security measures.
    - Adjust strategies for both immediate and long-term security goals.
    - Communicate with the Risk Manager to ensure all risk factors are adequately considered.
    - Calculate real-time risk scores for each security decision, providing an immediate snapshot of the organization's security profile.
    - Generate comprehensive reports with actionable recommendations, prioritizing high-risk areas for immediate attention.
    - Conduct dynamic and context-aware questioning to identify potential vulnerabilities in security strategies.
    - Verify security practices against relevant industry standards and compliance requirements.
"""

risk_manager_agent.role = "Risk Manager"
risk_manager_agent.goal = """
    - Evaluate risks of proposed security measures by analyzing organizational exposure and conducting threat assessments.
    - Ensure the organization stays within defined risk thresholds.
    - Monitor ongoing risks after security measure implementation.
    - Adjust risk thresholds based on threat landscape changes.
    - Report potential issues to the Security Manager that might require security posture adjustments.
    - Minimize security risks while maximizing operational efficiency.
    - Perform dynamic and context-aware questioning to identify potential vulnerabilities or gaps in risk management.
    - Assess infrastructure documentation to identify security gaps and generate follow-up questions.
    - Calculate a total risk score based on the sum of all risk scores across different security domains.
    - Verify the organization's security practices against common compliance standards like GDPR or HIPAA.
    - Generate a comprehensive security report with actionable recommendations after 10-15 questions.
"""

crew = Crew(
    agents=[
        research_analyst_agent,
        portfolio_manager_agent,
        risk_manager_agent,
    ],
    tasks=[research_task, portfolio_management_task, risk_assessment_task],
    process=Process.sequential,  # Execute tasks sequentially
)


def translate_md(file_path, target_language):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        translator = GoogleTranslator(source="en", target=target_language)
        translated_content = translator.translate(content)

        translated_file_path = f"investment_risk_analysis_{target_language}.md"
        with open(translated_file_path, "w", encoding="utf-8") as file:
            file.write(translated_content)

        print(f"The translation has been completed and saved in '{translated_file_path}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    company = str(input("What company do you want to Voidra to analyze? "))
    result = crew.kickoff(inputs={"empresa": company})
    
    # Save the original report
    original_file_path = "investment_risk_analysis.md"
    with open(original_file_path, "w", encoding="utf-8") as file:
        file.write(result)
    print(f"The original report has been saved in '{original_file_path}'.")
    
    # Translate the report
    target_language = input("Enter the target language for translation (e.g., 'es' for Spanish, 'fr' for French): ")
    translate_md(original_file_path, target_language)
    
    # Create a separate translated file
    translated_file_path = f"investment_risk_analysis_{target_language}.md"
    with open(translated_file_path, "r", encoding="utf-8") as file:
        translated_content = file.read()
    
    print(f"A separate translated file has been created: '{translated_file_path}'.")
