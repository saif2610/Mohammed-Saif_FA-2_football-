import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============================================================
# FOOTLENS ANALYTICS
# Player Injuries & Team Performance Dashboard
# Mathematics for AI-II | Artificial Intelligence
# ============================================================

st.set_page_config(
    page_title="FootLens Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f6f8fb;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

.hero {
    padding: 28px 32px;
    border-radius: 22px;
    background: linear-gradient(
        135deg,
        #101828 0%,
        #172554 55%,
        #0f766e 100%
    );
    color: white;
    margin-bottom: 22px;
    box-shadow: 0 12px 35px rgba(15, 23, 42, 0.15);
}

.hero h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -1px;
}

.hero p {
    margin-top: 8px;
    color: #dbeafe;
    font-size: 1rem;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 12px;
    color: #111827;
}

.insight {
    background: white;
    border-left: 5px solid #0f766e;
    padding: 15px 18px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.06);
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e4e7ec;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
}

.small-note {
    color: #667085;
    font-size: 0.85rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_column_name(column):
    """
    Convert column names into a consistent format.
    """
    return (
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("%", "pct")
    )


def standardize_columns(data):
    """
    Detect common variations of dataset column names.
    """

    data = data.copy()

    data.columns = [
        clean_column_name(column)
        for column in data.columns
    ]

    aliases = {

        "player": [
            "player_name",
            "player",
            "name",
            "footballer",
            "athlete"
        ],

        "team": [
            "team",
            "club",
            "club_name",
            "team_name"
        ],

        "result": [
            "match_result",
            "result",
            "outcome",
            "match_outcome"
        ],

        "injury_start": [
            "injury_start_date",
            "injury_start",
            "start_date",
            "injury_date"
        ],

        "injury_end": [
            "injury_end_date",
            "injury_end",
            "end_date",
            "recovery_date"
        ],

        "rating": [
            "performance_rating",
            "rating",
            "player_rating",
            "match_rating"
        ],

        "age": [
            "age",
            "player_age"
        ],

        "injury_type": [
            "injury_type",
            "injury",
            "injury_name",
            "injury_category"
        ],

        "goals": [
            "goals",
            "goal",
            "goals_scored"
        ],

        "season": [
            "season",
            "year",
            "season_year"
        ]
    }

    rename_dictionary = {}

    for standard_name, possible_names in aliases.items():

        if standard_name in data.columns:
            continue

        for possible_name in possible_names:

            if possible_name in data.columns:
                rename_dictionary[possible_name] = standard_name
                break

    data = data.rename(
        columns=rename_dictionary
    )

    # --------------------------------------------------------
    # Fallback columns
    # --------------------------------------------------------

    if "player" not in data.columns:
        data["player"] = "Unknown Player"

    if "team" not in data.columns:
        data["team"] = "Unknown Team"

    if "injury_type" not in data.columns:
        data["injury_type"] = "Unspecified"

    if "result" not in data.columns:
        data["result"] = "Unknown"

    if "age" not in data.columns:
        data["age"] = np.nan

    # --------------------------------------------------------
    # Fill text values
    # --------------------------------------------------------

    data["player"] = (
        data["player"]
        .fillna("Unknown Player")
        .astype(str)
    )

    data["team"] = (
        data["team"]
        .fillna("Unknown Team")
        .astype(str)
    )

    data["injury_type"] = (
        data["injury_type"]
        .fillna("Unspecified")
        .astype(str)
    )

    # --------------------------------------------------------
    # Convert dates
    # --------------------------------------------------------

    for column in [
        "injury_start",
        "injury_end"
    ]:

        if column in data.columns:

            data[column] = pd.to_datetime(
                data[column],
                errors="coerce"
            )

    # --------------------------------------------------------
    # Convert numerical columns
    # --------------------------------------------------------

    for column in [
        "rating",
        "age",
        "goals"
    ]:

        if column in data.columns:

            data[column] = pd.to_numeric(
                data[column]
                .astype(str)
                .str.replace(",", "", regex=False),
                errors="coerce"
            )

    # --------------------------------------------------------
    # Injury duration
    # --------------------------------------------------------

    if (
        "injury_start" in data.columns
        and
        "injury_end" in data.columns
    ):

        data["injury_days"] = (
            data["injury_end"]
            - data["injury_start"]
        ).dt.days

        data["injury_days"] = (
            data["injury_days"]
            .clip(lower=0)
        )

    else:

        data["injury_days"] = np.nan

    # --------------------------------------------------------
    # Injury month
    # --------------------------------------------------------

    if "injury_start" in data.columns:

        data["injury_month"] = (
            data["injury_start"]
            .dt.month_name()
        )

        data["injury_month_num"] = (
            data["injury_start"]
            .dt.month
        )

    else:

        data["injury_month"] = "Unknown"
        data["injury_month_num"] = np.nan

    # --------------------------------------------------------
    # Season
    # --------------------------------------------------------

    if "season" not in data.columns:

        if "injury_start" in data.columns:

            data["season"] = (
                data["injury_start"]
                .dt.year
                .astype("Int64")
                .astype(str)
            )

        else:

            data["season"] = "Unknown"

    return data


def calculate_result_points(result):

    """
    Convert football result into points.
    Win = 3
    Draw = 1
    Loss = 0
    """

    value = str(result).strip().lower()

    if value in [
        "w",
        "win",
        "won",
        "victory",
        "1"
    ]:
        return 3

    if value in [
        "d",
        "draw",
        "drawn",
        "tie"
    ]:
        return 1

    if value in [
        "l",
        "loss",
        "lost",
        "defeat",
        "0"
    ]:
        return 0

    return np.nan


def add_derived_metrics(data):

    data = data.copy()

    # --------------------------------------------------------
    # Match points
    # --------------------------------------------------------

    if "result" in data.columns:

        data["points"] = (
            data["result"]
            .apply(calculate_result_points)
        )

    else:

        data["points"] = np.nan

    # --------------------------------------------------------
    # Player average rating
    # --------------------------------------------------------

    if "rating" in data.columns:

        player_average = (
            data.groupby("player")["rating"]
            .transform("mean")
        )

        data["rating_gap_vs_player_avg"] = (
            data["rating"]
            - player_average
        )

    # --------------------------------------------------------
    # Injury Impact Index
    # --------------------------------------------------------

    duration = (
        pd.to_numeric(
            data["injury_days"],
            errors="coerce"
        )
        .fillna(0)
    )

    if len(duration) > 0:

        duration_reference = duration.quantile(0.95)

        if duration_reference <= 0:
            duration_reference = 1

    else:

        duration_reference = 1

    duration_component = np.clip(
        duration / duration_reference,
        0,
        1
    )

    # --------------------------------------------------------
    # Rating component
    # --------------------------------------------------------

    if (
        "rating" in data.columns
        and
        data["rating"].notna().any()
    ):

        rating_average = data["rating"].mean()

        rating_component = np.clip(
            (
                rating_average
                -
                data["rating"].fillna(rating_average)
            )
            /
            max(abs(rating_average), 1),
            -1,
            1
        )

        rating_component = (
            rating_component + 1
        ) / 2

    else:

        rating_component = 0.5

    # --------------------------------------------------------
    # Final impact index
    # --------------------------------------------------------

    data["injury_impact_index"] = (
        (
            0.60 * duration_component
            +
            0.40 * rating_component
        )
        * 100
    ).round(1)

    return data


def load_uploaded_file(uploaded_file):

    if uploaded_file is None:
        return None

    try:

        if uploaded_file.name.lower().endswith(".csv"):

            return pd.read_csv(
                uploaded_file
            )

        if uploaded_file.name.lower().endswith(
            (".xlsx", ".xls")
        ):

            return pd.read_excel(
                uploaded_file
            )

        st.error(
            "Please upload a CSV or Excel file."
        )

        return None

    except Exception as error:

        st.error(
            f"Unable to read the file: {error}"
        )

        return None


def safe_mean(series):

    values = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if len(values) == 0:
        return np.nan

    return float(values.mean())


def generate_insights(data):

    insights = []

    if len(data) == 0:

        return [
            "No records are available for the selected filters."
        ]

    # --------------------------------------------------------
    # Longest injury
    # --------------------------------------------------------

    if (
        "injury_days" in data.columns
        and
        data["injury_days"].notna().any()
    ):

        row = data.loc[
            data["injury_days"].idxmax()
        ]

        insights.append(
            f"Longest recorded injury: "
            f"{row['player']} — "
            f"{row['injury_days']:.0f} days."
        )

    # --------------------------------------------------------
    # Most injuries team
    # --------------------------------------------------------

    team_counts = (
        data["team"]
        .value_counts()
    )

    if len(team_counts) > 0:

        insights.append(
            f"Highest injury volume: "
            f"{team_counts.index[0]} "
            f"with {team_counts.iloc[0]:,} "
            f"recorded case(s)."
        )

    # --------------------------------------------------------
    # Most common injury
    # --------------------------------------------------------

    injury_counts = (
        data["injury_type"]
        .value_counts()
    )

    if len(injury_counts) > 0:

        insights.append(
            f"Most frequent injury category: "
            f"{injury_counts.index[0]} "
            f"({injury_counts.iloc[0]:,} case(s))."
        )

    # --------------------------------------------------------
    # Average rating
    # --------------------------------------------------------

    if (
        "rating" in data.columns
        and
        data["rating"].notna().any()
    ):

        insights.append(
            f"Average recorded performance rating: "
            f"{data['rating'].mean():.2f}."
        )

    # --------------------------------------------------------
    # Average points
    # --------------------------------------------------------

    if (
        "points" in data.columns
        and
        data["points"].notna().any()
    ):

        insights.append(
            f"Average match points in the available "
            f"records: {data['points'].mean():.2f}."
        )

    return insights[:5]


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <h1>⚽ FootLens Analytics</h1>

        <p>
            Player Injuries & Team Performance
            Intelligence Dashboard
        </p>

        <p class="small-note">
            Data-driven insights for injury monitoring,
            squad planning and football performance analysis.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "⚙️ Dashboard Controls"
)

