import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


st.write("# *Online Courses* ")
st.text("""This dataset provides detailed information about various online courses across different learning platforms. The key features of the dataset include:

    Course_ID: A unique identifier for each course.
    Course_Name: The name of the course.
    Category: The category or field to which the course belongs, such as Office Tools, Technology, etc.
    Duration (hours): The duration of the course in hours.
    Enrolled_Students: The number of students enrolled in the course.
    Completion_Rate (%): The percentage of students who completed the course.
    Platform: The platform offering the course, such as Coursera, edX, LinkedIn Learning, or Udemy.
    Price ($): The price of the course in dollars.
    Rating (out of 5): The course rating on a scale of 1 to 5.

This dataset can be used to analyze various aspects of online courses, such as their popularity, completion rates, and ratings across different platforms and categories.""")

df = pd.read_csv("10.csv")

# Initialize session state for the toggle
if 'show_dataframe' not in st.session_state:
    st.session_state.show_dataframe = False

# Function to toggle the display of the DataFrame
def toggle_dataframe():
    st.session_state.show_dataframe = not st.session_state.show_dataframe

# Button to toggle DataFrame display
st.button("Data Frame", on_click=toggle_dataframe)

# Display the DataFrame based on the toggle state
if st.session_state.show_dataframe:
    st.write(df)

# Course_nameni nanlarini to'ldirish

course_id = df["Course_Name"].to_list()
for i in range(len(course_id)):
    if course_id[i] != str:
        course_id[i] = f'Course_{i+1}'

df['Course_Name_full'] = course_id

# Category ustunini to'ldirish
df["Category_filled"] = df["Category"].fillna("Not given")

# Price ni mean va median bilan to'ldirish
df["Price_mean"] = df.groupby("Category_filled")["Price ($)"].transform(lambda x: x.fillna(x.mean()))
df["Price_median"] = df.groupby("Category_filled")["Price ($)"].transform(lambda x: x.fillna(x.median()))

# Completion rateni mean va madian bilan to'ldirish
df["CompletionRate_mean"] = df.groupby("Category_filled")["Completion_Rate (%)"].transform(lambda x: x.fillna(x.mean()))
df["CompletionRate_median"] = df.groupby("Category_filled")["Completion_Rate (%)"].transform(lambda x: x.fillna(x.median()))

# ENrolled studentsni mean va max bilan to'ldirish
df["Enrolled_mean"] = df.groupby("Category_filled")["Enrolled_Students"].transform(lambda x: x.fillna(x.mean()))
df["Enrolled_median"] = df.groupby("Category_filled")["Enrolled_Students"].transform(lambda x: x.fillna(x.median()))

# Duration ourni to'ldirish mean va median bilan
df["DurationHour_mean"] = df.groupby("Category_filled")["Duration (hours)"].transform(lambda x: x.fillna(x.mean()))
df["DurationHour_median"] = df.groupby("Category_filled")["Duration (hours)"].transform(lambda x: x.fillna(x.median()))

# Filling platformni moda va groupby orqali price meani bilan to'ldirish
df["Platform_mode"] = df["Platform"].fillna("Udemy")


mean_price = df['Price ($)'].mean()
count = [0]

def fill_platform(row, mean_price, count):
    if pd.isna(row['Platform']):
        if row['Price ($)'] < mean_price and count[0] % 2 == 0:
            platform = 'LinkedIn Learning'
        elif row['Price ($)'] < mean_price and count[0] % 2 != 0:
            platform = 'edX'
        elif row['Price ($)'] > mean_price and count[0] % 2 == 0:
            platform = 'Udemy'
        else:
            platform = 'Coursera'
        count[0] += 1
        return platform
    return row['Platform']

df['Platform_mean(Price)'] = df.apply(fill_platform, axis=1, mean_price=mean_price, count=count)


# Labeling
le = LabelEncoder()
df["labeled_Category"] = le.fit_transform(df["Category"])
df["labeled_Platform"] = le.fit_transform(df["Platform"])



# Pie chart with Category

category_counts = df['Category'].value_counts()

fig, ax = plt.subplots()
ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.title('Category Distribution Pie Chart')
st.pyplot(fig)




# Streamlit app
st.title('Price Distribution Analysis')

# Sidebar for selecting histogram types
options = st.sidebar.multiselect(
    'Select histogram(s) to display:',
    ['Original', 'Mean', 'Median'],
    default=['Original']  # Default selection
)



# Create histograms
fig, ax = plt.subplots(figsize=(10, 6))

# Plot based on user selection
if 'Original' in options:
    ax.hist(df['Price ($)'], bins=10, alpha=0.5, label='Original', edgecolor='black')

if 'Mean' in options:
    ax.hist(df['Price_mean'], bins=10, alpha=0.5, label='Mean', edgecolor='black')

