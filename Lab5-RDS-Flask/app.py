from flask import Flask, render_template, request
import pymysql
import logging

app = Flask(__name__,template_folder='templates')

# Database configuration
db_host = ''
db_user = ''
db_password = ''
db_name = ''

# Function to create a database connection
def create_db_connection():
    try:
        db = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )
        return db
    except Exception as e:
        app.logger.warning(f'Database connection failed due to {e}')
        return None

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    db = create_db_connection()

    if db:
        try:
            cursor = db.cursor()
            insert_query = "INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (name, email, message))
            db.commit()
            cursor.close()
            db.close()  # Close the database connection after use
            app.logger.info("Data submitted successfully: %s, %s, %s", name, email, message)
            return render_template('success.html')
        except Exception as e:
            app.logger.error(f'Database error: {e}')
            db.rollback()
            db.close()  # Close the database connection on error
            return 'An error occurred while submitting the data. Please try again later.'

def create_feedback_table():
    db = create_db_connection()

    if db:
        try:
            cursor = db.cursor()
            create_table_query = """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    message VARCHAR(255) NOT NULL
                )
            """
            cursor.execute(create_table_query)
            cursor.close()
            db.close()  # Close the database connection after use
            app.logger.info("Table 'feedback' created successfully.")
        except Exception as e:
            app.logger.error(f'Database error: {e}')
            db.rollback()
            db.close()  # Close the database connection on error

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    create_feedback_table()
    app.run(host='0.0.0.0', port=80)
