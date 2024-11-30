import streamlit as st

# Configure the app layout
st.set_page_config(page_title="Health Tracker App", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stButton > button {
        width: 200px;
        height: 50px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
        margin-top: 10px;
    }
    .category-container {
        text-align: center;
        margin: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main Page
st.title("Health Tracker App")
st.subheader("Built by 10xTechClub C2 Students")

# Categories with Images and Buttons
st.markdown("### Choose a Category")

# Align Categories in a Horizontal Row
col1, col2, col3 = st.columns([1, 1, 1])  # Equal-sized columns for perfect alignment

# Nutrition with col1:
with col1:
    st.image("nutrition.png", caption="Nutrition", width=120)
    if st.button("Nutrition"):
        st.session_state['page'] = 'nutrition'

# Fitness with col2:
with col2:
    st.image("fitness.png", caption="Fitness", width=120)
    if st.button("Fitness"):
        st.session_state['page'] = 'fitness'

# Sleep with col3:
with col3:
    st.image("sleeping.png", caption="Sleep", width=120)
    if st.button("Sleep"):
        st.session_state['page'] = 'sleep'

# Handle Page Navigation
if 'page' in st.session_state:
    if st.session_state['page'] == 'nutrition':
        st.write("**Opening Nutrition App...**")
        exec(open("Nutri.py").read())
        # Code to launch Nutrition App

    elif st.session_state['page'] == 'fitness':
        st.write("**Opening Fitness Subcategories...**")
        st.markdown("### Choose a Fitness Option")
        
        # Add Fitness options to the sidebar
        fitness_option = st.sidebar.selectbox(
            "Choose a Fitness App",
            ["Strava App", "Step Counter", "Workout Planner"]
        )

        if fitness_option == "Strava App":
            st.write("**Opening Strava App...**")
            exec(open("strava.py").read())
            # Code to launch Strava App

        elif fitness_option == "Step Counter":
            st.write("**Opening Step Counter App...**")
            exec(open("googlefit.py").read())
            # Code to launch Step Counter App

        elif fitness_option == "Workout Planner":
            st.write("**Opening Workout Planner App...**")
            exec(open("workout_planner.py").read())
            # Code to launch Workout Planner App

    elif st.session_state['page'] == 'sleep':
        st.write("**Opening Sleep Tracker App...**")
        exec(open("slept.py").read())
        # Code to launch Sleep Tracker
