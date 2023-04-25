## Usage
To create and populate the database, make sure that all sql files and the format_table.sh file is located in the lion directory of your VM. Then in your terminal run the command:

```
sh ./format_tables.sh
```

To run the application on a web browser, make sure your directory is within the project files and simply execute:

```
export FLASK_APP=app.py
flask run
# then browse to http://127.0.0.1:5000/
```

## Screenshots
To use: Decide wether you would like to see data from municipalities in a county or a specific municipality and hit the sumbit button.

![maingui](https://user-images.githubusercontent.com/94714783/234125462-697da2e5-7721-4b03-94a1-741a2e3f6915.png)
![countGUI](https://user-images.githubusercontent.com/94714783/234125474-48194a40-8e1b-4790-bc8a-8f88aae615c8.png)
![muniGUI](https://user-images.githubusercontent.com/94714783/234125480-869137db-3ebf-458f-97af-19d0ed8e2981.png)

