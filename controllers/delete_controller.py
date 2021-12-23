from services.google_sheet_conn import GoogleSheetConnection
from fastapi import APIRouter, HTTPException

delete_router = APIRouter()

@delete_router.delete("/{sheet_id_input}/{worksheet_name}")
def delete_api(
    sheet_id_input: str,
    worksheet_name: str,
    filter_key: str,
    filter_value: str
):

    ss = GoogleSheetConnection(sheet_id_input)
    df = ss.read_sheet(worksheet_name)

    df = df.loc[df[filter_key] == filter_value]

    if len(df) == 0:
        raise HTTPException(status_code=404, detail="No records found")

    indexes_to_delete = list(df.index)

    ss.delete_rows(worksheet_name, indexes_to_delete)
    
    return {"status": "success", "message": "records deleted"}