import speech_recognition as sr
import smtplib
import imaplib
import email
import pyttsx3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Speech recognition setup
recognizer = sr.Recognizer()

# Gmail credentials
email_address = "YOUREMAIL@gmail.com"
password = "PASSKEY"

# Text-to-speech setup
engine = pyttsx3.init()

def listen_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        speak_text("Listening")
        print("Listening...")
        
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            speak_text("Could not understand audio.")
            print("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return ""

def send_email():
    speak_text("Say the subject of the email:")
    print("Say the subject of the email:")
    subject = listen_command()

    speak_text("Say the body of the email")
    
    print("Say the body of the email:")
    
    body = listen_command()

    speak_text("Say the recipient's email address:")
    print("Say the recipient's email address:")
    
    recipient_email = listen_command().replace(" ", "").lower()  # Remove spaces and convert to lowercase

    # Construct the email
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient_email + "@gmail.com"
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    print("\nSubject:", subject)
    print("Body:", body)
    print("Recipient:", recipient_email)

    # Confirm before sending
    speak_text("\nDo you want to send this email? Say 'yes yes' to confirm.")
    print("\nDo you want to send this email? Say 'yes yes' to confirm.")
    confirmation = listen_command()
    print("Confirmation:", confirmation)  # Debug print
    if confirmation == "yes yes":
        try:
            # Send the email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_address, password)
            server.sendmail(email_address, recipient_email + "@gmail.com", msg.as_string())
            server.quit()
            print("Email sent successfully.")
            speak_text("Email sent successfully.")
            speak_text("THANK YOU.")
        except smtplib.SMTPAuthenticationError:
            print("Failed to authenticate. Please check your email and password.")
        except Exception as e:
            print("An error occurred while sending email:", str(e))
    else:
        speak_text("Email not sent. Restarting process.")

        print("Email not sent. Restarting process.")


def get_email_body(msg):
    try:
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    return body
        else:
            body = msg.get_payload(decode=True).decode()
            return body
    except Exception as e:
        
        return "Error: Unable to retrieve email body"

def read_emails():
    # Read the last 3 emails
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_address, password)
        mail.select("inbox")
        result, data = mail.search(None, "ALL")
        ids = data[0].split()
        ids = ids[::-1][:3]  # Fetch the latest 3 emails
        for i in ids:
            result, email_data = mail.fetch(i, "(RFC822)")
            raw_email = email_data[0][1]
            msg = email.message_from_bytes(raw_email)
            sender = msg["From"]
            subject = msg["Subject"]
            body = get_email_body(msg)
            print("Sender:", sender)
            print("Subject:", subject)
            
            print("=" * 50)
            # Read the email aloud
            speak_text(f"Sender: {sender}")
            speak_text(f"Subject: {subject}")
           
            speak_text("=" * 1)
    except Exception as e:
        print("An error occurred:", str(e))


def speak_text(text):
    engine.say(text)
    engine.setProperty('rate',130)
    engine.runAndWait()

def voice_interface():
    print("---------------------------------------------------------------------------------------------------------------------------------------")
    speak_text("This is a mini project of MCA 3rd semester Titled 'Voice-based Email for Blind', done by Apoorva SM and Rakshitha Divakar.")
    print("This is a mini project of MCA 3rd semester titled 'Voice-based Email for Blind', done by Apoorva SM and Rakshitha Divakar")
    speak_text("Here is a list of things it can do:")
    print("                                       Here is a list of things it can do:")
    speak_text("1. Write a mail")
    print("                                            1. Write a mail")
    speak_text("2. Read emails")
    print("                                            2. Read emails")
    print("----------------------------------------------------------------------------------------------------------------------------------------")
    print("Welcome to Voice-based Email System")
    speak_text("Welcome to Voice-based Email System")
    speak_text("Do you want to read emails or write a new email?")
    print("Do you want to read emails or write a new email?")
    response = listen_command()
    if "read" in response:
        read_emails()
    elif "write" in response or "new" in response:
        send_email()
    else:
        print("Sorry, I didn't understand your response.")

if __name__ == "__main__":
    voice_interface()
