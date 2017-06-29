import smtplib
import sys
# to_addr_list  = ['pit0sf0r0w@gmail.com']
# cc_addr_list = ['example@gmail.com']
# subject      = 'Howdy'
# # message      =  sys.argv[0]
# login        = 'pit0sf0r0w@gmail.com'
# password     = 'aa718vsaa718vs'
# from_addr    = ['jpscrap']


def sendemail(from_addr= ['alert@jpscr.ap'],
              to_addr_list=['pit0sf0r0w@gmail.com'],
              cc_addr_list=['bgtube@yahoo.it'],
              subject= 'Cercasi SISTEMISTA',
              message='',
              login='pit0sf0r0w@gmail.com',
              password='aa718vsaa718vs',
              smtpserver='smtp.gmail.com',
              smtpport=587,):  # split smtpserver and -port
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

# sendemail(from_addr    = 'python@RC.net',
#         to_addr_list = ['pit0sf0r0w@gmail.com'],
#         cc_addr_list = ['bgtube@yahoo.it'],
#         subject      = 'Cercasi SISTEMISTA',
#         # message      = sys.argv[1],
#         message      = sys.argv[0],
#         #                 lo cercano lo cercano lo cercano... \n
#         #                 e alla fine hanno trovato  http://www.kitlavoro.it/lavoro/3727022/sistemista-linux-roma-roma-provincia/''',
#         # login        = login,
#         login        = 'pit0sf0r0w@gmail.com',
#         password     = 'aa718vsaa718vs')

