import sys
try:
    from pyaxml.proto import axml_pb2
except ImportError:
    print("proto is not build")
    sys.exit(1)
from struct import pack, unpack
from pyaxml import public
import re
import ctypes
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

AXML_HEADER_SIZE=8
AXML_STRING_POOL_HEADER_SIZE=28
AXML_RES_TABLE_HEADER_SIZEM=AXML_HEADER_SIZE+4



class AXMLHeader:
    """AXMLHeader class to build an AXMLHeader
    """

    def __init__(self, type : int = 0, size : int = 0, proto : axml_pb2.AXMLHeader = None):
        """Initialize an AXMLHeader

        Args:
            type (int, optional): type element from ResType. Defaults to 0.
            size (int, optional): size of data contain belong to this AXMLHeader. Defaults to 0.
            proto (axml_pb2.AXMLHeader, optional): define AXMLHeader by a protobuff. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.AXMLHeader()
            self.proto.type = type
            self.proto.size = size
            self.proto.header_size = AXML_HEADER_SIZE
        else:
            self.proto = proto
        

    def pack(self) -> bytes:
        """pack the AXMLHeader element

        Returns:
            bytes: return the AXMLHeader element packed
        """
        return pack("<HHL", self.proto.type, self.proto.header_size, self.proto.size)
    
    def from_axml(buff):
        header = AXMLHeader()
        header.proto.type, header.proto.header_size, header.proto.size = unpack('<HHL', buff[:8])
        return header, buff[8:]
    

class AXMLHeader_XML(AXMLHeader):
    """AXMLHeader_XML class to build an AXMLHeader with the type RES_XML_TYPE
    """

    def __init__(self, size : int = 0, proto : axml_pb2.AXMLHeader = None):
        """Initialize an AXMLHeader with the type RES_XML_TYPE

        Args:
            size (int, optional): size of data contain belong to this AXMLHeader. Defaults to 0.
            proto (axml_pb2.AXMLHeader, optional): define AXMLHeader by a protobuff. Defaults to None.
        """
        if proto is None:
            super().__init__(axml_pb2.RES_XML_TYPE, size)
        else:
            self.proto = proto

    def from_axml(buff):
        header_xml = AXMLHeader_XML()
        header, buff = AXMLHeader.from_axml(buff)
        if header.proto.type != axml_pb2.RES_XML_TYPE:
            raise Exception("AXMLHeader_XML file wrong format no XML_TYPE")
        return header_xml, buff

class AXMLHeader_RES_TABLE:
    """AXMLHeader_RES_TABLE class to build an AXMLHeader with the type RES_RES_TABLE_TYPE
    """

    def __init__(self, size : int = 0, package_count : int = 0, proto : axml_pb2.AXMLHeader_RES_TABLE = None):
        """TODO
        """
        
        if proto is None:
            self.proto = axml_pb2.AXMLHeader_RES_TABLE()
            self.proto.package_count = package_count
            self.proto.hnd.CopyFrom(AXMLHeader(axml_pb2.RES_TABLE_TYPE, size).proto)
            self.proto.hnd.header_size = AXML_RES_TABLE_HEADER_SIZEM
        else:
            self.proto = proto
    
    def pack(self) -> bytes:
        """pack the AXMLHeader element

        Returns:
            bytes: return the AXMLHeader element packed
        """
        return AXMLHeader(proto=self.proto.hnd).pack() + pack("<L", self.proto.package_count)
    
    def from_axml(buff):
        restable_header = AXMLHeader_RES_TABLE()
        header, buff = AXMLHeader.from_axml(buff)
        restable_header.proto.hnd.CopyFrom(header.proto)
        restable_header.proto.package_count = unpack('<L', buff[:4])[0]
        return restable_header, buff[4:]
    
    


class AXMLHeader_STRING_POOL:
    """AXMLHeader_STRING_POOL class to build an AXMLHeader_STRING_POOL element
    """

    def __init__(self, sb : list = None, size : int = 0, proto : axml_pb2.AXMLHeader_STRING_POOL = None):
        """Initialize an AXMLHeader of STRING_POOL

        Args:
            sb (list, optional): list of Stringblock elements. Defaults to None.
            size (int, optional): size of data contain belong to this AXMLHeader. Defaults to 0.
            proto (axml_pb2.AXMLHeader_STRING_POOL, optional): define AXMLHeader_STRING_POOL by a protobuff. Defaults to None.
        """
        # TODO make version with initilisation without proto
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.AXMLHeader_STRING_POOL()
    
    def compute(self):
        """Compute all fields to have a Stringpool element
        """
        pass

    def pack(self) -> bytes:
        """pack the AXMLHeader_STRING_POOL element

        Returns:
            bytes: return the AXMLHeader_STRING_POOL element packed
        """
        return AXMLHeader(proto=self.proto.hnd).pack() + pack("<LLLLL", self.proto.len_stringblocks, self.proto.len_styleblocks,
                                                                        self.proto.flag, self.proto.stringoffset, self.proto.styleoffset)
    
    def from_axml(buff):
        hnd_str_pool = AXMLHeader_STRING_POOL()
        header, buff = AXMLHeader.from_axml(buff)
        hnd_str_pool.proto.hnd.CopyFrom(header.proto)
        hnd_str_pool.proto.len_stringblocks, hnd_str_pool.proto.len_styleblocks, hnd_str_pool.proto.flag, \
              hnd_str_pool.proto.stringoffset, hnd_str_pool.proto.styleoffset = unpack("<LLLLL", buff[:5*4])
        return hnd_str_pool, buff[5*4:]


##############################################################################
#
#                              STRINGBLOCKS
#
##############################################################################


class StringBlock:
    """StringBlock class to build an StringBlock element
    """

    def __init__(self, data : str = "", size : int = 0, utf8 : bool = False, proto : axml_pb2.StringBlock = None):
        """initialize a stringblock element

        Args:
            data (str, optional): value of the stringblock. Defaults to "".
            size (int, optional): size of data contain belong to this Stringblock. Defaults to 0.
            utf8 (bool, optional): Stringblock can be encoded in UTF8 or UTF16. set True if you want to encode in UTF8 else UTF16. Defaults to False.
            proto (axml_pb2.StringBlock, optional): define StringBlock by a protobuff. Defaults to None.
        """
        self.not_decoded = False
        if proto:
            self.proto = proto
            self.utf8= utf8
        else:
            self.proto = axml_pb2.StringBlock()
            self.utf8= utf8
            if self.utf8:
                self.proto.data = data.encode('utf-8')
            else:
                self.proto.data = data.encode('utf-16')[2:]

            self.proto.size = size

    
    def compute(self):
        """Compute all fields to have a StringBlock element
        """
        self.proto.size = (len(self.proto.data) | len(self.proto.data) << 8) if self.utf8 else int(len(self.proto.data)/2)
    
    def pack(self) -> bytes:
        """pack the StringBlock element

        Returns:
            bytes: return the StringBlock element packed
        """
        redundant = b""
        if self.proto.HasField('redundant_size'):
            redundant = pack('<H', self.proto.redundant_size)
        if self.utf8:
            return pack('<H', self.proto.size) + redundant + self.proto.data + b'\x00'
        else:
            return pack('<H', self.proto.size) + redundant + self.proto.data + b'\x00\x00'
    
    def from_axml(buff, utf8 : bool):
        str_block = StringBlock()
        str_block.utf8 = utf8
        if str_block.utf8:
            str_block.proto.size = unpack('<H', buff[:2])[0]
            size = str_block.proto.size >> 8
            if str_block.proto.size & 0x80 != 0:
                redundant = unpack('<H', buff[2:4])[0]
                size = ((redundant & 0xff00) >> 8 | (redundant & 0xf) << 8)
                buff = buff[2:]
                str_block.proto.redundant_size = redundant
        else:
            str_block.proto.size = unpack('<H', buff[:2])[0]
            if str_block.proto.size & 0x8000 != 0:
                redundant = unpack('<H', buff[2:4])[0]
                size = ((str_block.proto.size & 0x7FFF) << 16) | redundant
                buff = buff[2:]
                str_block.proto.redundant_size = redundant
            size = str_block.proto.size * 2

        while buff[2+size] != 0:
            size +=1

        str_block.proto.data = buff[2:2+size]
        return str_block, buff[2+size:]

class StringBlocks:
    """StringBlocks class to build all StringBlocks elements
    """
 
    def __init__(self, proto : axml_pb2.StringBlocks = None):
        """initialize the bunch of StringBlocks element

        Args:
            proto (axml_pb2.StringBlocks, optional): define Stringblocks by a protobuff. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.StringBlocks()
    
    def compute(self):
        """Compute all fields to have all StringBlocks elements
        """

        idx = 0
        del self.proto.stringoffsets[:]
        for s in self.proto.stringblocks:
            self.proto.stringoffsets.append(idx)
            idx += len(StringBlock(proto=s, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG).pack())

        self.proto.hnd.stringoffset = AXML_STRING_POOL_HEADER_SIZE + \
            len(b"".join(pack('<I', x) for x in self.proto.stringoffsets)) + \
            len(b"".join(pack('<I', x) for x in self.proto.styleoffsets))
        
        self.proto.hnd.styleoffset = 0
        self.proto.hnd.hnd.CopyFrom(AXMLHeader(axml_pb2.RES_STRING_POOL_TYPE, len(self.pack())).proto)
        self.proto.hnd.hnd.header_size = AXML_STRING_POOL_HEADER_SIZE
        self.proto.hnd.len_stringblocks = len(self.proto.stringoffsets)
        self.proto.hnd.len_styleblocks = len(self.proto.styleoffsets)
    
    def align(self, buf : bytes) -> bytes:
        """Align stringblocks elements

        Args:
            buf (bytes): align the buffer given in input

        Returns:
            bytes: return the element with padding to align
        """
        pad = b"\x00" * (4 - (len(buf) % 4))
        if len(pad) == 4:
            return buf
        else:
            return buf + pad

    def get(self, name : str) -> int:
        """Get index of a stringblock or if it doesn't exist append a new one.

        Args:
            name (str): the name of the stringblock

        Returns:
            int: return the index of the stringblock
        """
        try:
            index = self.index(name)
        except ValueError:
            index = len(self.proto.stringblocks)
            tmp = StringBlock(data=name, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG)
            tmp.compute()
            self.proto.stringblocks.append(tmp.proto)
        return index
    
    def index(self, name : str) -> int:
        """Get index of a stringblock or if it doesn't exist raise an error

        Args:
            name (str): the name of the stringblock
        
        Raises:
            ValueError: raise ValueError if this element didn't exist

        Returns:
            int: return the index of the stringblock
        """
        name_encoded = StringBlock(data=name, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG)
        for i in range(0, len(self.proto.stringblocks)):
            if self.proto.stringblocks[i].data == name_encoded.proto.data:
                return i
        raise ValueError

    def decode_str(self, index : int) -> str:
        data = self.proto.stringblocks[index].data
        try:
            return data.decode('utf-8') if self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG else data.decode('utf-16')
        except UnicodeDecodeError:
            return data
    def pack(self) -> bytes:
        """pack the StringBlocks element

        Returns:
            bytes: return the StringBlocks element packed
        """
        sb_offsets = b"".join(pack('<I', x) for x in self.proto.stringoffsets)
        st_offsets = b"".join(pack('<I', x) for x in self.proto.styleoffsets)
        sb = self.align(b"".join(StringBlock(proto=elt, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG).pack() for elt in self.proto.stringblocks))
        st = b"" # TODO
        return AXMLHeader_STRING_POOL(proto=self.proto.hnd).pack() + sb_offsets + st_offsets + sb + st
    
    def from_axml(buff):
        rest = buff
        str_blocks = StringBlocks()
        hnd, buff = AXMLHeader_STRING_POOL.from_axml(buff)
        rest = rest[hnd.proto.hnd.size:]
        str_blocks.proto.hnd.CopyFrom(hnd.proto)
        for i in range(str_blocks.proto.hnd.len_stringblocks):
            str_blocks.proto.stringoffsets.append(unpack('<I', buff[i*4:(i+1)*4])[0])
        buff = buff[str_blocks.proto.hnd.len_stringblocks*4:]
        for i in range(str_blocks.proto.hnd.len_styleblocks):
            str_blocks.proto.styleoffsets.append(unpack('<I', buff[i*4:(i+1)*4])[0])
        buff = buff[str_blocks.proto.hnd.len_styleblocks*4:]
        for i in range(str_blocks.proto.hnd.len_stringblocks):
            stbl , _ = StringBlock.from_axml(buff[str_blocks.proto.stringoffsets[i]:], str_blocks.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG)
            str_blocks.proto.stringblocks.append(stbl.proto)
        # IF no stringblock crash
        if len(str_blocks.proto.stringoffsets) > 0:
            buff = buff[str_blocks.proto.stringoffsets[-1] + len(StringBlock(proto=str_blocks.proto.stringblocks[-1], utf8=str_blocks.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG).pack()):]
        #TODO style
        return str_blocks, rest

