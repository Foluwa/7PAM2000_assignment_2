#!/usr/bin/python3
"""
Created on Tue Dec 12 03:20:25 2023

@author: Moronfoluwa Akintola
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bubble_chart import BubbleChart

# Declare constant variables
color_list = ['#5A69AF', '#579E65', '#27C518', '#FC944A', '#022356', '#574B59', '#3CA2CE', '#D9C784', '#1C944A',
              '#A24C00']


def read_world_bank(filename):
    """
        Function which takes a filename as argument, reads a dataframe in World-bank format
        and returns two dataframes: one with years as columns and one with countries as columns
    """
    df_data = pd.read_csv(filename)
    # Transpose the data
    df_countries_data = df_data.transpose()

    # Remove header
    df_countries_data.columns = df_countries_data.iloc[0]
    df_countries_data = df_countries_data.iloc[1:]

    # replace column headers with the first row:
    df_countries_data.columns = df_countries_data.iloc[0]
    df_countries_data = df_countries_data.iloc[1:]

    # grab the first row for the header
    new_header = df_countries_data.iloc[0]

    # take the data less the header row
    df_countries_data = df_countries_data[1:]

    # set the header row as the df header
    df_countries_data.columns = new_header

    df_countries_data_cleaned = df_countries_data.dropna()
    df_cleaned_data = df_data.dropna()

    return df_cleaned_data, df_countries_data


def extract_series_from_df(df_series, series_name):
    """
        Extract the series name in the dataframe in a list of unique names
    """
    # Define the column to extract and the specific value to match
    column_name = 'Series Name'
    # Extract the specified values into a new DataFrame
    extracted_values_df = df_series.loc[df_series[column_name] == series_name]
    # return the extracted DataFrame
    return extracted_values_df


def draw_bubble_chart(data):
    """ 
        Function draws bubble chart from the specified dataframe data
    """

    # Create an instance of BubbleChart
    bubble_chart = BubbleChart(area=data['values'], bubble_spacing=0.1)

    # Collapse the bubbles
    bubble_chart.collapse()

    # Create the figure and axis with a smaller figure size
    fig, ax = plt.subplots(figsize=(18, 18), subplot_kw=dict(aspect="equal"))

    # Plot the bubble chart with labels and legend
    bubble_chart.plot(ax, data['countries'], data['color'])

    # Customize the plot
    ax.axis("off")
    ax.relim()
    ax.autoscale_view()
    ax.set_title(f'Electric power consumption (kWh per capita) in year {data["year"]}')

    # Show the legend outside the plot area
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    return plt.show()


def extract_country_from_df(df_data, country_name):
    """
        Function take dataframe and country name as argument
        and extracts the specified series data
    """
    # Define the column to extract and the specific value to match
    column_name = 'Country Name'
    # Extract the specified values into a new DataFrame
    extracted_values_df = df_data.loc[df_data[column_name] == country_name]
    # return the extracted DataFrame
    return extracted_values_df


def extract_countries_series(df_country, series_name):
    """
        Function take dataframe and series name as argument
        and extracts the specified country data
    """
    all_country = df_country['Country Name'].values
    all_values = df_country[series_name].values
    return all_country, all_values


def truncate_legend_text(text, max_length=30):
    """
        Function truncate the length of text on the matplotlib legend
    """
    return text[:max_length] + "..." if len(text) > max_length else text


def draw_grouped_bar_chart(df_bar, year):
    """
        Function draws a grouped bar chart from the data frame and selected year
    """
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
    selected_data = df_bar[df_bar["Series Name"].isin(selected_series) &
                           df_bar["Country Code"].notna()][["Series Name", "Country Name"] + years]

    # Pivot the data for easier plotting
    pivot_data = selected_data.melt(id_vars=["Series Name", "Country Name"], var_name="Year", value_name="Value")
    # print('pivot_data', pivot_data)

    # Extract years from the "Year" column
    pivot_data["Year"] = pivot_data["Year"].str.extract(r"(\d{4})").astype(int)

    # Plot grouped bar chart with logarithmic y-axis scale
    fig, ax = plt.subplots(figsize=(12, 8))
    pivot_data.pivot(index=["Country Name", "Year"], 
                     columns="Series Name", 
                     values="Value").unstack().plot(kind="bar", ax=ax, width=0.8, logy=True)

    # Set labels and title
    plt.xlabel("Countries")
    plt.ylabel("Value (log scale)")
    plt.title(f"Comparison of Key Indicators Across Countries ({year})")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    # Add legend with truncated series names in the top right corner
    legend_labels = [truncate_legend_text(series) for series in selected_series]
    plt.legend(title="", labels=legend_labels, bbox_to_anchor=(1, 1), loc="upper right")

    # Show the plot
    plt.tight_layout()
    return plt.show()


def draw_correlation():
    """
        Function draws a correlation matrix from the selected country dataframe
    """
    df_selected_country = pd.read_csv('df_selected_country.csv', index_col=0)

    #  Series parameters  
    cols = ['Electric power consumption (kWh per capita)',
            'CO2 emissions (metric tons per capita)',
            'CO2 emissions from electricity and heat production, total (% of total fuel combustion)',
            'Electricity production from natural gas sources (% of total)',
            'Electricity production from renewable sources, excluding hydroelectric (% of total)',
            'GDP per capita (current US$)'
    ]

    df_selected_country = df_selected_country.loc[cols, '2000 [YR2000]':'2005 [YR2005]']
    corr = df_selected_country.corr()
    plt.subplots(figsize=(6, 5))
    sns.heatmap(corr,
                annot=True,
                vmin=-1, vmax=1,
                xticklabels=cols,
                yticklabels=cols,
                cmap='BrBG',
                linewidths=.5)
    cor_title = 'United Kingdom 2000-2005 coefficients related to electric power consumption and CO2 emissions'
    plt.title(cor_title)
    plt.tight_layout()
    return plt.show()


def draw_line_chart(df_chart, series_name, title, y_axis):
    """ Function take dataframe series name and title as argument
        and draws a linechart from the data
    """
    # Select data for the specified series name
    selected_data = df_chart[df_chart['Series Name'] == series_name]

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
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(y_axis)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    # Show the plot
    return plt.show()


# checks whether module is imported or run directly.
# code is not executed if imported
if __name__ == "__main__":

    # Function takes a filename of CSV file as argument, reads a dataframe in
    # World bank format and returns two dataframes: one with years as columns and one with
    # countries as columns.
    df_cleaned, df_countries = read_world_bank('./data.csv')
    numeric_cols = ['2000 [YR2000]', '2014 [YR2014]']

    # Use of dataframe method .describe() to explore dataset.
    summary_statistics = df_cleaned.describe()
    # # Other statistical methods
    data_mean = df_cleaned[numeric_cols].mean()
    correlation_matrix = df_cleaned[numeric_cols].corr()
    skewness = df_cleaned[numeric_cols].skew()

    # Display the results
    print('Summary Statistics:\n', summary_statistics)
    print('Mean of data :\n', data_mean)
    print('\nCorrelation Matrix:\n', correlation_matrix)
    print('\nSkewness of the data:\n', skewness)

    country_df = extract_country_from_df(df_cleaned, 'United Kingdom')

    # Save country to CSV
    country_df.to_csv('df_selected_country.csv', index=False)

    # Draw correlation from selected country
    draw_correlation()

    # Bubble chart
    selected_series_electric_power = extract_series_from_df(df_cleaned, 'Electric power consumption (kWh per capita)')

    countries_2000, values_2000 = extract_countries_series(selected_series_electric_power, '2000 [YR2000]')
    countries_2014, values_2024 = extract_countries_series(selected_series_electric_power, '2014 [YR2014]')

    market_1 = {
        'countries': countries_2000,
        'values': values_2000,
        'color': color_list,
        'year': '2000'
    }

    market_2 = {
        'countries': countries_2014,
        'values': values_2024,
        'color': color_list,
        'year': '2014'
    }

    draw_bubble_chart(market_1)
    draw_bubble_chart(market_2)

    # grouped bar chart
    draw_grouped_bar_chart(df_cleaned, 2000)
    draw_grouped_bar_chart(df_cleaned, 2014)

    selected_series_co2_emissions = extract_series_from_df(df_cleaned, 'CO2 emissions (metric tons per capita)')

    # print(selected_series_co2_emissions.head())

    draw_line_chart(selected_series_electric_power, 'Electric power consumption (kWh per capita)',
                    'Electric Power Consumption (kWh per capita) - 2000 to 2015',
                    'Electric Power Consumption (kWh per capita)')

    draw_line_chart(selected_series_co2_emissions, 'CO2 emissions (metric tons per capita)',
                    'CO2 emissions (metric tons per capita) - 2000 to 2015', 'CO2 emissions (metric tons per capita)')
