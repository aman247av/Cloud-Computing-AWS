from flask import Flask, render_template, request
import pymysql
import logging

application = Flask(__name__, template_folder='templates')

# Database configuration
db_host = ''
db_user = ''
db_password = ''
db_name = ''

# Function to create a database connection
def create_db_connection():
    try:
        return pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )
    except Exception as e:
        application.logger.warning(f'Database connection failed due to {e}')
        return None

@application.route("/")
def home():
    return render_template('index.html')

@application.route("/contact")
def contact():
    return render_template('contact.html')

@application.route('/submit', methods=['POST'])
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
            application.logger.info("Data submitted successfully: %s, %s, %s", name, email, message)

            select_query = "SELECT id, name, email, message FROM feedback ORDER BY id DESC"
            cursor.execute(select_query)
            data = cursor.fetchall()

            cursor.close()
            db.close()  # Close the database connection after the operation

            return render_template('display.html', data=data)
        except Exception as e:
            application.logger.error(f'Database error: {e}')
            db.rollback()
            db.close()  # Close the database connection in case of an error
            return 'An error occurred while submitting the data. Please try again later.'
    else:
        return 'Database connection failed.'

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    application.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 5000)))
    
z