st.sidebar.caption(
    "Upload the football dataset supplied for your assessment."
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Football Dataset",
    type=[
        "csv",
        "xlsx",
        "xls"
    ]
)


# ============================================================
# DATA LOADING
# ============================================================

if uploaded_file is None:

    st.info(
        "👋 Upload your football injury/performance "
        "dataset from the sidebar to start the dashboard."
    )

    st.markdown(
        "### Expected Dataset Fields"
    )

    st.write(
        """
        The dashboard supports common versions of:

        **Player Name • Team/Club • Match Result •
        Injury Start Date • Injury End Date •
        Performance Rating • Age • Injury Type •
        Goals • Match Date • Season**
        """
    )

    st.stop()


raw_data = load_uploaded_file(
    uploaded_file
)

if raw_data is None:
    st.stop()


original_row_count = len(
    raw_data
)


# ============================================================
# CLEAN DATA
# ============================================================

data = standardize_columns(
    raw_data
)

data = add_derived_metrics(
    data
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader(
    "🔎 Filters"
)

team_options = sorted(
    data["team"]
    .dropna()
    .unique()
    .tolist()
)

player_options = sorted(
    data["player"]
    .dropna()
    .unique()
    .tolist()
)

injury_options = sorted(
    data["injury_type"]
    .dropna()
    .unique()
    .tolist()
)


selected_teams = st.sidebar.multiselect(
    "Teams / Clubs",
    team_options,
    default=team_options
)


selected_players = st.sidebar.multiselect(
    "Players",
    player_options,
    default=player_options
)


selected_injuries = st.sidebar.multiselect(
    "Injury Types",
    injury_options,
    default=injury_options
)


filtered_data = data[
    data["team"].isin(
        selected_teams
    )
    &
    data["player"].isin(
        selected_players
    )
    &
    data["injury_type"].isin(
        selected_injuries
    )
].copy()


# ============================================================
# DATE FILTER
# ============================================================

if (
    "injury_start" in filtered_data.columns
    and
    filtered_data["injury_start"].notna().any()
):

    minimum_date = (
        filtered_data["injury_start"]
        .min()
        .date()
    )

    maximum_date = (
        filtered_data["injury_start"]
        .max()
        .date()
    )

    selected_dates = st.sidebar.date_input(
        "Injury Date Range",
        value=(
            minimum_date,
            maximum_date
        ),
        min_value=minimum_date,
        max_value=maximum_date
    )

    if (
        isinstance(selected_dates, tuple)
        and
        len(selected_dates) == 2
    ):

        filtered_data = filtered_data[
            filtered_data["injury_start"]
            .dt.date
            .between(
                selected_dates[0],
                selected_dates[1]
            )
        ]


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📊 Executive Overview'
    '</div>',
    unsafe_allow_html=True
)


