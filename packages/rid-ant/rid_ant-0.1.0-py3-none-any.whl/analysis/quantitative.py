import pandas as pd
import numpy as np
import scipy.stats as stats
import numpy as np
import statsmodels.api as sm

class QuantitativeAnalysis:
    def __init__(self, data):
        self.data = data
    
    def correlation_matrix(self, method='pearson'):
        """
        Calculate the correlation matrix for the data.
        
        Parameters:
        - method: string, optional (default='pearson')
            Method used for correlation calculation.
            Possible values: 'pearson', 'kendall', 'spearman'
        
        Returns:
        - DataFrame: Correlation matrix
        """
        corr_matrix = self.data.corr(method=method)
        return corr_matrix
    
    def covariance_matrix(self):
        """
        Calculate the covariance matrix for the data.
        
        Returns:
        - DataFrame: Covariance matrix
        """
        cov_matrix = self.data.cov()
        return cov_matrix
    
    def linear_regression(self, x_column, y_column):
        """
        Perform linear regression on the given data.
        
        Parameters:
        - x_column: string
            Name of the independent variable column.
        - y_column: string
            Name of the dependent variable column.
        
        Returns:
        - Tuple: (slope, intercept)
            Slope and intercept of the regression line.
        """
        x = self.data[x_column]
        y = self.data[y_column]
        slope, intercept = np.polyfit(x, y, 1)
        return slope, intercept
    
    def descriptive_statistics(self):
        """
        Calculate descriptive statistics for the data.
        
        Returns:
        - DataFrame: Descriptive statistics summary
        """
        stats_summary = self.data.describe()
        return stats_summary
    
    def summary_statistics_categorical(self, column):
        """
        Calculate summary statistics for a categorical variable.
        
        Parameters:
        - column: string
            Name of the categorical variable column.
        
        Returns:
        - DataFrame: Summary statistics for the categorical variable
        """
        summary_stats = self.data[column].value_counts().reset_index()
        summary_stats.columns = ['Category', 'Count']
        return summary_stats
    
    def t_test(self, column, value):
        """
        Perform one-sample t-test on a numeric column.
        
        Parameters:
        - column: string
            Name of the numeric column.
        - value: float
            Expected value to test against.
        
        Returns:
        - Tuple: (t_statistic, p_value)
            T-statistic and p-value of the test.
        """
        t_statistic, p_value = stats.ttest_1samp(self.data[column], value)
        return t_statistic, p_value
    
    def chi_square_test(self, column1, column2):
        """
        Perform chi-square test of independence between two categorical columns.
        
        Parameters:
        - column1: string
            Name of the first categorical column.
        - column2: string
            Name of the second categorical column.
        
        Returns:
        - Tuple: (chi2_statistic, p_value)
            Chi-square test statistic and p-value.
        """
        contingency_table = pd.crosstab(self.data[column1], self.data[column2])
        chi2_statistic, p_value, _, _ = stats.chi2_contingency(contingency_table)
        return chi2_statistic, p_value
    
    def normality_test(self, column, method='shapiro'):
        """
        Perform normality test on a numeric column.
        
        Parameters:
        - column: string
            Name of the numeric column.
        - method: string, optional (default='shapiro')
            Method for normality test.
            Possible values: 'shapiro', 'normaltest', 'anderson'
        
        Returns:
        - Tuple: (test_statistic, p_value)
            Test statistic and p-value of the normality test.
        """
        if method == 'shapiro':
            test_statistic, p_value = stats.shapiro(self.data[column])
        elif method == 'normaltest':
            test_statistic, p_value = stats.normaltest(self.data[column])
        elif method == 'anderson':
            test_statistic = stats.anderson(self.data[column], dist='norm')
            p_value = test_statistic[1]
            test_statistic = test_statistic[0]
        else:
            raise ValueError("Invalid method. Choose from 'shapiro', 'normaltest', 'anderson'")
        return test_statistic, p_value
    
    def fit_distribution(self, column, dist_name):
        """
        Fit a probability distribution to a numeric column.
        
        Parameters:
        - column: string
            Name of the numeric column.
        - dist_name: string
            Name of the distribution to fit (e.g., 'norm' for normal distribution).
        
        Returns:
        - Tuple: (parameters)
            Parameters of the fitted distribution.
        """
        dist_params = getattr(stats, dist_name).fit(self.data[column])
        return dist_params
    
    def detect_outliers_zscore(self, column, threshold=3):
        """
        Detect outliers in a numeric column using Z-score method.
        
        Parameters:
        - column: string
            Name of the numeric column.
        - threshold: float, optional (default=3)
            Z-score threshold for outlier detection.
        
        Returns:
        - Series: Boolean Series indicating outliers.
        """
        z_scores = np.abs(stats.zscore(self.data[column]))
        outliers = z_scores > threshold
        return outliers    
    def time_series_analysis(self, time_column, value_column):
        """
        Perform time series analysis on the data.
        
        Parameters:
        - time_column: string
            Name of the column containing time or date information.
        - value_column: string
            Name of the column containing the values to analyze over time.
        
        Returns:
        - DataFrame: Results of time series analysis.
        """
        time_series = self.data[[time_column, value_column]].copy()
        time_series[time_column] = pd.to_datetime(time_series[time_column])
        time_series.set_index(time_column, inplace=True)
        return time_series
    
    def calculate_growth_rate(self, column, period):
        """
        Calculate growth rate over a specified period.
        
        Parameters:
        - column: string
            Name of the column containing the values to calculate growth rate.
        - period: int
            Number of periods over which to calculate the growth rate.
        
        Returns:
        - float: Growth rate over the specified period.
        """
        values = self.data[column]
        initial_value = values.iloc[0]
        final_value = values.iloc[-1]
        growth_rate = ((final_value / initial_value) ** (1 / period)) - 1
        return growth_rate
    
    def trend_analysis(self, x_column, y_column):
        """
        Perform trend analysis on the data.
        
        Parameters:
        - x_column: string
            Name of the independent variable column (time or other).
        - y_column: string
            Name of the dependent variable column.
        
        Returns:
        - Tuple: (slope, intercept)
            Slope and intercept of the trend line.
        """
        x = sm.add_constant(self.data[x_column])
        y = self.data[y_column]
        model = sm.OLS(y, x).fit()
        slope = model.params[x_column]
        intercept = model.params['const']
        return slope, intercept  
    def cramers_v(self, column1, column2):
        """
        Calculate Cramér's V for association between two categorical variables.
        
        Parameters:
        - column1: string
            Name of the first categorical variable column.
        - column2: string
            Name of the second categorical variable column.
        
        Returns:
        - float: Cramér's V statistic.
        """
        contingency_table = pd.crosstab(self.data[column1], self.data[column2])
        chi2_statistic = stats.chi2_contingency(contingency_table)[0]
        n = contingency_table.sum().sum()
        min_dim = min(contingency_table.shape) - 1
        cramers_v = np.sqrt(chi2_statistic / (n * min_dim))
        return cramers_v


