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

def SInt32(data, offset, islittleendian=True):
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

def SInt16(data, offset, islittleendian=True):
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

def SInt8(data, offset, islittleendian=True):
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


def SFix32_16(data, offset, islittleendian=True):
    
    if islittleendian:
        # little endian
        nums = data[offset + 2 : offset + 4]
        fract = data[offset : offset + 2][::-1]

        # print(fract)

        f = 0

        power = -1
        for c in str(bin(int(fract.hex(), base=16)))[2:]:
            f = f + int(c) * (2 ** power)
            power = power - 1

        i, = struct.unpack('<h', nums)
        return i + f
    else:
        # big endian
        nums = data[offset : offset + 2]
        fract = data[offset + 2 : offset + 4]

        f = 0

        power = -1
        for c in str(bin(int(fract.hex(), base=16)))[2:]:
            f = f + int(c) * (2 ** power)
            power = power - 1

        i, = struct.unpack('>h', nums)
        return i + f


def SFix16_8(data, offset, islittleendian=True):
    
    if islittleendian:
        # little endian
        nums = data[offset + 1 : offset + 2]
        fract = data[offset : offset + 1][::-1]

        f = 0

        power = -1
        for c in str(bin(int(fract.hex(), base=16)))[2:]:
            f = f + int(c) * (2 ** power)
            power = power - 1

        i, = struct.unpack('<b', nums)
        return i + f
    else:
        # big endian
        nums = data[offset : offset + 2]
        fract = data[offset + 2 : offset + 4]

        f = 0

        power = -1
        for c in str(bin(int(fract.hex(), base=16)))[2:]:
            f = f + int(c) * (2 ** power)
            power = power - 1

        i, = struct.unpack('>b', nums)
        return i + f

def SFix(data, offset, n_bits=32, n_bits_int=16 ,islittleendian=True):

    num_bytes = int(n_bits / 8)
    
    is_negative = False

    if islittleendian:
        # little endian
        nums = data[offset : offset + num_bytes][::-1]

        f = 0

        nums = str(bin(int(nums.hex(), base=16)))[2:].rjust(n_bits, "0")
        # print(nums)
        if nums[0] == "1":
            is_negative = True
            nums_i = nums[:n_bits_int]
            nums_f = nums[n_bits_int:]
            # print(nums_i)
            # print(nums_f)
            nums = _twos(nums_i) + _ones(nums_f)
        # print(nums)
        power = n_bits_int-2
        for c in nums[1:]:
            f = f + int(c) * (2 ** power)
            power = power - 1

        if is_negative:
            f = f * -1

        return f
    else:
        # big endian
        nums = data[offset : offset + num_bytes]

        f = 0

        nums = str(bin(int(nums.hex(), base=16)))[2:].rjust(n_bits, "0")
        if nums[0] == "1":
            is_negative = True
            nums = _twos(nums)

        power = n_bits_int-2
        for c in nums[1:]:
            f = f + int(c) * (2 ** power)
            power = power - 1

        if is_negative:
            f = f * -1

        return f

def UFix(data, offset, n_bits=32, n_bits_int=16 ,islittleendian=True):

    num_bytes = int(n_bits / 8)
    
    if islittleendian:
        # little endian
        nums = data[offset : offset + num_bytes][::-1]

        f = 0

        power = n_bits_int-1
        for c in str(bin(int(nums.hex(), base=16)))[2:].rjust(n_bits, "0"):
            f = f + int(c) * (2 ** power)
            power = power - 1

        return f
    else:
        # big endian
        nums = data[offset : offset + num_bytes]
        f = 0

        power = n_bits_int-1
        for c in str(bin(int(nums.hex(), base=16)))[2:].rjust(n_bits, "0"):
            f = f + int(c) * (2 ** power)
            power = power - 1

        return f

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

def w_SInt32(data, offset, newdata, islittleendian=True):
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

def w_SInt16(data, offset, newdata, islittleendian=True):
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

def w_SInt8(data, offset, newdata, islittleendian=True):
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

