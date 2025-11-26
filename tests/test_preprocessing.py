"""
Test suite for data preprocessing functions
"""
import pytest
import numpy as np


def test_imports():
    """Test that required libraries can be imported"""
    import pandas as pd
    import sklearn
    assert pd.__version__ is not None
    assert sklearn.__version__ is not None


def test_data_directories_exist():
    """Test that data directories are properly set up"""
    import os
    
    base_dirs = ['data', 'notebooks', 'models']
    for dir_name in base_dirs:
        assert os.path.exists(dir_name), f"Directory {dir_name} should exist"


def test_numpy_operations():
    """Test basic numpy operations for feature engineering"""
    arr = np.array([1, 2, 3, 4, 5])
    
    # Test log1p transformation
    log_arr = np.log1p(arr)
    assert len(log_arr) == len(arr)
    assert all(log_arr > 0)
    
    # Test that we can reverse it
    reversed_arr = np.expm1(log_arr)
    np.testing.assert_array_almost_equal(reversed_arr, arr)
    

def test_train_test_split():
    """Test that train/test split logic works"""
    from sklearn.model_selection import train_test_split
    
    X = np.arange(100).reshape(-1, 1)
    y = np.arange(100)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )
    
    assert len(X_train) == 85
    assert len(X_test) == 15
    assert len(y_train) == 85
    assert len(y_test) == 15
