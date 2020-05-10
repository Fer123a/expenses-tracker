This project intends to develop an integrated platform in Android (TODO), Ubuntu and Windows to track and categorize expenses and incomes.

We use Google Sheets to store the incomes and expenses, the communication is provided by its Python API.

For now, the application is implemented only for Windows and Ubuntu.
Do not install the application on the "Programs File" folder.
In order to use it, after installing the released version, or downloading the source code, you must enable the Google Sheets API following the instructions in the topic "Step 1: Turn on the Google Sheets API" in https://developers.google.com/sheets/api/quickstart/python. After enabling it, click on "DOWNLOAD CLIENT CONFIGURATION" to download a "credential.json" file, copy it and paste in the application installation folder or in src/main/python.

After doing so, you must enable the Google Drive API following the instructions in https://developers.google.com/drive/api/v3/enable-drive-api.
