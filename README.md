# ⚽ FootLens Analytics

## Player Injuries & Team Performance Intelligence Dashboard

FootLens Analytics is an interactive football analytics dashboard developed using **Python and Streamlit**. The application analyses football injury and player-performance data to identify injury patterns, recovery trends, player performance changes, and team-level injury burden.

The dashboard converts raw football data into interactive visualisations and analytical insights that can support better decision-making in football management.

---

## 🎯 Project Objective

The main objective of FootLens Analytics is to investigate how player injuries can affect player performance and create an additional injury burden for football teams.

The application allows users to:

* Analyse player injury patterns.
* Compare injury frequency between teams.
* Examine injury recovery duration.
* Identify frequently occurring injury categories.
* Analyse player performance ratings.
* Explore relationships between age and injury impact.
* Identify players with strong comeback patterns.
* Compare injury burden across clubs.
* Examine monthly injury trends.
* Download filtered analytical data.

---

## 🔬 Research / Business Questions

FootLens Analytics focuses on the following questions:

### Q1. Which injuries are associated with the highest estimated performance impact?

The dashboard compares injury categories using the **Injury Impact Index**.

### Q2. What is the team's available win/draw/loss pattern in records associated with player absence?

Match-result information can be used to understand the team's performance pattern within the available dataset.

### Q3. How does player performance change around injury and recovery periods?

Performance ratings can be explored across the available match timeline to identify changes around injury periods.

### Q4. Are there particular months or clubs with clusters of injury cases?

Monthly trends and the team × month heatmap help identify possible injury clusters.

### Q5. Which clubs and players show the greatest injury burden or strongest comeback patterns?

Team-level statistics and the comeback leaderboard provide additional decision-support information.

---

## 🧰 Technologies Used

| Technology | Purpose                               |
| ---------- | ------------------------------------- |
| Python     | Data processing and application logic |
| Streamlit  | Interactive dashboard                 |
| Pandas     | Data cleaning and analysis            |
| NumPy      | Numerical calculations                |
| Plotly     | Interactive visualisations            |
| OpenPyXL   | Excel dataset support                 |

---

## 📊 Dashboard Features

### 1. Executive Overview

The dashboard provides key performance indicators including:

* Injury Cases
* Players Affected
* Clubs Analysed
* Average Recovery Duration
* Average Injury Impact

---

### 2. Interactive Filters

Users can filter the analysis by:

* Team / Club
* Player
* Injury Type
* Injury Date Range

All dashboard analysis updates according to the selected filters.

---

### 3. Injury Impact Analysis

The dashboard calculates an **Injury Impact Index** to provide a consistent analytical comparison between injury records.

The index considers:

* Injury duration
* Performance rating information

The index is intended for analytical comparison and **is not a medical severity score**.

---

### 4. Monthly Injury Trends

A monthly line chart helps identify periods with:

* Higher injury frequency
* Lower injury frequency
* Possible seasonal patterns

---

### 5. Team × Month Heatmap

The heatmap compares injury frequency across:

* Teams
* Months

This makes it easier to identify possible clusters of injuries.

---

### 6. Recovery Duration Analysis

The application analyses injury duration in days.

It provides:

* Recovery-duration distribution
* Longest recorded injuries
* Average recovery duration

---

### 7. Age vs Injury Impact

An interactive scatter plot compares:

**Player Age → Injury Impact Index**

This can help explore whether injury impact varies across different age groups in the dataset.

---

### 8. Player Performance Analysis

If performance ratings are available, the dashboard provides:

* Average player rating
* Maximum rating
* Performance timeline
* Player comparison

---

### 9. Comeback Leaderboard

The dashboard calculates a simple **Comeback Score** using the relationship between a player's average and maximum recorded performance rating.

This creates a comparative leaderboard of players showing stronger performance peaks.

---

### 10. Team Analysis

Team-level analysis includes:

* Number of injury cases
* Number of players affected
* Average recovery duration
* Average injury impact
* Injury load comparison

A scatter plot compares team injury volume against average injury impact.

---

### 11. Automated Insights

The dashboard automatically identifies useful observations such as:

* Longest recorded injury
* Team with the highest injury volume
* Most frequent injury category
* Average performance rating
* Average match points

---

### 12. Filtered Data Download

Users can download the currently filtered dataset as:

```text
footlens_filtered_data.csv
```

This allows further analysis outside the dashboard.

---

# 🧹 Data Cleaning

The application performs several data-preparation steps before analysis.

### Column Standardisation

Different common column-name variations are automatically recognised.

For example:

```text
Player Name
Player
Footballer
```

can be interpreted as the standard:

```text
player
```

Similarly, variations of team, rating, injury date and injury type fields are handled.

