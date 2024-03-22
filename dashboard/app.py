# --------------------------------------------
# Imports at the top
# --------------------------------------------

from shiny import App, render, ui, reactive
import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.graph_objects as go
from shinywidgets import render_widget, output_widget
from scipy import stats

# --------------------------------------------
# Import icons as you like
# --------------------------------------------

from faicons import icon_svg  

# From https://icons.getbootstrap.com/icons/piggy-bank/
piggy_bank = ui.HTML(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="bi bi-piggy-bank " style="fill:currentColor;height:100%;" aria-hidden="true" role="img" ><path d="M5 6.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0zm1.138-1.496A6.613 6.613 0 0 1 7.964 4.5c.666 0 1.303.097 1.893.273a.5.5 0 0 0 .286-.958A7.602 7.602 0 0 0 7.964 3.5c-.734 0-1.441.103-2.102.292a.5.5 0 1 0 .276.962z"></path>\n<path fill-rule="evenodd" d="M7.964 1.527c-2.977 0-5.571 1.704-6.32 4.125h-.55A1 1 0 0 0 .11 6.824l.254 1.46a1.5 1.5 0 0 0 1.478 1.243h.263c.3.513.688.978 1.145 1.382l-.729 2.477a.5.5 0 0 0 .48.641h2a.5.5 0 0 0 .471-.332l.482-1.351c.635.173 1.31.267 2.011.267.707 0 1.388-.095 2.028-.272l.543 1.372a.5.5 0 0 0 .465.316h2a.5.5 0 0 0 .478-.645l-.761-2.506C13.81 9.895 14.5 8.559 14.5 7.069c0-.145-.007-.29-.02-.431.261-.11.508-.266.705-.444.315.306.815.306.815-.417 0 .223-.5.223-.461-.026a.95.95 0 0 0 .09-.255.7.7 0 0 0-.202-.645.58.58 0 0 0-.707-.098.735.735 0 0 0-.375.562c-.024.243.082.48.32.654a2.112 2.112 0 0 1-.259.153c-.534-2.664-3.284-4.595-6.442-4.595zM2.516 6.26c.455-2.066 2.667-3.733 5.448-3.733 3.146 0 5.536 2.114 5.536 4.542 0 1.254-.624 2.41-1.67 3.248a.5.5 0 0 0-.165.535l.66 2.175h-.985l-.59-1.487a.5.5 0 0 0-.629-.288c-.661.23-1.39.359-2.157.359a6.558 6.558 0 0 1-2.157-.359.5.5 0 0 0-.635.304l-.525 1.471h-.979l.633-2.15a.5.5 0 0 0-.17-.534 4.649 4.649 0 0 1-1.284-1.541.5.5 0 0 0-.446-.275h-.56a.5.5 0 0 1-.492-.414l-.254-1.46h.933a.5.5 0 0 0 .488-.393zm12.621-.857a.565.565 0 0 1-.098.21.704.704 0 0 1-.044-.025c-.146-.09-.157-.175-.152-.223a.236.236 0 0 1 .117-.173c.049-.027.08-.021.113.012a.202.202 0 0 1 .064.199z"></path></svg>'
)

# --------------------------------------------
# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------

UPDATE_INTERVAL_SECS: int  = 3

# --------------------------------------------
# Initialize a REACTIVE VALUE with a common data structure 
# Used by all the live data components
# This reactive value is a wrapper around a DEQUE of readings
# --------------------------------------------

DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic 
    temp = round(random.uniform(-18, -16), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"temp": temp, "timestamp": timestamp}
    
    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # Processing: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)

    # Processing: Get the latest entry 
    latest_dictionary_entry = new_dictionary_entry

    # Return a tuple with everything we need 
    return deque_snapshot, df, latest_dictionary_entry