total_injuries = len(
    filtered_data
)

players_affected = (
    filtered_data["player"]
    .nunique()
)

clubs_affected = (
    filtered_data["team"]
    .nunique()
)

average_recovery = safe_mean(
    filtered_data["injury_days"]
)

average_rating = (
    safe_mean(
        filtered_data["rating"]
    )
    if "rating" in filtered_data.columns
    else np.nan
)

average_impact = safe_mean(
    filtered_data["injury_impact_index"]
)


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


kpi1.metric(
    "🩹 Injury Cases",
    f"{total_injuries:,}"
)

kpi2.metric(
    "👤 Players Affected",
    f"{players_affected:,}"
)

kpi3.metric(
    "🏟️ Clubs",
    f"{clubs_affected:,}"
)

kpi4.metric(
    "⏱️ Avg Recovery",
    (
        "N/A"
        if np.isnan(average_recovery)
        else f"{average_recovery:.1f} days"
    )
)

kpi5.metric(
    "📉 Avg Impact",
    (
        "N/A"
        if np.isnan(average_impact)
        else f"{average_impact:.1f}/100"
    )
)


st.caption(
    f"Original records: {original_row_count:,} | "
    f"Records after filters: {len(filtered_data):,} | "
    "The Injury Impact Index is an analytical comparison measure, "
    "not a medical severity score."
)


