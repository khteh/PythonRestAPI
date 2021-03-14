import os, re
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_cors import CORS
from .app import create_app
from .models import db, bcrypt
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
    regex = "^([\w\d\-_\s])+$"
    #regex = "[a-zA-Z\d\-_ ]*"
    if re.match(regex, "Hello World"):
        print(f"Match!")
    else:
        print(f"No match!")
    if re.match(regex, "Hello-World"):
        print(f"Match!")
    else:
        print(f"No match!")
    if re.match(regex, "Hello_World"):
        print(f"Match!")
    else:
        print(f"No match!")
    if re.match(regex, "Hello World 123"):
        print(f"Match!")
    else:
        print(f"No match!")		
    if re.match(regex, "Hello World!!!"):
        print(f"Match!")
    else:
        print(f"No match!")		
    if re.match(regex, "Hello World ~!@#$%^&*()_+"):
        print(f"Match!")
    else:
        print(f"No match!")
    emailRegex = "[\w.-]+@[\w.-]+.\w+"
    email = ""
    if re.match(emailRegex, email):
        print(f"Vaild email: {email}")
    else:
        print(f"Invalid email: {email}")	
    email = "a@b.c"
    if re.match(emailRegex, email):
        print(f"Vaild email: {email}")
    else:
        print(f"Invalid email: {email}")
    email = "~!@#$%^&*()_+@b.c"
    if re.match(emailRegex, email):
        print(f"Valid email: {email}")
    else:
        print(f"Invalid email: {email}")
    email = "~!#$%^&*()_+@b.c"
    if re.match(emailRegex, email):
        print(f"Valid email: {email}")
    else:
        print(f"Invalid email: {email}")		
    email = "kokhow.teh@b.c"
    if re.match(emailRegex, email):
        print(f"Valid email: {email}")
    else:
        print(f"Invalid email: {email}")				
    email = "kokhow teh@b.c"
    if re.match(emailRegex, email):
        print(f"Valid email: {email}")
    else:
        print(f"Invalid email: {email}")				
    email = "kok-how_teh@b.c"
    if re.match(emailRegex, email):
        print(f"Valid email: {email}")
    else:
        print(f"Invalid email: {email}")				
    email = "kok-how_teh@b.c.d"
    if re.match(emailRegex, email):
        print(f"Valid email: {email}")
    else:
        print(f"Invalid email: {email}")						
    app.run(HOST, PORT)