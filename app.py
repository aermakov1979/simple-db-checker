from flask import Flask
import psycopg2, boto3

app = Flask(__name__)

# Retrieve the database connection parameters from Parameter Store
def get_db_parameters():
    try:
        ssm = boto3.client("ssm", region_name='us-east-1')
        db_host = ssm.get_parameter(Name="/testdb/host")["Parameter"]["Value"]
        db_name = ssm.get_parameter(Name="/testdb/name")["Parameter"]["Value"]
        db_user = ssm.get_parameter(Name="/testdb/username")["Parameter"]["Value"]
        db_password = ssm.get_parameter(Name="/testdb/password", WithDecryption=True)["Parameter"]["Value"]
    except:
        db_host = "NoValueReceived"
        db_name = "NoValueReceived"
        db_user = "NoValueReceived"
        db_password = "NoValueReceived"
    return db_host, db_name, db_user, db_password

# Connect to the database
def check_db_connection():
    db_host, db_name, db_user, db_password = get_db_parameters()
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port='5432'
        )
        return f"<h2><b><p style=\"color:green;\"> Success!!! Connected to DB {db_host}! DBName = {db_name}, DBUser = {db_user}, DBPassword = {db_password}.</p></b></h2>"
    except:
        return f"<h2><b><p style=\"color:red;\"> Failed!!! No connection to DB {db_host}! DBName = {db_name}, DBUser = {db_user}, DBPassword = {db_password}. Check parameters! </p></b></h2>"

@app.route("/")
def index():
    return check_db_connection()

if __name__ == "__main__":
    app.run(debug=True)