# https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
def _bitstring_to_bytes(s, islittleendian=True):
    if islittleendian:
        return int(s, 2).to_bytes(len(s) // 8, byteorder='little')
    else:
        return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

def w_SFix32_16(data, offset, newdata, islittleendian=True):
    il = 4
    data = bytearray(data)
    if islittleendian:
        # little endian
        if "." in str(newdata):
            nums = str(newdata).split(".")
            fract = nums[1]
            nums = int(nums[0])
            # f = bytearray(2)
            f = ""

            for i in range(16):
                fract = float("0." + fract) * 2
                _f = str(fract).split(".")
                f = f + _f[0]
                fract = _f[1]

            f = _bitstring_to_bytes(f)
        else:
            f = bytearray(2)
            nums = newdata

        i = bytearray(struct.pack('<h', nums))

        bd = f + i

        for i in range(il):
            data[offset+i] = bd[i]

        return data
    else:
        # big endian TODO
        if "." in str(newdata):
            nums = str(newdata).split(".")
            fract = nums[1]
            nums = int(nums[0])
            # f = bytearray(2)
            f = ""

            for i in range(16):
                fract = float("0." + fract) * 2
                _f = str(fract).split(".")
                f = f + _f[0]
                fract = _f[1]

            f = _bitstring_to_bytes(f, False)
        else:
            f = bytearray(2)
            nums = newdata

        i = bytearray(struct.pack('>h', nums))

        bd = i + f

        for i in range(il):
            data[offset+i] = bd[i]

        return data


def w_SFix16_8(data, offset, newdata, islittleendian=True):
    il = 2
    data = bytearray(data)
    if islittleendian:
        # little endian
        if "." in str(newdata):
            nums = str(newdata).split(".")
            fract = nums[1]
            nums = int(nums[0])
            # f = bytearray(2)
            f = ""

            for i in range(8):
                fract = float("0." + fract) * 2
                _f = str(fract).split(".")
                f = f + _f[0]
                fract = _f[1]

            f = _bitstring_to_bytes(f)
        else:
            f = bytearray(1)
            nums = newdata

        i = bytearray(struct.pack('<b', nums))

        bd = f + i

        for i in range(il):
            data[offset+i] = bd[i]

        return data
    else:
        # big endian
        if "." in str(newdata):
            nums = str(newdata).split(".")
            fract = nums[1]
            nums = int(nums[0])
            # f = bytearray(2)
            f = ""

            for i in range(8):
                fract = float("0." + fract) * 2
                _f = str(fract).split(".")
                f = f + _f[0]
                fract = _f[1]

            # f = _bitstring_to_bytes(f, False)
        else:
            f = bytearray(1)
            nums = newdata

        i = bytearray(struct.pack('>b', nums))

        bd = i + f

        for i in range(il):
            data[offset+i] = bd[i]

        return data

def w_SFix(data, offset, newdata, n_bits=32, n_bits_int=16 ,islittleendian=True):

    data = bytearray(data)
    num_bytes = int(n_bits / 8)
    
    is_negative = False
    if newdata < 0:
        is_negative = True
    
    if "." in str(newdata):
        nums = str(newdata).split(".")
        fract = nums[1]
        nums = int(nums[0])
        
        f = ""
        for i in range(n_bits - n_bits_int):
            fract = float("0." + fract) * 2
            _f = str(fract).split(".")
            f = f + _f[0]
            fract = _f[1]
        
        f = f.rjust(n_bits - n_bits_int, "0")
        
    else:
        if is_negative:
            f = "1" * (n_bits - n_bits_int)
        else:
            f = "0" * (n_bits - n_bits_int)
        nums = newdata

    i = ""
    for _ in range(n_bits_int - 1):
        i = i + str(nums % 2)
        nums = int(nums / 2)
        if nums == 0:
            break
    i = i[::-1]
    
    if is_negative:
        
        i = i.rjust(n_bits_int, "0")

        i = _twos(i)

        list_i = list(i)
        list_i[0] = '1'
        i = "".join(list_i)

        _out = (i + _ones(f))
    else:
        i = i.rjust(n_bits_int, "0")

        _out = i + f

    bd = _bitstring_to_bytes(_out, islittleendian)

    for i in range(num_bytes):
        data[offset+i] = bd[i]

    return data

def w_UFix(data, offset, newdata, n_bits=32, n_bits_int=16 ,islittleendian=True):

    data = bytearray(data)
    num_bytes = int(n_bits / 8)

    if "." in str(newdata):
        nums = str(newdata).split(".")
        fract = nums[1]
        nums = int(nums[0])

        f = ""
        for i in range(n_bits - n_bits_int):
            fract = float("0." + fract) * 2
            _f = str(fract).split(".")
            f = f + _f[0]
            fract = _f[1]
        f.rjust(n_bits - n_bits_int, "0")
    else:
        f = "0" * (n_bits - n_bits_int)
        nums = newdata

    i = ""
    for _i in range(n_bits_int):
        i = i + str(nums % 2)
        nums = int(nums / 2)
    i = i[::-1]
    i.rjust(n_bits_int, "0")

    bd = _bitstring_to_bytes((i + f), islittleendian)

    for i in range(num_bytes):
        data[offset+i] = bd[i]

    return data

# s = "OneNice"
# buffer = bytearray(24)
# print(w_UTF8String(buffer, 4 , 16 , s).hex())
def _ones(num):
    s = str(num)
    s = s.replace("1", "_")
    s = s.replace("0", "1")
    s = s.replace("_", "0")
    return s

def _twos(num, reverse=False):
    s = str(num)
    size = len(s)

    s = _ones(s)
    if not reverse:
        if not ("0" in s):
            s = _ones(s)
        else:
            s = (str(bin(int(s, 2)+1)[2:])).rjust(size, "0")
    else:
        if int(s, 2) == 0:
            s = _ones(s)
        else:
            s = (str(bin(int(s, 2)-1))[2:]).rjust(size, "0")
    if len(s) > size:
        return s[len(s)-size:]
        # raise ValueError("todo") #TODO
    # print(int(s2) & b'111111')
    return s

if __name__ == "__main__":
    print(_twos("110011"))
