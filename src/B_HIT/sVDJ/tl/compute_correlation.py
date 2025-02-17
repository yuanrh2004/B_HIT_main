import pandas as pd
from scipy.stats import pearsonr

def compute_correlation(cloneRich, groupby_cols, corr1, corr2, save=False, path=None):
    """
    Compute the Pearson correlation between two columns (e.g., 'BaggArea' and 'cloneFamilyRichness') 
    for each group in the DataFrame, and optionally save the results to a CSV file.
    
    Parameters
    ----------
    cloneRich : pd.DataFrame
        The input DataFrame containing the data to be analyzed.
    groupby_cols : list of str
        List of columns to group by (e.g., ['Cregion_simple', 'tissue']). 
        The correlation will be computed within each group.
    corr1, corr2 : str
        The column names for which the Pearson correlation is computed. 
        These are typically columns containing numerical data (e.g., 'BaggArea' and 'cloneFamilyRichness').
    save : bool, optional
        Whether to save the correlation results to a CSV file. Default is False.
    path : str, optional
        The file path to save the correlation results (required if save is True).

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the Pearson correlation and P-value for each group defined by the 'groupby_cols'.
        Columns will be ['corr', 'Pvalue'].
    """
    
    # Initialize an empty dictionary to store the correlation results for each group
    grouped_correlations = {}
    
    # Loop through each group defined by 'groupby_cols' and compute Pearson correlation for 'corr1' and 'corr2'
    for group, group_data in cloneRich.groupby(groupby_cols):
        correlation, p_value = pearsonr(group_data[corr1], group_data[corr2])  # Pearson correlation
        grouped_correlations[group] = (correlation, p_value)  # Store the results for each group
    
    # Convert the dictionary of results into a DataFrame
    corrDf = pd.DataFrame(grouped_correlations).T  # Transpose to get groups as rows
    corrDf.columns = ['corr', 'Pvalue']  # Name the columns
    
    # If 'save' is True, write the DataFrame to a CSV file at the specified 'path'
    if save and path:
        corrDf.to_csv(path)
    
    # Return the DataFrame containing correlation results
    return corrDf

# grouped_correlations = {}
# for group, group_data in tmp_df.groupby(['Cregion_simple','tissue']):
#     group_data = group_data.dropna(subset=['Clonal_diversification'])
#     correlation, _ = pearsonr(group_data['BaggArea'], group_data['Clonal_diversification'])
#     grouped_correlations[group] = (correlation, _)
# print(grouped_correlations)

def compute_groupwise_corr_matrix(grouped_correlations, corr_col, pvalue_col, groupby_cols, save=False, path=None):
    """
    Compute the Pearson correlation and p-value for each group defined by groupby_cols and return the correlation and p-value matrices.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing the data.
    corr_col : str
        The column name for which the Pearson correlation is computed (e.g., 'BaggArea').
    pvalue_col : str
        The column name for which the p-value is calculated (e.g., 'cloneFamilyRichness').
    groupby_cols : list of str
        List of columns to group by (e.g., ['chain', 'region']).
    save : bool, optional
        Whether to save the resulting correlation and p-value matrices as CSV files. Default is False.
    path : str, optional
        The file path to save the matrices if save=True.

    Returns
    -------
    tuple of pd.DataFrame
        Two DataFrames: one for the correlation matrix and one for the p-value matrix.
    """

    corrDf = pd.DataFrame(grouped_correlations).T
    corrDf.columns = ['corr', 'Pvalue']
    
    corrmat = corrDf[['corr']].copy().pivot_table(index=groupby_cols[0], columns=groupby_cols[1])
    corrmat.columns = corrmat.columns.get_level_values(1)  # Flatten the multi-index of columns
    Pmat = corrDf[['Pvalue']].copy().pivot_table(index=groupby_cols[0], columns=groupby_cols[1])
    Pmat.columns = Pmat.columns.get_level_values(1)  # Flatten the multi-index of columns
    
    if save and path:
        corrmat.to_csv(f'{path}_correlation_matrix.csv')
        Pmat.to_csv(f'{path}_pvalue_matrix.csv')

    return corrmat, Pmat