# --------------------------------------------
# Shiny Core
# Define the Shiny UI layout
# --------------------------------------------

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.h2("Antarctic Explorer", class_="text-center"),
            ui.p("A demonstration of real-time temperature readings in Antarctica.", class_="text-center"),
        ),
        ui.panel_main(
          ui.value_box(
            "Real Temp",
            ui.output_text("display_temp"),
            "Warmer than usual",
            showcase=piggy_bank,
            theme="bg-gradient-indigo-purple",
              full_screen=False,
          ),
          ui.value_box(
            "Real Time",
            ui.output_text("display_time"),
            "Daylight Savings Time",
            showcase=piggy_bank,
            theme="bg-gradient-indigo-purple",
            full_screen=False,
          ),
          ui.output_data_frame("display_df"),
          output_widget("display_plot"),
        )
    )
)

# --------------------------------------------
# Shiny Core 
# Define the server logic to render the UI components based on reactive values
# ---------------------------------------------

def server(input, output, session):

  # --------------
  # Define a function to render.text with the TEMP
  # With Core, we must add this function to the app_ui
  # by calling ui.output_text()
  # And passing in whatever we name this function as a string
  # --------------
  @render.text
  def display_temp():
    ''' Get the latest reading and return a temperature string'''
    deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
    return f"{latest_dictionary_entry['temp']}°C"

  # --------------
  # Define a function to render.text with the TIME
  # With Core, we must add this function to the app_ui
  # by calling ui.output_text()
  # And passing in whatever we name this function as a string
  # --------------
  @render.text
  def display_time():
    ''' Get the latest reading and return a timestamp string'''
    deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
    return f"{latest_dictionary_entry['timestamp']}"
  
  # --------------
  # Define a function to render.data_frame with our DF
  # With Core, we must add this function to the app_ui
  # by calling ui.output_data_frame()
  # And passing in whatever we name this function as a string
  # --------------
  @render.data_frame
  def display_df():
    ''' Get the latest reading and return a dataframe with current readings'''
    deque_snapshot, df, latest_dictionary_entry =  reactive_calc_combined()
    return df

  # --------------
  # Define a function to render_widget with a PLOT
  # With Core, we must add this function to the app_ui
  # by calling output_widget() - NOT ui.output_widget - 
  # And passing in whatever we name this function as a string
  # --------------

  @render_widget
  def display_plot():
    # Fetch from the reactive calc function
    deque_snapshot, df, latest_dictionary_entry =  reactive_calc_combined()

    # Ensure the DataFrame is not empty before plotting
    if not df.empty:
        # Convert the 'timestamp' column to datetime for better plotting
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Create scatter plot for readings
        fig = go.Figure()
        fig.add_trace(
           go.Scatter(
              x=df['timestamp'], 
              y=df['temp'],
              mode='markers',
              name='Temperature Readings',
              marker=dict(size=10, color='blue') 
            )
        )

        # Linear regression - we need to get a list of the
        # Independent variable x values (time) and the
        # Dependent variable y values (temp)
        # then, it's pretty easy using scipy.stats.linregress()

        # For x let's generate a sequence of integers from 0 to len(df)
        sequence = range(len(df))
        x_vals = list(sequence)
        y_vals = df['temp']

        slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
        best_fit_line = [slope * x + intercept for x in x_vals]

        fig.add_trace(go.Scatter(
           x=df['timestamp'], 
           y=best_fit_line,
           mode='lines',
           name='Regression Line'))

        # Update layout with a dynamic x-axis range to create the scrolling effect
        # Set the window size to display in the plot. Adjust 'window_size' as needed.
        window_size = 5  # Example: last N entries
        if len(df) > window_size:
            # Set the range to the last 'window_size' timestamps
            window_start = df['timestamp'].iloc[-window_size]
            window_end = df['timestamp'].iloc[-1]
            fig.update_xaxes(range=[window_start, window_end])

        fig.update_layout(title='Temperature Readings with Regression Line',
                          xaxis_title='Time',
                          yaxis_title='Temperature (°C)')

        return fig

# --------------------------------------------
# Create and run the PyShiny app
# --------------------------------------------
app = App(app_ui, server)
