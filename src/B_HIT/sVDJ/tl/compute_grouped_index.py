from .spatial_bcr_desc import compute_index
def compute_grouped_index(_Index_compute, index, groups, column_name, exclude_values=None, exclude_name=None):
    """
    Compute a specified index for each group defined by `groups` in the DataFrame.

    Parameters
    ----------
    _Index_compute : pd.DataFrame
        The input DataFrame containing the data to compute the index.
    index : str
        The index to compute (e.g., 'gini_index', 'Clonality', etc.).
    groups : list of str
        List of columns to group by (e.g., ['sample', 'Cregion_simple', 'familyLocClass']).
    column_name : str
        The name of the column ('freq' or 'count') to use for the index calculation.
    exclude_values : list, optional
        List of values to exclude from the (exclude_name) column, by default excludes ['Shared'].
    exclude_values : str, optional
        The name of the column to be excluded.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the computed index for each group.
    """
    # Compute the index for each group
    tmp_df = _Index_compute.groupby(groups)[column_name].apply(lambda x: compute_index(index, x)).reset_index(name=index)
    
    # Drop rows with NaN values in the computed index column
    tmp_df = tmp_df.dropna(subset=[index])
    
    # Exclude values if specified
    if exclude_values is not None:
        tmp_df = tmp_df[~tmp_df[exclude_name].isin(exclude_values)]
    
    return tmp_df
