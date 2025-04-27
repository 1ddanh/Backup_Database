import os
import shutil
import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def backup_database():
    source_dir = './'  # Directory containing the database files
    backup_dir = './backup/'  # Directory to store the backup files

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    try:
        for file_name in os.listdir(source_dir):
            if file_name.endswith('.sql') or file_name.endswith('.sqlite3'):
                full_file_name = os.path.join(source_dir, file_name)
                if os.path.isfile(full_file_name):
                    shutil.copy(full_file_name, backup_dir)
        send_email("Backup Successful", "The database backup was successful.")
    except Exception as e:
        send_email("Backup Failed", f"The database backup failed: {e}")

# Schedule the backup to run at midnight every day
schedule.every().day.at("00:00").do(backup_database)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait for one minute``