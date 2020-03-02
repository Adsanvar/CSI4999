import smtplib, sys

try:
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()
    s.login("pitest873@gmail.com", "TESt123!")
            
    s.sendmail("pitest873@gmail.com", sys.argv[1], sys.argv[2])
    s.quit()
except:
    raise

