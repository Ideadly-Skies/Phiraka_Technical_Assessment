# Phiraka_Technical_Assessment
code repo for phiraka technical assessment which tests candidate's fundamental full stack web development understanding. There are two subfolders within this repo which denotes the questions to complete for this technical assessment. The specs are kept secret and are not included in this repo to maintain privacy of the content of the actual test.

## Q1 - Fibonnaci Sequence
To invoke the fibonnaci sequence simply open Q1.html on your browser and input the desired amount of Rows and Columns. Don't forget to click submit to display the table with the fibonnaci sequence.

## Q2 - Simple User CRUD Form

**note**: *I used **Supabase** which is an open-sourced backend service that lets you build application using PostgreSQL.* I adhered to the ***Flask Framework** which is an easy-to-use **Python** microframework for building web applications.* You should install all dependencies using `pip` before running this project and create a .env file within the subdirectory Q2 first. The detail on the project structure and the content for the .env file could be found within **Screenshots**.

After installing all of the dependencies, simply invoke the project by running the command `python3 app.py`. This project works as intended as shown in the screenshot. Email me at @obie.kal22@gmail.com if you found any problems when running the script. To migrate the tables first to supabase see the
*how_to_migrate* screenshot; comment the `app.run()` command and uncomment the `db.create()` command.