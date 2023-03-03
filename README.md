# -VERO-Digital-Solutions-Task
The project allow you to send .csv file to a API server, downloads a certain set of resources, 
merges them with the .csv flle, and converts them to a formatted excel file.

To run the scripts open terminal in project folder and execute following commands:

1. Make sure your venv is active (you should see "(venv)" before the project path). If venv is not active execute "venv\Scripts\activate" for Windows or "source ./venv/bin/activate" for Linux

2.Download the project requirements with command "pip install -r requirements.txt"

3. Run the server.py with command "python server.py" (you should see output in terminal like this:)

Serving Flask app 'server'
Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
Running on http://127.0.0.1:5000
Press CTRL+C to quit

4. In new terminal activate venv and run client script with corresponding arguments see examples bellow:
- If you want a colored rows in excel result file use command "python client.py -k kurzname info labelIds -c"
- If you don't want a colored rows use command without -c flag "python client.py -k kurzname info labelIds"
- Arguments passed after -k in examples above are just a sample you can pass what you need in excel result file as columns

5. Result excel file will be saved in project folder with name "vehicles_{current_date_separated_with_underscores}.xlsx" after the command from point 4 is done
- Example for result file name if you run the program on 05.03.2023 will be "vehicles_2023_03_05.xlsx"
