import streamlit as st
import pandas as pd
raw_dataset = pd.read_csv("raw_datas_job_postings.csv")
parsed_dataset = pd.read_csv("Parsed_dataset.csv")
st.write("# Web Scraped Job posting Analysis")
st.write("####  From Onlinejobs.ph")
st.write("#####  Author: John Jefferson B. Leonardo")
st.write("""This report investigates the **Philippine Data Analyst job market** by scraping 200 job posting from Onlinejobs.ph.
The purpose of this report is to answer:
- What is the most sought after skill for a DA position
- What Qualifications are the most relevant
- How much is the average salary for eac Responsibilities DA positions has
""")
st.write("The Job posting infos that will be used to perform this analysis are:")
st.write("""
- Job Title
- Job Type
- Work hours
- Skills
- Qualifications
- Responsibilities
""")
st.write("### Metrics")
metric1, metric2, metric3 = st.columns(3)
metric1.metric("Total Postings", str(raw_dataset.shape[0]))
metric2.metric("Average Salary per Hour", str(parsed_dataset["Salary"].mean()))
st.write("### Here is the raw scraped Dataset")
st.write(raw_dataset)
st.write("## Description Parsing")
st.write("the column **Description** will be parsed with an array of keywords in order to get the Skills, Qualification, and Responsibility given from each Job Posting")

st.write("The given keywords were obtained from Claude-AI and were reviewed manually")
skills = [
    "SQL", "Python", "Excel", "Tableau", "Power BI"," BI",
    "Visual", "Statistic", "Machine Learning", " ML ", " AI", "Artificial Intelligence",
    "Cleaning", "Wrangling", "ETL", "Big Data", "Data Modeling",
    "Intelligence", "Reporting", "Dashboard", "A/B",
    "Predictive", "Data Mining", "Google Sheet","Google Analytics", "Looker",
    "Snowflake", "Spark", "Hadoop", "Critical Thinking", "Problem Solving",
    "Communication", "Stakeholder", "Management", "Governance", "KPI",
    "Metrics", "Pipeline", "Warehouse", "Azure", "AWS", "GCP",
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter", "Git",
    "Storytelling", "Regression", "Hypothesis",
    "Strategy", "spreadsheet"
]

responsibility = [
    "analyze", "report", "dashboards", "trends", "insights",
    "decision-making", "collaborate", "clean", "organize", "monitor",
    "present", "findings", "track", "KPI", "build", "interpret",
    "gather requirements", "automate", "accuracy", "datasets", "analysis",
    "visual", "solve", "business problems", "communicate", "metrics",
    "validation", "stakeholders", "extract", "transform", "load", "query",
    "document", "forecast", "trends"
]

qualifications = [
    "bachelor's degree", "master's degree", "mathematics", "computer science",
    "engineering", "economics", "information technology", "data science",
    "proven experience", "demonstrated experience", "strong analytical skills",
    "proficiency", "familiarity", "experience", "hands-on experience",
    "excellent communication skills", "detail-oriented", "self-motivated",
    "team player", "fast learner", "critical thinker", "problem solver",
    "results-driven", "data-driven", "certifications", "Google Data Analytics",
    "Microsoft Certified", "AWS Certified", "Tableau Desktop Specialist",
    "portfolio", "project", "internship", "entry-level", "mid-level",
    "senior-level", "internet connection"
]
col1, col2, col3 = st.columns(3)

with col1:
    st.write("### Skills")
    for items in skills:
        st.write(items)
with col2:
    st.write("### Qualifications")
    for items in qualifications:
        st.write(items)
with col3:
    st.write("### Responsibility")
    for items in responsibility:
        st.write(items)

st.write("After the **Description** were parsed, new **Dataset** will be created with 3 new columns that holds an array of values **[Skills, Qualifications, Responsibilities]** hence the column Description will be removed")
st.write(parsed_dataset)
st.write("for the purpose of individual investigation of each columns that has a nested datas, the next step would be focusing on splitting them")
st.write("## Splitting the columns")
st.write("### 3 Derived table from the main dataset")
st.write("These tables are already flatten from the notebook")
skills_table = pd.read_csv("Skills_table.csv")
qualifications_table = pd.read_csv("Qualifications_table.csv")
responsibilities_table = pd.read_csv("Responsibilities_table.csv")

tab1, tab2, tab3 = st.tabs(["Skills", "Qualifications", "Responsibilities"])
with tab1:
    st.dataframe(skills_table)
