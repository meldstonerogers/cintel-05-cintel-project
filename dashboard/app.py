# --------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# --------------------------------------------

# From shiny, import just reactive and render
from shiny import reactive, render

# From shiny.express, import just ui and inputs if needed
from shiny.express import ui

import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats
from shinyswatch import theme

# --------------------------------------------
# Import icons as you like
# --------------------------------------------

# https://fontawesome.com/v4/cheatsheet/
from faicons import icon_svg

# --------------------------------------------
# Shiny EXPRESS VERSION
# --------------------------------------------

# --------------------------------------------
# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------

UPDATE_INTERVAL_SECS: int = 3

# --------------------------------------------
# Initialize a REACTIVE VALUE with a common data structure
# The reactive value is used to store state (information)
# Used by all the display components that show this live data.
# This reactive value is a wrapper around a DEQUE of readings
# --------------------------------------------

DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

# --------------------------------------------
# Initialize a REACTIVE CALC that all display components can call
# to get the latest data and display it.
# The calculation is invalidated every UPDATE_INTERVAL_SECS
# to trigger updates.
# It returns a tuple with everything needed to display the data.
# Very easy to expand or modify.
# --------------------------------------------


@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic
    temp = round(random.uniform(-18, -16), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"temp":temp, "timestamp":timestamp}

    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # For Display: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)

    # For Display: Get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry

    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, df, latest_dictionary_entry

# CSS for scrollable content
style = """
<style>
    body {
        overflow-y: scroll;  /* Always show the vertical scrollbar */
        padding: 20px;
        height: 100vh;        /* Ensure the body takes full viewport height */
    }
    .shiny-main-content {
        max-height: 80vh;     /* Limit the height of the main content */
        overflow-y: scroll;   /* Always add vertical scrollbar if needed */
    }
</style>
"""

# Define the Shiny UI Page layout
# Call the ui.page_opts() function
# Set title to a string in quotes that will appear at the top
# Set fillable to True to use the whole page width for the UI
ui.page_opts(
     title="Melissa's PyShiny Express: Live Data Example", 
     fillable=True, 
     theme=theme.darkly, 
     head=ui.HTML('<link rel="icon" href="www/favicon.ico" type="image/x-icon">')
     ) 


# Sidebar is typically used for user interaction/information
# Note the with statement to create the sidebar followed by a colon
# Everything in the sidebar is indented consistently
with ui.sidebar(bg="#301A4B"):
    ui.h2("Antarctic Explorer", class_="text-center")
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )
    ui.hr()
    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/meldstonerogers/cintel-05-cintel",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://meldstonerogers.github.io/cintel-05-cintel-project/",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "PyShiny Express",
        href="hhttps://shiny.posit.co/blog/posts/shiny-express/",
        target="_blank",
    )

# In Shiny Express, everything not in the sidebar is in the main panel

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("snowflake"),
        theme="bg-gradient-blue-purple",
    ):

        "Current Temperature"

        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} C"

        "warmer than usual"

  

    with ui.card(full_screen=True):
        ui.card_header("Current Date and Time")

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"

with ui.layout_columns():
#with ui.card(full_screen=True, height="800px"):
        with ui.card(full_screen=True):
            ui.card_header("Most Recent Readings")

            @render.data_frame
            def display_df():
                """Get the latest reading and return a dataframe with current readings"""
                deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
                pd.set_option('display.width', None)        # Use maximum width
                return render.DataGrid( df,width="100%")

        with ui.value_box(
                showcase=icon_svg("thermometer"),
                theme="bg-gradient-blue-purple",
            ):
                "Average Temperature Last 24 Hours"
                @render.text
                def display_avgtemp():
                        """Get the average temperature for the last 24 hours."""
                        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

                        # Ensure the DataFrame is not empty
                        if not df.empty:
                            # Convert the 'timestamp' column to datetime for filtering
                            df["timestamp"] = pd.to_datetime(df["timestamp"])

                            # Filter for the last 24 hours
                            now = pd.Timestamp.now()
                            last_24_hours = df[df["timestamp"] >= now - pd.Timedelta(hours=24)]

                            # Compute the average temperature if there are any readings
                            if not last_24_hours.empty:
                                avg_temp = last_24_hours["temp"].mean()
                                return f"{avg_temp:.2f} °C"
                            else:
                                return "No temperature readings in the last 24 hours."

                        return "No data available."


with ui.card(full_scree=True):
    ui.card_header("Chart with Current Temperature Trend")
    @render_plotly
    def display_plot():
        # Fetch from the reactive calc function
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

        # Ensure the DataFrame is not empty before plotting
        if not df.empty:
            # Convert the 'timestamp' column to datetime for better plotting
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # Create scatter plot for readings
            # pass in the df, the name of the x column, the name of the y column,
            # and more
        
            fig = px.scatter(df,
            x="timestamp",
            y="temp",
            title="Temperature Readings with Regression Line",
            labels={"temp": "Temperature (°C)", "timestamp": "Time"},
            )

            # Add Emoji symbols as "text" on the markers
            fig.update_traces(
                marker=dict(size=.5, color="dark blue"),  # Marker customization
                text=["❄️" for _ in range(len(df))],  # Snowflake emoji for all points
                textposition="middle center",  # Position of the emoji
                mode="markers+text"  # Show both marker and text
            )
            
            # Linear regression - we need to get a list of the
            # Independent variable x values (time) and the
            # Dependent variable y values (temp)
            # then, it's pretty easy using scipy.stats.linregress()

            # For x let's generate a sequence of integers from 0 to len(df)
            sequence = range(len(df))
            x_vals = list(sequence)
            y_vals = df["temp"]

            slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
            df['best_fit_line'] = [slope * x + intercept for x in x_vals]

            # Add the regression line to the figure
            fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line', line=dict(color='darkblue', width=2))

            # Update layout as needed to customize further
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Temperature (°C)",
                plot_bgcolor='#F0F3F1',
                paper_bgcolor='#434343',
                font=dict(color='white'), 
                ),

        return fig

import warnings
warnings.simplefilter("ignore", category=RuntimeWarning)


    




