from services.google_sheet_conn import GoogleSheetConnection
from utils.dataframe_operations import get_row_by_index
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

class PatchModifier(BaseModel):
    item_key: str
    item_value: str

class PatchRequest(BaseModel):
    filter_key: str
    filter_value: str
    to_update: List[PatchModifier]

patch_router = APIRouter()


@patch_router.patch("/{sheet_id_input}/{worksheet_name}", status_code=201)
def patch_api(
    sheet_id_input:str,
    workesheet_name:str,
    patch_request: PatchRequest  
):
    ss = GoogleSheetConnection(sheet_id_input)
    df = ss.read_sheet(workesheet_name)

    df = df.loc[df[patch_request.filter_key] == patch_request.filter_value]

    if len(df) == 0:
        raise HTTPException(status_code=404, detail="No records found")
    
    columns_to_update = [x.item_key for x in patch_request.to_update]

    if not all([x in df.columns for x in columns_to_update]):
        raise HTTPException(status_code=400, detail=f"At least a column do not exists in this worksheet. Columns sent in the request: {columns_to_update}")


    for idx in df.index:
        for modifier in patch_request.to_update:
            df.loc[idx, modifier.item_key] = modifier.item_value

        ss.write_on_sheet_loc(workesheet_name, df.loc[[idx]], get_row_by_index(idx), 1)


    return {"status": "success", "message": "records updated"}