from urllib.request import urlopen
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError
import json
import base64


#set the api url
url = 'http://test-api-app-apptest.k-apps.osh.massopen.cloud/api/v1/get-example-certificates'

#create a new request with the given url
request = Request(url)
#format the usename and password
userpass = 'testuser:T3st9paS$w0rd!'
#base 64 encode the authorization
encoded = base64.b64encode(userpass.encode('utf-8')).decode('utf-8')
#add a header with the authorization info to the request
request.add_header("Authorization", 'Basic %s' % encoded)

#try to send the request
try:
    u = urlopen(request)
    text = u.read().decode() #read and decode the response into a string
    dict = json.loads(text) #read the text as a json and convert it to a py dictionary
    certs = dict['Certificates'] #certs is a list of the certificates in the dict
    result = '' #set initial result
    f = open("frank_eli.crt", "w") #open the file for writing

    for i in range (0,len(certs)): #loop through each certificate in certs
        index = 0 #initial index is 0 because we are starting at the start of the cert
        result =  result + '-----BEGIN CERTIFICATE-----\n' #add header to cert
        while index * 64 < len(certs[i]): #loop in increments of 64 character so that we don't exceed 64 non-newline chars
            result = result + certs[i][index * 64 : (index + 1) * 64] + '\n' #parse by taking substring of 64 chars and add \t
            index += 1 #increment index
    result = result + '-----END CERTIFICATE-----\n' #add footer to cert
    print(result) #print result on command line for testing purposes
    f.write(result) #write the result to our opened file
    f.close() #close the file
except HTTPError as e: #print out the error in case we don't get an okay response
    print(e)
    print(e.headers)
