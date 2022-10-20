from mail_tasks import send_mail,search_mail

#mail_details = {'From_type':'college','To':'spandise@gmail.com,vp.shivasan@iitgn.ac.in','Subject':'Test subject 2','Body':"Hello world Test mail",'attachments':['E1_19110104_V P Shivasankaran.pdf','wierd.jpg']}
#send_mail(mail_details)
from_addr = 'vp.shivasan@iitgn.ac.in'
m_subject = 'a bc'
body = "HE y"
m_type = 'personal'
b_date = 'NA'
s_date = 'NA'
search_mail(mail_type =m_type, FROM = from_addr,SUBJECT = m_subject, BODY = body, BEFORE= b_date, AFTER = s_date)
'''def search_string( criteria):
	query_string = ''
	for key,value in criteria.items():
		if value != 'NA':
			query_string+= key + " " +value + " "
	return query_string
print(search_string(criteria))

def search1_mail(**kwargs):
	del kwargs['mail_type']
	print(search_string(kwargs))
m_type = 'personal'

body = 'NA'

search1_mail(mail_type =m_type, FROM = from_addr,SUBJECT = m_subject, BODY = body, BEFORE= b_date, AFTER = a_date)
#search_mail(mail_type =m_type, FROM = from_addr,SUBJECT = 'sub')'''