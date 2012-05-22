#
# Provides base functions for manipulating files. 
import mmap
from header import Header, leap_year
import numpy as np
import sys
import struct
import ctypes



class VarLenRec():
    def __init__(self, reader):
        self.Reserved = reader.ReadWords("<H", 1, 2)
        self.UserID = "".join(reader.ReadWords("<s",16,1))
        self.RecordID = reader.ReadWords("<H", 1,2)
        self.RecLenAfterHeader = reader.ReadWords("<H",1,2)
        self.Description = "".join(reader.ReadWords("<s",32,1))

class Reader():
    def __init__(self,filename):
        self.Header = False
        self.VLRs = False
        self.bytesRead = 0
        self.filename = filename
        self.fileref = open(filename, "r+b")
        self._map = mmap.mmap(self.fileref.fileno(), 0)
        self.bytesRead = 0
        self.GetHeader()
        self.populateVLRs()
        self.X = False
        self.Y = False
        self.Z = False
        self.PointRefs = False
        return
    
    def close(self):
        self._map.close()
        return

    def read(self, bytes):
        self.bytesRead += bytes
        return(self._map.read(bytes))
    
    def reset(self):
        self._map.close()
        self.fileref.close()
        self.fileref = open(self.filename, "rb")
        self._map = mmap.mmap(self.fileref.fileno(), 0)
        return
     
    def seek(self, bytes):
        # Seek relative to current pos
        self._map.seek(bytes,1)

    def ReadWords(self, fmt, num, bytes):
        outData = []
        for i in xrange(num):
            dat = self.read(bytes)
            outData.append(struct.unpack(fmt, dat)[0])
        if len(outData) > 1:
            return(outData)
        return(outData[0])


    def GetHeader(self):
        ## Why is this != neccesary?
        if self.Header != False:
            return(self.Header)
        else:
            self.Header = Header(self)
    
    def populateVLRs(self):
        self.VLRs = []
        for i in xrange(self.Header.NumVariableLenRecs):
            self.VLRs.append(VarLenRec(self))
            self.seek(self.VLRs[-1].RecLenAfterHeader)
            if self._map.tell() > self.Header.data_offset:
                raise Exception("Error, Calculated Header Data "
                    "Overlaps The Point Records!")
        self.VLRStop = self._map.tell()
        return

    def GetVLRs(self):
        # This return needs to be modified
        return(self.VLRs)
    
    def get_padding(self):
        return(self.Header.data_offset - self.VLRStop)

    def get_pointrecordscount(self):
        if self.Header.get_version != "1.3": 
            return((self._map.size()-self.Header.data_offset)/self.Header.data_record_length)
        return((self.Header.StWavefmDatPktRec - self.Header.data_offset)/self.Header.data_record_length)       

    def SetInputSRS(self):
        pass
    
    def SetOutputSRS(self):
        pass

    def close(self):
        pass

    def GetRawPointIndex(self,index):
        return(self.Header.data_offset + 
            index*self.Header.data_record_length)

    def GetRawPoint(self, index):
        start = (self.Header.data_offset + 
            index * self.Header.data_record_length)
        return(self._map[start : start +
             self.Header.data_record_length])

    def GetPoint(self, index):
        pass
    
    def GetNextPoint(self):
        pass

    def buildPointRefs(self):
        pts = self.get_pointrecordscount()
        self.PointRefs = np.array([self.GetRawPointIndex(i) for i in xrange(pts)])
        return

    def GetDimension(self,offs, fmt, length):
        if type(self.PointRefs) == bool:
            self.buildPointRefs()            
        return(map(lambda x: struct.unpack(fmt, 
            self._map[x+offs:x+offs+length]),self.PointRefs))
    
                

    def GetX(self, scale=False):
        return(self.GetDimension(0,"<L",4))
       
    def GetY(self, scale=False):
        return(self.GetDimension(4,"<L",4))

    def GetZ(self, scale=False):
        return(self.GetDimension(8,"<L",4))
    
    ## To Be Implemented
    
    def GetIntensity(self):
        pass
    
    def GetFlagByte(self):
        pass
    
    def GetClassification(self):
        pass
    
    def GetScanAngleRank(self):
        pass
    
    def GetUserData(self):
        pass 
    
    def GetPTSrcId(self):
        pass
    
    def GetGPSTime(self):
        pass
    
    def GetRed(self):
        pass
    
    def GetGreen(self):
        pass
    
    def GetBlue(self):
        pass

    def GetWavePacketDescpIdx(self):
        pass

    def GetByteOffsetToWaveFmData(self):
        pass

    def GetWavefmPktSize(self):
        pass

    def GetX_t(self):
        pass

    def GetY_t(self):
        pass

    def GetZ_t(self):
        pass





class Writer():
    def __init__(self,filename):
        pass

    def close(self):
        pass

    def get_header(self):
        pass
       




def CreateWithHeader(filename, header):
    pass
