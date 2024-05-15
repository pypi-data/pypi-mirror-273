import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from combogenius.models.make_combos import combos

def test_combos():
    # Initialize the combos class
    combo_instance = combos()

    # Test has_multiple_components method
    assert combo_instance.has_multiple_components("product1/product2", 2) == True
    assert combo_instance.has_multiple_components("product1", 2) == False

    # Test calculate_combo_price method
    price = combo_instance.calculate_combo_price(['product1', 'product2'], 10)
    assert isinstance(price, float), "calculate_combo_price should return a float"

    # Test make_combos method
    combos_df = combo_instance.make_combos(5, 10)
    assert isinstance(combos_df, pd.DataFrame), "make_combos should return a DataFrame"
    assert 'Combo_Price' in combos_df.columns, "Combo_Price column should be present in the DataFrame"

    # Test visualize_most_frequent_combos method
    try:
        combo_instance.visualize_most_frequent_combos(5)
        # Assuming visualization works if no exceptions are raised
        assert True
    except Exception as e:
        assert False, f"An exception occurred: {e}"

    # Test visualize_expensive_combos method
    try:
        combo_instance.visualize_expensive_combos(5)
        # Assuming visualization works if no exceptions are raised
        assert True
    except Exception as e:
        assert False, f"An exception occurred: {e}"

    # Test visualize_cheap_combos method
    try:
        combo_instance.visualize_cheap_combos(5)
        # Assuming visualization works if no exceptions are raised
        assert True
    except Exception as e:
        assert False, f"An exception occurred: {e}"

