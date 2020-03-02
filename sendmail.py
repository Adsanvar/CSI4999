import smtplib, sys

try:
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()
    s.login("smartlock.vertification.noreply@gmail.com", "TESt123!")
            
    #s.sendmail("pitest873@gmail.com", sys.argv[1], sys.argv[2])
    #msg = 'http://localhost:5000/verification/adrian/'
    msg_1 = '\"{}\"'.format(sys.argv[2])
    msg = "WELCOME TO SMART LOCK"
    s.sendmail("smartlock.vertification.noreply@gmail.com", sys.argv[1], msg)
    s.quit()
except:
    raise