##############################################################################
#
#                              RESOURCEMAP
#
##############################################################################

class ResourceMap:
    """ResourceMap class to build all ResourceMap elements
    """


    def __init__(self, res : [StringBlock] = [], proto : axml_pb2.ResourceMap = None):
        """initialize ResourceMap element

        Args:
            res (StringBlock], optional): List of StringBlock elements. Defaults to [].
            proto (axml_pb2.ResourceMap, optional): define ResourceMap by a protobuff. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.ResourceMap()
            self.proto.res.extend(res)
            self.proto.header.CopyFrom(AXMLHeader(axml_pb2.RES_XML_RESOURCE_MAP_TYPE, 8).proto)
            self.proto.header.size = AXML_HEADER_SIZE + 4 * len(res)
        else:
            self.proto = proto
    
    def pack(self) -> bytes:
        """pack the ResourceMap element

        Returns:
            bytes: return the ResourceMap element packed
        """
        return AXMLHeader(proto=self.proto.header).pack() + b"".join(pack("<L", x) for x in self.proto.res)
    
    def from_axml(buff):
        res_maps = ResourceMap()
        header, buff = AXMLHeader.from_axml(buff)
        res_maps.proto.header.CopyFrom(header.proto)
        for i in range(int((res_maps.proto.header.size-res_maps.proto.header.header_size)/4) ):
            res_maps.proto.res.append(unpack('<L', buff[:4])[0])
            buff = buff[4:]
        return res_maps, buff

##############################################################################
#
#                              XML ELEMENTS
#
##############################################################################

class AXMLHeader_RES_XML(AXMLHeader):
    """AXMLHeader_RES_XML class to build an header of RES_XML
    """

    def __init__(self, type=0, size=0, proto : axml_pb2.AXMLHeader = None):
        """Initialize header of Res_XML

        Args:
            type (int, optional): define the type. Defaults to 0.
            size (int, optional): define the size of whole element. Defaults to 0.
            proto (axml_pb2.AXMLHeader, optional): define RES_XML header by a protobuff. Defaults to None.
        """
        if proto is None:
            super().__init__(type, size + 8, proto)
            self.proto.header_size = 16
        else:
            self.proto = proto 

class AXMLHeader_START_ELEMENT(AXMLHeader_RES_XML):
    """AXMLHeader_START_ELEMENT class to build an header of Start element
    """

    def __init__(self, size : int):
        """initialize START_ELEMENT element

        Args:
            size (int): size of START_ELEMENT and its header
        """
        super().__init__(axml_pb2.RES_XML_START_ELEMENT_TYPE, size)

class AXMLHeader_END_ELEMENT(AXMLHeader_RES_XML):
    """AXMLHeader_END_ELEMENT class to build an header of End element
    """

    def __init__(self, size : int):
        """initialize END_ELEMENT element

        Args:
            size (int): size of END_ELEMENT and its header
        """
        super().__init__(axml_pb2.RES_XML_END_ELEMENT_TYPE, size)

class AXMLHeader_START_NAMESPACE(AXMLHeader_RES_XML):
    """AXMLHeader_START_NAMESPACE class to build an header of Start namespace
    """

    def __init__(self, size : int):
        """initialize START_NAMESPACE element

        Args:
            size (int): size of START_NAMESPACE and its header
        """
        super().__init__(axml_pb2.RES_XML_START_NAMESPACE_TYPE, size)

class AXMLHeader_END_NAMESPACE(AXMLHeader_RES_XML):
    """AXMLHeader_END_NAMESPACE class to build an header of End namespace
    """

    def __init__(self, size : int):
        """initialize END_NAMESPACE element

        Args:
            size (int): size of END_NAMESPACE and its header
        """
        super().__init__(axml_pb2.RES_XML_END_NAMESPACE_TYPE, size)

class Classical_RES_XML:
    """RES_XML class to build RES_XML element
    """

    def __init__(self, lineNumber : int = 0, Comment : int = 0xffffffff, proto : axml_pb2.ResXML = None):
        """initialize RES_XML element

        Args:
            lineNumber (int, optional): _description_. Defaults to 0.
            Comment (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.ResXML, optional): define RES_XML by a protobuff. Defaults to None.
        """
        if proto is None:
            self.proto.generic.lineNumber = lineNumber
            self.proto.generic.Comment = Comment
        else:
            self.proto.generic.CopyFrom(proto)

    @property
    def content(self):
        return pack('<LL', self.proto.generic.lineNumber, self.proto.generic.Comment)
    
    def compute(self):
        """Compute all fields to have all RES_XML elements
        """
        pass

    def pack(self) -> bytes:
        """pack the RES_XML element

        Returns:
            bytes: return the RES_XML element packed
        """
        return self.content

    def from_axml(buff, class_xml):
        class_xml.proto.generic.lineNumber, \
                class_xml.proto.generic.Comment = unpack('<LL', buff[:8])
        return class_xml, buff[8:]

class RES_XML_START_ELEMENT(Classical_RES_XML):

    def __init__(self, namespaceURI : int = 0xffffffff, name : int =0xffffffff, attributes : list = [],
            styleAttribute : int = -1, classAttribute : int = -1, lineNumber : int = 0, Comment : int = 0xffffffff,
            fix_attributevalue = 0x140014,
            proto : axml_pb2.ResXMLStartElement = None):
        """_summary_

        Args:
            namespaceURI (int, optional): _description_. Defaults to 0xffffffff.
            name (int, optional): _description_. Defaults to 0xffffffff.
            attributes (list, optional): _description_. Defaults to [].
            styleAttribute (int, optional): _description_. Defaults to -1.
            classAttribute (int, optional): _description_. Defaults to -1.
            lineNumber (int, optional): _description_. Defaults to 0.
            Comment (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.ResXMLStartElement, optional): _description_. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.ResXMLStartElement()
            super().__init__(lineNumber, Comment)
            self.proto.namespaceURI = namespaceURI
            self.proto.name = name
            self.proto.attributes.extend(attributes)
            self.proto.styleAttribute = styleAttribute
            self.proto.classAttribute = classAttribute
            self.proto.fix_attributevalue = fix_attributevalue
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)
            

    def compute(self):
        """Compute all fields to have all RES_XML_START_ELEMENT elements
        """
        self.proto.len_attributes = len(self.proto.attributes)
        super().compute()

    @property
    def content(self) -> bytes:
        """_summary_

        Returns:
            bytes: _description_
        """
        return super().content + pack('<LLLLhh',
                self.proto.namespaceURI,
                self.proto.name,
                self.proto.fix_attributevalue, # potential attribute value
                self.proto.len_attributes,
                self.proto.styleAttribute,
                self.proto.classAttribute) + \
                        b"".join(Attribute(proto=a).pack() for a in self.proto.attributes)
    
    def from_axml(buff):
        class_xml = RES_XML_START_ELEMENT()
        class_xml, buff = Classical_RES_XML.from_axml(buff, class_xml=class_xml)

        class_xml.proto.namespaceURI, class_xml.proto.name, class_xml.proto.fix_attributevalue, class_xml.proto.len_attributes,  class_xml.proto.styleAttribute,  class_xml.proto.classAttribute = unpack('<LLLLhh', buff[:20])
        buff = buff[20:]

        for i in range(class_xml.proto.len_attributes):
            attr, buff = Attribute.from_axml(buff)
            class_xml.proto.attributes.append(attr.proto)

        return class_xml, buff

