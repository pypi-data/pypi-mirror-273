"""
Pandas Objects Command
"""
import pandas as _vp_pd
import IPython as _vp_ipython
# LAB: prevent import error
_ipython_version = _vp_ipython.version_info
if _ipython_version[0] < 7 or ( _ipython_version[0] == 7 and _ipython_version[1] <= 13 ):
    from IPython.core.display import display
else:
    # from IPython.core.display is deprecated since IPython 7.14
    from IPython.display import display

def _vp_get_rows_list(df, start_idx=0):
    """
    Get Rows List with Detail Information
    """
    rowInfo = { 'name': df.index.name, 'level': df.index.nlevels, 'list': [] }
    indexType = str(df.index.dtype)
    # make dict for rows info
    for i, r in enumerate(df.index):
        rInfo = { 'label': r, 'value': r, 'location': start_idx + i }
        
        # value
        if type(r).__name__ == 'str':
            rInfo['value'] = "'{}'".format(r)
            rInfo['index_dtype'] = indexType # object
        elif type(r).__name__ == 'Timestamp':
            rInfo['label'] = str(r)
            rInfo['value'] = "'{}'".format(r)
            rInfo['index_dtype'] = indexType # datetime64[ns] TODO: exception consideration needed
        rowInfo['list'].append(rInfo)
    return rowInfo

def _vp_get_columns_list(df):
    """
    Get Columns List with Detail Information
    """
    colInfo = { 'name': list(df.columns.names), 'level': df.columns.nlevels, 'list': [] }
    for i, c in enumerate(df.columns):
        cInfo = { 'label': c, 'value': c, 'dtype': str(df[c].dtype), 'is_numeric': _vp_pd.api.types.is_numeric_dtype(df[c]), 'array': str(df[c].array), 'location': i }
        # value
        if type(c).__name__ == 'list' or type(c).__name__ == 'tuple':
            cInfo['label'] = list(c)
            cInfo['value'] = ["'{}'".format(ci) if type(ci).__name__ == 'str' else str(ci) if type(ci).__name__ == 'Timestamp' else ci for ci in c]
        elif type(c).__name__ == 'str':
            cInfo['value'] = "'{}'".format(c)
        elif type(c).__name__ == 'Timestamp':
            cInfo['value'] = str(c)
        # category - iopub data rate limit issue...
        if str(df[c].dtype) == 'object':
            uniqValues = df[c].dropna().unique()
            if len(uniqValues) <= 20:
                cInfo['category'] = [{ "value": "'{}'".format(u) if type(u) == str else u, "label": u } for u in uniqValues]
            else:
                cInfo['category'] = []
        else:
            cInfo['category'] = []
        colInfo['list'].append(cInfo)
    return colInfo

def _vp_get_multi_columns_list(dfs = []):
    """
    Get Columns List with Detail Information of multiple dataframe
    """
    if len(dfs) <= 0:
        return []

    common_set = set(dfs[0].columns)
    for df in dfs[1:]:
        common_set = common_set & set(df.columns)
    common_columns = list(common_set)

    colList = []
    for i, c in enumerate(common_columns):
        cInfo = { 'label': c, 'value': c, 'dtype': str(dfs[0][c].dtype), 'location': i }
        # value
        if type(c).__name__ == 'str':
            cInfo['value'] = "'{}'".format(c)
        elif type(c).__name__ == 'Timestamp':
            cInfo['value'] = str(c)
        colList.append(cInfo)
    return colList

def _vp_get_column_category(df, col):
    """
    Get Column's Uniq values(Categrical data only, limit 20)
    """
    uniqValues = df[col].dropna().unique()
    category = []
    if len(uniqValues) <= 20:
        category = [{ "value": "{}".format(u) if type(u) == str else u, "label": u } for u in uniqValues]
    return category

def _vp_get_dataframe_as_list(df):
    """
    Get Dataframe as List
    """
    return df.values.tolist()

def _vp_display_dataframe_info(df):
    """
    Get info of dataframe
    """
    # display(df.shape)
    _desc = df.describe().T
    _info = _vp_pd.DataFrame({'Non-Null Count': df.notnull().sum(), 'Dtype': df.dtypes})
    display(_vp_pd.concat([_info, _desc], axis=1).fillna(''))