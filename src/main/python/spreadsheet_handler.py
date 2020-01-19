import os
import sys
import pickle
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from drive_handler import DriveHandler
from fbs_runtime.application_context.PyQt5 import ApplicationContext


# TODO: Understand what does this "type" argument means
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


# TODO: Undestand metaclass implementation
class SpreadsheetHandler(metaclass=Singleton):
    def __init__(self, credentials=None, file_name=None, spreadsheet_id=None):
        self.credentials = credentials
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.spreadsheet_id = spreadsheet_id
        self.file_name = file_name

    def create_spreadsheet(self):

        drv_hdl = DriveHandler(self.credentials)

        # Check for existing spreadsheet:
        try:
            spreadsheet_id = drv_hdl.get_spreadsheet_id(self.file_name)
            self.spreadsheet_id = spreadsheet_id
        except FileNotFoundError:
            spreadsheet = {
                "properties": {
                    "title": self.file_name
                },
                "sheets": [
                    {
                        "properties": {
                            "sheetId": 1,
                            "title": "Expenses"
                        }
                    },
                    {
                        "properties": {
                            "sheetId": 2,
                            "title": "Income"
                        }
                    },
                    {
                        "properties": {
                            "sheetId": 3,
                            "title": "Summary"
                        }
                    },
                    {
                        "properties": {
                            "sheetId": 4,
                            "title": "Resources",
                            "hidden": True
                        }
                    }
                ]
            }
            spreadsheet = self.service.spreadsheets().create(body=spreadsheet,
                                                             fields="spreadsheetId").execute()

            self.spreadsheet_id = spreadsheet.get('spreadsheetId')
            try:
                self.format_spreadsheet()
            # TODO: remove this try except block
            except:
                self.delete_spreadsheet()

        finally:
            return self.spreadsheet_id

    def write_data(self, data, range, value_input_option='USER_ENTERED'):
        body = {
            'values': data
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=range,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

    def append_data(self, data, range='Sheet1',
                    value_input_option='USER_ENTERED'):
        body = {
            'values': data
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id, range=range,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells appended.'.format(result
                                           .get('updates')
                                           .get('updatedCells')))
        self.sort_by_date()

    def update_spreadsheet(self, json_file):
        with open(json_file, encoding='utf-8') as json_file:
            body = json.load(json_file)

        self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body=body).execute()

    def format_spreadsheet(self):
        appctx = ApplicationContext()
        self.update_spreadsheet(appctx.get_resource("spreadsheet_formatting.json"))

    def sort_by_date(self):
        appctx = ApplicationContext()
        self.update_spreadsheet(appctx.get_resource("sort_by_date.json"))

    def delete_spreadsheet(self):
        drv_hdl = DriveHandler(self.credentials)
        drv_hdl.service.files().delete(fileId=self.spreadsheet_id).execute()

    def rename_spreadsheet(self, new_name):
        drv_hdl = DriveHandler(self.credentials)

        file = {'name': new_name}
   
        drv_hdl.service.files().update(fileId=self.spreadsheet_id,
                                      body=file,
                                      fields='name').execute()