class RES_XML_END_ELEMENT(Classical_RES_XML):

    def __init__(self, namespaceURI : int = 0xffffffff, name : int = 0xffffffff,
                 lineNumber : int = 0, Comment : int = 0xffffffff,
                 proto : axml_pb2.ResXMLEndElement = None):
        """_summary_

        Args:
            namespaceURI (int, optional): _description_. Defaults to 0xffffffff.
            name (int, optional): _description_. Defaults to 0xffffffff.
            lineNumber (int, optional): _description_. Defaults to 0.
            Comment (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.ResXMLEndElement, optional): _description_. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.ResXMLEndElement()
            super().__init__(lineNumber, Comment)
            self.proto.namespaceURI = namespaceURI
            self.proto.name = name
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)


    @property
    def content(self) -> bytes:
        """_summary_

        Returns:
            bytes: _description_
        """
        return super().content + pack('<LL',
                self.proto.namespaceURI,
                self.proto.name)

    def from_axml(buff):
        class_xml = RES_XML_END_ELEMENT()
        class_xml, buff = Classical_RES_XML.from_axml(buff, class_xml=class_xml)
        class_xml.proto.namespaceURI, \
                class_xml.proto.name = unpack('<LL', buff[:8])
        return class_xml, buff[8:]


class RES_XML_START_NAMESPACE(Classical_RES_XML):

    def __init__(self, prefix : int = 0xffffffff, uri : int = 0xffffffff,
                lineNumber : int = 0, Comment : int = 0xffffffff,
                proto : axml_pb2.ResXMLStartNamespace = None):
        """_summary_

        Args:
            prefix (int, optional): _description_. Defaults to 0xffffffff.
            uri (int, optional): _description_. Defaults to 0xffffffff.
            lineNumber (int, optional): _description_. Defaults to 0.
            Comment (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.ResXMLStartNamespace, optional): _description_. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.ResXMLStartNamespace()
            super().__init__(lineNumber, Comment)
            self.proto.prefix = prefix
            self.proto.uri = uri
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)
            

    @property
    def content(self) -> bytes:
        """_summary_

        Returns:
            bytes: _description_
        """
        return super().content + pack('<LL',
                self.proto.prefix,
                self.proto.uri)
    
    def from_axml(buff):
        class_xml = RES_XML_START_NAMESPACE()
        class_xml, buff = Classical_RES_XML.from_axml(buff, class_xml=class_xml)
        class_xml.proto.prefix, \
                class_xml.proto.uri = unpack('<LL', buff[:8])
        return class_xml, buff[8:]

