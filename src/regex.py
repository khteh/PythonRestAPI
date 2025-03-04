import logging, os, re
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')	

numberRegex = "^(\d)+$"
print("numberRegex: Match!") if re.match(numberRegex, "123") else print("numberRegex: No match!") # Should match
print("numberRegex: Match!") if re.match(numberRegex, "Hello World") else print("numberRegex: No match!") # Should NOT match	
print("numberRegex: Match!") if re.match(numberRegex, "123 ") else print("numberRegex: No match!") # Should NOT match	
print("numberRegex: Match!") if re.match(numberRegex, " 123") else print("numberRegex: No match!") # Should NOT match	
print("numberRegex: Match!") if re.match(numberRegex, "123.") else print("numberRegex: No match!") # Should NOT match	
print("numberRegex: Match!") if re.match(numberRegex, "123-") else print("numberRegex: No match!") # Should NOT match	

regex = "^([\w\d\-_\s])+$"
print("regex: Match!") if re.match(regex, "Hello World") else print("regex: No match!") # Should match
print("regex: Match!") if re.match(regex, "Hello-World") else print("regex: No match!") # Should match
print("regex: Match!") if re.match(regex, "Hello_World") else print("regex: No match!") # Should match
print("regex: Match!") if re.match(regex, "Hello World 123") else print("regex: No match!") # Should match
print("regex: Match!") if re.match(regex, "Hello World!!!") else print("regex: No match!") # Should NOT match
print("regex: Match!") if re.match(regex, "Hello World ~!@#$%^&*()_+") else print("regex: No match!") # Should NOT match

regexMax = "^([\w\d\-_\s]){5,10}$"
print("regexMax: Match!") if re.match(regexMax, "Hello-Worl") else print("regexMax: No match!") # Should match
print("regexMax: Match!") if re.match(regexMax, "Hello_Worl") else print("regexMax: No match!") # Should match
print("regexMax: Match!") if re.match(regexMax, "HelloWorl8") else print("regexMax: No match!") # Should match
print("regexMax: Match!") if re.match(regexMax, "Helo") else print("regexMax: No match!") # Should NOT match
print("regexMax: Match!") if re.match(regexMax, "HelloWorl89") else print("regexMax: No match!") # Should NOT match
print("regexMax: Match!") if re.match(regexMax, "Hello World ~!@#$%^&*()_+") else print("regexMax: No match!") # Should NOT match

lettersRegex = "^([a-zA-Z]){0,10}$"
print("lettersRegex: Match!") if re.match(lettersRegex, "HelloWorld") else print("lettersRegex: No match!") # Should match
print("lettersRegex: Match!") if re.match(lettersRegex, "HelloWorl0") else print("lettersRegex: No match!") # Should NOT match due to number
print("lettersRegex: Match!") if re.match(lettersRegex, "Hello Worl") else print("lettersRegex: No match!") # Should NOT match due to space
print("lettersRegex: Match!") if re.match(lettersRegex, "Hello World") else print("lettersRegex: No match!") # Should NOT match due to length

emailRegex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
email = ""
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = ".@."
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "-@-"
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "a@"
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "a@b"
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "ab@de"
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "abc@def"
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
email = "123@456"
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "123@ntu.edu.sg"
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "funcoolgeek@gmail.com"
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "teh_k_h@gmail.com"
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "teh-k.h@gmail.com"
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "teh-k.h@gmail.co.uk"
print(f"Valid email: {email}") if re.match(emailRegex, email) else print(f"Invalid email: {email}")
email = "teh k h@gmail.com"
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
#app.run(HOST, PORT)
