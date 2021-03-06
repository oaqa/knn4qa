#
# Autogenerated by Thrift Compiler (0.12.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys
import logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
all_structs = []


class Iface(object):
    def getScoresFromParsed(self, query, docs):
        """
        Parameters:
         - query
         - docs

        """
        pass

    def getScoresFromRaw(self, query, docs):
        """
        Parameters:
         - query
         - docs

        """
        pass


class Client(Iface):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def getScoresFromParsed(self, query, docs):
        """
        Parameters:
         - query
         - docs

        """
        self.send_getScoresFromParsed(query, docs)
        return self.recv_getScoresFromParsed()

    def send_getScoresFromParsed(self, query, docs):
        self._oprot.writeMessageBegin('getScoresFromParsed', TMessageType.CALL, self._seqid)
        args = getScoresFromParsed_args()
        args.query = query
        args.docs = docs
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getScoresFromParsed(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getScoresFromParsed_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationException.MISSING_RESULT, "getScoresFromParsed failed: unknown result")

    def getScoresFromRaw(self, query, docs):
        """
        Parameters:
         - query
         - docs

        """
        self.send_getScoresFromRaw(query, docs)
        return self.recv_getScoresFromRaw()

    def send_getScoresFromRaw(self, query, docs):
        self._oprot.writeMessageBegin('getScoresFromRaw', TMessageType.CALL, self._seqid)
        args = getScoresFromRaw_args()
        args.query = query
        args.docs = docs
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getScoresFromRaw(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getScoresFromRaw_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.err is not None:
            raise result.err
        raise TApplicationException(TApplicationException.MISSING_RESULT, "getScoresFromRaw failed: unknown result")


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["getScoresFromParsed"] = Processor.process_getScoresFromParsed
        self._processMap["getScoresFromRaw"] = Processor.process_getScoresFromRaw

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_getScoresFromParsed(self, seqid, iprot, oprot):
        args = getScoresFromParsed_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getScoresFromParsed_result()
        try:
            result.success = self._handler.getScoresFromParsed(args.query, args.docs)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("getScoresFromParsed", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getScoresFromRaw(self, seqid, iprot, oprot):
        args = getScoresFromRaw_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getScoresFromRaw_result()
        try:
            result.success = self._handler.getScoresFromRaw(args.query, args.docs)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except ScoringException as err:
            msg_type = TMessageType.REPLY
            result.err = err
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("getScoresFromRaw", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

# HELPER FUNCTIONS AND STRUCTURES


class getScoresFromParsed_args(object):
    """
    Attributes:
     - query
     - docs

    """


    def __init__(self, query=None, docs=None,):
        self.query = query
        self.docs = docs

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.query = TextEntryParsed()
                    self.query.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.docs = []
                    (_etype10, _size7) = iprot.readListBegin()
                    for _i11 in range(_size7):
                        _elem12 = TextEntryParsed()
                        _elem12.read(iprot)
                        self.docs.append(_elem12)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('getScoresFromParsed_args')
        if self.query is not None:
            oprot.writeFieldBegin('query', TType.STRUCT, 1)
            self.query.write(oprot)
            oprot.writeFieldEnd()
        if self.docs is not None:
            oprot.writeFieldBegin('docs', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.docs))
            for iter13 in self.docs:
                iter13.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.query is None:
            raise TProtocolException(message='Required field query is unset!')
        if self.docs is None:
            raise TProtocolException(message='Required field docs is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(getScoresFromParsed_args)
getScoresFromParsed_args.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, 'query', [TextEntryParsed, None], None, ),  # 1
    (2, TType.LIST, 'docs', (TType.STRUCT, [TextEntryParsed, None], False), None, ),  # 2
)


class getScoresFromParsed_result(object):
    """
    Attributes:
     - success

    """


    def __init__(self, success=None,):
        self.success = success

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.MAP:
                    self.success = {}
                    (_ktype15, _vtype16, _size14) = iprot.readMapBegin()
                    for _i18 in range(_size14):
                        _key19 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val20 = []
                        (_etype24, _size21) = iprot.readListBegin()
                        for _i25 in range(_size21):
                            _elem26 = iprot.readDouble()
                            _val20.append(_elem26)
                        iprot.readListEnd()
                        self.success[_key19] = _val20
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('getScoresFromParsed_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.MAP, 0)
            oprot.writeMapBegin(TType.STRING, TType.LIST, len(self.success))
            for kiter27, viter28 in self.success.items():
                oprot.writeString(kiter27.encode('utf-8') if sys.version_info[0] == 2 else kiter27)
                oprot.writeListBegin(TType.DOUBLE, len(viter28))
                for iter29 in viter28:
                    oprot.writeDouble(iter29)
                oprot.writeListEnd()
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(getScoresFromParsed_result)
getScoresFromParsed_result.thrift_spec = (
    (0, TType.MAP, 'success', (TType.STRING, 'UTF8', TType.LIST, (TType.DOUBLE, None, False), False), None, ),  # 0
)


class getScoresFromRaw_args(object):
    """
    Attributes:
     - query
     - docs

    """


    def __init__(self, query=None, docs=None,):
        self.query = query
        self.docs = docs

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.query = TextEntryRaw()
                    self.query.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.docs = []
                    (_etype33, _size30) = iprot.readListBegin()
                    for _i34 in range(_size30):
                        _elem35 = TextEntryRaw()
                        _elem35.read(iprot)
                        self.docs.append(_elem35)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('getScoresFromRaw_args')
        if self.query is not None:
            oprot.writeFieldBegin('query', TType.STRUCT, 1)
            self.query.write(oprot)
            oprot.writeFieldEnd()
        if self.docs is not None:
            oprot.writeFieldBegin('docs', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.docs))
            for iter36 in self.docs:
                iter36.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.query is None:
            raise TProtocolException(message='Required field query is unset!')
        if self.docs is None:
            raise TProtocolException(message='Required field docs is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(getScoresFromRaw_args)
getScoresFromRaw_args.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, 'query', [TextEntryRaw, None], None, ),  # 1
    (2, TType.LIST, 'docs', (TType.STRUCT, [TextEntryRaw, None], False), None, ),  # 2
)