class RES_XML_END_NAMESPACE(Classical_RES_XML):

    def __init__(self, prefix : int = 0xffffffff, uri : int = 0xffffffff,
                 lineNumber : int = 0, Comment : int = 0xffffffff,
                 proto : axml_pb2.ResXMLEndNamespace = None):
        """_summary_

        Args:
            prefix (int, optional): _description_. Defaults to 0xffffffff.
            uri (int, optional): _description_. Defaults to 0xffffffff.
            lineNumber (int, optional): _description_. Defaults to 0.
            Comment (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.ResXMLEndNamespace, optional): _description_. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.ResXMLEndNamespace()
            super().__init__(lineNumber, Comment)
            self.proto.prefix = prefix
            self.proto.uri = uri
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)
            

    @property
    def content(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return super().content + pack('<LL',
                self.proto.prefix,
                self.proto.uri)
    
    def from_axml(buff):
        class_xml = RES_XML_END_NAMESPACE()
        class_xml, buff = Classical_RES_XML.from_axml(buff, class_xml=class_xml)
        class_xml.proto.prefix, \
                class_xml.proto.uri = unpack('<LL', buff[:8])
        return class_xml, buff[8:]
    

class Attribute:

    def __init__(self, namespaceURI : int = 0xffffffff, name : int = 0xffffffff, value : int = 0xffffffff, type : int = 0xffffffff, data : int = 0xffffffff, proto : axml_pb2.Attribute = None):
        """_summary_

        Args:
            namespaceURI (int, optional): _description_. Defaults to 0xffffffff.
            name (int, optional): _description_. Defaults to 0xffffffff.
            value (int, optional): _description_. Defaults to 0xffffffff.
            type (int, optional): _description_. Defaults to 0xffffffff.
            data (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.Attribute, optional): _description_. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.Attribute()
            self.proto.namespaceURI = namespaceURI
            self.proto.name = name
            self.proto.value = value
            self.proto.type = type
            self.proto.data = data
        else:
            self.proto = proto

    def pack(self) -> bytes:
        """pack the Attribute element

        Returns:
            bytes: return the Attribute element packed
        """
        return pack('<LLLLL', self.proto.namespaceURI, self.proto.name, self.proto.value,
                self.proto.type, self.proto.data)

    def from_axml(buff):
        attr = Attribute()
        attr.proto.namespaceURI, \
        attr.proto.name, \
        attr.proto.value, \
        attr.proto.type, \
        attr.proto.data = unpack('<LLLLL', buff[:20])
        return attr, buff[20:]


