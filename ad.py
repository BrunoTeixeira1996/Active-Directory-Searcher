from ldap3 import *
from ldap3.core.exceptions import *
from colorama import *
from dateutil.parser import parse


server_name = 'YOURSERVERNAME WITH .[YOUR TLD]'
domain_name = 'YOURSERVERNAME'
user_name = 'YOURSERVERNAME WITH .[YOUR TLD]\Administrator'
password = 'YOURPASSWORD'

print(Fore.GREEN+''' 
==================================
|                                |
|                                |
|   Active Directory Finder      |
|                                |
|       by: Bruno Teixeira       |
|                                |
|                                |
==================================
	''')

def connection_to_ad():
	server = Server(server_name, get_info = ALL)
	conn = Connection(server, user = user_name, password = password,  authentication = NTLM, auto_bind = True)
	conn.search('dc = {}, dc = pt'.format(domain_name), '(objectclass=person)', attributes = [ALL_ATTRIBUTES,ALL_OPERATIONAL_ATTRIBUTES])
	return conn


def search(conn):
	name = input('Name: ')
	for people in conn.entries:
		if name == people['sAMAccountName']:
			created = (parse(people['whenCreated'].value.strftime('%Y-%m-%d %H:%M:%S')))
			email = people['userPrincipalName']
			logoncount = people['logonCount']
			pwdLastSet = (parse(people['pwdLastSet'].value.strftime('%Y-%m-%d %H:%M:%S')))
			lastlogon = (parse(people['lastLogon'].value.strftime('%Y-%m-%d %H:%M:%S')))
			lastlogoff = (parse(people['lastLogoff'].value.strftime('%Y-%m-%d %H:%M:%S')))
			accexpires = (parse(people['accountExpires'].value.strftime('%Y-%m-%d %H:%M:%S')))
			memberoff = people['memberOf']
			print(f'\nName:{name}\n\nEmail:{email}\n\nAccountCreated:{created}\n\nPasswordLastSet:{pwdLastSet}\n\nLogonCount:{logoncount}\n\nLastLogon:{lastlogon}\n\nLastLogoff:{lastlogoff}\n\nAccountExpires:{accexpires}\n\nMemberOff:{memberoff}')
			print(Style.RESET_ALL)
if __name__ == '__main__':
	conn = connection_to_ad()
	search(conn)
