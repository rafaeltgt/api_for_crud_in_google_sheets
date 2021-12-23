import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from gspread_dataframe import set_with_dataframe


class GoogleSheetConnection:
    def __init__(self, sheet_id):
        jsonname = "./client_secret.json"
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(jsonname, scope)
        client = gspread.authorize(creds)
        self.spreadsheet = client.open_by_key(sheet_id)

    def read_sheet(self, worksheet_name):

        worksheet = self.spreadsheet.worksheet(worksheet_name)
        values = worksheet.get_all_values()
        header = values.pop(0)
        df = pd.DataFrame(values, columns=header)
        if len(values):
            df = self.map_bool(df)
        return df

    def read_range(self, worksheet_name, the_range):

        worksheet = self.spreadsheet.worksheet(worksheet_name)
        values = worksheet.range(the_range)
        coluna_inicial = int(values[0].col)
        coluna_final = int(values[-1].col)

        data = {}
        for y in range(coluna_inicial, coluna_final + 1):
            valores = [x.value for x in values if x.col == y]
            header = valores.pop(0)
            data[header] = valores
        df = pd.DataFrame(data)
        df = self.map_bool(df)
        return df

    def map_bool(self, df_inside):

        mapa = {"FALSE": False, "TRUE": True}

        colunas = df_inside.columns
        for coluna in colunas:
            if df_inside[coluna][0] in list(mapa.keys()):
                df_inside[coluna] = df_inside[coluna].map(mapa)
        return df_inside

    def write_on_sheet(self, worksheet_name, df):

        ws = self.spreadsheet.worksheet(worksheet_name)
        insert_line = len(ws.col_values(1)) + 1
        set_with_dataframe(ws, df, row=insert_line, col=1, include_index=False, include_column_header=False)

    def write_on_sheet_loc(self, worksheet_name, df, row, col):

        ws = self.spreadsheet.worksheet(worksheet_name)
        set_with_dataframe(ws, df, row=row, col=col, include_index=False, include_column_header=False)
    
    def delete_rows(self, worksheet_name, rows_to_delete):

        ws = self.spreadsheet.worksheet(worksheet_name)
        for row in rows_to_delete:
            ws.delete_row(row)
        
