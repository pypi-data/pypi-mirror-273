import sqlite3
import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

class combos:
    """
    A class for generating and visualizing product combos.

    Attributes:
        df (pd.DataFrame): DataFrame containing product data.
        price_df (pd.DataFrame): DataFrame containing price data.
    """

    def __init__(self) -> None:
        """
        Initializes the combos class by reading data from the database.
        """
        conn = sqlite3.connect('database.db')
        self.df = pd.read_sql_query("SELECT * FROM checks", conn)
        self.price_df = pd.read_sql_query("SELECT * FROM price_list", conn)
        conn.close()

    def has_multiple_components(self, string: str, n: int) -> bool:
        """
        Checks if a product combo has at least 'n' components.

        Args:
            string (str): The product combo string.
            n (int): Minimum number of components.

        Returns:
            bool: True if the combo has at least 'n' components, False otherwise.
        """
        return len(string.split('/')) >= n

    def calculate_combo_price(self, products: list, discount: float = 10) -> float:
        """
        Calculates the total price of a combo.

        Args:
            products (list): List of products in the combo.
            discount (float): Discount percentage (default is 10).

        Returns:
            float: Total price of the combo after discount.
        """
        combo_price = 0
        for product in products:
            price = self.price_df.loc[self.price_df['product'] == product, 'price'].values
            combo_price += price
        return combo_price * (1 - discount / 100)

    def make_combos(self, k: int = 10, discount: float = 10) -> pd.DataFrame:
        """
        Generates combos based on product frequency and visualizes them.

        Args:
            k (int): Maximum number of combos to generate (default is 10).
            discount (float): Discount percentage (default is 10).

        Returns:
            pd.DataFrame: DataFrame containing the generated combos.
        """
        unique_products = set(self.df['products'])
        product_frequencies = Counter(unique_products)
        frequencies = list(product_frequencies.values())
        unique_products = self.df['products'].unique()
        product_frequencies = Counter(self.df['products'])
        frequencies = [product_frequencies[product] for product in unique_products]
        frequency_table = pd.DataFrame({'Products': unique_products, 'Frequency': frequencies})
        sorted_frequency_table = frequency_table.sort_values(by='Frequency', ascending=False)

        best_i, best_j = None, None
        min_len = float('inf')  

        for i in range(3, 5):
            for j in range(2, int(np.sqrt(len(sorted_frequency_table)))):
                sorted_frequency_table['Products'] = sorted_frequency_table['Products'].astype(str)

                mask = sorted_frequency_table['Products'].apply(lambda x: self.has_multiple_components(x, i))
                filtered_table = sorted_frequency_table[mask].copy()

                filtered_table.drop(filtered_table[filtered_table['Frequency'] < j].index, inplace=True)

                length = len(filtered_table) 
                if length <= k:
                    mask = sorted_frequency_table['Products'].apply(lambda x: self.has_multiple_components(x, best_i))
                    filtered_table = sorted_frequency_table[mask].copy()
                    filtered_table.drop(filtered_table[filtered_table['Frequency'] < best_j].index, inplace=True)
            
                    # Calculate prices for each combo
                    filtered_table['Combo_Price'] = filtered_table['Products'].apply(lambda x: self.calculate_combo_price(x.split('/'), discount)[0])
            
                    return filtered_table

                if length < min_len:  
                    best_i, best_j = i, j
                    min_len = length

        mask = sorted_frequency_table['Products'].apply(lambda x: self.has_multiple_components(x, best_i))
        filtered_table = sorted_frequency_table[mask].copy()
        filtered_table.drop(filtered_table[filtered_table['Frequency'] < best_j].index, inplace=True)

        # Calculate prices for each combo
        filtered_table['Combo_Price'] = filtered_table['Products'].apply(lambda x: self.calculate_combo_price(x.split('/'), discount)[0])

        return filtered_table
                                                
    def visualize_most_frequent_combos(self, top_n: int = 5):
        """
        Visualizes the top most frequent combos in a bar chart.

        Args:
            top_n (int): Number of top most frequent combos to visualize (default is 5).

        Returns:
            None
        """
        most_frequent_combos = self.df['products'].value_counts().nlargest(top_n)
        most_frequent_combos.plot(kind='bar', figsize=(10, 6), color='skyblue')
        plt.title('Top {} Most Frequent Combos'.format(top_n))
        plt.xlabel('Combo')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.show()

    def visualize_expensive_combos(self, top_n: int = 5):
        """
        Visualizes the top most expensive combos in a bar chart.

        Args:
            top_n (int): Number of top most expensive combos to visualize (default is 5).

        Returns:
            None
        """
        combos_df = self.make_combos(discount=0)
        sorted_combos = combos_df.nlargest(top_n, 'Combo_Price')

        # Plot the top expensive combos
        sorted_combos.plot(kind='bar', x='Products', y='Combo_Price', figsize=(10, 6), color='salmon')
        plt.title('Top {} Expensive Combos'.format(top_n))
        plt.xlabel('Combo')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.show()

    def visualize_cheap_combos(self, top_n: int = 5):
        """
        Visualizes the top cheapest combos in a bar chart.

        Args:
            top_n (int): Number of top cheapest combos to visualize (default is 5).

        Returns:
            None
        """
        combos_df = self.make_combos(discount=0)
        sorted_combos = combos_df.nsmallest(top_n, 'Combo_Price')

        # Plot the top expensive combos
        sorted_combos.plot(kind='bar', x='Products', y='Combo_Price', figsize=(10, 6), color='salmon')
        plt.title('Top {} Expensive Combos'.format(top_n))
        plt.xlabel('Combo')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.show()
