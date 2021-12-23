
# A Python API to perform CRUD operations on your google spreadsheets

## Requirements

### 1. Download `client_secret.json` file with your credentials to Google Drive Api
Instead of making your google spreadsheet open to anyone like other services, this api allows only you to read and write in your document. 

First, you need to create an account in Google Cloud and then create project and request access to Google Drive API. 

Follow instructions in [this video](https://www.youtube.com/watch?v=vISRn5qFrkM) to download a json file name `client_secret.json` with your credentials. 

Paste the `client_secret.json` file in the main folder. 

In this file, grab the email after `client_email` key and share your spreadsheet with it with **Editor** permission

### 2. Python 3

### 3. Install these Python Modules
- fastapi
- uvicorn
- pydantic
- gspread
- gspread_dataframe
- oauth2client
- pandas

Run this to install all dependencies
`pip install -r requirements.txt`

## Running the server

To start the webserver, run this command inside the source path
`uvicorn main:app --reload`

When running in your machine, it starts a local server in localhost:8000 


## Operations
When running the server, you can view the api docs in {server_name}/docs
e g. **localhost:8000/docs** 

## GET (Read records)
Path parameters: `URL/{sheet_id}/{worksheet_name}`

**sheet_id:** (required) the id of the spreadsheet (it is in the url of the spreadsheet)

**worksheet_name:** (required) the name of the worksheet you are reading

Query paramenters: `URL/{sheet_id}/{worksheet_name}?query={query}&limit={limit}&offset={offset}`

**query:** (optional) to perform simple filters in your GET request

e g. 
  `name == "steve"`

  `country != "usa"`

  `age > 40`

  AND: `name == "steve" & age < 40`

  OR `name == "steve" | age < 40`

  IN `year in [2015, 2020]`

**limit:** (optional) limits the number of records. Default = 50

**offset:** (optional) offset the first shown record. Defatul = 0


## POST (Insert Records)
Path parameters: `URL/{sheet_id}/{worksheet_name}`

**sheet_id:** (required) the id of the spreadsheet (it is in the url of the spreadsheet)

**worksheet_name:** (required) the name of the worksheet you are reading

Request body:
array with records in format `{key1:value1, key2: value2}`. The keys must match the columns names of the worksheet
e g. 

To insert 2 records

`[
{"first_name":"John", 
"last_name":"Doe", 
"age": 35},
{"first_name":"Jane", 
"last_name":"Doe", 
"age": 30},
]`

## Patch (Update Records)
Path parameters: `URL/{sheet_id}/{worksheet_name}`

**sheet_id:** (required) the id of the spreadsheet (it is in the url of the spreadsheet)

**worksheet_name:** (required) the name of the worksheet you are reading

Request body:

    {
    "filter_key":"string",
    "filter_value":"string",
    "to_update":
	    [
		    {"item_key":"string", 
		    "item_value":"string"
		    },
		    {"item_key":"string", 
		    "item_value":"string"
		    }
	    ]
    }
    
 Example:
 This will update the line where `id == 123` to `name -> Jonny` and `email -> jonny@example.com`
 

    {
    "filter_key":"id",
    "filter_value":"123",
    "to_update":
	    [
		    {"item_key":"name", 
		    "item_value":"Jonny"
		    },
		    {"item_key":"email", 
		    "item_value":"jonny@example.com"
		    }
	    ]
    }

*WARNING: if the filter returns more than 1 line, all the lines filtered will be updated*

## Delete (Delete records)
Path parameters: `URL/{sheet_id}/{worksheet_name}`

**sheet_id:** (required) the id of the spreadsheet (it is in the url of the spreadsheet)

**worksheet_name:** (required) the name of the worksheet you are reading

Query paramenters: `URL/{sheet_id}/{worksheet_name}?filter_key={filter_key}&filter_value={filter_value}`

**filter_key:** (required) name of the column you want to filter 

**filter_value:** (required) value you want to filter

Example: To delete all lines with `id==123`:

**filter_key:** "id"

**filter_value:** "123"

*WARNING: if the filter returns more than 1 line, all the lines filtered will be deleted*
