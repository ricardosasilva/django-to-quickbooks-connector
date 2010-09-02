from django.http import HttpResponse
from soaplib.serializers import primitive as soap_types
from soaplib.serializers.primitive import _element_to_unicode, Null, \
    _generic_to_xml, _element_to_integer
from soaplib.service import soapmethod
from soaplib.wsgi_soap import SimpleWSGISoapApp
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    import cElementTree as ElementTree


class DjangoSoapApp(SimpleWSGISoapApp):

    def __call__(self, request):
        django_response = HttpResponse()
        def start_response(status, headers):
            status, reason = status.split(' ', 1)
            django_response.status_code = int(status)
            for header, value in headers:
                django_response[header] = value
        response = super(SimpleWSGISoapApp, self).__call__(request.META, start_response)
        django_response.content = "\n".join(response)

        print django_response.content
        return django_response    


class String:
    '''
    Custom String Serializer without namespace
    in order to avoid problems with the .NET SOAP client 
    '''
    @classmethod
    def to_xml(cls, value, name='retval'):
        element = ElementTree.Element(name)
        #element.set('xs:string','1')
        element.text=value
        return element
    
    @classmethod
    def from_xml(cls, element):
        return _element_to_unicode(element)
    
    @classmethod
    def get_datatype(cls, withNamespace=False):
        return 'string'

    @classmethod
    def add_to_schema(cls, added_params):
        pass


class Integer:
    '''
    Custom Integer Serializer without namespace
    in order to avoid problems with the .NET SOAP client 
    '''

    @classmethod
    def to_xml(cls,value,name='retval'):
        element = ElementTree.Element(name)
        #element.set('xs:string','1')
        element.text=str(value)
        return element
    
    @classmethod
    def from_xml(cls,element):
        return _element_to_integer(element)

    @classmethod
    def get_datatype(cls,withNamespace=False):
        return 'int'

    @classmethod
    def add_to_schema(cls,added_params):
        pass


class Array:
    '''
    Custom Array Serializer without namespace
    in order to avoid problems with the .NET SOAP client 
    '''

    
    def __init__(self,serializer,type_name=None,namespace='tns'):
        self.serializer = serializer
        self.namespace = namespace
        if not type_name:
            self.type_name = '%sArray'%self.serializer.get_datatype()
        else:
            self.type_name = type_name

    def to_xml(self,values,name='retval'):
        res = ElementTree.Element(name)
        typ = self.get_datatype(True)
        #res.set('xmlns','') 
        if values == None:
            values = []
        #res.set('xsi:type',self.get_datatype(True))
        for value in values:
            serializer = self.serializer
            if value == None:
                serializer = Null
            res.append(
                serializer.to_xml(value,name=serializer.get_datatype(False))
            )
        return res    

    def from_xml(self,element):
        results = []
        for child in element.getchildren():
            results.append(self.serializer.from_xml(child))
        return results

    def get_datatype(self,withNamespace=False):
        if withNamespace:
            return '%s:%s'%(self.namespace,self.type_name)
        return self.type_name

    def add_to_schema(self,schema_dict):
        typ = self.get_datatype()
        
        self.serializer.add_to_schema(schema_dict)

        if not schema_dict.has_key(typ):

            complexTypeNode = ElementTree.Element("xs:complexType")
            complexTypeNode.set('name',self.get_datatype(False))

            sequenceNode = ElementTree.SubElement(complexTypeNode, 'xs:sequence')
            elementNode = ElementTree.SubElement(sequenceNode, 'xs:element')
            elementNode.set('minOccurs','0')
            elementNode.set('maxOccurs','unbounded')
            elementNode.set('type',self.serializer.get_datatype(True))
            elementNode.set('name',self.serializer.get_datatype(False))

            typeElement = ElementTree.Element("xs:element")            
            typeElement.set('name',typ)
            typeElement.set('type',self.get_datatype(True))
            
            schema_dict['%sElement'%(self.get_datatype(True))] = typeElement
            schema_dict[self.get_datatype(True)] = complexTypeNode
