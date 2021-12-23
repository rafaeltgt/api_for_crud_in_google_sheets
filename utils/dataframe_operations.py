def limit_df(df, n):
    return df.head(n)

def offset_df(df, n):
    return df.tail(len(df) - n)

def get_records(df, limit=None, offset=None, query=None):
    df = convert_numerics(df)

    if query:
        df = df.query(query)
    if offset:
        df = offset_df(df, offset)
    if limit:
        df = limit_df(df, limit)
    return df

def convert_numerics(df_in):

    columns = df_in.columns

    for column in columns:
        if df_in[column].dtype == object:

            is_int = all([isint(x) for x in df_in[column]])
            if is_int:
                df_in[column] = df_in[column].astype(int)
            else:
                is_float = all([isfloat(x) for x in df_in[column]])
                if is_float:
                    df_in[column] = df_in[column].astype(float)

 
    return df_in

def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_row_by_index(index):
    return index+2

