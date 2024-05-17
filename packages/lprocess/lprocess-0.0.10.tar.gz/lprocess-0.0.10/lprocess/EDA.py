import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class EDA:
    def __init__(self, data):
        self.data = data

    def handle_missing_values(self, strategy='mean'):
        """
        Handle missing values in the dataset using a specified strategy.
        """
        numeric_cols = self.data.select_dtypes(include=['float64', 'int64']).columns
        categorical_cols = self.data.select_dtypes(include=['object']).columns

        if strategy == 'mean':
            self.data[numeric_cols] = self.data[numeric_cols].fillna(self.data[numeric_cols].mean())
            for col in categorical_cols:
                mode_value = self.data[col].mode().values[0]
                self.data[col] = self.data[col].fillna(mode_value)
        elif strategy == 'median':
            self.data[numeric_cols] = self.data[numeric_cols].fillna(self.data[numeric_cols].median())
            for col in categorical_cols:
                mode_value = self.data[col].mode().values[0]
                self.data[col] = self.data[col].fillna(mode_value)
        elif strategy == 'mode':
            self.data = self.data.fillna(self.data.mode().iloc[0].to_numpy())
        elif strategy == 'drop':
            self.data = self.data.dropna()
        else:
            raise ValueError("Invalid strategy. Choose from 'mean', 'median', 'mode', or 'drop'.")

        return self.data

    def data_summary(self):
        """
        Print a summary of the dataset, including information about data types, missing values, and summary statistics.
        """
        print("Dataset Information:")
        print(self.data.info())
        print("\nMissing Values:")
        print(self.data.isnull().sum())
        print("\nSummary Statistics:")
        print(self.data.describe())

    def plot_distributions(self, cols=None, figsize=(20, 25), plot_type='hist', ncols = 2):
        """
        Plot distributions for specified columns in the dataset.
        """
        if cols is None:
            cols = self.data.columns
    
        plt.figure(figsize=figsize)
        num_plots = len(cols)
        rows = (num_plots + ncols - 1) // ncols
        cols_per_row = ncols
        
        for i, col in enumerate(cols):
            plt.subplot(rows, cols_per_row, i+1)
            if self.data[col].dtypes == 'object':  # Check if the column is categorical
                if plot_type == 'hist':
                    self.plot_categorical_hist(col)
                elif plot_type == 'kde':
                    self.plot_categorical_kde(col)
            else:  # Numerical column
                if plot_type == 'hist':
                    self.plot_numerical_hist(col)
                elif plot_type == 'kde':
                    self.plot_numerical_kde(col)
            plt.title(f"Distribution of {col}")
        plt.tight_layout()
        plt.show()

    def plot_categorical_hist(self, col):
        """
        Plot a histogram for a categorical column.
        """
        value_counts = self.data[col].value_counts()
        categories = value_counts.index
        counts = value_counts.values
        plt.bar(categories, counts)
        plt.xticks(rotation=45)

    def plot_categorical_kde(self, col):
        """
        Plot a kernel density estimate for a categorical column.
        """
        codes = self.data[col].astype('category').cat.codes
        plt.hist(codes, density=True, histtype='stepfilled', alpha=0.5)

    def plot_numerical_hist(self, col):
        """
        Plot a histogram for a numerical column.
        """
        plt.hist(self.data[col].dropna(),  density=True, alpha=0.5, ec="red")

    def plot_numerical_kde(self, col):
        """
        Plot a kernel density estimate for a numerical column.
        """
        values = self.data[col].dropna().values
        kde = self.calc_kde(values)
        x_grid = np.linspace(values.min(), values.max(), len(values))
        y_grid = kde(x_grid)
        plt.plot(x_grid, y_grid)

    def calc_kde(self, data):
        """
        Calculate the kernel density estimate for a given data array.
        """
        bandwidth = 1.06 * data.std() * len(data) ** (-1/5)
        kernel = self.gaussian_kernel(bandwidth)
        data = data[:, np.newaxis]  # Add a new axis to make data 2D
        return lambda x: np.mean(kernel((x - data) / bandwidth), axis=1)

    def gaussian_kernel(self, bandwidth):
        """
        Gaussian kernel function.
        """
        def kernel(x):
            return (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)
        return kernel

    def plot_correlation(self, figsize=(10, 8), missing_strategy='mean'):
        """
        Plot a correlation matrix heatmap for the dataset.
        """
        # Handle missing values
        data_filled = self.handle_missing_values(strategy=missing_strategy)
    
        # Create a DataFrame with only numeric columns
        numeric_cols = data_filled.select_dtypes(include=['float64', 'int64']).columns
        numeric_data = data_filled[numeric_cols]
    
        plt.figure(figsize=figsize)
        corr = numeric_data.corr()
        plt.imshow(corr, cmap='coolwarm')
        plt.colorbar()
        plt.xticks(range(len(corr)), corr.columns, rotation=90)
        plt.yticks(range(len(corr)), corr.columns)
        plt.title('Correlation Matrix')
        plt.show()

    def categorical_analysis(self, col):
        """
        Analyze a categorical column by printing its value counts and plotting a bar chart.
        """
        print(f"Value Counts for {col}:")
        print(self.data[col].value_counts())
        plt.figure(figsize=(8, 6))
        self.plot_categorical_hist(col)
        plt.title(f"Distribution of {col}")
        plt.show()
