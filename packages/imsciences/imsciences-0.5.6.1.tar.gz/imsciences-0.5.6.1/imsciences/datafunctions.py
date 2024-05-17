import pandas as pd
import calendar
import os
import plotly.express as px
import plotly.graph_objs as go
from dateutil.parser import parse
import numpy as np
from datetime import datetime
import datetime
import re
from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime
from imsciences import *
from fredapi import Fred
import pandas as pd
import datetime
from datetime import timedelta
import time

class dataprocessing:
    
    def help(self):
        print("This is the help section. The functions in the package are as follows:")

        print("\n1. get_wd_levels")
        print("   - Description: Get the working directory with the option of moving up parents.")
        print("   - Usage: get_wd_levels(levels)")
        print("   - Example: get_wd_levels(0)")

        print("\n2. remove_rows")
        print("   - Description: Removes a specified number of rows from a pandas DataFrame.")
        print("   - Usage: remove_rows(data_frame, num_rows_to_remove)")
        print("   - Example: remove_rows(df, 2)")

        print("\n3. aggregate_daily_to_wc_long")
        print("   - Description: Aggregates daily data into weekly data, grouping and summing specified columns, starting on a specified day of the week.")
        print("   - Usage: aggregate_daily_to_wc_long(df, date_column, group_columns, sum_columns, wc, aggregation='sum')")
        print("   - Example: aggregate_daily_to_wc_long(df, 'date', ['platform'], ['cost', 'impressions', 'clicks'], 'mon', 'average')")

        print("\n4. convert_monthly_to_daily")
        print("   - Description: Converts monthly data in a DataFrame to daily data by expanding and dividing the numeric values.")
        print("   - Usage: convert_monthly_to_daily(df, date_column, divide)")
        print("   - Example: convert_monthly_to_daily(df, 'date')")

        print("\n5. plot_two")
        print("   - Description: Plots specified columns from two different DataFrames using a shared date column. Useful for comparing data.")
        print("   - Usage: plot_two(df1, col1, df2, col2, date_column, same_axis=True)")
        print("   - Example: plot_two(df1, 'cost', df2, 'cost', 'obs', True)")

        print("\n6. remove_nan_rows")
        print("   - Description: Removes rows from a DataFrame where the specified column has NaN values.")
        print("   - Usage: remove_nan_rows(df, col_to_remove_rows)")
        print("   - Example: remove_nan_rows(df, 'date')")

        print("\n7. filter_rows")
        print("   - Description: Filters the DataFrame based on whether the values in a specified column are in a provided list.")
        print("   - Usage: filter_rows(df, col_to_filter, list_of_filters)")
        print("   - Example: filter_rows(df, 'country', ['UK', 'IE'])")

        print("\n8. plot_one")
        print("   - Description: Plots a specified column from a DataFrame.")
        print("   - Usage: plot_one(df1, col1, date_column)")
        print("   - Example: plot_one(df, 'Spend', 'OBS')")

        print("\n9. week_of_year_mapping")
        print("   - Description: Converts a week column in 'yyyy-Www' or 'yyyy-ww' format to week commencing date.")
        print("   - Usage: week_of_year_mapping(df, week_col, start_day_str)")
        print("   - Example: week_of_year_mapping(df, 'week', 'mon')")

        print("\n10. exclude_rows")
        print("    - Description: Removes rows from a DataFrame based on whether the values in a specified column are not in a provided list.")
        print("    - Usage: exclude_rows(df, col_to_filter, list_of_filters)")
        print("    - Example: exclude_rows(df, 'week', ['2022-W20', '2022-W21'])")

        print("\n11. rename_cols")
        print("    - Description: Renames columns in a pandas DataFrame.")
        print("    - Usage: rename_cols(df, cols_to_rename)")
        print("    - Example: rename_cols(df, {'old_col_name': 'new_col_name'})")

        print("\n12. merge_new_and_old")
        print("    - Description: Creates a new DataFrame with two columns: one for dates and one for merged numeric values.")
        print("    - Merges numeric values from specified columns in the old and new DataFrames based on a given cutoff date.")
        print("    - Usage: merge_new_and_old(old_df, old_col, new_df, new_col, cutoff_date, date_col_name='OBS')")
        print("    - Example: merge_new_and_old(df1, 'old_col', df2, 'new_col', '2023-01-15')")

        print("\n13. merge_dataframes_on_date")
        print("    - Description: Merge a list of DataFrames on a common column.")
        print("    - Usage: merge_dataframes_on_date(dataframes, common_column='OBS', merge_how='outer')")
        print("    - Example: merge_dataframes_on_date([df1, df2, df3], common_column='OBS', merge_how='outer')")

        print("\n14. merge_and_update_dfs")
        print("    - Description: Merges two dataframes on a key column, updates the first dataframe's columns with the second's where available, and returns a dataframe sorted by the key column.")
        print("    - Usage: merge_and_update_dfs(df1, df2, key_column)")
        print("    - Example: merged_dataframe = merge_and_update_dfs(processed_facebook, finalised_meta, 'OBS')")

        print("\n15. convert_us_to_uk_dates")
        print("    - Description: Convert a DataFrame column with mixed date formats to datetime.")
        print("    - Usage: convert_us_to_uk_dates(df, date_col)")
        print("    - Example: convert_us_to_uk_dates(df, 'date')")
        
        print("\n16. combine_sheets")
        print("    - Description: Combines multiple DataFrames from a dictionary into a single DataFrame.")
        print("    - Usage: combine_sheets(all_sheets)")
        print("    - Example: combine_sheets({'Sheet1': df1, 'Sheet2': df2})")
        
        print("\n17. pivot_table")
        print("    - Description: Dynamically pivots a DataFrame based on specified columns.")
        print("    - Usage: pivot_table(df, filters_dict, index_col, columns, values_col, fill_value=0,aggfunc='sum',margins=False,margins_name='Total',datetime_trans_needed=True)")
        print("    - Example: pivot_table(df, {'Master Include':' == 1','OBS':' >= datetime(2019,9,9)','Metric Short Names':' == 'spd''}, 'OBS', 'Channel Short Names', 'Value', fill_value=0,aggfunc='sum',margins=False,margins_name='Total',datetime_trans_needed=True)")
        
        print("\n18. apply_lookup_table_for_columns")
        print("    - Description: Equivalent of xlookup in excel. Allows you to map a dictionary of substrings within a column. If multiple columns are need for the LUT then a | seperator is needed.")
        print("    - Usage: classify_within_column(df, col_names, to_find_dict, if_not_in_country_dict='Other'), new_column_name='Mapping'")
        print("    - Example: classify_within_column(df, ['campaign type','media type'], {'France Paid Social FB|paid social': 'facebook','France Paid Social TW|paid social': 'twitter'}, 'other','mapping')")

        print("\n19. aggregate_daily_to_wc_wide")
        print("   - Description: Aggregates daily data into weekly data, grouping and summing specified columns, starting on a specified day of the week.")
        print("   - Usage: aggregate_daily_to_wc_wide(df, date_column, group_columns, sum_columns, wc, aggregation='sum', include_totals=False)")
        print("   - Example: aggregate_daily_to_wc_wide(df, 'date', ['platform'], ['cost', 'impressions', 'clicks'], 'mon', 'average', True)")

        print("\n20. merge_cols_with_seperator")
        print("   - Description: Merge multiple columns in a dataframe into 1 column with a seperator '_'.Can be used if multiple columns are needed for a LUT.")
        print("   - Usage: merge_cols_with_seperator(self, df, col_names,seperator='_',output_column_name = 'Merged',starting_prefix_str=None,ending_prefix_str=None)")
        print("   - Example: merge_cols_with_seperator(df, ['Campaign','Product'],seperator='|','Merged Columns',starting_prefix_str='start_',ending_prefix_str='_end')")        

        print("\n21. check_sum_of_df_cols_are_equal")
        print("   - Description: Checks if the sum of two columns in two dataframes are the same, and provides the sums of each column and the difference between them.")
        print("   - Usage: check_sum_of_df_cols_are_equal(df_1,df_2,cols_1,cols_2)")
        print("   - Example: check_sum_of_df_cols_are_equal(df_1,df_2,'Media Cost','Spend')")        

        print("\n22. convert_2_df_cols_to_dict")
        print("   - Description: Can be used to create an LUT. Creates a dictionary using two columns in a dataframe.")
        print("   - Usage: convert_2_df_cols_to_dict(df, key_col, value_col)")
        print("   - Example: convert_2_df_cols_to_dict(df, 'Campaign', 'Channel')")        

        print("\n23. create_FY_and_H_columns")
        print("   - Description: Used to create a financial year, half year, and financial half year column.")
        print("   - Usage: create_FY_and_H_columns(df, index_col, start_date, starting_FY,short_format='No',half_years='No',combined_FY_and_H='No')")
        print("   - Example: create_FY_and_H_columns(df, 'Week (M-S)', '2022-10-03', 'FY2023',short_format='Yes',half_years='Yes',combined_FY_and_H='Yes')")        
        
        print("\n24. keyword_lookup_replacement")
        print("   - Description: Essentially provides an if statement with a xlookup if a value is something. Updates certain chosen values in a specified column of the DataFrame based on a lookup dictionary.")
        print("   - Usage: keyword_lookup_replacement(df, col, replacement_rows, cols_to_merge, replacement_lookup_dict,output_column_name='Updated Column')")
        print("   - Example: keyword_lookup_replacement(df, 'channel', 'Paid Search Generic', ['channel','segment','product'], qlik_dict_for_channel,output_column_name='Channel New')")        

        print("\n25. create_new_version_of_col_using_LUT")
        print("   - Description: Creates a new column in a dataframe, which takes an old column and uses a lookup table to changes values in the new column to reflect the lookup table. The lookup is based on a column in the dataframe.")
        print("   - Usage: create_new_version_of_col_using_LUT(df, keys_col,value_col, dict_for_specific_changes, new_col_name='New Version of Old Col')")
        print("   - Example: keyword_lookup_replacement(df, '*Campaign Name','Campaign Type',search_campaign_name_retag_lut,'Campaign Name New')")        

        print("\n26. convert_df_wide_2_long")
        print("   - Description: Changes a dataframe from wide to long format.")
        print("   - Usage: convert_df_wide_2_long(df,value_cols,variable_col_name='Stacked',value_col_name='Value')")
        print("   - Example: keyword_lookup_replacement(df, ['Media Cost','Impressions','Clicks'],variable_col_name='Metric')") 
        
        print("\n27. manually_edit_data")
        print("   - Description: Allows the capability to manually update any cell in dataframe by applying filters and chosing a column to edit in dataframe.")
        print("   - Usage: manually_edit_data(df, filters_dict, col_to_change, new_value, change_in_existing_df_col='No', new_col_to_change_name='New', manual_edit_col_name=None, add_notes='No', existing_note_col_name=None, note=None)")
        print("   - Example: keyword_lookup_replacement(df, {'OBS':' <= datetime(2023,1,23)','File_Name':' == 'France media''},'Master Include',1,change_in_existing_df_col = 'Yes',new_col_to_change_name = 'Master Include',manual_edit_col_name = 'Manual Changes')")      

        print("\n28. format_numbers_with_commas")
        print("   - Description: Converts data in numerical format into numbers with commas and a chosen decimal place length.")
        print("   - Usage: format_numbers_with_commas(df, decimal_length_chosen=2)")
        print("   - Example: format_numbers_with_commas(df,1)")         
    
        print("\n29. filter_df_on_multiple_conditions")
        print("   - Description: Filters dataframe on multiple conditions, which come in the form of a dictionary.")
        print("   - Usage: filter_df_on_multiple_conditions(df, filters_dict)")
        print("   - Example: filter_df_on_multiple_conditions(df, {'OBS':' <= datetime(2023,1,23)','File_Name':' == 'France media''})")       
    
    
    def get_wd_levels(self, levels):
        """
        Gets the current wd of whoever is working on it and gives the options to move the number of levels up.

        Parameters:
        - data_frame: pandas DataFrame
            The input data frame.
        - num_rows_to_remove: int
            The number of levels to move up pathways.

        Returns:
        - Current wd
        """

        directory = os.getcwd()
        for _ in range(levels):
            directory = os.path.dirname(directory)
        return directory

    def remove_rows(self, data_frame, num_rows_to_remove):
        """
        Removes the specified number of rows from the given data frame, including the top row containing column names. 
        The next row will be treated as the new set of column headings.

        Parameters:
        - data_frame: pandas DataFrame
            The input data frame.
        - num_rows_to_remove: int
            The number of rows to remove from the data frame, starting from the original header.

        Returns:
        - pandas DataFrames
            The modified data frame with rows removed and new column headings.

        Raises:
        - TypeError: If num_rows_to_remove is not an integer.
        - ValueError: If num_rows_to_remove is negative or exceeds the total number of rows.
        """
        
        if not isinstance(num_rows_to_remove, int):
            raise TypeError("num_rows_to_remove must be an integer")

        if num_rows_to_remove < 0 or num_rows_to_remove >= len(data_frame):
            raise ValueError("Number of rows to remove must be non-negative and less than the total number of rows in the data frame.")

        if num_rows_to_remove == 0:
            return data_frame

        new_header = data_frame.iloc[num_rows_to_remove - 1]
        modified_data_frame = data_frame[num_rows_to_remove:] 
        modified_data_frame.columns = new_header

        return modified_data_frame
    
    def aggregate_daily_to_wc_long(self, df : pd.DataFrame, date_column : str, group_columns : list[str], sum_columns : list[str], wc : str = 'sun', aggregation : str = 'sum') -> pd.DataFrame:
        """
        Aggregates daily data into weekly data, starting on a specified day of the week, 
        and groups the data by additional specified columns. It aggregates specified numeric columns 
        by summing, averaging, or counting them, and pivots the data to create separate columns for each combination 
        of the group columns and sum columns. NaN values are replaced with 0 and the index is reset. 
        The day column is renamed from 'Day' to 'OBS'.

        Parameters:
        - df: pandas DataFrame
            The input DataFrame containing daily data.
        - date_column: string
            The name of the column in the DataFrame that contains date information.
        - group_columns: list of strings
            Additional column names to group by along with the weekly grouping.
        - sum_columns: list of strings
            Numeric column names to be aggregated during aggregation.
        - wc: string
            The week commencing day (e.g., 'sun' for Sunday, 'mon' for Monday).
        - aggregation: string, optional (default 'sum')
            Aggregation method, either 'sum', 'average', or 'count'.

        Returns:
        - pandas DataFrame
            A new DataFrame with weekly aggregated data. The index is reset,
            and columns represent the grouped and aggregated metrics. The DataFrame 
            is in long format, with separate columns for each combination of 
            grouped metrics.
        """

        # Map the input week commencing day to a weekday number (0=Monday, 6=Sunday)
        days = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
        if wc.lower() not in days:
            return print(f"Incorrect week commencing day input: '{wc}'. Please choose a valid day of the week (e.g., 'sun', 'mon', etc.).")

        start_day = days[wc.lower()]

        # Make a copy of the DataFrame
        df_copy = df.copy()

        # Convert the date column to datetime
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])

        # Determine the start of each week
        df_copy['week_start'] = df_copy[date_column].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - start_day) % 7))

        # Convert sum_columns to numeric and fill NaNs with 0, retaining decimal values
        for col in sum_columns:
            df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').fillna(0)

        # Group by the new week start column and additional columns, then aggregate the numeric columns
        if aggregation == 'average':
            grouped = df_copy.groupby(['week_start'] + group_columns)[sum_columns].mean().reset_index()
        elif aggregation == 'count':
            grouped = df_copy.groupby(['week_start'] + group_columns)[sum_columns].count().reset_index()
        else:  # Default to 'sum' if any other value is provided
            grouped = df_copy.groupby(['week_start'] + group_columns)[sum_columns].sum().reset_index()

        # Rename 'week_start' column to 'OBS'
        grouped = grouped.rename(columns={'week_start': 'OBS'})

        return grouped
    
    def convert_monthly_to_daily(self, df, date_column, divide = True):
        """
        Convert a DataFrame with monthly data to daily data.
        This function takes a DataFrame and a date column, then it expands each
        monthly record into daily records by dividing the numeric values by the number of days in that month.

        :param df: DataFrame with monthly data.
        :param date_column: The name of the column containing the date.
        :param divide: boolean divide by the number of days in a month (default True)
        :return: A new DataFrame with daily data.
        """

        # Convert date_column to datetime
        df[date_column] = pd.to_datetime(df[date_column])

        # Initialize an empty list to hold the daily records
        daily_records = []

        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            # Calculate the number of days in the month
            num_days = calendar.monthrange(row[date_column].year, row[date_column].month)[1]

            # Create a new record for each day of the month
            for day in range(1, num_days + 1):
                daily_row = row.copy()
                daily_row[date_column] = row[date_column].replace(day=day)

                # Divide each numeric value by the number of days in the month
                for col in df.columns:
                    if pd.api.types.is_numeric_dtype(df[col]) and col != date_column:
                        if divide == True:
                            daily_row[col] = row[col] / num_days
                        else: 
                            daily_row[col] = row[col]
                daily_records.append(daily_row)

        # Convert the list of daily records into a DataFrame
        daily_df = pd.DataFrame(daily_records)
        
        return daily_df
    
    def plot_two(self, df1, col1, df2, col2, date_column, same_axis=True):
        """
        Plots specified columns from two different dataframes with both different and the same lengths,
        using a specified date column as the X-axis, and charting on either the same or separate y axes.

        :param df1: First DataFrame
        :param col1: Column name from the first DataFrame
        :param df2: Second DataFrame
        :param col2: Column name from the second DataFrame
        :param date_column: The name of the date column to use for the X-axis
        :param same_axis: If True, plot both traces on the same y-axis; otherwise, use separate y-axes.
        :return: Plotly figure
        """

        # Create traces for the first and second dataframes
        trace1 = go.Scatter(x=df1[date_column], y=df1[col1], mode='lines', name=col1, yaxis='y1')
        
        if same_axis:
            trace2 = go.Scatter(x=df2[date_column], y=df2[col2], mode='lines', name=col2, yaxis='y1')
        else:
            trace2 = go.Scatter(x=np.array(df2[date_column].to_pydatetime()), y=df2[col2], mode='lines', name=col2, yaxis='y2')
            
        # Define layout for the plot
        layout = go.Layout(
            title="",
            xaxis=dict(title="OBS", showline=True, linecolor='black'),
            yaxis=dict(title="", showline=True, linecolor='black', rangemode='tozero'),
            yaxis2=dict(title="", overlaying='y', side='right', showline=True, linecolor='black', rangemode='tozero'),
            showlegend=True,
            plot_bgcolor='white'  # Set the plot background color to white
        )

        # Create the figure with the defined layout and traces
        fig = go.Figure(data=[trace1, trace2], layout=layout)

        return fig

    def remove_nan_rows(self, df, col_to_remove_rows):
    # This line drops rows where the specified column has NaN values
        return df.dropna(subset=[col_to_remove_rows])
    
    def filter_rows(self, df, col_to_filter, list_of_filters):
    # This line filters the DataFrame based on whether the values in the specified column are in the list_of_filters
        return df[df[col_to_filter].isin(list_of_filters)]
    
    def plot_one(self, df1, col1, date_column):
        """
        Plots specified column from a DataFrame with white background and black axes,
        using a specified date column as the X-axis.

        :param df1: DataFrame
        :param col1: Column name from the DataFrame
        :param date_column: The name of the date column to use for the X-axis
        """

        # Check if columns exist in the DataFrame
        if col1 not in df1.columns or date_column not in df1.columns:
            raise ValueError("Column not found in DataFrame")

        # Check if the date column is in datetime format, if not convert it
        if not pd.api.types.is_datetime64_any_dtype(df1[date_column]):
            df1[date_column] = pd.to_datetime(df1[date_column])

        # Plotting using Plotly Express
        fig = px.line(df1, x=date_column, y=col1)

        # Update layout for white background and black axes lines, and setting y-axis to start at 0
        fig.update_layout(
            plot_bgcolor='white',
            xaxis=dict(
                showline=True,
                linecolor='black'
            ),
            yaxis=dict(
                showline=True,
                linecolor='black',
                rangemode='tozero'  # Setting Y-axis to start at 0 if suitable
            )
        )

        return fig

    def week_of_year_mapping(self, df, week_col, start_day_str):
        from datetime import datetime, timedelta
        # Mapping of string day names to day numbers (1 for Monday, 7 for Sunday)
        day_mapping = {
            'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7
        }

        # Convert the day string to a number, or raise an error if not valid
        start_day = day_mapping.get(start_day_str.lower())
        if start_day is None:
            raise ValueError(f"Invalid day input: '{start_day_str}'. Please use one of 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'.")

        # Function to convert week number to start date of the week
        def week_to_startdate(week_str, start_day):
            year, week = map(int, week_str.split('-W'))
            first_day_of_year = datetime(year, 1, 1)
            day_of_week = first_day_of_year.isocalendar()[2]
            days_to_add = (7 - day_of_week + 1) if day_of_week > 4 else (1 - day_of_week)
            start_of_iso_week = first_day_of_year + timedelta(days=days_to_add)

            # Adjust start day
            days_to_shift = (start_day - 1) % 7
            start_of_week = start_of_iso_week + timedelta(days=days_to_shift)

            return start_of_week + timedelta(weeks=week - 1)

        # Apply the function to each row in the specified week column
        df['OBS'] = df[week_col].apply(lambda x: week_to_startdate(x, start_day)).dt.strftime('%d/%m/%Y')
        return df
    
    def exclude_rows(self, df, col_to_filter, list_of_filters):
        # This line filters the DataFrame based on whether the values in the specified column are not in the list_of_filters
        return df[~df[col_to_filter].isin(list_of_filters)]
    
    def rename_cols(self, df, cols_to_rename):
        """
        Renames columns in a pandas DataFrame.

        Parameters:
        - df: pandas DataFrame
            The DataFrame whose columns are to be renamed.
        - cols_to_rename: dict
            A dictionary where keys are the current column names and values are the new column names.

        Returns:
        - pandas DataFrame
            The DataFrame with renamed columns.
        """
        
        return df.rename(columns=cols_to_rename)
    
    def merge_new_and_old(self, old_df, old_col, new_df, new_col, cutoff_date, date_col_name='OBS'):
        """
        Creates a new DataFrame with two columns: one for dates and one for merged numeric values.
        Merges numeric values from specified columns in the old and new DataFrames based on a given cutoff date.

        Parameters:
        - old_df: pandas DataFrame
            The old DataFrame from which to take the numeric values up to the specified date.
        - old_col: str
            The name of the numeric column in the old DataFrame whose values are to be taken.
        - new_df: pandas DataFrame
            The new DataFrame from which to take the numeric values from the specified date onwards.
        - new_col: str
            The name of the numeric column in the new DataFrame whose values are to be taken.
        - cutoff_date: str
            The cut-off date in 'YYYY-MM-DD' format to split the data between the two DataFrames.
        - date_col_name: str, optional (default 'OBS')
            The name of the date column in both DataFrames.

        Returns:
        - pandas DataFrame
            A new DataFrame with two columns: 'Date' and a column named after 'new_col' containing merged numeric values.
        """

        # Convert date columns in both dataframes to datetime for comparison
        old_df[date_col_name] = pd.to_datetime(old_df[date_col_name])
        new_df[date_col_name] = pd.to_datetime(new_df[date_col_name])

        # Convert the cutoff date string to datetime
        cutoff_date = pd.to_datetime(cutoff_date)

        # Split old and new dataframes based on the cutoff date
        old_values = old_df[old_df[date_col_name] <= cutoff_date]
        new_values = new_df[new_df[date_col_name] > cutoff_date]

        # Create a new DataFrame with two columns: 'Date' and a column named after 'new_col'
        merged_df = pd.DataFrame({
            'OBS': pd.concat([old_values[date_col_name], new_values[date_col_name]], ignore_index=True),
            new_col: pd.concat([old_values[old_col], new_values[new_col]], ignore_index=True)
        })

        return merged_df
    
    def merge_dataframes_on_column(self, dataframes, common_column='OBS', merge_how='outer'):
        """
        Merge a list of DataFrames on a common column.

        Parameters:
        - dataframes: A list of DataFrames to merge.
        - common_column: The name of the common column to merge on.
        - merge_how: The type of merge to perform ('inner', 'outer', 'left', or 'right').

        Returns:
        - A merged DataFrame.
        """
        if not dataframes:
            return None
        
        merged_df = dataframes[0]  # Start with the first DataFrame

        for df in dataframes[1:]:
            merged_df = pd.merge(merged_df, df, on=common_column, how=merge_how)

        # Check if the common column is of datetime dtype
        if merged_df[common_column].dtype == 'datetime64[ns]':
            merged_df[common_column] = pd.to_datetime(merged_df[common_column])
        merged_df = merged_df.sort_values(by=common_column)
        merged_df = merged_df.fillna(0)
        
        return merged_df
    
    def merge_and_update_dfs(self, df1, df2, key_column):
        """
        Merges two dataframes on a key column, updates the first dataframe's columns with the second's where available,
        and returns a dataframe sorted by the key column.

        Parameters:
        df1 (DataFrame): The first dataframe to merge (e.g., processed_facebook).
        df2 (DataFrame): The second dataframe to merge (e.g., finalised_meta).
        key_column (str): The name of the column to merge and sort by (e.g., 'OBS').

        Returns:
        DataFrame: The merged and updated dataframe.
        """

        # Sort both DataFrames by the key column
        df1_sorted = df1.sort_values(by=key_column)
        df2_sorted = df2.sort_values(by=key_column)

        # Perform the full outer merge
        merged_df = pd.merge(df1_sorted, df2_sorted, on=key_column, how='outer', suffixes=('', '_finalised'))

        # Update with non-null values from df2
        for column in merged_df.columns:
            if column.endswith('_finalised'):
                original_column = column.replace('_finalised', '')
                merged_df.loc[merged_df[column].notnull(), original_column] = merged_df.loc[merged_df[column].notnull(), column]
                merged_df.drop(column, axis=1, inplace=True)

        # Sort the merged DataFrame by the key column
        merged_df.sort_values(by=key_column, inplace=True)

        # Handle null values (optional, can be adjusted as needed)
        merged_df.fillna(0, inplace=True)

        return merged_df
    
    def convert_us_to_uk_dates(self, df, date_col):
        import datetime
        def fix_date(d):
            # Convert datetime objects to string
            if isinstance(d, pd.Timestamp) or isinstance(d, datetime.datetime):
                d = d.strftime('%m/%d/%Y')
            
            # Split date string into components
            parts = d.split('/')
            
            # Check for two formats: mm/dd/yyyy and dd/mm/yyyy
            if len(parts) == 3:
                year, month, day = parts[2], parts[0], parts[1]
                # Correct for two-digit years
                if len(year) == 2:
                    year = '20' + year
                # Identify dates needing correction: where month > 12 or it follows the yyyy-dd-mm pattern
                if int(month) > 12 or (int(day) <= 12 and int(year) > 31):
                    # Assume year is correct, flip 'month' and 'day' for correction
                    month, day = day, month
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            else:
                # Handle already correct or non-standard formats cautiously
                return d

        # Apply the fix to the specified column
        df[date_col] = df[date_col].apply(lambda x: fix_date(x) if not pd.isnull(x) else x)
        return df

    def combine_sheets(self, all_sheets):
        """
        Combines multiple DataFrames from a dictionary into a single DataFrame.
        Adds a column 'SheetName' indicating the origin sheet of each row.

        Parameters:
        all_sheets (dict): A dictionary of DataFrames, typically read from an Excel file with multiple sheets.

        Returns:
        DataFrame: A concatenated DataFrame with an additional 'SheetName' column.
        """
        combined_df = pd.DataFrame()

        for sheet_name, df in all_sheets.items():
            df['SheetName'] = sheet_name 
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        return combined_df
    
    def pivot_table(self, df, filters_dict, index_col, columns, values_col, fill_value=0,aggfunc='sum',margins=False,margins_name="Total",datetime_trans_needed=True):
        """
        Provides the ability to create pivot tables, filtering the data to get to data you want and then pivoting on certain columns

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            filters_dict (dict): Dictionary of conditions for the boolean mask i.e. what to filter your df on to get to your chosen cell
            index_col (str): Name of Column for your pivot table to index on
            columns (str): Name of Columns for your pivot table.
            values_col (str): Name of Values Columns for your pivot table.
            fill_value (int, optional): The value to replace nan with. Defaults to 0.
            aggfunc (str, optional): The method on which to aggregate the values column. Defaults to sum.
            margins (bool, optional): Whether the pivot table needs a total rows and column. Defaults to False.
            margins_name (str, optional): The name of the Totals columns. Defaults to "Total".
            datetime_trans_needed (bool, optional): Whether the index column needs to be transformed into datetime format. Defaults to False.

        Returns:
            pandas.DataFrame: The pivot table specified
        """
        
        # Create the filtered df by applying the conditions
        df_filtered = self.filter_df_on_multiple_conditions(df, filters_dict)
        
        # Ensure OBS is in datetime format for proper sorting
        df_filtered = df_filtered.copy()
        
        # If datetime transformation is needed
        if datetime_trans_needed is True:
            df_filtered.loc[:,index_col] = pd.to_datetime(df_filtered[index_col], dayfirst=True)
        
        # Create the pivot table
        pivoted_df = df_filtered.pivot_table(index=index_col, columns=columns, values=values_col, aggfunc=aggfunc,margins=margins,margins_name=margins_name)
            
        # Handling MultiIndex columns if present, making them a flat structure
        if isinstance(pivoted_df.columns, pd.MultiIndex):
            pivoted_df.columns = ['_'.join(map(str, col)).strip() for col in pivoted_df.columns.values]
        else:
            pivoted_df.columns = pivoted_df.columns.map(str)
        
        # Reset the pivot before returning
        pivoted_df = pivoted_df.reset_index()
        
        # Sort by OBS from oldest to newest
        if datetime_trans_needed is True:
            # pivoted_df = pivoted_df.reset_index()
            pivoted_df[index_col] = pd.to_datetime(pivoted_df[index_col])  # Ensure sorting works correctly
            pivoted_df = pivoted_df.sort_values(by=index_col)
        
            # Convert OBS back to a string in YYYY-MM-DD format for display purposes
            pivoted_df[index_col] = pivoted_df[index_col].dt.strftime('%Y-%m-%d')
            
            # Set index back to date column
            # pivoted_df.set_index(index_col,inplace=True)
        
        # Fill in any NaNs
        pivoted_df = pivoted_df.fillna(fill_value)
        
        return pivoted_df

    def apply_lookup_table_for_columns(self, df, col_names, to_find_dict, if_not_in_dict="Other", new_column_name="Mapping"):
        """
        Creates a new DataFrame column based on a look up table, possibly with multiple columns to look up on (dictionary of substrings to class mappings).

        Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        col_names (list of str): these are the columns which are used for the lookup. One column or several columns can be inputted as a list, provided there is a merged column to lookup on. If there are multiple columns to look up on then a merged column must be inputted as the key of the dictionary of format e.g. col1|col2|col3
        to_find_dict (dict): your look up table, where keys are the values being looked up, and the values are the resulting mappings. 
        if_not_in_dict (str, optional): default value if no substring matches are found in the look up table dictionary. Defaults to "Other".
        new_column_name (str, optional): name of new column. Defaults to "Mapping".

        Returns:
        pandas.DataFrame: DataFrame with a new column containing the look up table results.
        """

        # Create regex pattern from the dictionary keys
        regex_pattern = "|".join(re.escape(key) for key in to_find_dict.keys())
        
        # Preprocess DataFrame if multiple columns
        if len(col_names) > 1:
            df["Merged"] = df[col_names].astype(str).apply('|'.join, axis=1)
            col_to_use = "Merged"
        else:
            col_to_use = col_names[0]

        # Extract the first match using the regex pattern
        matches = df[col_to_use].str.extract(f'({regex_pattern})', expand=False, flags=re.IGNORECASE)
        
        # Map the matches to the corresponding values in the dictionary
        df[new_column_name] = matches.str.lower().map({k.lower(): v for k, v in to_find_dict.items()}).fillna(if_not_in_dict)
        
        # Drop intermediate column if created
        if len(col_names) > 1:
            df.drop(columns=["Merged"], inplace=True)

        return df

    def aggregate_daily_to_wc_wide(self, df : pd.DataFrame, date_column : str, group_columns : list[str], sum_columns : list[str], wc : str = 'sun', aggregation : str = 'sum', include_totals : bool = False) -> pd.DataFrame:
        """
        Aggregates daily data into weekly data, starting on a specified day of the week, 
        and groups the data by additional specified columns. It aggregates specified numeric columns 
        by summing, averaging, or counting them, and pivots the data to create separate columns for each combination 
        of the group columns and sum columns. NaN values are replaced with 0 and the index is reset. 
        The day column is renamed from 'Day' to 'OBS'.

        Parameters:
        - df: pandas DataFrame
            The input DataFrame containing daily data.
        - date_column: string
            The name of the column in the DataFrame that contains date information.
        - group_columns: list of strings
            Additional column names to group by along with the weekly grouping.
        - sum_columns: list of strings
            Numeric column names to be aggregated during aggregation.
        - wc: string
            The week commencing day (e.g., 'sun' for Sunday, 'mon' for Monday).
        - aggregation: string, optional (default 'sum')
            Aggregation method, either 'sum', 'average', or 'count'.
        - include_totals: boolean, optional (default False)
            If True, include total columns for each sum_column.

        Returns:
        - pandas DataFrame
            A new DataFrame with weekly aggregated data. The index is reset,
            and columns represent the grouped and aggregated metrics. The DataFrame 
            is in wide format, with separate columns for each combination of 
            grouped metrics.
        """
        
        grouped = self.aggregate_daily_to_wc_long(df, date_column, group_columns, sum_columns, wc, aggregation)
        
        # Pivot the data to wide format
        if group_columns:
            wide_df = grouped.pivot_table(index='OBS', 
                                        columns=group_columns, 
                                        values=sum_columns,
                                        aggfunc='first')
            # Flatten the multi-level column index and create combined column names
            wide_df.columns = ['_'.join(col).strip() for col in wide_df.columns.values]
        else:
            wide_df = grouped.set_index('OBS')

        # Fill NaN values with 0
        wide_df = wide_df.fillna(0)

        # Adding total columns for each unique sum_column, if include_totals is True
        if include_totals:
            for col in sum_columns:
                total_column_name = f'Total {col}'
                if group_columns:
                    columns_to_sum = [column for column in wide_df.columns if col in column]
                else:
                    columns_to_sum = [col]
                wide_df[total_column_name] = wide_df[columns_to_sum].sum(axis=1)

        # Reset the index of the final DataFrame
        wide_df = wide_df.reset_index()

        return wide_df

    def merge_cols_with_seperator(self, df, col_names,seperator='_',output_column_name = "Merged",starting_prefix_str=None,ending_prefix_str=None):
        """
        Creates a new column in the dataframe that merges 2 or more columns together with a "_" seperator, possibly to be used for a look up table where multiple columns are being looked up

        Parameters:
        df (pandas.DataFrame): Dataframe to make changes to.
        col_names (list): list of columm names ot merge.
        seperator (str, optional): Name of column outputted. Defaults to "_".
        output_column_name (str, optional): Name of column outputted. Defaults to "Merged".
        starting_prefix_str (str, optional): string of optional text to be added before the merged column str value
        ending_prefix_str (str, optional): string of optional text to be added after the merged column str value

        Raises:
        ValueError: if more less than two column names are inputted in the list there is nothing to merge on

        Returns:
        pandas.DataFrame: DataFrame with additional merged column
        """
        # Specify more than one column must be entered
        if len(col_names) < 2:
            raise ValueError("2 or more columns must be specified to merge")
        
        # Create a new column with the merged columns
        df[output_column_name] = df[col_names].astype(str).apply(seperator.join, axis=1)

        # Add string before 
        if starting_prefix_str is not None:
            df[output_column_name] = starting_prefix_str + df[output_column_name].astype(str)
        
        # Add string after
        if ending_prefix_str is not None:
            df[output_column_name] = df[output_column_name].astype(str) + ending_prefix_str
                    
        return df

    def check_sum_of_df_cols_are_equal(self, df_1,df_2,cols_1,cols_2):
        """
        Checks the sum of two different dataframe column or columns are equal

        Parameters:
        df_1 (pandas.DataFrame): First dataframe for columnsa to be summed on.
        df_2 (pandas.DataFrame): Second dataframe for columnsa to be summed on.
        cols_1 (list of str): Columns from first dataframe to sum.
        cols_2 (list of str): Columns from second dataframe to sum.

        Returns:
        Tuple: Answer is the true or false answer to whether sums are the same, df_1_sum is the sum of the column/columns in the first dataframe, df_2_sum is the sum of the column/columns in the second dataframe
        """
        # Find the sum of both sets of columns
        df_1_sum = df_1[cols_1].sum().sum()
        df_2_sum = df_2[cols_2].sum().sum()
        
        # If the the two columns are 
        if df_1_sum == df_2_sum:
            Answer = "They are equal"
        if df_1_sum != df_2_sum:
            Answer = "They are different by " + str(df_2_sum-df_1_sum)     
            
        return Answer,df_1_sum,df_2_sum
    
    def convert_2_df_cols_to_dict(self, df, key_col, value_col):
        """
        Create a dictionary mapping from two columns of a DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        key_col (str): The column name to use as keys in the dictionary.
        value_col (str): The column name to use as values in the dictionary.

        Returns:
        dict: A dictionary with keys from 'key_col' and values from 'value_col'.
        """
        if key_col not in df or value_col not in df:
            raise ValueError("Specified columns are not in the DataFrame")

        return {df[key_col].iloc[i]: df[value_col].iloc[i] for i in range(len(df))}
    
    def create_FY_and_H_columns(self, df, index_col, start_date, starting_FY,short_format="No",half_years="No",combined_FY_and_H="No"):
        """
        Creates new DataFrame columns containing companies' Financial Year, Half Years and Financial Half years, based on the start date of the first full financial year 

        Parameters:
        df (pandas.DataFrame): Dataframe to operate on.
        index_col (str): Name of the column to use for datetime
        start_date (str): String used to specify the start date of an FY specified, needs to be of format "yyyy-mm-dd" e.g. 2021-11-31
        starting_FY (str): String used to specify which FY the start date refers to, needs to be formatted LONG e.g. FY2021
        short_format (str, optional): String used to specify if short format is desired (e.g. FY21) or if long format is desired (e.g. FY2021). Defaults to "No".
        half_years (str, optional): String used to specify if half year column is desired. Defaults to "No".
        combined_FY_and_H (str, optional): String used to specify is a combined half year and FY column is desired. Defaults to "No".

        Returns:
        pandas.DataFrame: DataFrame with a new column 'FY' containing the FY as well as, if desired, a half year column and a combined FY half year column.
        """
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            print("Error: Date must be of format yyyy-mm-dd")
            return df
        
        df["OBS"] = pd.to_datetime(df[index_col])
        df["OBS as string"] = df["OBS"].dt.strftime("%Y-%m-%d")

        df[index_col] = pd.to_datetime(df[index_col])

        start_year = int(starting_FY[2:])

        def calculate_FY_vectorized(date_series):
            years_since_start = ((date_series - start_date).dt.days / 365.25).astype(int)
            fy = 'FY' + (start_year + years_since_start).astype(str)
            if short_format == "Yes":
                fy = 'FY' + fy.str[-2:]
            return fy

        df['FY'] = calculate_FY_vectorized(df[index_col])

        if half_years == "Yes" or combined_FY_and_H == "Yes":
            end_of_h1 = start_date + pd.DateOffset(months=6) - pd.DateOffset(days=1)
            df['Half Years'] = np.where(df[index_col] <= end_of_h1, 'H1', 'H2')
        
        if combined_FY_and_H == "Yes":
            df['Financial Half Years'] = df['FY'] + ' ' + df['Half Years']

        return df
    
    def keyword_lookup_replacement(self, df, col, replacement_rows, cols_to_merge, replacement_lookup_dict,output_column_name="Updated Column"):
        """
        This function updates values in a specified column of the DataFrame based on a lookup dictionary.
        It first merges several columns into a new 'Merged' column, then uses this merged column to determine
        if replacements are needed based on the dictionary.

        Parameters:
        df (pd.DataFrame): The DataFrame to process.
        col (str): The name of the column whose values are potentially replaced.
        replacement_rows (str): The specific value in 'col' to check for replacements.
        cols_to_merge (list of str): List of column names whose contents will be merged to form a lookup key.
        replacement_lookup_dict (dict): Dictionary where keys are merged column values and values are the new data to replace in 'col'.
        output_column_name (str, optional): Name of column outputted. Defaults to "Updated Column".

        Returns:
        pd.DataFrame: The modified DataFrame with updated values in the specified column.
        """
        df["Merged"] = df[cols_to_merge].apply(lambda row: '|'.join(row.values.astype(str)), axis=1)
        
        def replace_values(x):
            if x[col] == replacement_rows:
                merged_value = x['Merged']  
                if merged_value in replacement_lookup_dict:
                    return replacement_lookup_dict[merged_value]
            return x[col]
        
        df[output_column_name] = df.apply(replace_values, axis=1)
        
        return df
    
    def create_new_version_of_col_using_LUT(self, df, keys_col,value_col, dict_for_specific_changes, new_col_name="New Version of Old Col"):
        """
        Creates a new column in a dataframe, which takes an old column and uses a lookup table to changes values in the new column to reflect the lookup table. 
        The lookup is based on a column in the dataframe. Can only input one column and output one new column.

        Parameters:
            df (pandas.DataFrame): The DataFrame containing the data.
            keys_col (str): The name of the column which the LUT will be refercing to ouput a value.
            value_col (str): The name of the column which the new column will be based off. If a key in the key column is not found in the LUT, the values from this column are used instead.
            dict_for_specific_changes (dict): The LUT which the keys_col will be mapped on to find any values that need changing in the new column.
            new_col_name (str, optional): This is the name of the new column being generated. Defaults to "New Version of Old Col".

        Returns:
        pandas.DataFrame: DataFrame with a new column which is similar to the old column, except for where changes have been made to reflect the lookup table.
        """
    
        # Extract columns to change using new dictionary
        smaller_df = df[[keys_col,value_col]]

        # Use the new dictionary to create a new LUT
        smaller_df_with_LUT = self.apply_lookup_table_for_columns(smaller_df,[keys_col,value_col],dict_for_specific_changes)
        
        # In a new column, keep values from the old column that don't need updating as they are not in the dictionary, and replace values that do need updating with values from the dictionary based on the keys
        smaller_df_with_LUT["Updated Col"]=smaller_df_with_LUT.apply(lambda x: x['Mapping'] if x['Mapping'] != "Other" else x[value_col],axis=1)

        # Drop the extra unecessary cols
        smaller_df_with_LUT.drop([keys_col,'Mapping'],axis=1,inplace=True)
        
        # # Output dataframes as dictionary to be used in a LUT
        new_dict = self.convert_2_df_cols_to_dict(smaller_df_with_LUT,value_col,"Updated Col")

        # # Use new dictionary to create a new version of an old column
        df_final = self.apply_lookup_table_for_columns(df,[keys_col],new_dict,"other",new_col_name)
        
        return df_final
    
    def convert_df_wide_2_long(self, df,value_cols,variable_col_name='Stacked',value_col_name='Value'):
        """
        Changes a dataframe from wide to long format.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            value_cols (list of str or str if only one): list of column names which are to be transformed from several columns into one.
            variable_col_name (str, optional): Name of new variables column, which contains the names of the columns which have been stacked into one. Defaults to 'Stacked'.
            value_col_name (str, optional): Name of the new value column which contains all the data from the stacked columns. Defaults to 'Value'.

        Returns:
            pandas.DataFrame:: Returns dataframe transformed from long to wide.
            
        Raises:
            ValueError: If number of column names to be depivoted is less than 2, then this function is not neccesary.
        """
        
        # Check length of value cols is greater than 1
        if len(value_cols) < 2:
            raise ValueError("Number of inputs in list must be greater than 1")
        
        # Find the columns that are not to be depivoted into one column
        id_vars = list(set(df.columns.tolist()) - set(value_cols))
        
        # Melt all columns chosen into one column
        df_final = pd.melt(df, id_vars,value_cols,var_name=variable_col_name,value_name=value_col_name)
        
        return df_final
    
    def manually_edit_data(self, df, filters_dict, col_to_change, new_value, change_in_existing_df_col="No", new_col_to_change_name='New', manual_edit_col_name=None, add_notes="No", existing_note_col_name=None, note=None):
        """
        Allows the capability to manually update any cell in dataframe by applying filters and chosing a column to edit in dataframe

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            filters_dict (dict): Dictionary of conditions for the boolean mask i.e. what to filter your df on to get to your chosen cell
            col_to_change (str): String name of column to edit
            new_value (any): Value of new input for cell
            change_in_existing_df_col (str, optional): Input of Yes or No to describe whether to make the change in an existing column. Defaults to "No".
            new_col_to_change_name (str, optional): Name of the new column to copy the column being edited into and to make the change in. Defaults to 'New'.
            manual_edit_col_name (str, optional): Name of the current manual edits column, if one is not specified it will be created. Defaults to None.
            add_notes (str, optional): Gives the option to create a new notes column. Defaults to "No".
            existing_note_col_name (str, optional): If there is an existing notes column this can be specified. Defaults to None.
            note (str), optional): The string of the note to be added to the column. Defaults to None.

        Raises:
            TypeError: The column for the column to change can only be specified as one column as it is a string not a list
            ValueError: You can only input the values of "Yes" or "No" for whether to make the change in existing column
            ValueError: You can only input the values of "Yes" or "No" for whether to make a new notes column

        Returns:
            pandas.DataFrame: Dataframe with manual changes added
        """
        # Raise type error if more than one col is supported
        if isinstance(col_to_change, list):
            raise TypeError("Col to change must be specified as a string, not a list")
        
        # Raises value error if input is invalid for change_in_existing_df_col
        if change_in_existing_df_col not in ["Yes", "No"]:
            raise ValueError("Invalid input value for change_in_existing_df_col. Allowed values are: ['Yes', 'No']")
        
        # Raises value error if input is invalid for add_notes_col
        if add_notes not in ["Yes", "No"]:
            raise ValueError("Invalid input value for add_notes. Allowed values are: ['Yes', 'No']")

        # Create the filtered df by applying the conditions
        df_filtered = self.filter_df_on_multiple_conditions(df, filters_dict)

        # Create a new column to add the changes if desired, else edit in the current chosen column
        col_to_update = col_to_change if change_in_existing_df_col == "Yes" else new_col_to_change_name
        if change_in_existing_df_col == "No" and new_col_to_change_name not in df.columns:
            df = df.copy()
            df[new_col_to_change_name] = df[col_to_change]
            
        # Update the new cell in the chosen column
        df.loc[df_filtered.index, col_to_update] = new_value

        # Add in manual edit column if desired or specify where one already is
        if manual_edit_col_name:
            if manual_edit_col_name not in df.columns:
                df[manual_edit_col_name] = 0
            df.loc[df_filtered.index, manual_edit_col_name] = 1
        elif not manual_edit_col_name and 'Manual Changes' not in df.columns:
            df['Manual Changes'] = 0
            df.loc[df_filtered.index, 'Manual Changes'] = 1

        # Add note if desired in new column or an existing column
        if add_notes == "Yes":
            note_col = existing_note_col_name if existing_note_col_name else 'Notes'
            if note_col not in df.columns:
                df[note_col] = None
            df.loc[df_filtered.index, note_col] = note

        return df
    
    def format_numbers_with_commas(self, df, decimal_length_chosen=2):
        """
        Converts data in numerical format into numbers with commas and a chosen decimal place length

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            decimal_length_chosen (int, optional): _description_. Defaults to 2.
            
        Returns:
            pandas.DataFrame: The dataframe with the chosen updated format
        """
        def format_number_with_commas(x, decimal_length=decimal_length_chosen):
            if isinstance(x, (int, float)):
                if decimal_length is not None:
                    format_str = "{:,.{}f}".format(x, decimal_length)
                    formatted_number = format_str.format(x)
                else:
                    formatted_number = "{:,}".format(x)
                return formatted_number
            else:
                return x  # Return unchanged if not a number


        # Apply the function across several columns using applymap()
        formatted_df = df.applymap(format_number_with_commas)

        return formatted_df
    
    def filter_df_on_multiple_conditions(self, df, filters_dict):
        """
        Filter a dataframe based on mulitple conditions

        Args:
            df (pandas.DatFrame): Dataframe to filter on
            filters_dict (dict): Dictionary with strings as conditions

        Returns:
            pandas.DatFrame: Filtered Da
        """
        mask = pd.Series(True, index=df.index)
        for col, cond in filters_dict.items():
            cond = cond.strip()
            operator, value = cond.split(maxsplit=1)
            
            # If value is a string condition make sure to check if there are new lines
            if "'" in value:
                value = value.strip().strip("'\"")
            # If not a string e.g. datetime or number condition you need to transform the string into a value
            else:
                value = eval(value)  

            if operator == "==":
                temp_mask = (df[col] == value)
            elif operator == "!=":
                temp_mask = (df[col] != value)
            elif operator == ">=":
                temp_mask = (df[col] >= value)
            elif operator == "<=":
                temp_mask = (df[col] <= value)
            elif operator == ">":
                temp_mask = (df[col] > value)
            elif operator == "<":
                temp_mask = (df[col] < value)                          
            mask &= temp_mask

        # Create the filtered df by applying the conditions
        df_filtered = df[mask]
    
        return df_filtered

