import pandas as pd

def compute_clone_counts(rep_loc, groupby_cols, count_col, count_name='count', freq_name='freq'):
    """
    Compute clone count and frequency for each group defined by groupby_cols.
    
    Parameters
    ----------
    rep_loc : pd.DataFrame
        Input DataFrame containing the raw data.
    groupby_cols : list of str
        List of columns to group by (e.g., ['sample', 'Cregion_simple', 'family_id', 'Bcell_aggregate_label']).
    count_col : list of str
        List of columns for counting and computing the frequency(e.g., 'clone').
    count_name : str, optional
        Name for the count result column (default is 'count').
    freq_name : str, optional
        Name for the frequency result column (default is 'freq').

    Returns
    -------
    pd.DataFrame
        A merged DataFrame containing both count and frequency results. If `freq_col` is None, only count results will be included.
    """
    # Step 1: Calculate the value counts (UmiCount)
    rep_agg = rep_loc[groupby_cols + [count_col]].value_counts().reset_index(name='UmiCount')
    
    # Step 2: Compute count per group
    count_df = rep_agg.groupby(groupby_cols)[count_col].value_counts().reset_index(name=count_name)
    
    # Step 3: Compute frequency per group
    freq_df = rep_agg.groupby(groupby_cols)[count_col].value_counts(normalize=True).reset_index(name=freq_name)
    # Merge count and frequency data
    merged_df = pd.merge(freq_df, count_df, on=groupby_cols + [count_col])

    return merged_df

def compute_richness(rep_loc, groupby_cols, richness_col, richness_name=None, if_saved=False):
    """
    Compute richness (unique counts) for each group defined by groupby_cols.
    
    Parameters
    ----------
    rep_loc : pd.DataFrame
        Input DataFrame containing the raw data.
    groupby_cols : list of str
        List of columns to group by (e.g., ['Bcell_aggregate_label', 'Cregion_simple']).
    richness_col : list of str
        List of columns for which richness will be calculated (e.g., ['clone']).
    richness_name : str, optional
        Name for the richness result column (default is None, which will use the column name as richness name).
    if_saved : bool, optional
        If True, returns the richness as a dictionary with group keys as the index. If False, returns a DataFrame (default is False).

    Returns
    -------
    richness_df : pd.DataFrame or dict
        If `if_saved` is False, returns a DataFrame with richness counts. 
        If `if_saved` is True, returns a dictionary mapping group keys (e.g., ('Bcell_aggregate_label', 'Cregion_simple')) to richness counts.
    """
    # Step 1: Drop duplicates to get unique combinations
    richness_df = rep_loc[groupby_cols + richness_col].drop_duplicates()
    
    # Step 2: Calculate richness as the size of each group
    richness_df = richness_df.groupby(richness_col).size().reset_index(name=richness_name)
    
    if not if_saved:
        return richness_df
    else:
        # Step 3: Remove groups with zero richness
        richness_df = richness_df[richness_df[richness_name] != 0].copy()
        
        # Step 4: Create a dictionary for fast lookup
        richness_dict = richness_df.set_index(richness_col).to_dict()[richness_name]
        
        return richness_dict
