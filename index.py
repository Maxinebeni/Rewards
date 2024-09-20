import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from CSV
@st.cache_data
def load_data():
    return pd.read_csv("Rewards.csv")

data = load_data()

# Calculate Key Metrics
total_redemptions = data['Redemptions_by_User'].sum()
total_reward_value = data['Reward_Value_Amount_in_Dollars'].sum()
new_users = data['Member_Name_Surname_Per_Redemption'].nunique()
top_performers = data.groupby('Member_Name_Surname_Per_Redemption')['Redemptions_by_User'].sum().nlargest(5)
low_engagement_users = data[data['Redemptions_by_User'] <= 5]
reward_types_count = data['Reward_Received'].value_counts()

# Title of the dashboard
st.title("Rewards Program Dashboard")

# KPIs
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Redemptions", total_redemptions)

with col2:
    st.metric("Total Reward Value ($)", total_reward_value)

with col3:
    st.metric("New Users", new_users)

with col4:
    st.metric("Top Performers", len(top_performers))


# First row: Satisfaction Rating Area Chart and Redemptions by Country
col1, col2 = st.columns(2)

with col1:
    st.write("### Satisfaction Ratings Distribution")
    fig, ax = plt.subplots()
    sns.kdeplot(data['Satisfaction_Rating_on_Reward'], shade=True, ax=ax)
    ax.set_title("Satisfaction Rating Distribution")
    st.pyplot(fig)

with col2:
    st.write("### Redemptions by Country")
    redemptions_by_country = data.groupby('Country')['Redemptions_by_User'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.pie(redemptions_by_country, labels=redemptions_by_country.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title("Redemptions by Country")
    st.pyplot(fig)

# Second row: High Performers, Low Engagement Users, and Reward Type Distribution
col1, col2, col3 = st.columns(3)

with col1:
    st.write("### Top Performers")
    fig, ax = plt.subplots()
    top_performers.plot(kind='bar', ax=ax, color='lightblue')
    ax.set_ylabel("Number of Redemptions")
    ax.set_title("Top Performers")
    st.pyplot(fig)

with col2:
    st.write("### Low-Engagement Users")
    low_engagement_count = low_engagement_users.groupby('Reward_Received')['Redemptions_by_User'].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots()
    low_engagement_count.plot(kind='bar', ax=ax, color='lightgreen')
    ax.set_ylabel("Number of Redemptions")
    ax.set_title("Low-Engagement Users - Reward Types")
    st.pyplot(fig)

with col3:
    st.write("### Count of Different Reward Types Received")
    fig, ax = plt.subplots()
    reward_types_count.plot(kind='bar', ax=ax, color='coral')
    ax.set_ylabel("Count")
    ax.set_title("Rewards Types Distribution")
    st.pyplot(fig)

# Third row: Cost per Redemption and Time to Reward vs Satisfaction
col1, col2 = st.columns(2)

with col1:
    st.write("### Cost per Redemption per User")
    cost_per_redemption = data.groupby('Member_Name_Surname_Per_Redemption')['Cost_Per_Redemption_in_Dollars'].mean().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots()
    cost_per_redemption.plot(kind='bar', ax=ax, color='orange')
    ax.set_ylabel("Average Cost (in Dollars)")
    ax.set_title("Cost per Redemption")
    st.pyplot(fig)

with col2:
    st.write("### Time to Reward vs Satisfaction Rating")
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x='Time_to_Reward_Received_in_Seconds', y='Satisfaction_Rating_on_Reward', hue='Reward_Value_Amount_in_Dollars', size='Redemptions_by_User', ax=ax)
    ax.set_title("Time to Reward vs Satisfaction Rating")
    st.pyplot(fig)