class GroupAnalysis:
    def __init__(self, data):
        self.data = data
    
    def t_test(self, group_column, value_column, group1, group2):
        """
        Perform independent samples t-test between two groups.
        
        Parameters:
        - group_column: string
            Name of the column containing group labels.
        - value_column: string
            Name of the column containing the values to compare between groups.
        - group1: value or list-like
            Label(s) of the first group.
        - group2: value or list-like
            Label(s) of the second group.
        
        Returns:
        - Tuple: (t_statistic, p_value)
            T-statistic and p-value of the t-test.
        """
        group1_data = self.data[self.data[group_column].isin(group1)][value_column]
        group2_data = self.data[self.data[group_column].isin(group2)][value_column]
        t_statistic, p_value = stats.ttest_ind(group1_data, group2_data)
        return t_statistic, p_value
    
    def anova(self, group_column, value_column):
        """
        Perform one-way ANOVA test among multiple groups.
        
        Parameters:
        - group_column: string
            Name of the column containing group labels.
        - value_column: string
            Name of the column containing the values to compare between groups.
        
        Returns:
        - Tuple: (F_statistic, p_value)
            F-statistic and p-value of the ANOVA test.
        """
        groups = self.data[group_column].unique()
        group_data = [self.data[self.data[group_column] == g][value_column] for g in groups]
        f_statistic, p_value = stats.f_oneway(*group_data)
        return f_statistic, p_value
    
    def kruskal_wallis(self, group_column, value_column):
        """
        Perform Kruskal-Wallis H-test among multiple groups.
        
        Parameters:
        - group_column: string
            Name of the column containing group labels.
        - value_column: string
            Name of the column containing the values to compare between groups.
        
        Returns:
        - Tuple: (H_statistic, p_value)
            H-statistic and p-value of the Kruskal-Wallis test.
        """
        groups = self.data[group_column].unique()
        group_data = [self.data[self.data[group_column] == g][value_column] for g in groups]
        h_statistic, p_value = stats.kruskal(*group_data)
        return h_statistic, p_value

    
    def wilcoxon_signed_rank_test(self, column1, column2):
        """
        Perform the Wilcoxon signed-rank test for related samples.
        
        Parameters:
        - column1: string
            Name of the first column containing paired observations.
        - column2: string
            Name of the second column containing paired observations.
        
        Returns:
        - Tuple: (test_statistic, p_value)
            Test statistic and p-value of the Wilcoxon signed-rank test.
        """
        test_statistic, p_value = stats.wilcoxon(self.data[column1], self.data[column2])
        return test_statistic, p_value
