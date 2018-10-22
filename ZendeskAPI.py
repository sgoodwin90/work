#get important fields from zendesk for customer care excel reports based on ticket creation date (includes pagination)

import requests
import csv
from collections import defaultdict
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
from datetime import date, datetime, timedelta
 

#grab list of all ticket ids filtered on created_at based on user input 

#date_filter = input('Enter desired date period for all tickets after certain date(format: yyyy-mm-dd):')

#pull tickets for previous 7 days from todays date
today = datetime.now().date()
date_filter = today - timedelta(days=8)


startTime = datetime.now()

search_string = 'type:ticket created>' + str(date_filter)

search_url = 'https://anki.zendesk.com/api/v2/search.json?query=' + search_string
user = 'sgoodwin@anki.com' + '/token'
pwd = ''

ticket_list = []

print('gathering ticket list...')

while search_url:
    search_response = requests.get(search_url, auth=(user, pwd))

    search_data = search_response.json()
  

    for field in search_data['results']:
        for k,v in field.items():
            if k == 'id':
                ticket_list.append(str(v))
    search_url = search_data['next_page']



dict_list = []

print('gathering fields from ticket list...')
    
for x in ticket_list:

    url = 'https://anki.zendesk.com/api/v2/tickets/' + x + '.json'
    user = 'sgoodwin@anki.com' + '/token'
    pwd = ''
    
    
    response = requests.get(url, auth=(user, pwd))
    
    data = response.json()
    
    
    for k,v in data['ticket'].items():
        if k =='id':
            ticket_id = str(v)
        if k == 'subject':
            subject = str(v)
        if k == 'description':
            description = str(v)
        if k == 'created_at':
            created_at = str(v)
        if k == 'priority':
            priority = str(v)
        if k == 'status':
            status = str(v)
        if k == 'via':
            for k,v in (v['source']['from'].items()):
                if k == 'address':
                    address = str(v)
                if k == 'name':
                    name = str(v)
    
    ticket_dict = {
        'ticket':ticket_id,
        'subject':subject,
        'description':description,
        'created_at':created_at,
        'priority':priority,
        'status':status,
        'address':address,
        'name':name
        }
    
    dict_list.append(ticket_dict)


merged_dict = defaultdict(list)


for dict in dict_list:
    for k, v in dict.items():
        merged_dict[k].append(v)

        
# create csv file using merged dictionary keys as headers and put associated values into columns    

print('writing csv file...')

keys = sorted(merged_dict.keys())
with open("ticket_output.csv", "w") as csvfile:
    writer = csv.writer(csvfile, delimiter = ",")
    writer.writerow(keys)
    writer.writerows(zip(*[merged_dict[key] for key in keys]))

print('script finished.')
print('total time =' + ' ' + str(datetime.now() - startTime))



# email csv file
 
fromaddr = "sgoodwin@anki.com"
toaddr = "sgoodwin@anki.com"
#pw = ""

msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Zendesk Weekly Tickets" + ' ' + str(time.strftime("%x"))
 
#body = "TEXT YOU WANT TO SEND"
 
#msg.attach(MIMEText(body, 'plain'))
 
filename = "ticket_output.csv"
attachment = open("/Users/stuart/ticket_output.csv", "rb")
 
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
msg.attach(part)
 
server = smtplib.SMTP('smtp-relay.gmail.com', 587)
server.starttls()
#server.login(fromaddr, pw)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