class datapull:

    def pull_fred_data(self, week_commencing: str = 'sun', series_id_list: list[str] = ["GPDIC1", "Y057RX1Q020SBEA", "GCEC1", "ND000333Q", "Y006RX1Q020SBEA"]) -> pd.DataFrame:
        '''
        Parameters
        ----------
        week_commencing : str
            specify the day for the week commencing, the default is 'sun' (e.g., 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

        series_id_list : list[str]
            provide a list with IDs to download data series from FRED (link: https://fred.stlouisfed.org/tags/series?t=id). Default list is 
            ["GPDIC1", "Y057RX1Q020SBEA", "GCEC1", "ND000333Q", "Y006RX1Q020SBEA"]
        
        Returns
        ----------
        pd.DataFrame
            Return a data frame with FRED data according to the series IDs provided

        Example
        ----------
        pull_fred_data("mon", ["GCEC1", "SP500"])
        '''
        # Fred API
        fred = Fred(api_key='76f5f8156145fdb8fbaf66f1eb944f8a')

        # Fetch the metadata for each series to get the full names
        series_names = {series_id: fred.get_series_info(series_id).title for series_id in series_id_list}

        # Download data from series id list
        fred_series = {series_id: fred.get_series(series_id) for series_id in series_id_list}

        # Data processing
        date_range = {'OBS': pd.date_range("1950-01-01", datetime.today().strftime('%Y-%m-%d'), freq='d')}
        fred_series_df = pd.DataFrame(date_range)

        for series_id, series_data in fred_series.items():
            series_data = series_data.reset_index()
            series_data.columns = ['OBS', series_names[series_id]]  # Use the series name as the column header
            fred_series_df = pd.merge_asof(fred_series_df, series_data, on='OBS', direction='backward')

        # Handle duplicate columns
        for col in fred_series_df.columns:
            if '_x' in col:
                base_col = col.replace('_x', '')
                fred_series_df[base_col] = fred_series_df[col].combine_first(fred_series_df[base_col + '_y'])
                fred_series_df.drop([col, base_col + '_y'], axis=1, inplace=True)

        # Ensure sum_columns are present in the DataFrame
        sum_columns = [series_names[series_id] for series_id in series_id_list if series_names[series_id] in fred_series_df.columns]

        # Aggregate results by week
        fred_df_final = dataprocessing.aggregate_daily_to_wc_wide(df=fred_series_df, 
                                                    date_column="OBS", 
                                                    group_columns=[], 
                                                    sum_columns=sum_columns,
                                                    wc=week_commencing,
                                                    aggregation="average")

        # Remove anything after the instance of any ':' in the column names and rename
        fred_df_final.columns = ['macro_' + col.lower().split(':')[0].replace(' ', '_') for col in fred_df_final.columns]

        return fred_df_final
    
    def pull_boe_data(week_commencing="mon", max_retries=30, delay=5):
        # Week commencing dictionary
        day_dict = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}
        
        # Function to fetch the data with retries
        def fetch_data_with_retries(url, max_retries, delay):
            for attempt in range(max_retries):
                try:
                    html_table = pd.read_html(url)[0]
                    return html_table
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        raise
        
        # Import HTML data from Bank of England rate
        url = 'https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp'
        html_table = fetch_data_with_retries(url, max_retries, delay)
        
        df = pd.DataFrame(html_table)
        df.rename(columns={"Date Changed": "OBS", "Rate": "macro_boe_intr_rate"}, inplace=True)
        
        # Change date column to datetime and find the corresponding week to the date
        df["OBS"] = pd.to_datetime(df["OBS"], format="%d %b %y")
        df.sort_values("OBS", axis=0, inplace=True)
        
        # Create a daily date range and find the week commencing for that day
        date_range = pd.date_range(df["OBS"].iloc[0], datetime.date.today(), freq="d")
        df_daily = pd.DataFrame(date_range, columns=["OBS"])
        
        # Find the start of the week for each day
        df_daily['OBS'] = df_daily["OBS"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        
        # Outer merge the daily date range on the boe dataframe and forward fill in the blanks
        df_final = df_daily.merge(df, on='OBS', how="left")
        df_final.ffill(inplace=True)
        
        # Group by the week start date and get the mean of the interest rates for each week
        df_final = df_final.groupby('OBS')['macro_boe_intr_rate'].mean().reset_index()
        
        # Format the dates in the final dataframe
        df_final['OBS'] = df_final['OBS'].dt.strftime('%d/%m/%Y')
        
        return df_final