class getScoresFromRaw_result(object):
    """
    Attributes:
     - success
     - err

    """


    def __init__(self, success=None, err=None,):
        self.success = success
        self.err = err

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.MAP:
                    self.success = {}
                    (_ktype38, _vtype39, _size37) = iprot.readMapBegin()
                    for _i41 in range(_size37):
                        _key42 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val43 = []
                        (_etype47, _size44) = iprot.readListBegin()
                        for _i48 in range(_size44):
                            _elem49 = iprot.readDouble()
                            _val43.append(_elem49)
                        iprot.readListEnd()
                        self.success[_key42] = _val43
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.err = ScoringException()
                    self.err.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('getScoresFromRaw_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.MAP, 0)
            oprot.writeMapBegin(TType.STRING, TType.LIST, len(self.success))
            for kiter50, viter51 in self.success.items():
                oprot.writeString(kiter50.encode('utf-8') if sys.version_info[0] == 2 else kiter50)
                oprot.writeListBegin(TType.DOUBLE, len(viter51))
                for iter52 in viter51:
                    oprot.writeDouble(iter52)
                oprot.writeListEnd()
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.err is not None:
            oprot.writeFieldBegin('err', TType.STRUCT, 1)
            self.err.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(getScoresFromRaw_result)
getScoresFromRaw_result.thrift_spec = (
    (0, TType.MAP, 'success', (TType.STRING, 'UTF8', TType.LIST, (TType.DOUBLE, None, False), False), None, ),  # 0
    (1, TType.STRUCT, 'err', [ScoringException, None], None, ),  # 1
)
fix_spec(all_structs)
del all_structs

