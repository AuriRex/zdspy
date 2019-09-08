# E
import struct

def ReadFile(filename):
        with open(filename, "rb") as binary_file:
                # Read the whole file at once
                return bytearray(binary_file.read())

def Decode(data):
        return bytearray(reversed(data)).decode()

def Encode(data):
        return bytearray(reversed(data.encode()))

# Write UTF-8 String "string" into data "data" at offset "offset" with zeroed out length "length"
def w_UTF8String(data, offset, length, string):
        if len(string) > length:
                print("[ERROR] String too long for valid space: "+str(length))
                return bytearray(length)
        data[offset:offset+len(string)] = string.encode()
        return data
        

def UInt32(data, offset, islittleendian=True):
        nums = data[offset: offset+4]
        # print(nums)
        if islittleendian:
                # little endian
                i, = struct.unpack('<I', nums)
                return i
        else:
                # big endian
                i, = struct.unpack('>I', nums)
                return i

def UInt16(data, offset, islittleendian=True):
        nums = data[offset: offset+2]
        # print(nums)
        if islittleendian:
                # little endian
                i, = struct.unpack('<H', nums)
                return i
        else:
                # big endian
                i, = struct.unpack('>H', nums)
                return i

def UInt8(data, offset, islittleendian=True):
        nums = data[offset: offset+1]
        # print(nums)
        if islittleendian:
                # little endian
                i, = struct.unpack('<B', nums)
                return i
        else:
                # big endian
                i, = struct.unpack('>B', nums)
                return i

def Int32(data, offset, islittleendian=True):
        nums = data[offset: offset+4]
        # print(nums)
        if islittleendian:
                # little endian
                i, = struct.unpack('<i', nums)
                return i
        else:
                # big endian
                i, = struct.unpack('>i', nums)
                return i

def Int16(data, offset, islittleendian=True):
        nums = data[offset: offset+2]
        # print(nums)
        if islittleendian:
                # little endian
                i, = struct.unpack('<h', nums)
                return i
        else:
                # big endian
                i, = struct.unpack('>h', nums)
                return i

def Int8(data, offset, islittleendian=True):
        nums = data[offset: offset+1]
        # print(nums)
        if islittleendian:
                # little endian
                i, = struct.unpack('<b', nums)
                return i
        else:
                # big endian
                i, = struct.unpack('>b', nums)
                return i

def w_UInt32(data, offset, newdata, islittleendian=True):
        il = 4
        data = bytearray(data)
        if islittleendian:
                # little endian
                bd = bytearray(struct.pack('<I', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data
        else:
                # big endian
                bd = bytearray(struct.pack_into('>I', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data

def w_UInt16(data, offset, newdata, islittleendian=True):
        il = 2
        data = bytearray(data)
        if islittleendian:
                # little endian
                bd = bytearray(struct.pack('<H', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data
        else:
                # big endian
                bd = bytearray(struct.pack_into('>H', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data

def w_UInt8(data, offset, newdata, islittleendian=True):
        il = 1
        data = bytearray(data)
        if islittleendian:
                # little endian
                bd = bytearray(struct.pack('<B', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data
        else:
                # big endian
                bd = bytearray(struct.pack_into('>B', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data

def w_Int32(data, offset, newdata, islittleendian=True):
        il = 4
        data = bytearray(data)
        if islittleendian:
                # little endian
                bd = bytearray(struct.pack('<i', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data
        else:
                # big endian
                bd = bytearray(struct.pack_into('>i', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data

def w_Int16(data, offset, newdata, islittleendian=True):
        il = 2
        data = bytearray(data)
        if islittleendian:
                # little endian
                bd = bytearray(struct.pack('<h', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data
        else:
                # big endian
                bd = bytearray(struct.pack_into('>h', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data

def w_Int8(data, offset, newdata, islittleendian=True):
        il = 1
        data = bytearray(data)
        if islittleendian:
                # little endian
                bd = bytearray(struct.pack('<b', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data
        else:
                # big endian
                bd = bytearray(struct.pack_into('>b', newdata))

                for i in range(il):
                        data[offset+i] = bd[i]

                return data
# s = "OneNice"
# buffer = bytearray(24)
# print(w_UTF8String(buffer, 4 , 16 , s).hex())