# ============================================================
# AUTOMATED INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🧠 Automated Insights'
    '</div>',
    unsafe_allow_html=True
)


insights = generate_insights(
    filtered_data
)

insight_columns = st.columns(3)


for index, insight in enumerate(
    insights
):

    with insight_columns[
        index % 3
    ]:

        st.markdown(
            f"""
            <div class="insight">
                💡 {insight}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# TABS
# ============================================================

performance_tab, injury_tab, player_tab, team_tab, data_tab = st.tabs(
    [
        "📊 Performance",
        "🩹 Injury Intelligence",
        "🏆 Players & Comebacks",
        "🏟️ Team Analysis",
        "📋 Data & Method"
    ]
)


# ============================================================
# PERFORMANCE TAB
# ============================================================

with performance_tab:

    st.markdown(
        "### 📊 Performance Impact Analysis"
    )

    chart1, chart2 = st.columns(2)

    # --------------------------------------------------------
    # Chart 1
    # --------------------------------------------------------

    with chart1:

        if (
            "injury_type" in filtered_data.columns
            and
            "injury_impact_index"
            in filtered_data.columns
        ):

            impact_data = (
                filtered_data
                .groupby(
                    "injury_type",
                    as_index=False
                )
                .agg(
                    impact=(
                        "injury_impact_index",
                        "mean"
                    ),
                    cases=(
                        "injury_type",
                        "size"
                    )
                )
                .sort_values(
                    "impact",
                    ascending=False
                )
                .head(10)
            )

            figure = px.bar(
                impact_data,
                x="impact",
                y="injury_type",
                orientation="h",
                text="impact",
                hover_data=["cases"],
                title=(
                    "Top Injury Categories "
                    "by Impact Index"
                ),
                labels={
                    "impact":
                    "Average Impact Index",

                    "injury_type":
                    "Injury Type"
                }
            )

            figure.update_traces(
                texttemplate="%{text:.1f}",
                textposition="outside"
            )

            figure.update_layout(
                height=450,
                yaxis={
                    "categoryorder":
                    "total ascending"
                }
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )


    # --------------------------------------------------------
    # Chart 2
    # --------------------------------------------------------

    with chart2:

        if (
            "age" in filtered_data.columns
            and
            "injury_impact_index"
            in filtered_data.columns
        ):

            scatter_data = (
                filtered_data
                .dropna(
                    subset=[
                        "age",
                        "injury_impact_index"
                    ]
                )
            )

            if len(scatter_data) > 0:

                figure = px.scatter(
                    scatter_data,
                    x="age",
                    y="injury_impact_index",
                    color="team",
                    hover_name="player",
                    hover_data=[
                        "injury_type",
                        "injury_days"
                    ],
                    trendline=(
                        "ols"
                        if len(scatter_data) >= 3
                        else None
                    ),
                    title=(
                        "Player Age vs "
                        "Injury Impact"
                    ),
                    labels={
                        "age":
                        "Player Age",

                        "injury_impact_index":
                        "Impact Index"
                    }
                )

                figure.update_layout(
                    height=450
                )

                st.plotly_chart(
                    figure,
                    use_container_width=True
                )

            else:

                st.warning(
                    "Age data is unavailable "
                    "for the selected records."
                )


    # --------------------------------------------------------
    # Performance Timeline
    # --------------------------------------------------------

    st.markdown(
        "### 📈 Player Performance Timeline"
    )

    if "rating" in filtered_data.columns:

        timeline_data = (
            filtered_data
            .dropna(
                subset=["rating"]
            )
            .copy()
        )

        if (
            "match_date"
            in timeline_data.columns
            and
            timeline_data["match_date"]
            .notna()
            .any()
        ):

            timeline_data = (
                timeline_data
                .sort_values(
                    "match_date"
                )
            )

            figure = px.line(
                timeline_data,
                x="match_date",
                y="rating",
                color="player",
                markers=True,
                hover_data=[
                    "team",
                    "injury_type"
                ],
                title=(
                    "Player Performance "
                    "Timeline"
                ),
                labels={
                    "match_date":
                    "Match Date",

                    "rating":
                    "Performance Rating"
                }
            )

            figure.update_layout(
                height=480
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )

        else:

            st.info(
                "A Match Date column is needed "
                "for the full before/during/after "
                "performance timeline."
            )


# ============================================================
# INJURY INTELLIGENCE TAB
# ============================================================

with injury_tab:

    st.markdown(
        "### 🩹 Injury Intelligence"
    )

    chart3, chart4 = st.columns(2)

    # --------------------------------------------------------
    # Monthly Injury Trend
    # --------------------------------------------------------

    with chart3:

        if (
            "injury_month_num"
            in filtered_data.columns
        ):

            monthly_data = (
                filtered_data
                .dropna(
                    subset=[
                        "injury_month_num"
                    ]
                )
                .groupby(
                    [
                        "injury_month_num",
                        "injury_month"
                    ]
                )
                .size()
                .reset_index(
                    name="cases"
                )
                .sort_values(
                    "injury_month_num"
                )
            )

            figure = px.line(
                monthly_data,
                x="injury_month",
                y="cases",
                markers=True,
                title=(
                    "Monthly Injury Trend"
                ),
                labels={
                    "injury_month":
                    "Month",

                    "cases":
                    "Injury Cases"
                }
            )

            figure.update_layout(
                height=420
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )


    # --------------------------------------------------------
    # Heatmap
    # --------------------------------------------------------

    with chart4:

        if (
            "team" in filtered_data.columns
            and
            "injury_month"
            in filtered_data.columns
        ):

            heatmap_data = pd.crosstab(
                filtered_data["team"],
                filtered_data["injury_month"]
            )

            month_order = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
            ]

            available_months = [
                month
                for month in month_order
                if month in heatmap_data.columns
            ]

            heatmap_data = (
                heatmap_data[
                    available_months
                ]
            )

            if len(heatmap_data.columns) > 0:

                figure = px.imshow(
                    heatmap_data,
                    aspect="auto",
                    text_auto=True,
                    title=(
                        "Injury Frequency "
                        "Heatmap — Team × Month"
                    ),
                    labels={
                        "x": "Month",
                        "y": "Team",
                        "color": "Cases"
                    }
                )

                figure.update_layout(
                    height=420
                )

                st.plotly_chart(
                    figure,
                    use_container_width=True
                )


    # --------------------------------------------------------
    # Recovery Distribution
    # --------------------------------------------------------

    if (
        filtered_data["injury_days"]
        .notna()
        .any()
    ):

        figure = px.histogram(
            filtered_data.dropna(
                subset=["injury_days"]
            ),
            x="injury_days",
            nbins=20,
            marginal="box",
            title=(
                "Recovery Duration Distribution"
            ),
            labels={
                "injury_days":
                "Injury Duration (Days)"
            }
        )

        figure.update_layout(
            height=430
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )


    # --------------------------------------------------------
    # Longest Injuries
    # --------------------------------------------------------

    longest_injuries = (
        filtered_data
        .dropna(
            subset=["injury_days"]
        )
        .sort_values(
            "injury_days",
            ascending=False
        )
        .head(10)
    )

    if len(longest_injuries) > 0:

        figure = px.bar(
            longest_injuries
            .sort_values(
                "injury_days"
            ),
            x="injury_days",
            y="player",
            color="team",
            orientation="h",
            hover_data=[
                "injury_type"
            ],
            title=(
                "10 Longest Recorded Injuries"
            ),
            labels={
                "injury_days":
                "Days",

                "player":
                "Player"
            }
        )

        figure.update_layout(
            height=470
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )


# ============================================================
# PLAYER / COMEBACK TAB
# ============================================================

with player_tab:

    st.markdown(
        "### 🏆 Player & Comeback Analysis"
    )

    if "rating" in filtered_data.columns:

        player_summary = (
            filtered_data
            .groupby(
                "player",
                as_index=False
            )
            .agg(

                matches=(
                    "player",
                    "size"
                ),

                avg_rating=(
                    "rating",
                    "mean"
                ),

                max_rating=(
                    "rating",
                    "max"
                ),

                avg_impact=(
                    "injury_impact_index",
                    "mean"
                ),

                avg_recovery=(
                    "injury_days",
                    "mean"
                )
            )
        )

        # ----------------------------------------------------
        # Comeback score
        # ----------------------------------------------------

        player_summary[
            "comeback_score"
        ] = (

            (
                player_summary[
                    "max_rating"
                ]
                -
                player_summary[
                    "avg_rating"
                ]
            )
            /
            player_summary[
                "avg_rating"
            ].replace(
                0,
                np.nan
            )
            * 100

        )

        player_summary[
            "comeback_score"
        ] = (
            player_summary[
                "comeback_score"
            ]
            .replace(
                [
                    np.inf,
                    -np.inf
                ],
                np.nan
            )
        )

        leaderboard = (
            player_summary
            .dropna(
                subset=[
                    "comeback_score"
                ]
            )
            .sort_values(
                "comeback_score",
                ascending=False
            )
            .head(10)
        )

        # ----------------------------------------------------
        # Leaderboard chart
        # ----------------------------------------------------

        if len(leaderboard) > 0:

            figure = px.bar(
                leaderboard
                .sort_values(
                    "comeback_score"
                ),
                x="comeback_score",
                y="player",
                orientation="h",
                text="comeback_score",
                title=(
                    "🏆 Comeback Leaderboard"
                ),
                labels={
                    "comeback_score":
                    "Comeback Score (%)"
                }
            )

            figure.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside"
            )

            figure.update_layout(
                height=470
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Player table
        # ----------------------------------------------------

        st.markdown(
            "#### Player Summary"
        )

        display_columns = [
            "player",
            "matches",
            "avg_rating",
            "max_rating",
            "avg_impact",
            "avg_recovery",
            "comeback_score"
        ]

        st.dataframe(
            player_summary
            .sort_values(
                "avg_impact",
                ascending=False
            )[display_columns]
            .round(2),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Performance Rating is required "
            "for comeback analysis."
        )


# ============================================================
# TEAM ANALYSIS TAB
# ============================================================

with team_tab:

    st.markdown(
        "### 🏟️ Team-Level Decision Support"
    )

    team_summary = (
        filtered_data
        .groupby(
            "team",
            as_index=False
        )
        .agg(

            injury_cases=(
                "team",
                "size"
            ),

            players_affected=(
                "player",
                "nunique"
            ),

            avg_recovery_days=(
                "injury_days",
                "mean"
            ),

            avg_impact=(
                "injury_impact_index",
                "mean"
            )
        )
        .sort_values(
            "avg_impact",
            ascending=False
        )
    )

    team_chart1, team_chart2 = st.columns(2)

    # --------------------------------------------------------
    # Team injury cases
    # --------------------------------------------------------

    with team_chart1:

        figure = px.bar(
            team_summary
            .sort_values(
                "injury_cases"
            ),
            x="injury_cases",
            y="team",
            orientation="h",
            text="injury_cases",
            title=(
                "Injury Cases by Club"
            ),
            labels={
                "injury_cases":
                "Cases",

                "team":
                "Club"
            }
        )

        figure.update_layout(
            height=450
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )


    # --------------------------------------------------------
    # Injury load vs impact
    # --------------------------------------------------------

    with team_chart2:

        figure = px.scatter(
            team_summary,
            x="injury_cases",
            y="avg_impact",
            size="players_affected",
            color="team",
            hover_data=[
                "avg_recovery_days"
            ],
            title=(
                "Club Injury Load vs "
                "Average Impact"
            ),
            labels={
                "injury_cases":
                "Number of Injury Cases",

                "avg_impact":
                "Average Impact Index"
            }
        )

        figure.update_layout(
            height=450
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )


    # --------------------------------------------------------
    # Team table
    # --------------------------------------------------------

    st.markdown(
        "#### Team Performance Summary"
    )

    st.dataframe(
        team_summary.round(2),
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # Result distribution
    # --------------------------------------------------------

    if "result" in filtered_data.columns:

        result_data = (
            filtered_data[
                "result"
            ]
            .astype(str)
            .str.title()
            .value_counts()
            .reset_index()
        )

        result_data.columns = [
            "result",
            "count"
        ]

        if len(result_data) > 0:

            figure = px.pie(
                result_data,
                names="result",
                values="count",
                hole=0.48,
                title=(
                    "Match Result Distribution"
                )
            )

            figure.update_layout(
                height=420
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )


# ============================================================
# DATA & METHOD TAB
# ============================================================

with data_tab:

    st.markdown(
        "### 📋 Data Quality & Methodology"
    )

    quality1, quality2, quality3 = st.columns(3)

    quality1.metric(
        "Original Rows",
        f"{original_row_count:,}"
    )

    quality2.metric(
        "Filtered Rows",
        f"{len(filtered_data):,}"
    )

    quality3.metric(
        "Columns",
        f"{filtered_data.shape[1]:,}"
    )


    # --------------------------------------------------------
    # Cleaning
    # --------------------------------------------------------

    st.markdown(
        "#### 🧹 Data Cleaning Performed"
    )

    cleaning_steps = [

        "Column names are standardised for consistent analysis.",

        "Injury dates are converted to datetime format.",

        "Numeric variables such as age, goals and ratings "
        "are converted safely.",

        "Missing text values are replaced with readable "
        "placeholders.",

        "Injury duration is calculated using injury start "
        "and end dates.",

        "Month and season features are created for "
        "trend analysis.",

        "An Injury Impact Index is engineered to compare "
        "records consistently."
    ]

    for step in cleaning_steps:

        st.write(
            "✓",
            step
        )


    # --------------------------------------------------------
    # Research questions
    # --------------------------------------------------------

    st.markdown(
        "#### 🔬 Five Business Questions"
    )

    questions = [

        "Which injuries are associated with the highest "
        "estimated team/player performance impact?",

        "What is the team's available win/draw/loss "
        "pattern in records associated with player absence?",

        "How does player performance change around "
        "the injury and recovery period?",

        "Are there particular months or clubs with "
        "clusters of injury cases?",

        "Which clubs and players show the greatest "
        "injury burden or strongest comeback patterns?"
    ]

    for number, question in enumerate(
        questions,
        1
    ):

        st.write(
            f"**Q{number}.** {question}"
        )


    # --------------------------------------------------------
    # Raw data
    # --------------------------------------------------------

    st.markdown(
        "#### 📄 Data Preview"
    )

    st.dataframe(
        filtered_data.head(100),
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    csv_data = (
        filtered_data
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label=(
            "⬇️ Download Filtered "
            "Analysis Data"
        ),
        data=csv_data,
        file_name=(
            "footlens_filtered_data.csv"
        ),
        mime="text/csv"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "⚽ FootLens Analytics • "
    "Mathematics for AI-II • "
    "Artificial Intelligence • "
    "Interactive Football Analytics Dashboard"
)