if 'Median' in options:
    ax.hist(df['Price_median'], bins=10, alpha=0.5, label='Median', edgecolor='black')

ax.set_xlabel('Prices')
ax.set_ylabel('Frequency')
ax.set_title('Comparison of Selected Histograms')
ax.legend(loc='upper right')

st.pyplot(fig)




st.title("Category, Platforms, and Completion Rate Bar Chart")

# Grouped Bar Chart
plt.figure(figsize=(14, 7))
sns.set(style="whitegrid")

# Create the bar plot
bar_plot = sns.barplot(x="Category", y="Completion_Rate (%)", hue="Platform", data=df, palette="muted")

# Add labels and title
plt.xlabel('Category')
plt.ylabel('Completion Rate (%)')
plt.title('Completion Rate by Category and Platform')

# Display the plot in Streamlit
st.pyplot(plt)


platform_counts1 = df['Platform'].value_counts()
platform_counts2 = df['Platform_mode'].value_counts()
platform_counts3 = df['Platform_mean(Price)'].value_counts()

# Sidebar for selecting pie charts to display
selected_pie_charts = st.sidebar.multiselect(
    'Select pie chart(s) to display:',
    ['Original', 'Mode', 'Price'],
    default=['Original']  # Default selection
)

# Create subplots based on the number of selected pie charts
num_selected = len(selected_pie_charts)
fig, axes = plt.subplots(1, num_selected, figsize=(6 * num_selected, 6))

if num_selected == 1:
    axes = [axes]

# Plot the selected pie charts
for i, chart_type in enumerate(selected_pie_charts):
    if chart_type == 'Original':
        axes[i].pie(platform_counts1, labels=platform_counts1.index, autopct='%1.1f%%', startangle=90)
        axes[i].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        axes[i].set_title('Platform Original')
    elif chart_type == 'Mode':
        axes[i].pie(platform_counts2, labels=platform_counts2.index, autopct='%1.1f%%', startangle=90)
        axes[i].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        axes[i].set_title('Platform Mode')
    elif chart_type == 'Price':
        axes[i].pie(platform_counts3, labels=platform_counts3.index, autopct='%1.1f%%', startangle=90)
        axes[i].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        axes[i].set_title('Platform (Price)')

# Display the plots in Streamlit
st.title('Comparing Pie Charts')
st.pyplot(fig)

# Table
grouped_df = df.groupby("Platform")[["Duration (hours)", "Enrolled_Students", "Completion_Rate (%)", "Price ($)", "Rating (out of 5)"]].mean()
st.title('Platform Data Analysis')
st.write('Grouped and averaged data by Platform:')
st.dataframe(grouped_df)





st.title("Duration hours for different fields!")

# Seaborn settings
sns.set_style("whitegrid")

# Create the catplot with the desired layout
g = sns.catplot(x="Category", y="Duration (hours)", data=df, hue="Category", kind="box", col="Platform", col_wrap=2)

# Set the overall title
g.fig.suptitle("Duration hours for different fields!", y=1.08)

# Rotate x-axis labels for each subplot
for ax in g.axes.flatten():
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

# Display the plot in Streamlit
st.pyplot(g.fig)




st.title('Showing selected information')
st.sidebar.title('User Inputs')

# User input for selecting the chart type
chart_type = st.sidebar.selectbox('Select chart type', ['Bar Chart', 'Line Chart', 'scatter_chart'])

# User input for selecting the data columns to display
selected_columns = st.sidebar.multiselect(
    'Select columns to display', 
    ['Category', 'Duration (hours)', 'Enrolled_Students', 'Completion_Rate (%)', 'Platform', 'Price ($)', 'Rating (out of 5)'], 
    default=['Duration (hours)', 'Enrolled_Students']
)

overlay_chart = st.sidebar.checkbox('Overlay Charts')

# Check if any columns are selected
if selected_columns:
    # Group by 'Platform' and calculate the mean for the selected columns
    grouped_df = df.groupby("Platform")[selected_columns].mean()

    st.write('Grouped and averaged data by Platform:')
    st.dataframe(grouped_df)

    if overlay_chart:
        st.write("Overlay Chart")
        for col in selected_columns:
            st.line_chart(grouped_df[col], use_container_width=True)
            st.bar_chart(grouped_df[col], use_container_width=True)
    else:
        if chart_type == 'Bar Chart':
            st.bar_chart(grouped_df)
        elif chart_type == 'Line Chart':
            st.line_chart(grouped_df)
else:
    st.write("Please select at least one column to display.")



# Heat map
st.title("Correlation Heatmap")

cols = ['Duration (hours)', 'Enrolled_Students', 'Completion_Rate (%)', 'Price ($)', 'Rating (out of 5)']

plt.figure(figsize=(10, 6))
heatmap = sns.heatmap(df[cols].corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)

st.pyplot(plt)