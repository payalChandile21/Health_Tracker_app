import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Path to your client secret JSON file
CLIENT_SECRETS_FILE = "client_secret.json"

# The scopes required to access Fit data
SCOPES = [
    "https://www.googleapis.com/auth/fitness.activity.read",
    "https://www.googleapis.com/auth/fitness.location.read",
    "https://www.googleapis.com/auth/fitness.body.read"
]

# API version
API_SERVICE_NAME = 'fitness'
API_VERSION = 'v1'

# Sidebar for user input
st.sidebar.title("Google Fit Data Settings")
st.sidebar.subheader("Authentication and Data Settings")

# Authentication flow
@st.cache_resource
def authenticate_google_fit():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials

# Button to trigger authentication
if st.sidebar.button("Authenticate Google Fit"):
    credentials = authenticate_google_fit()
    # Build the API service after authentication
    service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    
    # Date Range Input
    start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=7))
    end_date = st.sidebar.date_input("End Date", datetime.now())
    
    # Convert selected date to timestamp for API query
    start_time = int(datetime.combine(start_date, datetime.min.time()).astimezone(timezone.utc).timestamp() * 1000)
    end_time = int(datetime.combine(end_date, datetime.min.time()).astimezone(timezone.utc).timestamp() * 1000)
    
    # Request step data from the API
    dataset = f"{start_time}-{end_time}"
    response = service.users().dataset().aggregate(userId="me", body={
        "aggregateBy": [{"dataTypeName": "com.google.step_count.delta"}],
        "bucketByTime": {"durationMillis": 86400000},  # Daily steps
        "startTimeMillis": start_time,
        "endTimeMillis": end_time
    }).execute()

    # Initialize lists for plotting
    dates = []
    steps_counts = []
    total_calories_per_date = {}
    calories_per_step = 0.05  # Average calories burned per step

    # Extract data for plotting
    for bucket in response.get('bucket', []):
        steps = 0
        start_time = int(bucket['startTimeMillis'])
        date = datetime.utcfromtimestamp(start_time / 1000).strftime('%Y-%m-%d')

        for dataset in bucket.get('dataset', []):
            for point in dataset.get('point', []):
                for value in point.get('value', []):
                    steps += value.get('intVal', 0)

        # Calculate estimated calories burned
        estimated_calories = steps * calories_per_step

        # Store data for plotting
        dates.append(date)
        steps_counts.append(steps)

        # Accumulate calories for the same date
        total_calories_per_date[date] = total_calories_per_date.get(date, 0) + estimated_calories

    # Prepare data for plotting calories
    calories_burned = list(total_calories_per_date.values())

    # Streamlit app layout
    st.title("Fitness Data Overview")
    
    # Step Count Plot
    st.header("Step Count Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dates, steps_counts, marker='o', linestyle='-', color='b')
    ax.set_title('Step Count Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Step Count')
    ax.grid(True)
    st.pyplot(fig)

    # Calories Burned Plot
    st.header("Estimated Calories Burned by Date")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(dates, calories_burned, color='green')
    ax.set_title('Estimated Calories Burned by Date')
    ax.set_xlabel('Date')
    ax.set_ylabel('Estimated Calories Burned')
    ax.grid(axis='y')
    st.pyplot(fig)
