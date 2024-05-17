import altair as alt
import pandas as pd

class DataVisualizer:
    """
    A class for generating charts using Altair.

    Attributes:
    data (DataFrame): The input data for visualization.
    """

    def __init__(self, data):
        """
        Initializes the DataVisualizer class with input data.

        Args:
        data (DataFrame): The input DataFrame for visualization.
        """
        self.data = data

    def scatter_plot(self, x, y):
        """
        Generates a scatter plot.

        Args:
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        """
        chart = alt.Chart(self.data).mark_point().encode(
            x=x,
            y=y
        ).properties(
            title=f'Scatter Plot: {x} vs {y}'
        )
        return chart

    def bar_chart(self, x, y):
        """
        Generates a bar chart.

        Args:
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        """
        chart = alt.Chart(self.data).mark_bar().encode(
            x=x,
            y=y
        ).properties(
            title=f'Bar Chart: {x} vs {y}'
        )
        return chart

    def line_chart(self, x, y):
        """
        Generates a line chart.

        Args:
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        """
        chart = alt.Chart(self.data).mark_line().encode(
            x=x,
            y=y
        ).properties(
            title=f'Line Chart: {x} vs {y}'
        )
        return chart

# Example usage:
# Assuming 'df' is your DataFrame

# Initialize DataVisualizer instance
visualizer = DataVisualizer(df)

# Generate scatter plot
scatter_plot = visualizer.scatter_plot('x_column', 'y_column')
scatter_plot.show()

# Generate bar chart
bar_chart = visualizer.bar_chart('category_column', 'value_column')
bar_chart.show()

# Generate line chart
line_chart = visualizer.line_chart('time_column', 'value_column')
line_chart.show()