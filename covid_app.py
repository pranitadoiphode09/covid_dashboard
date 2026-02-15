import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🦠 COVID-19 Analysis Dashboard")

# Load dataset
df = pd.read_csv("covid_daily_full.csv")
icu_df = pd.read_csv("covid_daily_hospital_icu.csv")
testing_df = pd.read_csv("covid_daily_testing.csv")
vaccination_df = pd.read_csv("covid_daily_vaccinations.csv")

st.subheader("Dataset Preview")
st.write("") 
st.dataframe(df.head())
st.write("") 
st.dataframe(icu_df.head())
st.write("") 
st.dataframe(testing_df.head())
st.write("") 
st.dataframe(vaccination_df.head())
st.write("") 
st.write("") 
st.write("") 




# ---------------- PIE CHART ----------------
st.subheader("🌍 Total COVID-19 Cases by Continent")

total_cases_plot = df.groupby("continent")["total_cases"].max()
fig1, ax1 = plt.subplots(figsize=(10,7))
ax1.pie(
    total_cases_plot.values,
    labels=total_cases_plot.index,
    autopct="%1.1f%%",
    startangle=140
)

ax1.set_title("Total COVID-19 Cases by Continent",fontsize=15,pad=55)
ax1.axis("equal")
st.pyplot(fig1)
st.write("") 
st.markdown("### Insight")  
st.markdown("""North America (35%) and Asia (33.7%) account for the largest share of global COVID-19 cases.

Despite having the largest population, Asia’s share is close to North America, indicating widespread transmission across both regions.

Africa shows a very small share (1.4%), which may reflect lower testing, underreporting, or later waves rather than truly low spread.

Oceania’s small proportion (4%) reflects strong border control and containment policies during early waves.""")
st.write("") 
st.write("") 




# ---------------- BAR CHART ----------------
st.subheader("📊Top 10 Countries by Total Cases")

cases_by_location = (
    df.groupby("location")["total_cases_per_million"]
    .max()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2, ax2 = plt.subplots(figsize=(9,5))
sns.barplot(
    data=cases_by_location,
    x="location",
    y="total_cases_per_million",
    palette="viridis",hue="location",
    ax=ax2
)
ax2.set_xlabel("Country")
ax2.set_ylabel("Total Cases per Million")
ax2.set_title("Top 10 Countries by Total Cases per Million")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig2)
st.write("") 
st.markdown("### Insight")  
st.markdown("""Small countries like Brunei, San Marino, and Austria top the list, showing extremely high cases per million.

This indicates that cases per million is influenced heavily by population size — smaller nations show higher ratios even with moderate absolute cases.

European microstates and developed nations dominate, suggesting extensive testing and reporting accuracy.

High cases per million do not necessarily mean high deaths, indicating better healthcare response.""")
st.write("")   
st.write("") 





# ---------------- BAR CHART ----------------
st.subheader("📊 Top 10 Countries by Total Deaths")

deaths_by_location = (df.groupby("location")["total_deaths_per_million"].max().sort_values(ascending=False).head(10).reset_index())

fig3, ax3 = plt.subplots(figsize=(9,5))
sns.barplot(
    data=deaths_by_location,
    x="location",
    y="total_deaths_per_million",
    palette="magma",hue="location",
    ax=ax3
)

ax3.set_xlabel("Country")
ax3.set_ylabel("Total Deaths per Million")
ax3.set_title("Top 10 Countries by Total Deaths per Million", fontsize=15,pad=20)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig3)
st.write("") 
st.markdown("### Insight")  
st.markdown("""Peru leads by a large margin, followed by several Eastern European countries.

These regions were hit hard during early waves before vaccination and effective treatment protocols were widely available.

Many of these countries have aging populations and limited ICU capacity, contributing to higher mortality.

This highlights how healthcare readiness and timing of waves influenced death rates more than total case count.""")  
st.write("") 
st.write("") 




df["date"] = pd.to_datetime(df["date"],format="mixed",dayfirst=True)
icu_df['date'] = pd.to_datetime(icu_df['date'],format="mixed",dayfirst=True)
testing_df['date'] = pd.to_datetime(testing_df['date'],format="mixed",dayfirst=True)
vaccination_df['date'] = pd.to_datetime(vaccination_df['date'],format="mixed",dayfirst=True)


# ---------------- LINE CHART ----------------
st.subheader("📈 Monthly Trend")
monthly_cases = (df.set_index('date').resample('ME')['new_cases_smoothed'].sum().reset_index())

sns.set_style("whitegrid")

fig4, ax4 = plt.subplots(figsize=(9,5))
sns.lineplot(data= monthly_cases, x='date',y='new_cases_smoothed')

