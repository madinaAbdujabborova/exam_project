# Online Cources

## This dataset provides detailed information about various online courses across different learning platforms. The key features of the dataset include:

    Course_ID: A unique identifier for each course.
    Course_Name: The name of the course.
    Category: The category or field to which the course belongs, such as Office Tools, Technology, etc.
    Duration (hours): The duration of the course in hours.
    Enrolled_Students: The number of students enrolled in the course.
    Completion_Rate (%): The percentage of students who completed the course.
    Platform: The platform offering the course, such as Coursera, edX, LinkedIn Learning, or Udemy.
    Price ($): The price of the course in dollars.
    Rating (out of 5): The course rating on a scale of 1 to 5.

This dataset can be used to analyze various aspects of online courses, such as their popularity, completion rates, and ratings across different platforms and categories.

### Usage
Display Data:

Click on the "Data Frame" button to toggle the display of the dataset.
Data Cleaning:

The dataset is automatically cleaned and missing values are filled upon loading.
Visualizations:

Pie Chart for Category Distribution: Displays the distribution of courses across different categories.
Histogram: Choose between Original, Mean, and Median values for the price distribution.
Pie Charts for Platform Distribution: Compare the original, mode-filled, and mean-filled platform distributions.
Correlation Heatmap: Shows the correlation between numerical columns.
Box Plot: Displays Duration (hours) for different Category and Platform.
Interactive Charts: Choose between different chart types and columns to display average data by platform. Option to overlay charts.
Interactive Sidebars:

Choose histogram types, pie charts, columns to display, and chart types from the sidebar.
Additional sidebar options for future extensions.
File Structure
app.py: Main Streamlit app script.
10.csv: Dataset file (make sure this is in the same directory as app.py).
Dependencies
pandas
seaborn
matplotlib
streamlit
scikit-learn