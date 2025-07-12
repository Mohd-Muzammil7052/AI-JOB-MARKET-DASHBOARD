import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import matplotlib.pyplot as plt
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("dataset.csv")
st.set_page_config(layout='wide')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
image = Image.open('image2.png')

col1, col2 = st.columns([0.3,0.7])
with col1:
    st.image(image,caption="AI Job Market",use_container_width=True)

html_title = """
    <style>
    .title-test {
    font-weight = bold;
    padding = 5px;
    font-size: 40px;
    font-family: Arial, sans-serif;
    color: #000000;
    }
    </style>
    <center><h1 class = "title-test">AI Job Market Dashboard</h1></center>
"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4= st.columns([0.1,0.9])
with col3:
    date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last Updated by: \n {date}")


avg_salary_df = df.groupby("job_title", as_index=False)["salary_usd"].mean()
avg_salary_df = avg_salary_df.sort_values(by="salary_usd", ascending=False)
with col4:
    
    pivot_df = df.pivot_table(
    index="education_required",
    columns="job_title",
    values="salary_usd",
    aggfunc="mean"
    )

    fig = px.imshow(
        pivot_df,
        text_auto=True,
        color_continuous_scale="Blues",
        title="💸 Average Salary by Education & Job Role"
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("View Data: Education vs Salary"):
        st.write(pivot_df)
    st.download_button("Download CSV", data=pivot_df.to_csv().encode("utf-8"), file_name="Education_Salary.csv", mime="text/csv", key="edu_salary")

st.divider()

_, col5= st.columns([0.1,0.9])
with col5:
    df["posting_date"] = pd.to_datetime(df["posting_date"], errors='coerce')
    df["posting_month"] = df["posting_date"].dt.to_period("M").dt.to_timestamp()

    job_titles = sorted(df["job_title"].dropna().unique())

    selected_roles = st.multiselect(
        "Select Job Titles to View Monthly Trends",
        options=job_titles,
        default=job_titles[:5],
    )

    filtered_df = df[df["job_title"].isin(selected_roles)]

    result = (
        filtered_df
        .groupby(["posting_month", "job_title"])
        .size()
        .reset_index(name="count")
    )

    fig1 = px.line(
        result,
        x="posting_month",
        y="count",
        color="job_title",
        title="📈 Monthly Job Openings for Selected Roles",
        markers=True,
        line_shape="spline",
    )
    fig1.update_layout(
        xaxis_title="Month",
        yaxis_title="Job Count",
        legend_title_text="Job Title",
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)
    with st.expander("View Data: Monthly Job Openings"):
        st.write(result)
    st.download_button("Download CSV", data=result.to_csv(index=False).encode("utf-8"), file_name="Monthly_Job_Trend.csv", mime="text/csv", key="monthly_trend")

st.divider()

_, col6 = st.columns([0.1,0.9])
edu_job_df = df.groupby(["education_required", "job_title"]).size().reset_index(name="count")
with col6:
    fig = px.bar(
    edu_job_df,
    x="job_title",
    y="count",
    color="education_required",
    title="Education Levels Required per Job Role",
    labels={"count": "Number of Job Postings", "job_title": "Job Title", "education_required": "Education Level"},
    template="plotly_white"
    )

    st.plotly_chart(fig,use_container_width=True)
    with st.expander("View Data: Education Level per Job Role"):
        st.write(edu_job_df)
    st.download_button("Download CSV", data=edu_job_df.to_csv(index=False).encode("utf-8"), file_name="Education_Job_Role.csv", mime="text/csv", key="edu_job")

st.divider()

_, col7 = st.columns([0.1,0.9])

with col7:
    df["required_skills"] = df["required_skills"].fillna("")
    df["required_skills"] = df["required_skills"].str.split(",")
    df_exploded = df.explode("required_skills")
    df_exploded["required_skills"] = df_exploded["required_skills"].str.strip()

    skills_df = df_exploded.groupby(["job_title", "required_skills"]).size().reset_index(name="count")

    fig = px.bar(
    skills_df,
    x="required_skills",
    y="count",
    color="job_title",
    title="Job Role Distribution for Each Skill",
    labels={"required_skills": "Skill"},
    template="plotly_white"
    )
    
    fig.update_layout(barmode="stack", xaxis_tickangle=45)

    st.plotly_chart(fig,use_container_width=True)
    with st.expander("View Data: Skills by Job Title"):
        st.write(skills_df)
    st.download_button("Download CSV", data=skills_df.to_csv(index=False).encode("utf-8"), file_name="Skills_By_Job.csv", mime="text/csv", key="skills_by_job")

st.divider()

_, col8 = st.columns([0.1,0.9])

with col8:
    experience_mapping = {
        "EN": "Entry-level",
        "MI": "Mid-level",
        "SE": "Senior",
        "EX": "Executive"
    }

    df["experience_label"] = df["experience_level"].map(experience_mapping)
    experience_order = ["Entry-level", "Mid-level", "Senior", "Executive"]

    fig = px.violin(
        df,
        x="experience_label",
        y="salary_usd",
        color="experience_label",
        category_orders={"experience_label": experience_order},
        box=True,
        points="all",
        title="🎻 Salary Distribution by Experience Level",
        template="plotly_white"
    )

    fig.update_layout(xaxis_title="Experience Level", yaxis_title="Salary (USD)")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("View Data: Salary by Experience"):
        st.write(df[["experience_label", "salary_usd"]])
    st.download_button("Download CSV", data=df[["experience_label", "salary_usd"]].to_csv(index=False).encode("utf-8"), file_name="Salary_Experience.csv", mime="text/csv", key="exp_salary")

st.divider()

_, col9 = st.columns([0.1,0.9])

with col9 :
    skill_counts = df_exploded["required_skills"].value_counts().nlargest(20).reset_index()
    skill_counts.columns = ["Skill", "Count"]

    fig = px.bar(
        skill_counts,
        x="Skill",
        y="Count",
        title="🔥 Top 20 In-Demand Skills",
        text_auto=True,
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("View Data: Top Skills"):
        st.write(skill_counts)
    st.download_button("Download CSV", data=skill_counts.to_csv(index=False).encode("utf-8"), file_name="Top_Skills.csv", mime="text/csv", key="top_skills")
