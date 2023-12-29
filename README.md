# 7PAM2000 Applied Data Science 1
## Assignment 2: Statistics and trends.

### Data Source
 The CSV data ued for this analysis [DATA](./data.csv)
 
### Instructions
Your goal is to:
1. Ingest and manipulate the data using pandas dataframes. Your program should
include a function which takes a filename as argument, reads a dataframe in World-
bank format and returns two dataframes: one with years as columns and one with
countries as columns. Do not forget to clean the transposed dataframe.

2. Explore the statistical properties of a few indicators, that are of interest to you, and
cross-compare between individual countries (you do not have to do all the countries,
just a select few will do) and produce appropriate summary statistics. You can also
use aggregated data for regions and other categories. You are expected to use the
.describe() method to explore your data and two other statistical methods.

3. Explore and understand any correlations (or lack of) between indicators (e.g. popu-
lation growth and energy consumption). Does this vary between country, have any
correlations or trends changed with time?

4. You are expected to use your initiative and “tell a story” with the data. You should
use appropriate visualisation (hint: time series could be useful) and provide a text
narrative to communicate and explain your findings. Details of the implementation
and the coding do not belong in such a report. Your boss wants to see results and
interpretation. What are the key findings?
5. You will be assessed on the overall quality of the report, good use of visualisation
tools and good use of the methods and tools available for dataframes. See mark
scheme for details. Good reports often combine information from graphs to draw
conclusions or follow up on insights/questions from one graph with another graph.

6. You do not have to document all your data exploration. Usually one tries different
plots and graphs and select the most meaningful ones for the report.

### How to run
Download the csv data and put in the root directory

### Setup python virtual environment and install packages
`python3 -m venv assignment2`

`source assignment2/bin/activate`

`pip install requirements.txt`

then run 

```
python main.py
```