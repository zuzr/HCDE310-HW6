import urllib2, json

print "Input terrestrial (Earth) year, month, and day to retrieve the offical Martian Forecast Summary (MFS) from that day!"
year = raw_input("Terr. year (yyyy: 2012 - 2016): ")
month = raw_input("Terr. month (mm: 01 - 12): ")
rough_date = '%s-%s'%(year, month)
api_url = 'http://marsweather.ingenology.com/v1/archive/'

def getMFS(rough_date):
    print "Aggregating data..."

    hasNextPage = True
    page = 1
    count = 1
    mars_data_list = []
    while (hasNextPage == True):
        mars_request = urllib2.urlopen(api_url + '?page=%s'%count)
        mars_data = json.load(mars_request)
        for entry in mars_data['results']:
            mars_data_list.append(entry)
        count += 1
        if (mars_data['next'] == None):
            hasNextPage = False
        page += 1


    print "Choose terr. day (dd) from the following: "

    mars_month_list = []
    for entry in mars_data_list:
        if (entry['terrestrial_date'][:7] == rough_date):
            print entry['terrestrial_date'][8:]
            mars_month_list.append(entry)
    day = raw_input("Terr day (dd): ")
    date = "%s-%s"%(rough_date, day)
    for entry in mars_month_list:
        if (entry['terrestrial_date'] == date):
            return entry
    return None

def printMFS(date_data):
    print "\nMFS on earth date %s"%date_data['terrestrial_date']
    print "Sol: %s"%date_data['sol']
    print "Season: %s"%date_data['season']
    outString = "It is a %s"%date_data['atmo_opacity']
    outString += " day on Mars, with highs around %s"%date_data['max_temp']
    outString += " degrees Celsius and lows around %s"%date_data['min_temp']
    outString += ". \nWe are currently experiencing %s"%date_data['pressure_string']
    outString += " atmospheric pressures than average. "
    print outString

def getSafe(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.URLError, e:
        if hasattr(e,'code'):
            print "The server couldn't fulfill the request."
            print "Error code: ", e.code
        elif hasattr(e,'reason'):
            print "We failed to reach a server"
            print "Reason: ", e.reason
        return None

def printMFSSafe(rough_date):
    if (getSafe(api_url) != None):
        printMFS(getMFS(rough_date))

printMFSSafe(rough_date)
