import streamlit as st
import requests

st.set_page_config(page_title="BeSman Script Generator", layout="wide")

def main():
    st.title("Script Generator")
    st.write("Generate  environments, scripts and playbooks")
    
    # Create two columns for environment scripts and playbooks
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Environment Script Generator")
        st.write("""
        Create environment scripts that define:
        - Required components
        - Dependencies
        - Configurations
        - Setup commands
        """)
        
        env_requirements = st.text_area(
            "Describe your environment requirements",
            height=150,
            placeholder="Example: Python 3.8 development environment with pip, virtualenv, and common data science packages including pandas, numpy, and scikit-learn",
            key="env_input"
        )
        
        if st.button("Generate Environment Script"):
            if env_requirements:
                with st.spinner("Generating environment script..."):
                    try:
                        response = requests.post(
                            "http://127.0.0.1:5002/generate/environment",
                            json={"requirements": env_requirements}
                        )
                        if response.status_code == 200:
                            script = response.json().get("script", "")
                            st.subheader("Generated Environment Script")
                            st.code(script, language="bash")
                            st.write("Copy this script and save it as a .sh file in your BeSman environment directory.")
                        else:
                            st.error("Failed to generate script!")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {e}")
            else:
                st.warning("Please enter environment requirements.")
    
    with col2:
        st.header("Playbook Generator")
        st.write("""
        Create playbooks that define:
        - Series of tasks
        - Execution order
        - Error handling
        - Workflow automation
        """)
        
        playbook_requirements = st.text_area(
            "Describe your playbook requirements",
            height=150,
            placeholder="Example: Deploy a web application with the following steps: install dependencies, run tests, build Docker image, push to registry, and deploy to Kubernetes",
            key="playbook_input"
        )
        
        if st.button("Generate Playbook"):
            if playbook_requirements:
                with st.spinner("Generating playbook..."):
                    try:
                        response = requests.post(
                            "http://127.0.0.1:5002/generate/playbook",
                            json={"requirements": playbook_requirements}
                        )
                        if response.status_code == 200:
                            script = response.json().get("script", "")
                            st.subheader("Generated Playbook")
                            st.code(script, language="bash")
                            st.write("Copy this script and save it as a .sh file in your  playbooks directory.")
                        else:
                            st.error("Failed to generate script!")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {e}")
            else:
                st.warning("Please enter playbook requirements.")

if __name__ == "__main__":
    main()