---

### Date Conversion

Injury start and end dates are converted into proper datetime values.

This allows the application to calculate:

```text
Injury Duration = Injury End Date − Injury Start Date
```

---

### Numerical Cleaning

Numerical variables such as:

* Age
* Goals
* Performance Rating

are converted into numeric formats for analysis.

---

### Missing Values

Missing text values are handled using readable placeholders such as:

```text
Unknown Player
Unknown Team
Unspecified
```

Invalid numerical values are safely converted to missing values rather than stopping the application.

---

# 📐 Feature Engineering

FootLens Analytics creates additional analytical variables.

## Injury Duration

```text
Injury Duration = Injury End Date − Injury Start Date
```

The result is measured in days.

---

## Match Points

Football results are converted into points:

```text
Win  = 3 points
Draw = 1 point
Loss = 0 points
```

---

## Injury Month

The injury start date is used to create a month variable.

This supports monthly trend analysis.

---

## Injury Impact Index

The application creates an analytical index based on:

* Injury duration
* Performance rating information

The resulting value is scaled to approximately:

```text
0 – 100
```

A higher value represents a greater estimated analytical impact within this dashboard.

This should not be interpreted as a medical diagnosis or official injury severity measurement.

---

# 📈 Visualisations

FootLens Analytics contains multiple interactive visualisations, including:

1. Injury Category Impact Chart
2. Age vs Injury Impact Scatter Plot
3. Player Performance Timeline
4. Monthly Injury Trend
5. Team × Month Injury Heatmap
6. Recovery Duration Histogram
7. Longest Injuries Chart
8. Comeback Leaderboard
9. Injury Cases by Club
10. Club Injury Load vs Impact
11. Match Result Distribution

The charts are interactive and allow users to explore the dataset dynamically.

---

# 📁 Project Structure

```text
FootLens-Analytics/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/FootLens-Analytics.git
```

Move into the project folder:

```bash
cd FootLens-Analytics
```

---

## Step 2 — Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## Step 3 — Run the Application

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📦 Requirements

The project uses the following Python packages:

```text
streamlit
pandas
numpy
plotly
openpyxl
```

---

# ☁️ Streamlit Deployment

The application can be deployed using **Streamlit Community Cloud**.

### Deployment Steps

1. Upload the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub account.
4. Select the `FootLens-Analytics` repository.
5. Select `app.py` as the main file.
6. Deploy the application.
7. Upload the required football dataset through the dashboard.

---

# 📊 Dataset

The application is designed to work with a football injury/performance dataset containing relevant fields such as:

```text
Player
Team / Club
Match Result
Injury Start Date
Injury End Date
Performance Rating
Age
Injury Type
Goals
Season
```

The exact available fields depend on the dataset supplied for the project.

The application also supports common variations in column names.

---

# 🧠 Analytical Approach

The project follows a simple data-analysis workflow:

```text
Raw Football Data
        ↓
Data Cleaning
        ↓
Data Standardisation
        ↓
Feature Engineering
        ↓
Exploratory Data Analysis
        ↓
Interactive Visualisation
        ↓
Insights
        ↓
Football Decision Support
```

---

# 🎯 Potential Users

FootLens Analytics can be useful for:

* Football coaches
* Team analysts
* Sports management teams
* Performance analysts
* Player development staff
* Sports-data students
* Football researchers

The dashboard provides analytical information that could support squad planning and performance monitoring.

---

# ⚠️ Limitations

The dashboard has several limitations:

* Results depend on the quality of the supplied dataset.
* Missing performance data can limit player-level analysis.
* Injury duration does not necessarily represent medical severity.
* Correlation between injury and team performance does not prove causation.
* The Injury Impact Index is an analytical metric created for this project.
* The Comeback Score is a simplified comparative measure.
* The dashboard should not be used for medical decisions.

---

# 🔮 Future Improvements

Future versions could include:

* Machine-learning injury-risk prediction
* Player workload monitoring
* GPS and training-load integration
* Real-time football data
* Injury-risk forecasting
* More advanced recovery prediction
* Team availability forecasting
* Player recommendation systems
* AI-generated scouting insights
* Automated injury alerts
* Predictive analytics for future matches

---

# 👨‍💻 Project Information

**Project:** FootLens Analytics
**Domain:** Artificial Intelligence / Data Analytics
**Application:** Interactive Football Analytics Dashboard
**Framework:** Streamlit
**Language:** Python

---

## ⭐ Conclusion

FootLens Analytics transforms football injury and performance data into an interactive analytical dashboard. By combining data cleaning, feature engineering, exploratory analysis and interactive visualisation, the project provides a practical way to investigate player injuries, recovery patterns, performance and team-level injury burden.
