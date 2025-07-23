import streamlit as st
import google.generativeai as genai
import os
from streamlit_mermaid import st_mermaid  # install this separately

# Set up Gemini API
genai.configure(api_key=os.getenv("your_api_key"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="AI App Architecture Generator", layout="wide")
st.title("App Architecture Generator")
st.write("Enter your app idea. Let AI build your system design, tech stack, folder layout, and a visual diagram.")

# User Input
idea = st.text_area("Describe your app idea:", placeholder="e.g., A pet-sitting booking platform with payments and reviews")

if st.button("🚀 Generate Architecture"):
    if idea.strip():
        with st.spinner("Thinking like a software architect..."):
            prompt = f"""
You're a senior software architect. The user will describe a product idea.

Your task:
1. Propose the most suitable **tech stack** (frontend, backend, database, auth, payment, notifications, deployment)
2. Break the system into **key components/services**
3. Design a **folder structure** with short explanations
4. Output a **system design diagram in MermaidJS** syntax. Include:
   - Frontend
   - Backend services (auth, payments, notifications, etc.)
   - API Gateway (if needed)
   - Database
   - External APIs (email/SMS/payment gateways)
   - User roles if relevant

Now respond to this product idea:
\"""{idea}\"""
Return results clearly under these headings:
- Tech Stack
- Component Breakdown
- Folder Structure
- Mermaid Diagram (code block)
IMPORTANT: Only return valid MermaidJS code. Use "graph TD" or "flowchart TD". Follow these rules:
- Use only alphanumeric node names (e.g., FrontendApp, PaymentService)
- DO NOT use colons, emojis, or slashes
- Connect nodes using --> or --- only
- No text outside the code block

"""

            response = model.generate_content(prompt)
            output = response.text.strip()

            # Split Mermaid diagram from rest of text
            if "```mermaid" in output:
                parts = output.split("```mermaid")
                before_mermaid = parts[0]
                mermaid_code = parts[1].split("```")[0].strip()
            else:
                before_mermaid = output
                mermaid_code = "graph TD\nError[Could not generate diagram]"

            # Show results
            st.markdown(before_mermaid)
            st.subheader("System Design Diagram")
            st_mermaid(mermaid_code)
    else:
        st.warning("Please enter an app idea to proceed.")
