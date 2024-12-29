import mysql.connector

from App.configuration import UserDbConnetion


# Database connection class
class UserDatabase:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def make_connection(self):
        """Establish a connection to the database and enable a dictionary cursor."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            # Enable dictionary cursor
            self.cursor = self.connection.cursor(dictionary=True)
            print("Database connection established.")
        except mysql.connector.Error as e:
            print(f"Connection error: {e}")
            raise e

    def close_connection(self):
        """Close the database connection and cursor."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def get_cursor(self):
        return self.cursor


# User model class
class UserModel:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor(dictionary=True)  # Enable dictionary cursor

    def register_user(self, username, password, role):
        """Registers a new user with the provided username, password, and role."""
        try:
            # Check if the username already exists
            check_sql = "SELECT COUNT(*) AS count FROM users WHERE username = %s"
            self.cursor.execute(check_sql, (username,))
            count = self.cursor.fetchone()['count']

            if count > 0:
                return False, "Username already exists."

            # Insert the user into the database
            sql = '''
            INSERT INTO users(username, password, role)
            VALUES(%s, %s, %s)
            '''
            self.cursor.execute(sql, (username, password, role))
            self.connection.commit()
            print("User registered successfully!")
            return True, "User registered successfully!"
        except Exception as e:
            print(f"Error registering user: {e}")
            return False, f"Error: {e}"

    def get_all_users(self):
        """Fetches all users from the database."""
        try:
            sql = "SELECT id, username, role, created_at FROM users"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()  # Returns a list of dictionaries
            return True, result
        except Exception as e:
            print(f"Error fetching users: {e}")
            return False, f"Error: {e}"

    def authenticate_user(self, username, password, role):
        """Authenticates a user by checking username, password, and role."""
        try:
            sql = '''
            SELECT COUNT(*) AS count FROM users
            WHERE username = %s AND password = %s AND role = %s
            '''
            self.cursor.execute(sql, (username, password, role))
            count = self.cursor.fetchone()['count']

            if count > 0:
                return True, "Login successful."
            else:
                return False, "Invalid username, password, or role."
        except Exception as e:
            print(f"Error while authenticating user: {e}")
            return False, f"Error: {e}"

    def close_connection(self):
        """Close the cursor and database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()


# Utility function to initialize the UserModel
def get_user_model():
    """
    Returns an instance of UserModel with a database connection.
    """
    try:
        # Get database configuration from the configuration module
        db_config = UserDbConnetion()
        user_db = UserDatabase(
            host=db_config.DB_HOSTNAME,
            port=3306,
            user=db_config.DB_USERNAME,
            password=db_config.DB_PASSWORD,
            database=db_config.DB_NAME,
        )
        user_db.make_connection()
        return True, UserModel(user_db.connection)
    except Exception as e:
        print(f"Error initializing user model: {e}")
        return False, f"Error: {e}"
