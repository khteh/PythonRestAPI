import os, re, logging
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_cors import CORS
from .app import create_app
from .models import db, bcrypt
from .common.Authentication import oidc
load_dotenv()
if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080
    env_name = os.getenv('ENV', "Please set ENV in .env")
    print(f"env_name: {env_name}, __name__: {__name__}, {HOST}:{PORT}")
	# for v in re.findall(r'0x[0-9a-fA-F]+|\d+', value):
	#    print(f"value: {int(v, 0)}")
    app = create_app(env_name)
    CORS(app, supports_credentials = True)
    csrf = CSRFProtect(app)
    bcrypt.init_app(app)
    db.init_app(app)
    oidc.init_app(app)
    numberRegex = "^(\d)+$"
    print("Match!") if re.match(numberRegex, "123") else print("No match!") # Should match
    print("Match!") if re.match(numberRegex, "Hello World") else print("No match!") # Should NOT match	
    print("Match!") if re.match(numberRegex, "123 ") else print("No match!") # Should NOT match	
    print("Match!") if re.match(numberRegex, " 123") else print("No match!") # Should NOT match	
    print("Match!") if re.match(numberRegex, "123.") else print("No match!") # Should NOT match	
    print("Match!") if re.match(numberRegex, "123-") else print("No match!") # Should NOT match	
    regex = "^([\w\d\-_\s])+$"
    print("Match!") if re.match(regex, "Hello World") else print("No match!") # Should match
    print("Match!") if re.match(regex, "Hello-World") else print("No match!") # Should match
    print("Match!") if re.match(regex, "Hello_World") else print("No match!") # Should match
    print("Match!") if re.match(regex, "Hello World 123") else print("No match!") # Should match
    print("Match!") if re.match(regex, "Hello World!!!") else print("No match!") # Should NOT match
    print("Match!") if re.match(regex, "Hello World ~!@#$%^&*()_+") else print("No match!") # Should NOT match
    emailRegex = "[\w.-]+@[\w.-]+.\w+"
    email = ""
    print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
    email = "a@b.c"
    print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
    email = "~!@#$%^&*()_+@b.c"
    print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
    email = "~!#$%^&*()_+@b.c"
    print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
    email = "kokhow.teh@b.c"
    print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
    email = "kokhow teh@b.c"
    print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
    email = "kok-how_teh@b.c"
    print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
    email = "kok-how_teh@b.c.d"
    print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
    regex = "^(\d{8,10})$"
    print("Match!") if re.match(regex, "1234567") else print("No match!") # Should NOT match
    print("Match!") if re.match(regex, "12345678") else print("No match!")
    print("Match!") if re.match(regex, "123456789") else print("No match!")
    print("Match!") if re.match(regex, "1234567890") else print("No match!")
    print("Match!") if re.match(regex, "12345678901") else print("No match!") # Should NOT match
	# 91234567, +123-1234567890
    phoneRegex = "^(\+\d{1,3}\-?)*(\d{8,10})$"
    phone = "1234567" # Invalid due to length < 8
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")
    phone = "12345678"
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")
    phone = "1234567890"
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")
    phone = "12345678901" # Invalid due to length > 10
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")
    phone = "+6512345678"
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")	
    phone = "+65-12345678"
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")		
    phone = "+ab-91234567"
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")			
    phone = "+65 91234567" # Invalid due to space
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")
    phone = "+123-1234567" # Invalid due to length < 8
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")					
    phone = "+123-12345678"
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")
    phone = "+123-1234567890"
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")	
    phone = "+123-12345678901" # Invalid due to length > 10
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")		
    phone = "+-1234567890" # Invalid due to country code < 1
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")	
    phone = "-1234567890" # Invalid due to country code < 1
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")	
    phone = "+1234-1234567890" # Invalid due to country code > 3
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")	
    phone = "+123-HelloWorld"
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")		
    phone = "+123-"
    print(f"Valid phone: {phone}") if re.match(phoneRegex, phone) else print(f"Invalid phone: {phone}")			
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')	
    app.run(HOST, PORT)
