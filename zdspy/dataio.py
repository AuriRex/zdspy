# E
import struct

def ReadFile(filename):
    file_content: bytearray
    with open(filename, "rb") as binary_file:
        # Read the whole file at once
        file_content = bytearray(binary_file.read())
    return file_content

def Decode(data: bytearray) -> str:
    return bytearray(reversed(data)).decode()

def Encode(data: str) -> bytearray:
    return bytearray(reversed(data.encode()))

# 
def w_UTF8String(data: bytearray, offset: int, length: int, string: str) -> bytearray:
    """Write the str `string` into the bytearray `data` at offset `offset` with length `length` using the UTF-8 encoding."""

    if len(string) > length:
        print("[WARNING] String too long for valid space: "+str(length)+" - string truncated!")
        string = string[:length]
    data[offset:offset+len(string)] = string.encode()
    return data


def _Int(data: bytearray, offset: int, is_little_endian: bool=True, number_of_bytes: int=1, is_signed: bool=True) -> int:
    pack_fmt = _get_pack_fmt(number_of_bytes, is_little_endian, is_signed)

    nums = data[offset: offset+number_of_bytes]

    value, = struct.unpack(pack_fmt, nums)

    return value

def UInt32(data: bytearray, offset: int, is_little_endian: bool=True) -> int:
    number_of_bytes = 4
    return _Int(data, offset, is_little_endian, number_of_bytes, is_signed=False)

def UInt16(data: bytearray, offset: int, is_little_endian: bool=True) -> int:
    number_of_bytes = 2
    return _Int(data, offset, is_little_endian, number_of_bytes, is_signed=False)

def UInt8(data: bytearray, offset: int, is_little_endian: bool=True) -> int:
    number_of_bytes = 1
    return _Int(data, offset, is_little_endian, number_of_bytes, is_signed=False)

def SInt32(data: bytearray, offset: int, is_little_endian: bool=True) -> int:
    number_of_bytes = 4
    return _Int(data, offset, is_little_endian, number_of_bytes, is_signed=True)

def SInt16(data: bytearray, offset: int, is_little_endian: bool=True) -> int:
    number_of_bytes = 2
    return _Int(data, offset, is_little_endian, number_of_bytes, is_signed=True)

def SInt8(data: bytearray, offset: int, is_little_endian: bool=True) -> int:
    number_of_bytes = 1
    return _Int(data, offset, is_little_endian, number_of_bytes, is_signed=True)

def SFix(data, offset, n_bits=32, n_bits_int=16 ,islittleendian=True) -> float:

    num_bytes = int(n_bits / 8)
    
    is_negative = False

    if islittleendian:
        # little endian
        nums = data[offset : offset + num_bytes][::-1]

        f: float = 0.0

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

        f: float = 0.0

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

def UFix(data, offset, n_bits=32, n_bits_int=16 ,islittleendian=True) -> float:

    num_bytes = int(n_bits / 8)
    
    if islittleendian:
        # little endian
        nums = data[offset : offset + num_bytes][::-1]

        f: float = 0.0

        power = n_bits_int-1
        for c in str(bin(int(nums.hex(), base=16)))[2:].rjust(n_bits, "0"):
            f = f + int(c) * (2 ** power)
            power = power - 1

        return f
    else:
        # big endian
        nums = data[offset : offset + num_bytes]
        f: float = 0.0

        power = n_bits_int-1
        for c in str(bin(int(nums.hex(), base=16)))[2:].rjust(n_bits, "0"):
            f = f + int(c) * (2 ** power)
            power = power - 1

        return f


def _w_Int(data: bytearray, offset: int, value: int, is_little_endian=True, number_of_bytes=1, is_signed=True) -> bytearray:
    pack_fmt = _get_pack_fmt(number_of_bytes, is_little_endian, is_signed)

    packed_value = bytearray(struct.pack(pack_fmt, value))

    for i in range(number_of_bytes):
        data[offset+i] = packed_value[i]

    return data

