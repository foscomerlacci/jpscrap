import smtplib

def sendemail(from_addr,
              to_addr_list,
              cc_addr_list,
              subject,
              message,
              login,
              password,
              smtpserver='smtp.gmail.com', smtpport=587):  # split smtpserver and -port
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver, smtpport)  # use both smtpserver  and -port
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

sendemail(from_addr    = 'python@RC.net',
        to_addr_list = ['pit0sf0r0w@gmail.com'],
        cc_addr_list = ['example@gmail.com'],
        subject      = 'Howdy',
        message      = 'Hello!',
        login        = 'pit0sf0r0w@gmail.com',
        password     = 'aa718vsaa718vs')