with tab2:
    st.dataframe(qualifications_table)
with tab3:
    st.dataframe(responsibilities_table)

st.write("## EDA(Exploratory Data Analysis)")
### A bit of CLeaning for the R value
st.write("#### Whats the count of each required Skills and Qualifications mentioned in each postings?")
st.write("### Skills")
value_counts_skills = skills_table["Skills"].value_counts().reset_index()
value_counts_skills.columns = ["skill", "count"]
value_counts_skills = value_counts_skills.sort_values(ascending=False, by="count")

import matplotlib.pyplot as plt

figSkill, axSkill = plt.subplots(figsize=(10, 15))

axSkill.barh(value_counts_skills["skill"], value_counts_skills["count"])

axSkill.set_xlabel("Count")
axSkill.set_ylabel("Skill")
axSkill.set_title("Skill Frequency")

st.pyplot(figSkill)

st.write("### ***Key Observations:***")
st.write("""
- The most *Dominant* **Skill and Tool** out of 200 postings is **Excel**. 
- The following 2 skills below it, **Communication and Reporting**, focuses on the soft skills necessary for a DA position
- There is a gap between Excel and other given technical skills, but Soft skills are compact at the top, This indicates analyst are not always purely required of technical skills
         
What: Excel is still the widespread tool, even after 40 years of its initial release, used for many data analytical position. The market are still holding to a tool of which they are already akin to
""")

st.write("### Qualifications")
value_counts_qualifications = qualifications_table["Qualifications"].value_counts().reset_index()
value_counts_qualifications.columns = ["Qualifications", "Count"]
value_counts_qualifications = value_counts_qualifications.sort_values(ascending=False, by="Count")

figQual, axQual = plt.subplots(figsize=(10,15))

axQual.barh(value_counts_qualifications["Qualifications"], value_counts_qualifications["Count"])
axQual.set_xlabel("Count")
axQual.set_ylabel("Qualifications")
axQual.set_title("Qualifications Frequency")

st.pyplot(figQual)

st.write("### ***Key Observations:***")
st.write("""
- **Experience** is present in 175/200 posting, making it a prevalent qualification for each job posting
- *Portfolios & Projects* Comes at the 2nd and 3rd place, as an alternative for experience
- This indicates that experience often dominates the criteria of every job qualifiers, and projects or education coming as another gateway
         
What: Experience still is, as every other tech jobs there is, the very foundation of what employers look for as a reference to your credibility. and with that, projects, portfolios, and education still are the other ways to break through that barrier
""")

st.write("#### What is the mean of salary per hour for each job type, required hours, and responsibilities a DA position has?")

st.write("### Job type")
grouped_job_type = parsed_dataset.groupby('Job_type')["Salary"].agg(Average="mean", Count="count").reset_index().sort_values(ascending=False, by="Average")
st.bar_chart(data=grouped_job_type, x="Job_type", y="Average", horizontal=True)
st.write("### Hours per Week")
st.write("Average and Count")
grouped_Hours = parsed_dataset.groupby('Hours')["Salary"].agg(Average="mean", Count="count").reset_index().sort_values(ascending=False, by="Count")
st.write(grouped_Hours)
st.write("""
### ***Key Observations:***
- Employers often seek individuals that are willing to work full time, about 40 hours a week. In this case, companies could depend more to them considering from the agreed expected hours and job type
- Frequency of each mentioned Responsibilities for a Data Analyst have a lower Standard Deviation as oppose to other scope of this report.  """)
st.write("### Responsibilities")
st.write("Count of Responsibilities mentioned")
grouped_responsibilities = responsibilities_table.groupby('Responsibilities')["Salary"].agg(Average_Salary="mean", Count="count").reset_index().sort_values(ascending=False, by="Count")
st.write(grouped_responsibilities[["Responsibilities", "Count"]])
st.write("Average salary of Responsibilities")
st.bar_chart(data=grouped_responsibilities, x="Responsibilities", y="Average_Salary", horizontal=True, sort=True)
st.write("""
### ***Key Observations:***
- In the first five items, they could be encapsulated as soft skills, revealing that responsibilities for a DA position mostly consist of skills that arent so technical as oppose to the consensus that it is
- After this given indication, Technical skills are then mentioned. Responsibilities such as creating a dashboard, tracking datas, visuals, metrics, KPI and many more. This suggest that such positions are commonly given of task of that could help them get more business insight as oppose to the lease mentioned tech skills such as automation, forecasting, etc..""")    
