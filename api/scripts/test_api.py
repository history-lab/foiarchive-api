import urllib.request as urllib

###simple script to test api

def test(urls):

    for u in urls:
        print u
        try:
            response = urllib.urlopen(u)
            print 'ok'
        except urllib2.HTTPError, err:
            print err

if __name__=="__main__":
    address = "localhost:5000"
    address = "api.declassification-engine.org"
    urls = [
            "http://"+address+"/declass/v0.3/?geo_ids=004AND804",
            "http://"+address+"/declass/v0.3/?ids=frus1969-76v17d123,frus1977-80v13d104&fields=names,date,body",
            "http://"+address+"/declass/v0.3/documents/frus1950-55Inteld203",
            "http://"+address+"/declass/v0.3/?start_date=1947-01-01&end_date=1970-12-01&geo_ids=008",
            "http://"+address+"/declass/v0.3/?start_date=1947-01-01&end_date=1980-12-01&geo_ids=008OR040&collections=kissinger",
            "http://"+address+"/declass/v0.3/?ids=frus1969-76v17d123,frus1977-80v13d104,0000BA5A,1975010100004"]
    test(urls)
