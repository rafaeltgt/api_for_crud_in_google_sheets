from services.google_sheet_conn import GoogleSheetConnection
from utils.dataframe_operations import get_records
from fastapi import APIRouter

get_router = APIRouter()

@get_router.get("/{sheet_id_input}/{worksheet_name}")
def get_api(
    sheet_id_input: str,
    worksheet_name: str,
    query: str = None,
    limit: int = 50,
    offset: int = 0,
):
    
    ss = GoogleSheetConnection(sheet_id_input)
    df = ss.read_sheet(worksheet_name)
    total = len(df)
    df = get_records(df, limit, offset, query)
    records = df.to_dict(orient="records")

    response = {"paging": {"total":total, "count":len(records), "limit": limit, "offset": offset}, "result": records}

    return response
