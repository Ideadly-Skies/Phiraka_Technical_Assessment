import os
from supabase import create_client, Client # type: ignore
from dotenv import load_dotenv             # type: ignore
import psycopg2                            # type: ignore

# bcrypt to encrypt the password
import bcrypt                              # type: ignore 

# load .env file when connecting to the DB 
load_dotenv()

class DB:
    def __init__(self):
        """
        Initialize the database connection. All of the code here aren't GPT Generated. Visit this documentation to learn
        more about how to connect to the postgresql db using python https://supabase.com/docs/reference/python/update. I also
        provided the code to create the tbl_user so that the end user just need to execute the `Invoke_DB` 
        script to both create the table and connect to the db simultaneously. :)
        """
        # derive url and key from .env to connect to db
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

        # output successful connection message
        print("DB Connected Successfully!")

    # create table user
    def create_table(self):
        """
        create `tbl_user` in supabase postgreSQL.
        """
        try:
            # create tbl_user table using psycopg2
            # Get credentials from environment variables
            DATABASE_URL = os.getenv("SUPABASE_DB_URL")

            # Connect to the database
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()

            # Drop the table if it exists query
            drop_table_sql = "DROP TABLE IF EXISTS tbl_user CASCADE;"

            # SQL command to create the table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS tbl_user (
                id SERIAL PRIMARY KEY,
                username VARCHAR(128) NOT NULL,
                password VARCHAR(60) NOT NULL,
                CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            # Execute SQL statements
            cur.execute(drop_table_sql)
            cur.execute(create_table_sql)
            conn.commit()

            print("Table 'tbl_user' created successfully!")

            # close connection
            cur.close()
            conn.close()

        except Exception as e:
            print("Error creating table: %s" %(e)) 

    # instance method to login into system 
    def login(self, username, password):
        """verify the username and password against the databases."""
        # Fetch the user by username
        response = self.supabase.table("tbl_user").select("*").eq("username", username).execute()
        
        if response.data:
            user = response.data[0]
            # Compare the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                return True
            else:
                return False
        else:
            return False

    # CRUD Operations for users
    def insert_user(self, username, password):
        """Insert a new user into the tbl_user table."""
        # Hash the password with SHA-256 and truncate it to 54 characters
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Decode the hashed password to store it as a string in the database
        decoded_password = hashed_password.decode('utf-8')

        response = self.supabase.table("tbl_user").insert({
            "username": username,
            "password": decoded_password 
        }).execute()
        
        return response.data
    
    # Select all users
    def get_all_users(self):
        """Retrieve all users from tbl_user."""
        response = self.supabase.table("tbl_user").select("*").execute()
        return response.data 
    
    # Select a user by ID
    def get_user_by_id(self, user_id):
        """Retrieve a single user by ID."""
        response = self.supabase.table("tbl_user").select("*").eq("id", user_id).execute()
        return response.data 

    # Update user
    def update_user(self, user_id, new_username, new_password):
        """Update username and password of an existing user."""
        # Hash the new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        # Decode the hashed password to store it as a string in the database
        decoded_password = hashed_password.decode('utf-8')

        response = self.supabase.table("tbl_user").update({
            "username": new_username,
            "password": decoded_password 
        }).eq("id", user_id).execute()
        return response.data
    
    # Delete user
    def delete_user(self, user_id):
        """Delete a user from tbl_user by ID."""
        response = self.supabase.table("tbl_user").delete().eq("id", user_id).execute()
        return response.data