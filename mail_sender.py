import smtplib

# tutto questo dovrebbe essere nascosto
def sendemail(from_addr= 'geipiscrap@gmail.com',
              to_addr_list=['pit0sf0r0w@gmail.com'],
              cc_addr_list=['bgtube@yahoo.it'],
              subject= 'Cercasi SISTEMISTA',
              message='thtf',
              login='geipiscrap@gmail.com',
              password='aa718vsaa718vs',
              smtpserver='smtp.gmail.com',
              smtpport=587,):  # split smtpserver and -port
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver, smtpport)  # use both smtpserver  and -port
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login,password)
    server.sendmail(from_addr, to_addr_list, message.encode('utf-8'))
    # problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

