import requests, json, unittest, os.path, logging, sys
from glob import glob

# test data directory
pattern = os.path.join('test/derivatives/', '*.json')

# url for GET
def getURL(postResponse, url):
    dirID = postResponse.json()["_id"]
    resURL = url + "/" + dirID
    return resURL  

def getRequest(postResponse, url):
    # GET
    getResponse = requests.get(getURL(postResponse, url))
    return getResponse.json()

###### MAIN ######
header = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
numOfTestData = 84

class TestCase(unittest.TestCase):

    def test_00_CountFiles(self):
        # 1. initialize param. change to others for later use
        url = "http://localhost:80/scenarios"
        log= logging.getLogger( "SomeTest.testSomething" )

        count = 0

        self.assertTrue( count == 0 )

        count = len(glob(pattern))

        self.assertTrue( count == numOfTestData )

    def test_01_GETAllData(self):
        # 1. initialize param. change to others for later use
        url = "http://localhost:80/scenarios"
        log= logging.getLogger( "SomeTest.testSomething" )

        inputCount = 0
        for fileName in glob(pattern):
            with open(fileName) as fp:
                inputCount += 1
                inputData = json.load(fp) 
                # POST request
                postResponse = requests.post(url, data = json.dumps(inputData), headers = header)
        # GET request
        getResponse = requests.get(url).json()
        log.debug( "total: %r", getResponse['_meta']['total'] )
        self.assertTrue( inputCount == getResponse['_meta']['total'] )

    def test_02_ConnectionStatus(self):
         # 1. initialize param. change to others for later use
        url = "http://localhost:80/scenarios"

        log= logging.getLogger( "SomeTest.testSomething" )
   
        for fileName in glob(pattern):
            with open(fileName) as fp:
                inputData = json.load(fp) 
                # POST request
                postResponse = requests.post(url, data = json.dumps(inputData), headers = header)
                self.assertTrue( postResponse.raise_for_status() == None )
                # GET request
                getResponse = requests.get( getURL(postResponse, url) )
                self.assertTrue( getResponse.raise_for_status() == None )

    def test_03_DataValid(self):
        # 1. initialize param. change to others for later use
        url = "http://localhost:80/scenarios"
        
        for fileName in glob(pattern):
            with open(fileName) as fp:
                inputData = json.load(fp) 
                # 2. POST request
                postResponse = requests.post(url, data = json.dumps(inputData), headers = header)

                # 3. GET request
                queriedData = getRequest(postResponse, url)
                
                # 4. validate input data and queried data
                for key in inputData:
                    # check missing key
                    self.assertTrue(key in queriedData)
                    # check key-value pair match
                    self.assertTrue( inputData[key] == queriedData[key] )



if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )

    unittest.main()