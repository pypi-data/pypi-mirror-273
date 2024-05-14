import pandas as pd
import matplotlib.pyplot as plt

class EDA:
    def __init__(self, df):
        self.df = df

    def summary_statistics(self):
        """
        Generate summary statistics for the DataFrame, handling null values.

        Returns:
        pandas.DataFrame: Summary statistics DataFrame.
        """
        summary_stats = self.df.describe(include='all').transpose()
        summary_stats['missing_values'] = self.df.isnull().sum()
        summary_stats['missing_percentage'] = (summary_stats['missing_values'] / len(self.df)) * 100
        return summary_stats

    def summary_tables(self):
        """
        Generate summary tables for categorical variables.

        Returns:
        dict: Summary tables for categorical variables.
        """
        summary_tables = {}
        for column in self.df.select_dtypes(include=['object']):
            summary_tables[column] = self.df[column].value_counts()
        return summary_tables
    
    def plot_histogram(self, column, bins=10):
        """
        Plot histogram for a numerical column.

        Args:
        column (str): Name of the column to plot histogram for.
        bins (int): Number of bins for the histogram (default is 10).
        """
        if column in self.df.select_dtypes(include=['int', 'float']):
            plt.hist(self.df[column].dropna(), bins=bins)
            plt.title(f'Histogram of {column}')
            plt.xlabel(column)
            plt.ylabel('Frequency')
            plt.show()
        else:
            print(f"{column} is not a numerical column.")

    def plot_histograms(self, columns=None, bins=10):
        """
        Plot histograms for multiple numerical columns.

        Args:
        columns (list): List of column names to plot histograms for. If None, plot histograms for all numerical columns.
        bins (int): Number of bins for the histograms (default is 10).
        """
        if columns is None:
            columns = self.df.select_dtypes(include=['int', 'float']).columns.tolist()
        for column in columns:
            self.plot_histogram(column, bins=bins)