class RessourceXML:

    def __init__(self, proto : axml_pb2.RessourceXML = None) -> None:
        """_summary_

        Args:
            proto (axml_pb2.RessourceXML, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.RessourceXML()
    
    def pack(self) -> bytes:
        """pack the RessourceXML element

        Returns:
            bytes: return the RessourceXML element packed
        """
        buf = b""
        for elt in self.proto.elts:
            header = AXMLHeader(proto=elt.header).pack()
            if elt.HasField('start_elt'):
                buf += header + RES_XML_START_ELEMENT(proto=elt.start_elt).pack()
            elif elt.HasField('end_elt'):
                buf += header + RES_XML_END_ELEMENT(proto=elt.end_elt).pack()
            elif elt.HasField('start_ns'):
                buf += header + RES_XML_START_NAMESPACE(proto=elt.start_ns).pack()
            elif elt.HasField('end_ns'):
                buf += header + RES_XML_END_NAMESPACE(proto=elt.end_ns).pack()
        return buf

    def from_axml(buff):
        xml = RessourceXML()
        while len(buff) > 0:
            elt = axml_pb2.XMLElement()
            hnd, buff = AXMLHeader.from_axml(buff)
            elt.header.CopyFrom(hnd.proto)
            if hnd.proto.type == axml_pb2.RES_XML_START_ELEMENT_TYPE:
                content, buff = RES_XML_START_ELEMENT.from_axml(buff)
                elt.start_elt.CopyFrom(content.proto)
            elif hnd.proto.type == axml_pb2.RES_XML_END_ELEMENT_TYPE:
                content, buff = RES_XML_END_ELEMENT.from_axml(buff)
                elt.end_elt.CopyFrom(content.proto)
            elif hnd.proto.type == axml_pb2.RES_XML_START_NAMESPACE_TYPE:
                content, buff = RES_XML_START_NAMESPACE.from_axml(buff)
                elt.start_ns.CopyFrom(content.proto)
            elif hnd.proto.type == axml_pb2.RES_XML_END_NAMESPACE_TYPE:
                content, buff = RES_XML_END_NAMESPACE.from_axml(buff)
                elt.end_ns.CopyFrom(content.proto)
            else:
                raise ValueError("RES_XML element header incorrect type")
            xml.proto.elts.append(elt)
        return xml, buff


##############################################################################
#
#                              ARSC OBJECT
#
##############################################################################

class ARSC:

    def __init__(self, proto : axml_pb2.ARSC = None):
        """_summary_

        Args:
            proto (axml_pb2.AXML, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSC()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self, recursive=True):
        """Compute all fields to have all AXML elements
        """
        if recursive:
            s = StringBlocks(proto=self.proto.stringblocks)
            s.compute()
            self.proto.stringblocks.CopyFrom(s.proto)
            for i in range(len(self.proto.restablespackage)):
                package = AXML_Res_Table_Package(proto=self.proto.restablespackage[i])
                package.compute()
                self.proto.restablespackage[i].CopyFrom(package.proto)
            
        self.proto.header_res.hnd.size = len(self.pack())
        self.proto.header_res.package_count = len(self.proto.restablespackage)

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        sb_pack = StringBlocks(proto=self.proto.stringblocks).pack()
        header_res = AXMLHeader_RES_TABLE(proto=self.proto.header_res).pack()
        packages = b""
        for package in self.proto.restablespackage:
            packages += AXML_Res_Table_Package(proto=package).pack()
        return header_res + sb_pack + packages
    
    def from_axml(buff : str):
        """read an AXML ARSC file to convert in pyaxml.ARSC object

        Args:
            buff (str): the string buffer to read

        Returns:
            ARSC: the ARSC object
            str: index of the reading string, if it's a valid file it should be the EOF.
        """
        arsc = ARSC()
        header, buff = AXMLHeader_RES_TABLE.from_axml(buff)
        arsc.proto.header_res.CopyFrom(header.proto)
        stringblocks, buff = StringBlocks.from_axml(buff)
        arsc.proto.stringblocks.CopyFrom(stringblocks.proto)
        for i in range(header.proto.package_count):
            restablepackage, buff = AXML_Res_Table_Package.from_axml(buff)
            arsc.proto.restablespackage.append(restablepackage.proto)
            

        return arsc, buff
    
    def convert_id(type_id : int, id : int) -> int:
        """convert id and type to a general id used on AXML file to refer to resources

        Args:
            type_id (int): type of value (xml, string, etc.)
            id (int): index from the list of type value

        Returns:
            int: the id built
        """
        return 0x7f000000 | (type_id & 0xff) << 16 | type_id & 0xff00 | id
    
    def get_id_public(self, package : str, type_ : str, name : str) -> tuple[int, int] | None:
        """get ID public from resource

        Args:
            package (str): package name
            type_ (str): type string
            name (str): name of value

        Returns:
            tuple[int, int] | None: return the id and the stringblock index of the value
        """
        for p in self.proto.restablespackage:
            n2 = p.name.split('\x00')[0]
            if n2 == package:
                for r in p.restypes:
                    if r.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                        for id in range(len(r.typetype.tables)):
                            table = r.typetype.tables[id]
                            index= table.index
                            n = StringBlocks(proto=p.key_sp_string).decode_str(index)
                            t = StringBlocks(proto=p.type_sp_string).decode_str(r.typetype.id-1)
                            if n == name and t == type_:
                                return ARSC.convert_id(r.typetype.id, id), table.key.data
        return None

    
    
    def add_id_public(self, package : str, type_ : str, name : str, path : str):
        for p in self.proto.restablespackage:
            n2 = p.name.split('\x00')[0]
            if n2 == package:
                s = StringBlocks(proto=self.proto.stringblocks)
                id_path = s.get(path)
                self.proto.stringblocks.CopyFrom(s.proto)
                res = AXML_Res_Table_Package(proto=p)
                ret = res.add_id_public(type_, name, id_path)
                return ret
        return None

    def list_packages(self):
        """print all package content
        """
        ret = ""
        general_st = StringBlocks(proto=self.proto.stringblocks)
        for package in self.proto.restablespackage:
            ret += f"{package.name}\n"
            for r in package.restypes:
                if r.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                    for id in range(len(r.typetype.tables)):
                        table = r.typetype.tables[id]
                        index= table.index
                        name = StringBlocks(proto=package.key_sp_string).decode_str(index)
                        type_ = StringBlocks(proto=package.type_sp_string).decode_str(r.typetype.id-1)
                        identifiant = ARSC.convert_id(r.typetype.id, id)
                        #print(table.key.data_type)
                        if table.key.data_type == 3:
                            data = general_st.decode_str(table.key.data)
                        else:
                            data = hex(table.key.data)
                        data_size = table.key.size
                        ret += f"<public type=\"{type_}\" name=\"{name}\" id=\"{hex(identifiant)}\" data={data} data_size={data_size}/>\n"
        return ret
    
    def get_packages(self) -> list[str]:
        """get in a list all package name of the resources.

        Returns:
            list[str]: the list of all packages
        """
        packages = []
        for p in self.proto.restablespackage:
            packages.append(p.name.split('\x00')[0])
        return packages
            
                               