def w_UInt32(data: bytearray, offset: int, value: int, is_little_endian: bool=True) -> bytearray:
    number_of_bytes = 4
    data = bytearray(data)
    return _w_Int(data, offset, value, is_little_endian, number_of_bytes, is_signed=False)

def w_UInt16(data: bytearray, offset: int, value: int, is_little_endian: bool=True) -> bytearray:
    number_of_bytes = 2
    data = bytearray(data)
    return _w_Int(data, offset, value, is_little_endian, number_of_bytes, is_signed=False)

def w_UInt8(data: bytearray, offset: int, value: int, is_little_endian: bool=True) -> bytearray:
    number_of_bytes = 1
    data = bytearray(data)
    return _w_Int(data, offset, value, is_little_endian, number_of_bytes, is_signed=False)


def w_SInt32(data: bytearray, offset: int, value: int, is_little_endian: bool=True) -> bytearray:
    number_of_bytes = 4
    data = bytearray(data)
    return _w_Int(data, offset, value, is_little_endian, number_of_bytes, is_signed=True)

def w_SInt16(data: bytearray, offset: int, value: int, is_little_endian: bool=True) -> bytearray:
    number_of_bytes = 2
    data = bytearray(data)
    return _w_Int(data, offset, value, is_little_endian, number_of_bytes, is_signed=True)

def w_SInt8(data: bytearray, offset: int, value: int, is_little_endian: bool=True) -> bytearray:
    number_of_bytes = 1
    data = bytearray(data)
    return _w_Int(data, offset, value, is_little_endian, number_of_bytes, is_signed=True)

# https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
def _bitstring_to_bytes(s: str, is_little_endian: bool=True) -> bytearray:
    if is_little_endian:
        return int(s, 2).to_bytes(len(s) // 8, byteorder='little')
    else:
        return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

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


_NUMBER_OF_BYTES_TO_STRUCT_CHARACTER = {
    1: "B",
    2: "H",
    4: "I"
}

def _get_pack_fmt(number_of_bytes: int, is_little_endian: bool, is_signed: bool) -> str:
    endianess_symbol = "<" if is_little_endian else ">"
    pack_fmt = endianess_symbol + (_NUMBER_OF_BYTES_TO_STRUCT_CHARACTER[number_of_bytes].lower() if is_signed else _NUMBER_OF_BYTES_TO_STRUCT_CHARACTER[number_of_bytes])
    return pack_fmt

def _ones(num) -> str:
    s = str(num)
    s = s.replace("1", "_")
    s = s.replace("0", "1")
    s = s.replace("_", "0")
    return s

def _twos(num, reverse=False) -> str:
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
    return s

if __name__ == "__main__":
    #print(_twos("110011"))
    import old_dataio as od

    datanew = bytearray(7)
    dataold = bytearray(7)

    print(175)
    datanew = w_UInt8(datanew, 0, 175, False)
    dataold = od.w_UInt8(dataold, 0, 175, False)

    print(48830)
    datanew = w_UInt16(datanew, 1, 48830, False)
    dataold = od.w_UInt16(dataold, 1, 48830, False)

    print(-305419896)
    datanew = w_SInt32(datanew, 3, -305419896, True)
    dataold = od.w_SInt32(dataold, 3, -305419896, True)

    print(datanew.hex())
    print(dataold.hex())

    print("1: " + UInt8(datanew, 0, False).__str__())
    print("1: " + od.UInt8(dataold, 0, False).__str__())

    print("2: " + UInt16(datanew, 1, False).__str__())
    print("2: " + od.UInt16(dataold, 1, False).__str__())

    print("4: " + SInt32(datanew, 3, True).__str__())
    print("4: " + od.SInt32(dataold, 3, True).__str__())
    
    #48830
    #3452816845
    #305419896
    
