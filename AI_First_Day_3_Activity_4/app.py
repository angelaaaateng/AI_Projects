import os
import openai
import numpy as np
import pandas as pd
import json
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from openai.embeddings_utils import get_embedding
import faiss
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention

warnings.filterwarnings("ignore")


st.set_page_config(page_title="Amber's News Summarizer Tool", page_icon="", layout="wide")

with st.sidebar :
    st.image('AI_First_Day_3_Activity_4/images/White_AI Republic.png')
    openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    if not (openai.api_key.startswith('sk-') and len(openai.api_key)==164):
        st.warning('Please enter your OpenAI API token!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
    with st.container() :
        l, m, r = st.columns((1, 3, 1))
        with l : st.empty()
        with m : st.empty()
        with r : st.empty()

    options = option_menu(
        "Dashboard", 
        ["Home", "About Us", "Model", "AI Persona"],
        icons = ['book', 'globe', 'tools', 'person'],
        menu_icon = "book", 
        default_index = 0,
        styles = {
            "icon" : {"color" : "#dec960", "font-size" : "20px"},
            "nav-link" : {"font-size" : "17px", "text-align" : "left", "margin" : "5px", "--hover-color" : "#262730"},
            "nav-link-selected" : {"background-color" : "#262730"}          
        })


if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None  # Placeholder for your chat session initialization

# Options : Home
if options == "Home" :

   st.title('Amber\'s News Summarizer Tool')
   st.write("Welcome to the News Article Summarizer Tool, designed to provide you with clear, concise, and well-structured summaries of news articles. This tool is ideal for readers who want to quickly grasp the essential points of any news story without wading through lengthy articles. Whether you’re catching up on global events, diving into business updates, or following the latest political developments, this summarizer delivers all the important details in a brief, easily digestible format.")
   st.write("## What the Tool Does")
   st.write("The News Article Summarizer Tool reads and analyzes full-length news articles, extracting the most critical information and presenting it in a structured manner. It condenses lengthy pieces into concise summaries while maintaining the integrity of the original content. This enables users to quickly understand the essence of any news story.")
   st.write("## How It Works")
   st.write("The tool follows a comprehensive step-by-step process to create accurate and objective summaries:")
   st.write("*Analyze and Extract Information:* The tool carefully scans the article, identifying key elements such as the main event or issue, people involved, dates, locations, and any supporting evidence like quotes or statistics.")
   st.write("*Structure the Summary:* It organizes the extracted information into a clear, consistent format. This includes:")
   st.write("- *Headline:* A brief, engaging headline that captures the essence of the story.")
   st.write("- *Lead:* A short introduction summarizing the main event.")
   st.write("- *Significance:* An explanation of why the news matters.")
   st.write("- *Details:* A concise breakdown of the key points.")
   st.write("- *Conclusion:* A wrap-up sentence outlining future implications or developments.")
   st.write("# Why Use This Tool?")
   st.write("- *Time-Saving:* Quickly grasp the key points of any article without having to read through long pieces.")
   st.write("- *Objective and Neutral:* The tool maintains an unbiased perspective, presenting only factual information.")
   st.write("- *Structured and Consistent:* With its organized format, users can easily find the most relevant information, ensuring a comprehensive understanding of the topic at hand.")
   st.write("# Ideal Users")
   st.write("This tool is perfect for:")
   st.write("- Busy professionals who need to stay informed but have limited time.")
   st.write("- Students and researchers looking for quick, accurate summaries of current events.")
   st.write("- Media outlets that want to provide readers with quick takes on trending news.")
   st.write("Start using the News Article Summarizer Tool today to get concise and accurate insights into the news that matters most!")
   
elif options == "About Us" :
     st.title('News Summarizer Tool')
     st.subheader("About Us")
     st.write("# Amber Teng")
     st.image('AI_First_Day_3_Activity_4/images/jiu.gen_httpss.mj.run_12Txpfa5fM_a_portrait_of_a_24_year_old__5603fd8a-d5e6-46e5-9cf6-1267e0c864fd_0.png')
     st.write("## AI First Bootcamp Instructor")
     st.text("Connect with me via Linkedin : https://www.linkedin.com/in/angelavteng/")
     st.write("\n")


elif options == "Model" :
     st.title('Model')
     col1, col2, col3 = st.columns([1, 2, 1])

     with col2:
          News_Article = st.text_area("News Article", placeholder="News : ")
          submit_button = st.button("Generate Summary")

     if submit_button:
        with st.spinner("Generating Summary"):
             System_Prompt = """"You are a professional news article summarizer, trained to provide clear, concise, and informative summaries of news articles. Your objective is to extract and present the most crucial information in a structured format. Follow the steps below:

Step 1: Read and Analyze the Article Thoroughly
Read the entire article carefully to understand the overall context, main points, and any supporting information.
Pay attention to the 5Ws (Who, What, When, Where, Why) and the How. Focus on the main event or issue and identify key people, organizations, locations, dates, and any other relevant details.
Step 2: Extract Key Elements for the Summary
Main Event or Topic: Identify the core event, development, or issue that the article covers.
Context: Determine the background information or the circumstances surrounding the main event.
Key Figures: Highlight any important individuals, groups, or organizations involved.
Quotes and Evidence: Select one or two impactful quotes or pieces of evidence that strengthen the article's message.
Future Implications: Consider any mentioned consequences, future actions, or possible developments linked to the event.
Step 3: Structure the Summary
The summary should be concise but informative, following this structured format:

Headline: Craft a short, compelling headline (5-10 words) that captures the essence of the article.
Lead (1-2 sentences): Provide a brief introduction summarizing the main event or topic. Aim to cover the ‘What’ and ‘Who’ aspects here.
Why it Matters (1-2 sentences): Explain the significance or impact of the event. Why should the reader care about this news?
Details (2-3 sentences): Offer additional key points, such as evidence, quotes, or relevant background information that help explain the event further. Ensure this section includes important facts like ‘When’ and ‘Where.’
Zoom in (1-2 sentences): Dive into a specific element or perspective mentioned in the article that adds depth, such as a quote from an official or a unique angle on the issue.
Flashback (1 sentence): Provide a quick historical reference or a brief look back at related past events to give context.
Reality Check (1 sentence): Highlight any contrasting information or balance the report with another viewpoint if applicable.
Conclusion (1 sentence): Conclude with a sentence summarizing potential future actions, outcomes, or implications.
Step 4: Maintain Objectivity and Neutrality
Ensure that the summary is free of any bias or personal opinions. Present the information factually, with clarity and neutrality.
Use a professional and accessible tone, making the summary understandable even to readers unfamiliar with the topic.
Step 5: Format and Review the Summary
Double-check the summary to make sure it flows logically, is free of errors, and accurately reflects the key points of the article.
Verify that the length of each section is appropriate—keeping each segment brief and to the point while ensuring nothing critical is omitted.
Once you have processed the article following these steps, present the summary in the format outlined above."""
             user_message = News_Article
             struct = [{'role' : 'system', 'content' : System_Prompt}]
             struct.append({"role": "user", "content": user_message})
             chat = openai.ChatCompletion.create(model="gpt-4o-mini", messages = struct)
             response = chat.choices[0].message.content
             struct.append({"role": "assistant", "content": response})
             st.success("Insight generated successfully!")
             st.subheader("Summary : ")
             st.write(response)


elif options == "AI Persona" :
     st.title('AI Persona: Cultural Heritage Preservation and Oral History Curator Agent')
     col1, col2 = st.columns([1, 1])
    
     with col1:
        uploaded_file = st.file_uploader("Upload an image of cultural artifact", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    
     with col2:
        text_input = st.text_area("Description of cultural artifact or practice", placeholder="Enter text here...")
    
     submit_button = st.button("Process Cultural Material")

     if submit_button:
        if uploaded_file is None and not text_input:
            st.warning("Please upload an image or provide a description (or both) before processing.")
        else:
            with st.spinner("Analyzing cultural material..."):
                System_Prompt = """
                    You are a Cultural Heritage Preservation and Oral History Curator Agent, skilled at safeguarding and analyzing cultural practices, stories, and heritage materials. Your mission is to process, document, and make accessible the diverse traditions and histories of different cultures by creating informative and engaging learning materials. Follow the steps below to fulfill your objectives:

                    Step 1: Process and Categorize Cultural Materials
                    Analyze visual, audio, and text recordings of cultural practices and oral histories to identify key elements.
                    Categorize the collected data by tradition, technique, and cultural significance. Highlight unique elements such as materials used, specific methods, and notable figures.
                    Identify patterns and connections between traditions, especially how different cultural practices relate to each other over time or across regions.
                    
                    Step 2: Generate Questions and Fill Knowledge Gaps
                    Use critical listening and analysis to identify gaps in recorded narratives or techniques.
                    Generate specific follow-up questions aimed at filling these gaps, focusing on historical context, variations in technique, and cultural significance.
                    Ensure questions are crafted to elicit rich, detailed answers that add depth to the cultural narrative and address aspects like community values, symbolism, and origins.
                    
                    Step 3: Create Interactive Learning Materials
                    Based on analyzed data, develop step-by-step guides, tutorials, and visual aids that detail traditional crafting techniques or cultural practices.
                    Ensure materials are structured in a way that appeals to both learners and practitioners, combining clear explanations with historical context and cultural relevance.
                    Develop interactive formats, such as quizzes or annotated images, that make learning about the culture engaging and educational.
                    
                    Step 4: Identify Preservation Priorities
                    Conduct a risk assessment to determine which traditions, artifacts, or stories are at the highest risk of loss, and suggest preservation priorities accordingly.
                    Use cultural importance, the fragility of materials, and the scarcity of skilled practitioners as criteria for determining priorities.
                    
                    Step 5: Document and Map Cultural Patterns
                    Map the relationships between various cultural elements, identifying how specific traditions, motifs, or techniques interconnect within a culture or across different cultures.
                    Generate visual or written documentation that provides a detailed account of these cultural elements, from crafting techniques to storytelling themes.
                    Suggest modern adaptations of traditional practices that honor core elements while accommodating current contexts, making them accessible and relevant for future generations.
                    
                    Step 6: Maintain Cultural Respect and Neutrality
                    Approach each culture with respect, presenting information without imposing external biases or judgments.
                    Ensure all documentation and materials are accurate, neutral, and factually representative of the culture's intentions and values.
                    Once you have processed the cultural material following these steps, present your findings, guides, and interactive materials in a structured and culturally sensitive format. 
                """
                user_message = ""
                if uploaded_file is not None:
                    user_message += "An image of a cultural artifact has been uploaded. "
                if text_input:
                    user_message += f"Description: {text_input}"

                struct = [{'role': 'system', 'content': System_Prompt}]
                struct.append({"role": "user", "content": user_message})
                
                chat = openai.ChatCompletion.create(model="gpt-4o-mini", messages=struct)
                response = chat.choices[0].message.content
                struct.append({"role": "assistant", "content": response})
                
                st.success("Analysis completed successfully!")
                st.subheader("Cultural Analysis:")
                st.write(response)
