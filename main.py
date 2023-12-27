#!/usr/bin/python3
"""
Created on Mon Dec 12 03:20:25 2023

@author: Moronfoluwa Akintola
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from stats import skew, kurtosis
from bubble_chart import BubbleChart

def convert_csv(filename):
    """ 
        Read the CSV file, convert to a dataframe and return the same dataframe 
    """
    df = pd.read_csv(filename)
    return df

def read_worldbank_data(df):
    """ 
        Function which takes a filename as argument, reads a dataframe in World-bank format 
        and returns two dataframes: one with years as columns and one with countries as columns
    """
    # Transpose the data
    df_countries = df.transpose()

    # Remove header
    df_countries.columns = df_countries.iloc[0]
    df_countries = df_countries.iloc[1:]

    # replace column headers with the first row:
    df_countries.columns = df_countries.iloc[0]
    df_countries = df_countries.iloc[1:]

    # grab the first row for the header
    new_header = df_countries.iloc[0] 

    # take the data less the header row
    df_countries = df_countries[1:] 

    #set the header row as the df header
    df_countries.columns = new_header 

    df_countries_cleaned = df_countries.dropna()
    df_cleaned = df.dropna()

    return df_cleaned, df_countries


def extract_series(df):
    """
        Extract the series name in the dataframe in a list of unique names
    """
    unique_values = df["Series Name"].unique()
    items_to_remove = ['Last Updated: 10/26/2023', 'Data from database: World Development Indicators', 'Time required to get electricity (days)' ]
    unique_values = [item for item in unique_values if item not in items_to_remove]
    return unique_values

def draw_bubble_chart():
    """ 
       
    """
    browser_market_share = {
    'browsers': ['United Kingdom', 'United States', 'United Arab Emirates', 'Switzerland', 'India', 'Indonesia', 'Algeria', 'Australia', 'Nigeria', 'Ghana'],
    'market_share': [5130.3902533002, 12993.9655794706, 11562.9885226842, 7520.16602494502,797.349232010839, 808.418972064685, 1368.62151887474, 10071.3989785006,142.129222071326, 339.19274255207],
    'color': ['#5A69AF', '#579E65', '#27C518', '#FC944A', '#022356', '#574B59', '#3CA2CE',  '#D9C784', '#1C944A', '#A24C00',]
    }


    # Create an instance of BubbleChart
    bubble_chart = BubbleChart(area=browser_market_share['market_share'],
                            bubble_spacing=0.1)

    # Collapse the bubbles
    bubble_chart.collapse()

    # Create the figure and axis with a smaller figure size
    fig, ax = plt.subplots(figsize=(18, 18), subplot_kw=dict(aspect="equal"))

    # Plot the bubble chart with labels and legend
    bubble_chart.plot(ax, browser_market_share['browsers'], browser_market_share['color'])

    # Customize the plot
    ax.axis("off")
    ax.relim()
    ax.autoscale_view()
    ax.set_title('Electric power consumption (kWh per capita) in year 2014')

    # Show the legend outside the plot area
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    return plt.show()

def extract_country_from_df(df, country_name): 
    """ Extract data matching specific country """
    # Define the column to extract and the specific value to match
    column_name = 'Country Name'
    # Extract the specified values into a new DataFrame
    extracted_values_df = df.loc[df[column_name] == country_name]
    # return the extracted DataFrame
    return extracted_values_df

def draw_line_chart(df, series_name, plot_title, y_axis_label):
    """ Draw Line chart """
    # Select data for the specified series name
    series_name = 'Electric power consumption (kWh per capita)'
    selected_data = df[df['Series Name'] == series_name]

    # Replace non-numeric values with NaN
    selected_data.replace('..', np.nan, inplace=True)

    # Extract country names, years, and corresponding values
    countries = selected_data['Country Name']
    years_raw = selected_data.columns[4:]

    values = selected_data.iloc[:, 4:].astype(float)

    # Convert years to a more readable format
    years = [year.split()[0] for year in years_raw]

    # Plot the data for each country
    plt.figure(figsize=(12, 8))
    for i in range(len(countries)):
        # Use a colormap for distinct colors
        color = plt.cm.viridis(i / len(countries))
        plt.plot(years, values.iloc[i, :], marker='o', label=countries.iloc[i], color=color, linewidth=2)

    # Customize the plot
    # plt.title('Electric Power Consumption (kWh per capita) - 2000 to 2015')
    plt.title(plot_title)
    plt.xlabel('Year')
    # plt.ylabel('Electric Power Consumption (kWh per capita)')
    plt.ylabel(y_axis_label)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # Show the plot
    return plt.show()


""" Function to truncate legend text """
def truncate_legend_text(text, max_length=30):
        return text[:max_length] + "..." if len(text) > max_length else text
    

def draw_grouped_bar_chart(dffff, year):
    # print('dffff', dffff)
    print('year', year)
    """ Draw grouped barchart """
    # Select relevant data for the specified series and years
    selected_series = [
        "Electric power consumption (kWh per capita)",
        "CO2 emissions (metric tons per capita)",
        "CO2 emissions from electricity and heat production, total (% of total fuel combustion)",
        "Electricity production from natural gas sources (% of total)",
        "GDP per capita (current US$)",
        "Electricity production from renewable sources, excluding hydroelectric (% of total)"
    ]

    # Selected Year
    years = [f"{year} [YR{year}]"]
    selected_data = dffff[dffff["Series Name"].isin(selected_series) & dffff["Country Code"].notna()][["Series Name", "Country Name"] + years]

    print('years', years)

    # Pivot the data for easier plotting
    pivot_data = selected_data.melt(id_vars=["Series Name", "Country Name"], var_name="Year", value_name="Value")
    print('pivot_data', pivot_data)

    # Extract years from the "Year" column
    pivot_data["Year"] = pivot_data["Year"].str.extract(r"(\d{4})").astype(int)

    # Plot grouped bar chart with logarithmic y-axis scale
    fig, ax = plt.subplots(figsize=(12, 8))
    pivot_data.pivot(index=["Country Name", "Year"], columns="Series Name", values="Value").unstack().plot(kind="bar", ax=ax, width=0.8, logy=True)

    # Set labels and title
    plt.xlabel("Countries")
    plt.ylabel("Value (log scale)")
    plt.title(f"Comparison of Key Indicators Across Countries ({year})")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    # Add legend with truncated series names on the top right corner
    legend_labels = [truncate_legend_text(series) for series in selected_series]
    plt.legend(title="", labels=legend_labels, bbox_to_anchor=(1, 1), loc="upper right")

    # Show the plot
    plt.tight_layout()
    plt.show()
    return #plt.show()


def draw_correlation(df):

    cols = ['Electric power consumption (kWh per capita)',
        'CO2 emissions (metric tons per capita)',
        'CO2 emissions from electricity and heat production, total (% of total fuel combustion)',
        'Electricity production from natural gas sources (% of total)',
        'Electricity production from renewable sources, excluding hydroelectric (% of total)',
        'GDP per capita (current US$)'
        ]

    df = df.loc[cols, '2000 [YR2000]':'2005 [YR2005]']

    corr = df.corr()

    fig, ax = plt.subplots(figsize=(6, 5))

    sns.heatmap(corr,
                annot=True,
                vmin=-1, vmax=1,
                xticklabels=cols,
                yticklabels=cols,
                cmap='BrBG',
                linewidths=.5)

    plt.title('United Kingdom 2000-2005 coefficients related to electric power consumption and CO2 emissions', fontsize=20)
    plt.tight_layout()
    plt.show()
    return plt.show()


# checks whether module is imported or run directly.
# code is not executed if imported
if __name__ == "__main__":
    
    # Load data into pandas dataframe from CSV file
    df = convert_csv('./data.csv')
    df.head()


    # Your program should
    df_cleaned, df_countries = read_worldbank_data(df)

    draw_correlation(df_countries)

    # draw_grouped_bar_chart(df_cleaned, 2014)

    # Bubble chart
    # draw_bubble_chart()

    # country_df = extract_country_from_df(df,'United Kingdom')

    # Line chart Electric power consumption (kWh per capita)
    series_name = 'Electric power consumption (kWh per capita)'
    plot_title = 'Electric Power Consumption (kWh per capita) - 2000 to 2015'
    y_axis_label = 'Electric Power Consumption (kWh per capita)'
    # draw_line_chart(df, series_name, plot_title, y_axis_label)
    
    # Line chart CO2 emissions (metric tons per capita)
    # series_name = 'Electric power consumption (kWh per capita)'
    # plot_title = 'Electric Power Consumption (kWh per capita) - 2000 to 2015'
    # y_axis_label = 'Electric Power Consumption (kWh per capita)'


 

    

    