class AXML_Res_Table_Package:

    def __init__(self, proto : axml_pb2.AXML_Res_Table_Package = None):
        """_summary_

        Args:
            proto (axml_pb2.AXML, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.AXML_Res_Table_Package()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self, recursive=True):
        """Compute all fields to have all AXML elements
        """

        if recursive:
            type_sp_string = StringBlocks(proto=self.proto.type_sp_string)
            type_sp_string.compute()
            self.proto.type_sp_string.CopyFrom(type_sp_string.proto)
            
            key_sp_string =  StringBlocks(proto=self.proto.key_sp_string)
            key_sp_string.compute()
            self.proto.key_sp_string.CopyFrom(key_sp_string.proto)

            for restype in self.proto.restypes:
                if restype.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE:
                    t = ARSCResTypeSpec(proto=restype.typespec)
                    t.compute(restype.hnd)
                    restype.typespec.CopyFrom(t.proto)
                elif restype.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                    t = ARSCResTypeType(proto=restype.typetype)
                    t.compute(restype.hnd)
                    restype.typetype.CopyFrom(t.proto)
        
        for restype in self.proto.restypes:
            if restype.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE:
                restype.hnd.size = len(ARSCResTypeSpec(proto=restype.typespec).pack()) + AXML_HEADER_SIZE
            elif restype.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                restype.hnd.size = len(ARSCResTypeType(proto=restype.typetype).pack()) + AXML_HEADER_SIZE #- restype.hnd.header_size + AXML_HEADER_SIZE

        # TODO analyse if it is needed
        type_sp_string = StringBlocks(proto=self.proto.type_sp_string).pack()
        self.proto.typeStrings = self.proto.hnd.header_size
        self.proto.keyStrings = self.proto.typeStrings + len(type_sp_string)
        
        self.proto.hnd.size = len(self.pack())

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        header = AXMLHeader(proto=self.proto.hnd).pack()
        name = self.proto.name.encode('utf-16')[2:]
        name.ljust(256, b"\x00")
        type_sp_string = StringBlocks(proto=self.proto.type_sp_string).pack()
        key_sp_string =  StringBlocks(proto=self.proto.key_sp_string).pack()
        data = b""
        for restype in self.proto.restypes:
            hnd = AXMLHeader(proto=restype.hnd)
            data += hnd.pack()
            if hnd.proto.type == axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE:
                d = ARSCResTypeSpec(proto=restype.typespec).pack()
                data += d
            elif hnd.proto.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                d = ARSCResTypeType(proto=restype.typetype).pack()
                data += d
        return header + pack("<L", self.proto.id) + name + pack("<LLLL", self.proto.typeStrings, self.proto.lastPublicType, self.proto.keyStrings, self.proto.lastPublicKey) + self.proto.padding + type_sp_string + key_sp_string + data
    
    def from_axml(buff):
        content = buff
        res_table_package = AXML_Res_Table_Package()
        header, buff = AXMLHeader.from_axml(buff)
        rest = content[header.proto.size:]
        content = content[:header.proto.size]
        res_table_package.proto.hnd.CopyFrom(header.proto)
        #buff = buff[32-8:]
        res_table_package.proto.id = unpack("<L", buff[:4])[0]
        buff = buff[4:]
        res_table_package.proto.name = buff[:256].decode('utf-16')
        buff = buff[256:]
        res_table_package.proto.typeStrings, res_table_package.proto.lastPublicType, \
            res_table_package.proto.keyStrings, res_table_package.proto.lastPublicKey = \
            unpack("<LLLL", buff[:4*4])
        buff = buff[4*4:]

        t_str_off = len(content[res_table_package.proto.typeStrings:])
        k_str_off = len(content[res_table_package.proto.keyStrings:])
        if t_str_off > k_str_off:
            len_pad = len(buff)-t_str_off
        else:
            len_pad = len(buff)-k_str_off
        res_table_package.proto.padding = buff[:len_pad]

        

        type_sp_string, at = StringBlocks.from_axml(content[res_table_package.proto.typeStrings:])
        res_table_package.proto.type_sp_string.CopyFrom(type_sp_string.proto)

        key_sp_string, ak = StringBlocks.from_axml(content[res_table_package.proto.keyStrings:])
        res_table_package.proto.key_sp_string.CopyFrom(key_sp_string.proto)

        if len(ak) < len(at):
            content = ak
        else:
            content = at
        

        while len(content) > 0:
            hdr, _ = AXMLHeader.from_axml(content)
            spec = axml_pb2.ARSCResType()
            spec.hnd.CopyFrom(hdr.proto)
            if hdr.proto.type == axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE:
                res, _ = ARSCResTypeSpec.from_axml(content[8:hdr.proto.size])
                spec.typespec.CopyFrom(res.proto)
                res_table_package.proto.restypes.append(spec)
            elif hdr.proto.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                res, _ = ARSCResTypeType.from_axml(content[8:hdr.proto.size])
                spec.typetype.CopyFrom(res.proto)
                res_table_package.proto.restypes.append(spec)
            else:
                print("other types ??")
            content = content[hdr.proto.size:]


        return res_table_package, rest
    
    def set_spec_entry(self, id, entry, index):
        for r in self.proto.restypes:
            if r.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE and r.typespec.id == id:
                if len(r.typespec.entries) < index:
                    r.typespec.entries[index] = entry
                else:
                    while index > len(r.typespec.entries):
                        r.typespec.entries.append(0)
                    r.typespec.entries.append(entry)
    
    def add_id_public(self, type_, name, id_path):
        for r in self.proto.restypes:
            if r.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                t = StringBlocks(proto=self.proto.type_sp_string).decode_str(r.typetype.id-1)
                if t == type_:
                    st_key = StringBlocks(proto=self.proto.key_sp_string)
                    spec = ARSCResTableEntry.create_element(st_key.get(name), id_path)
                    self.proto.key_sp_string.CopyFrom(st_key.proto)
                    self.set_spec_entry(r.typetype.id, 0, len(r.typetype.tables))
                    r.typetype.tables.append(spec.proto)
                    return ARSC.convert_id(r.typetype.id, len(r.typetype.tables)-1)
        
        
        st_type = StringBlocks(proto=self.proto.type_sp_string)
        id = st_type.get(type_)
        typetype = ARSCResTypeType.create_element(id=id+1)
        r = axml_pb2.ARSCResType()
        r.hnd.CopyFrom(AXMLHeader(axml_pb2.ResType.RES_TABLE_TYPE_TYPE).proto)
        r.hnd.header_size = 84
        r.typetype.CopyFrom(typetype.proto)
        
        st_key = StringBlocks(proto=self.proto.key_sp_string)
        spec = ARSCResTableEntry.create_element(st_key.get(name), id_path)
        self.proto.key_sp_string.CopyFrom(st_key.proto)
        r.typetype.tables.append(spec.proto)

        r_spec = axml_pb2.ARSCResType()
        r_spec.hnd.CopyFrom(AXMLHeader(axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE).proto)
        r_spec.hnd.header_size = 16
        r_spec.typespec.id = id+1

        self.proto.restypes.append(r_spec)
        self.proto.restypes.append(r)
        self.set_spec_entry(id+1, 0, 0)
        # TODO not appear on Androguard but type exist
        return ARSC.convert_id(r.typetype.id, len(r.typetype.tables)-1)
        

class ARSCResTypeType:

    def __init__(self, proto : axml_pb2.ARSCResTypeType = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCResTypeType, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCResTypeType()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self, hnd : axml_pb2.AXMLHeader, recursive=True):
        """Compute all fields to have all AXML elements
        """
        cur = 0
        index_cur = 0
        for i in self.proto.tables:
            if len(self.proto.entries) <= index_cur:
                self.proto.entries.append(cur)
            else:
                while self.proto.entries[index_cur] == 0xffffffff:
                    index_cur+=1
                self.proto.entries[index_cur] = cur
            index_cur += 1
            cur += len(ARSCResTableEntry(proto=i).pack())
        self.proto.entryCount = len(self.proto.entries)
        self.proto.entryStart = hnd.header_size + 4 * self.proto.entryCount

        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        head = pack("<BBHII", self.proto.id, self.proto.flags, self.proto.reserved, self.proto.entryCount, self.proto.entryStart)
        config = ARSCResTableConfig(proto=self.proto.config).pack()
        data = b""
        for i in self.proto.entries:
            data += pack('<I', i)
        for i in self.proto.tables:
            data += ARSCResTableEntry(proto=i).pack() 
        return head + config + data
    
    def from_axml(buff):
        content = buff
        res_table_typespec = ARSCResTypeType()
        #header, buff = AXMLHeader.from_axml(buff)
        #rest = content[header.proto.size:]
        #res_table_typespec.proto.hnd.CopyFrom(header.proto)
        res_table_typespec.proto.id, res_table_typespec.proto.flags, res_table_typespec.proto.reserved, res_table_typespec.proto.entryCount, res_table_typespec.proto.entryStart  = unpack("<BBHII", buff[:12])
        buff = buff[12:]  
        config, buff = ARSCResTableConfig.from_axml(buff)
        res_table_typespec.proto.config.CopyFrom(config.proto)

        for i in range(res_table_typespec.proto.entryCount):
            res_table_typespec.proto.entries.append(unpack('<I', buff[:4])[0])
            buff = buff[4:]
        
        entrie_cur = buff
        for i in res_table_typespec.proto.entries:
            if i == 0xffffffff:
                continue # TODO handle item with -1 entry
            table, buff = ARSCResTableEntry.from_axml(entrie_cur[i:])
            res_table_typespec.proto.tables.append(table.proto)
        return res_table_typespec, buff
    
    def create_element(id : int):
        typetype = ARSCResTypeType()
        typetype.proto.id = id
        typetype.proto.flags = 0
        typetype.proto.reserved = 0
        typetype.proto.entryCount = 0
        typetype.proto.config.CopyFrom(ARSCResTableConfig().proto)
        typetype.proto.entryStart = AXML_HEADER_SIZE + 64 + 12
        return typetype

class ARSCResTableEntry:

    # If set, this is a complex entry, holding a set of name/value
    # mappings.  It is followed by an array of ResTable_map structures.
    FLAG_COMPLEX = 1

    # If set, this resource has been declared public, so libraries
    # are allowed to reference it.
    FLAG_PUBLIC = 2

    # If set, this is a weak resource and may be overriden by strong
    # resources of the same name/type. This is only useful during
    # linking with other resource tables.
    FLAG_WEAK = 4

    def __init__(self, proto : axml_pb2.ARSCResTableEntry = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCResTableEntry, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCResTableEntry()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self):
        """Compute all fields to have all AXML elements
        """
        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        data = pack('<HHI', self.proto.size, self.proto.flags, self.proto.index)
        if self.is_complex():
            data += ARSCComplex(proto=self.proto.item).pack()
        else:
            data += ARSCResStringPoolRef(proto=self.proto.key).pack()
        
        return  data
    
    def is_public(self) -> bool:
        return (self.proto.flags & self.FLAG_PUBLIC) != 0

    def is_complex(self) -> bool:
        return (self.proto.flags & self.FLAG_COMPLEX) != 0

    def is_weak(self) -> bool:
        return (self.proto.flags & self.FLAG_WEAK) != 0
    
    def create_element(index_name, data):
        spec = ARSCResTableEntry()
        spec.proto.size = 8
        spec.proto.index = index_name
        spec.proto.key.size = 8
        spec.proto.key.data_type = 3
        spec.proto.key.data = data
        return spec
    
    def from_axml(buff):
        content = buff
        table = ARSCResTableEntry()
        table.proto.size, table.proto.flags, table.proto.index = unpack('<HHI', buff[:8])
        buff = buff[8:]
        if table.is_complex():
            item, buff =  ARSCComplex.from_axml(buff)
            table.proto.item.CopyFrom(item.proto)
        else:
            # If FLAG_COMPLEX is not set, a Res_value structure will follow
            key, buff = ARSCResStringPoolRef.from_axml(buff)
            table.proto.key.CopyFrom(key.proto)
        #table.proto.input = buff[8:]
        return table, buff  
    

class ARSCComplex:
   
    def __init__(self, proto : axml_pb2.ARSCComplex = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCComplex, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCComplex()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self):
        """Compute all fields to have all AXML elements
        """
        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        data = pack('<II', self.proto.id_parent, self.proto.count)
        for item in self.proto.items:
            data += pack('<I', item.id)
            data += ARSCResStringPoolRef(proto=item.data).pack()
        return data
    
    def from_axml(buff):
        content = buff
        complex = ARSCComplex()

        complex.proto.id_parent, complex.proto.count = unpack('<II', buff[:8])
        buff = buff[8:]
        # Parse self.count number of `ResTable_map`
        # these are structs of ResTable_ref and Res_value
        # ResTable_ref is a uint32_t.
        for i in range(0, complex.proto.count):
            item = axml_pb2.ItemComplex()
            item.id = unpack('<I', buff[:4])[0]
            buff = buff[4:]
            data, buff = ARSCResStringPoolRef.from_axml(buff)
            item.data.CopyFrom(data.proto)
            complex.proto.items.append(item)

        return complex, buff

class ARSCResStringPoolRef:
   
    def __init__(self, proto : axml_pb2.ARSCResStringPoolRef = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCResStringPoolRef, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCResStringPoolRef()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self):
        """Compute all fields to have all AXML elements
        """
        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        data = pack('<HBBI', self.proto.size, self.proto.res0, self.proto.data_type, self.proto.data)
        return data
    
    def from_axml(buff):
        content = buff
        ref = ARSCResStringPoolRef()

        ref.proto.size, ref.proto.res0, ref.proto.data_type, ref.proto.data  = unpack('<HBBI', buff[:8])
        buff = buff[8:]
        return ref, buff

class ARSCResTableConfig:

    def __init__(self, proto : axml_pb2.ARSCResTableConfig = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCResTableConfig, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCResTableConfig()
            self.proto.size = 64
            self.proto.input = b"\x00" * (64 -16) 
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self):
        """Compute all fields to have all AXML elements
        """
        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        return pack('<IIII', self.proto.size, self.proto.imsi, self.proto.locale, self.proto.screenType) + self.proto.input
    
    def from_axml(buff):
        content = buff
        config = ARSCResTableConfig()
        config.proto.size, config.proto.imsi, config.proto.locale, config.proto.screenType = unpack('<IIII', buff[:16])
        config.proto.input = buff[16:config.proto.size]
        return config, buff[config.proto.size:]

class ARSCResTypeSpec:
    
    def __init__(self, proto : axml_pb2.ARSCResTypeSpec = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCResTypeSpec, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCResTypeSpec()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self, hnd : axml_pb2.AXMLHeader):
        """Compute all fields to have all AXML elements
        """
        self.proto.entryCount = len(self.proto.entries)
        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        data = pack("<BBHI", self.proto.id, self.proto.res0, self.proto.res1, self.proto.entryCount)
        for entry in self.proto.entries:
            data += pack('<I', entry)
        return data
    
    def from_axml(buff):
        content = buff
        res_table_typespec = ARSCResTypeSpec()
        res_table_typespec.proto.id, res_table_typespec.proto.res0, res_table_typespec.proto.res1, res_table_typespec.proto.entryCount  = unpack("<BBHI", buff[:8])
        buff = buff[8:]        
        for i in range(res_table_typespec.proto.entryCount):
            res_table_typespec.proto.entries.append(unpack('<I', buff[:4])[0])
            buff = buff[4:]


        return res_table_typespec, buff


##############################################################################
#
#                              AXML OBJECT
#
##############################################################################

class AXML:

    def __init__(self, proto : axml_pb2.AXML = None):
        """_summary_

        Args:
            proto (axml_pb2.AXML, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
            self.stringblocks = StringBlocks(proto=self.proto.stringblocks)
        else:
            self.proto = axml_pb2.AXML()
            self.stringblocks = StringBlocks()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto

    ###########################################
    #                                         #
    #           ENOCDE from XML               #
    #                                         #
    ###########################################
    
    def from_xml(self, root : etree.ElementBase):
        """Convert Xml to Axml object

        Args:
            root (etree.ElementBase): Xml representation of AXML object
        """
        
        self.add_all_attrib(root)
        self.start_namespace("http://schemas.android.com/apk/res/android", "android")
        self.__from_xml_etree(root)
        self.end_namespace("http://schemas.android.com/apk/res/android", "android")
        self.compute()
   
    
    def __from_xml_etree(self, root : etree.ElementBase):
        """Convert Xml to Axml object internally

        Args:
            root (etree.ElementBase): Xml representation of AXML object
        """
        self.start(root.tag, root.attrib)
        for e in root:
            self.__from_xml_etree(e)
        self.end(root.tag)

    
    def add_xml_elt(self, res_xml : Classical_RES_XML, header_xml : AXMLHeader_RES_XML):
        """Function to add an element in function of the type

        Args:
            res_xml (Classical_RES_XML): Element
            header_xml (AXMLHeader_RES_XML): Header
        """
        res_xml.compute()

        header = header_xml(len(res_xml.content))

        elt = axml_pb2.XMLElement()
        elt.header.CopyFrom(header.proto)
        if type(res_xml.proto) is axml_pb2.ResXMLStartElement:
            elt.start_elt.CopyFrom(res_xml.proto)
        elif type(res_xml.proto) is axml_pb2.ResXMLStartNamespace:
            elt.start_ns.CopyFrom(res_xml.proto)
        elif type(res_xml.proto) is axml_pb2.ResXMLEndNamespace:
            elt.end_ns.CopyFrom(res_xml.proto)
        elif type(res_xml.proto) is axml_pb2.ResXMLEndElement:
            elt.end_elt.CopyFrom(res_xml.proto)
        self.proto.resourcexml.elts.append(elt)

    def start(self, root : str, attrib : dict):
        """Create start of element

        Args:
            root (str): Name of element
            attrib (dict): dict of all attribute of this element
        """
        index = self.stringblocks.get(root)
        i_namespace = self.stringblocks.get("android")
        attributes = []

        dic_attrib = attrib.items()
        for k, v in dic_attrib:
            tmp = k.split('{')
            if len(tmp) > 1:
                tmp = tmp[1].split('}')
                name = self.stringblocks.get(tmp[1])
                namespace = self.stringblocks.get(tmp[0])
            else:
                namespace = 0xffffffff
                name = self.stringblocks.get(k)

            if v == "true":
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x12000000, 1).proto)
            elif v == "false":
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x12000000, 0).proto)
            elif re.search("^@android:[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x1000000, int(v[-8:], 16)).proto)
            elif re.search("^@[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x1000000, int(v[1:], 16)).proto)
            elif re.search("^0x[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x11000000, int(v[2:], 16)).proto)
            else:
                if self.stringblocks.proto.stringblocks[name].data == "versionName":
                    value = self.stringblocks.get(v)
                    attributes.append(Attribute(namespace, name, value, 0x3000008, value).proto)
                elif self.stringblocks.proto.stringblocks[name].data == "compileSdkVersionCodename":
                    value = self.stringblocks.get(v)
                    attributes.append(Attribute(namespace, name, value, 0x3000008, value).proto)
                else:
                    try:
                        value = ctypes.c_uint32(int(v)).value
                        attributes.append(Attribute(namespace, name, 0xffffffff, 0x10000008, value).proto)
                    except ValueError:
                        try:
                            value = unpack('>L', pack('!f', float(v)))[0]
                            attributes.append(Attribute(namespace, name, 0xffffffff, 0x04000008, value).proto)
                        except ValueError:
                            value = self.stringblocks.get(v)
                            attributes.append(Attribute(namespace, name, value, 0x3000008, value).proto)


        content = RES_XML_START_ELEMENT(0xffffffff, index, attributes)
        self.add_xml_elt(content, AXMLHeader_START_ELEMENT)


    def start_namespace(self, prefix : str, uri : str):
        """Create start of namespace

        Args:
            prefix (str): prefix of namespace
            uri (str): uri of namespace
        """
        index = self.stringblocks.get(prefix)
        i_namespace = self.stringblocks.get(uri)


        content = RES_XML_START_NAMESPACE(i_namespace, index)
        self.add_xml_elt(content, AXMLHeader_START_NAMESPACE)

    def end_namespace(self, prefix : str, uri : str):
        """Create end of namespace

        Args:
            prefix (str): prefix of namespace
            uri (str): uri of namespace
        """
        index = self.stringblocks.get(prefix)
        i_namespace = self.stringblocks.get(uri)


        content = RES_XML_END_NAMESPACE(i_namespace, index)
        self.add_xml_elt(content, AXMLHeader_END_NAMESPACE)

    def end(self, attrib : str):
        """Create end of element

        Args:
            attrib (str): name of end element
        """
        index = self.stringblocks.index(attrib)
        i_namespace = self.stringblocks.index("android")

        content = RES_XML_END_ELEMENT(0xffffffff, index)
        self.add_xml_elt(content, AXMLHeader_END_ELEMENT)

    def add_all_attrib(self, root : etree.ElementBase):
        """Create Ressource Map

        Args:
            root (etree.ElementBase): XML representation of AXML
        """
        res = []
        namespace = "{http://schemas.android.com/apk/res/android}"
        queue = [root]
        while len(queue) > 0:
            r = queue.pop()
            for child in r:
                queue.append(child)
            for k in r.attrib.keys():
                if k.startswith(namespace):
                    name = k[len(namespace):]
                    if name in public.SYSTEM_RESOURCES['attributes']['forward']:
                        val = public.SYSTEM_RESOURCES['attributes']['forward'][name]
                        if not val in res:
                            self.stringblocks.get(name)
                            res.append(val)
        self.proto.resourcemap.CopyFrom(ResourceMap(res=res).proto)

    ###########################################
    #                                         #
    #           ENCODE from XML               #
    #                                         #
    ###########################################
    
    def compute(self):
        """Compute all fields to have all AXML elements
        """
        self.stringblocks.compute()
        self.proto.header_xml.CopyFrom(AXMLHeader_XML(len(self.pack())).proto)

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        self.proto.stringblocks.CopyFrom(self.stringblocks.proto)
        sb_pack = self.stringblocks.pack()
        res = ResourceMap(proto=self.proto.resourcemap).pack()
        resxml = RessourceXML(proto=self.proto.resourcexml).pack()
        header_xml = AXMLHeader_XML(proto=self.proto.header_xml).pack()
        return header_xml + sb_pack + res + resxml
    
    def from_axml(buff):
        axml = AXML()
        hnd, buff = AXMLHeader.from_axml(buff)
        sb, buff = StringBlocks.from_axml(buff)
        res, buff = ResourceMap.from_axml(buff)
        resxml, buff = RessourceXML.from_axml(buff)

        axml.proto.header_xml.CopyFrom(hnd.proto)
        axml.proto.stringblocks.CopyFrom(sb.proto)
        axml.stringblocks = sb
        axml.proto.resourcemap.CopyFrom(res.proto)
        axml.proto.resourcexml.CopyFrom(resxml.proto)

        return axml, buff
        

