from flask import Flask, render_template, request, redirect, g
import pymysql
import logging

app = Flask(__name__,template_folder='templates')

# Database configuration
db_host = ''
db_user = ''
db_password = ''
db_name = ''

# Function to create a database connection
def get_db():
    if 'db' not in g:
        try:
            g.db = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                port=3306
            )
        except Exception as e:
            app.logger.warning(f'Database connection failed due to {e}')
            g.db = None
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

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

    # name="Aman Verma"
    # email="aman@gmail.com"
    # message="Hi Aman!"

    db = get_db()

    if db:
        try:
            cursor = db.cursor()
            insert_query = "INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (name, email, message))
            db.commit()
            cursor.close()
            app.logger.info("Data submitted successfully: %s, %s, %s", name, email, message)
            return render_template('success.html')
        except Exception as e:
            app.logger.error(f'Database error: {e}')
            db.rollback()
            return 'An error occurred while submitting the data. Please try again later.'

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    app.run(host='0.0.0.0',port=8080)
