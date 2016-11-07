###### HCDE310, A15: Homework 6 Exercises
### version 1.2

import urllib, urllib2, json

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

#### Exercises: A RESTful API

# The FAA has put out a REST API for accessing current information about US
# airports. You'll be using it in the following exercises.

# Point your web browser to the following URL:
#   http://services.faa.gov/airport/status/SEA?format=json
#
# The text that is shown in your browser is a JSON-formatted dictionary.
# It can easily be converted into a python dictionary and processed in a
# manner similar to what we have done with the Facebook feed previously.
# The exercise below guides you through the process of writing python
# code that uses this RESTful API to extract information about some
# airports.


## Encoding query parameters in a URL
# (1a) Use urllib.urlencode() to generate the query parameter string with one
#      parameter:
#        'format', whose value should be 'json' (the other option is xml, which you can also try if you're adventurous)
#      Store the query parameter string in a variable called param_str
#      and print it out.  Your output should look like the screenshot.
print '-------1a--------'

param_dict = {'format' : 'json'}
param_str = urllib.urlencode(param_dict)
print param_str

# (1b) Add (concatenate) the airport and the param_str to the base URL:
#        http://services.faa.gov/airport/status/
#      Store the string in a variable called airport_request, and print it out.
print '-------1b--------'
baseurl = 'http://services.faa.gov/airport/status/'
airport = 'SEA'
airport_request = '%s%s?%s'%(baseurl, airport, param_str)
print airport_request

#uncomment this line to check if you generated the correct url
#print airport_request == 'http://services.faa.gov/airport/status/SEA?format=json'
## Grabbing data off the web
# (2)  Use urllib2.urlopen() retrieve data from the address airport_request.
#      Store the data in a string called airport_json_str.  Print it out.
print '-------2---------'

inFile = urllib2.urlopen(airport_request)
airport_json_str = inFile.read()
print airport_json_str

## Converting a JSON string to a dictionary
# (3)  Use json.loads() to convert airport_json_str into a dictionary.
#      Store the dictionary in a variable called airport_data.
#      Then, print the dictionary, using the pretty function to turn it into
#      a nicely indented format
print '-------3---------'

airport_data = json.loads(airport_json_str)
print pretty(airport_data)

## Extracting relevant information from a dictionary
# (4)  Extract and print the name, city, state, and the reason field from within the status
#      Your output format should match the sample output in the PDF
#      instructions, though the contents will different, depending on when you
#      query.
print '-------4---------'
name = airport_data['name']
city = airport_data['city']
state = airport_data['state']
print 'Airport: %s (%s, %s)'%(name, city, state)
print 'Reason: ' + airport_data['status']['reason']

print '-------5a--------'

## Generalizing your code
# (5a) Write a function called getAirport() that accepts a three-letter airport
# code and returns a data dictionary.  Uncomment out the test line.

def getAirport(code):
    base = 'http://services.faa.gov/airport/status/'
    param = 'format=json'
    request_url = '%s%s?%s'%(base, code, param)
    aFile = urllib2.urlopen(request_url)
    airport_str = aFile.read()
    return json.loads(airport_str)
#
# The following line of code tests getAirport():
print pretty(getAirport('SEA'))

print '-------5b--------'

# (5b) Write another function called printAirport() that accepts an airport code
#      and prints out the info as in exercise 4.
#      It should call getAirport().  Uncomment the test code to try it out.
def printAirport(code):
    thisData = getAirport(code)
    name = thisData['name']
    city = thisData['city']
    state = thisData['state']
    print 'Airport: %s (%s, %s)'%(name, city, state)
    print 'Reason: ' + thisData['status']['reason']

# The following line of code tests printAirport():
printAirport('SFO')
print '-------5c--------'


# (5c) Iterate over the fav_airports list and print out the abbreviated info for
# each, by calling printAirport().
#      Your output should match the format of the sample output

fav_airports = ['SEA', 'BOS', 'JFK', 'SJC']

for code in fav_airports:
    printAirport(code)


# Error handling and exceptions
# (6a) Uncomment the bogus URL request below.  It should throw an exception.
#      This exception occurs when you request an invalid URL.  Wrap the
#      urlopen() call in a try/except block similar to what was done in the
#      flickr example from class.
#      e.g. your block should catch urllib2.URLError exceptions, and print out
#      the appropriate reason or error code
print '-------6a--------'
#x = urllib2.urlopen('http://hcde.washington.edu/hcdestuff')
try:
    print urllib2.urlopen('http://hcde.washington.edu/hcdestuff')
except urllib2.URLError, e: 
    if hasattr(e,'code'):
        print "The server couldn't fulfill the request." 
        print "Error code: ", e.code 
    elif hasattr(e,'reason'): 
        print "We failed to reach a server" 
        print "Reason: ", e.reason 
        
#(6b) Define a function getAirportSafe().  It calls getAirport, but catches any
#     errors that might occur (i.e., use try/except around the whole getAirport
#     function call). If an error occurs, your function should print 'Error
#     trying to retrieve airport.', followed by information about the error,
#     and return None. If you fail to reach a server, you should say that.
#     If you reach a server but cannot find the airport, your error message should
#     include the airport code.
print '-------6b--------'
def getSafe(code):
    airport_request = baseurl + code + '?' + param_str
    try:
        return urllib2.urlopen(airport_request) 
    except urllib2.URLError, e: 
        print 'Error trying to retrieve airport: %s'%code
        if hasattr(e,'code'):
            print "The server couldn't fulfill the request." 
            print "Error code: ", e.code
        elif hasattr(e,'reason'): 
            print "We failed to reach a server" 
            print "Reason: ", e.reason
        return None

def getAirportSafe(code): 
    if (getSafe(code) != None):
        return getAirport(code)
    else:
        return None
# Uncomment the following code to test getAirportSafe():
print getAirportSafe('xy')
print getAirportSafe('SEA')

print '-------6c--------'
#(6c) Now define a function printAirportSafe that calls getAirportSafe and, if there's no error, prints the abbreviated data as in printAirport
def printAirportSafe(code):
    if (getSafe(code) != None):
        printAirport(code)
    else:
        return None

# Try out your own airports (6d) Create a list including at least
# your 3 top airports  and one that doesn't exist. 
# Print them out using the printAirportSafe()
# function.
print '-------6d--------'
# uncomment this code and fill in your_favs
your_favs = ['SEA', 'JFK', 'LAX', 'GUY']
for a in your_favs:
    printAirportSafe(a)


####Now you're ready for the next part, where you retrieve data from an API of
#your choice. Note that you may need to provide an authentication key for some
#APIs. For that, create another file, called hw8application.py. You will need to
#copy a few of the import statements from the top of this file.

##Note that when this API is queried for an airport that doesn't exist, it gives a
#404 error. Some APIs that you may use will return JSON-formatted data saying
#that the requested item couldn't be found. You may have to check the contents
#of the data you get back to see whether a query was successful. You don't have
#to do that with this API.