ax4.set_title('Monthly COVID-19 Cases Trend', fontsize=15,pad=20)
ax4.set_xlabel('Year')
ax4.set_ylabel('New Cases')
st.pyplot(fig4)
st.write("")  
st.markdown("### Insight")  
st.markdown("""Clear wave patterns are visible, with major peaks around early 2022 and early 2023.

The largest spike occurs in 2022, corresponding to highly transmissible variants (like Omicron).

After 2023, cases decline sharply, showing the combined effect of vaccination, herd immunity, and improved treatments.

Later waves show high cases but comparatively fewer deaths globally.""")  
st.write("")  
st.write("") 
st.write("")  




# ---------------- BAR CHART ----------------

st.subheader("🩺 How Deadly Was COVID-19 Across Continents")
tdtc = df.groupby('continent').agg({'total_deaths': 'max','total_cases': 'max'})

fig5, ax5 = plt.subplots(figsize=(9,5))
tdtc['death_rate'] = tdtc['total_deaths'] / tdtc['total_cases']

sns.barplot(data=tdtc, 
                x='continent',
                y='death_rate',
                palette="mako", 
                hue='continent')
ax5.set_title("  Total Cases VS Deaths", fontsize=15,pad=20)
ax5.set_xlabel("Continent")
ax5.set_ylabel("Death Rate")
st.pyplot(fig5)
st.write("") 
st.markdown("### Insight")  
st.markdown("""Africa shows the highest death rate relative to cases, indicating limited healthcare access and late vaccination rollout.

South America also shows a high death rate, reflecting severe early waves.

Oceania has the lowest death rate, demonstrating effective containment and healthcare management.

Europe and North America have moderate death rates despite high cases, suggesting strong medical infrastructure.""")  
st.write("")    
st.write("") 
st.write("") 




# ---------------- SCATTER CHART ----------------

st.subheader(" 🔬 Positive Rate VS Death Rate")
positive_vs_death = df.groupby("continent")[["positive_rate","new_deaths_smoothed"]].sum()

fig6, ax6 = plt.subplots(figsize=(9,5))
sns.scatterplot(data=positive_vs_death, 
                x='positive_rate',
                y='new_deaths_smoothed', 
                 hue='continent')

ax6.set_xlabel("Average Test Positivity Rate")
ax6.set_ylabel("Total COVID-19 Deaths")
ax6.set_title("Relation between COVID Positive rate and Total Deaths", fontsize=15,pad=20)
st.pyplot(fig6)
st.write("")   
st.markdown("### Insight")  
st.markdown("""Continents with higher test positivity rates tend to have higher total deaths.

This suggests that when testing is limited (high positivity), many infections go undetected, leading to uncontrolled spread and higher mortality.

Europe and South America show both high positivity and high deaths, indicating overwhelmed healthcare systems during peaks.

Africa and Oceania show lower values, possibly due to lower testing or better containment.""")  
st.write("") 
st.write("") 







# ---------------- BAR CHART ----------------
st.subheader("🚑 ICU Patitents Across Continents")
icu_by_location = (df.groupby("continent")["icu_patients_per_million"].max().sort_values(ascending=False).head(10).reset_index())

fig7, ax7 = plt.subplots(figsize=(9,5))

sns.barplot(
    data = icu_by_location,
    x = "continent",
    y = "icu_patients_per_million",
    palette="cividis",hue="continent"
)

ax7.set_xlabel("Country")
ax7.set_ylabel("Total Cases per Million")
ax7.set_title("🚑 ICU Patients Across Continents", fontsize=15,pad=20)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig7)
st.write("")  
st.markdown("### Insight")  
st.markdown("""Europe and South America show the highest ICU patient counts, reflecting severe case loads during peak waves.

North America follows, indicating significant strain on healthcare systems.

Africa and Oceania show lower ICU numbers, which may reflect limited ICU capacity rather than lower severity.

High ICU usage strongly correlates with higher death rates observed earlier.""")   
st.write("") 
st.write("") 





# ---------------- CONCLUSION ----------------
st.markdown("### ✅ Conclusion")  
st.markdown("""This dashboard shows how COVID-19 affected different continents and countries in different ways.

North America and Asia had the highest number of cases.

Some small and European countries had very high cases and deaths per million.

Africa and South America showed higher death rates, likely due to limited healthcare resources.

Clear waves of infection appeared in 2022 and 2023, after which cases reduced because of vaccines and immunity.

ICU data and positive rate trends show how healthcare pressure and testing levels influenced death rates.

Overall, the analysis shows that healthcare capacity, testing, and timely response played a major role in controlling deaths, not just the number of cases.""")   
st.write("") 