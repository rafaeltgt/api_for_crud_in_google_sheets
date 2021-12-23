from services.google_sheet_conn import GoogleSheetConnection
from fastapi import APIRouter, HTTPException

post_router = APIRouter()

@post_router.post("/{sheet_id_input}/{worksheet_name}", status_code=201)
def post_api(
    sheet_id_input: str,
    worksheet_name: str,
    records: list
):

    ss = GoogleSheetConnection(sheet_id_input)
    df = ss.read_sheet(worksheet_name)
    keys = list(records[0].keys())

    indexes_with_columns_erros = []

    for i, record in enumerate(records):
        keys = list(record.keys())

        if not all([x in df.columns for x in keys]):
            indexes_with_columns_erros.append(i)
    
    if len(indexes_with_columns_erros) > 0:
        raise HTTPException(status_code=400, detail=f"Records with erros in columns names: {indexes_with_columns_erros}")
    
    original_len_df = len(df)

    df = df.append(records, ignore_index=True)

    df_inserted = df[original_len_df:]

    ss.write_on_sheet(worksheet_name, df_inserted)

    return {"status": "success", "message": "records inserted"}