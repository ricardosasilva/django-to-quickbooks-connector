from mydjangoproject.qbwc.soaplib_handler import Array, String, Integer
from soaplib import soap
from soaplib.service import soapmethod
from soaplib_handler import DjangoSoapApp, soapmethod, soap_types

class QuickBooksService(DjangoSoapApp):
    
    __tns__ = 'http://developer.intuit.com/'

    @soapmethod(soap_types.String, _returns=soap_types.String)
    def serverVersion(self, ticket):
        print 'serverVersion()'
        print ticket
        return '1.0'

    @soapmethod(soap_types.String,
                soap_types.String, 
                _returns=Array(String),
                _outMessage='{http://developer.intuit.com/}authenticateResponse',
                _outVariableName='authenticateResult',
                )
    def authenticate(self, strUserName, strPassword):
        print 'authenticate()'
        results = []
        results.append('{85B41BEE-5CD9-427a-A61B-83964F1EB426}')
        results.append('')
        results.append('300')
        
        print strUserName
        print strPassword
        print results
        return results

    @soapmethod(soap_types.String, _returns=soap_types.String)
    def clientVersion(self, strVersion):
        print 'clientVersion()'
        print strVersion
        return ""

    @soapmethod(soap_types.String, _returns=soap_types.String)
    def closeConnection(self, ticket):
        print 'closeConnection()'
        print ticket
        return 'closeConnection() called on WS'

    @soapmethod(soap_types.String,
                soap_types.String,
                soap_types.String,
                _returns=soap_types.String)
    def connectionError(self, ticket, hresult, message):
        print 'connectionError'
        print ticket
        print hresult
        print message
        return 'done'

    @soapmethod(soap_types.String, _returns=soap_types.String)
    def getLastError(self, ticket):
        print 'lastError()'
        print ticket
        return 'Problems foo bar'

    @soapmethod(soap_types.String,
                soap_types.String,
                soap_types.String,
                soap_types.String,
                _returns=Integer,
                _outMessage='{http://developer.intuit.com/}receiveResponseXMLResponse',
                _outVariableName='receiveResponseXMLResult',)
    def receiveResponseXML(self, ticket, response, hresult, message):
        print 'receiveResponseXML()'
        print "ticket=" + ticket
        print "response=" + response
        if hresult:
            print "hresult=" + hresult
            print "message=" + message
        return 100

    @soapmethod(soap_types.String,
                soap_types.String,
                soap_types.String,
                soap_types.String,
                soap_types.Integer,
                soap_types.Integer,
                _returns=String,
                _outMessage='{http://developer.intuit.com/}sendRequestXMLResponse',
                _outVariableName='sendRequestXMLResult',)
    def sendRequestXML(self, ticket, strHCPResponse, strCompanyFileName, qbXMLCountry, qbXMLMajorVers, qbXMLMinorVers ):
        print 'sendRequestXML()'
        print strHCPResponse
        xml =   "<?xml version=\"1.0\" ?>" + \
                "<?qbxml version=\"2.0\"?>" + \
                    "<QBXML>" + \
                        "<QBXMLMsgsRq onError=\"stopOnError\">" + \
                        "<ItemQueryRq></ItemQueryRq>" + \
                    "</QBXMLMsgsRq>" + \
                "</QBXML>"
        return xml


    @soapmethod(soap_types.String,
                soap_types.String,
                _returns=soap_types.String)
    def interactiveUrl(self, ticket, sessionID):
        print 'interactiveUrl'
        print ticket
        print sessionID
        return 'http://localhost/test'

    @soapmethod(soap_types.String, _returns=soap_types.String)
    def interactiveDone(self, ticket):
        print 'interactiveDone()'
        print ticket
        return 'Done'

    @soapmethod(soap_types.String,
                soap_types.String,
                _returns=soap_types.String)
    def interactiveRejected(self, ticket, reason):
        print 'interactiveRejected()'
        print ticket
        print reason
        return 'Message to show'


quickbooks_service = QuickBooksService()
