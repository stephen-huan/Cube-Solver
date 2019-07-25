#with open("testing.txt", "wb") as binary_file:
#    # Write text or bytes to the file
#    binary_file.write("Write text by encoding\n".encode('utf8'))
#    num_bytes_written = binary_file.write(b'\xDE\xAD\xBE\xEF')
#    print("Wrote %d bytes." % num_bytes_written)

import numpy
filename = "testing.txt"
Bytes = numpy.fromfile(filename, dtype = "uint8")
Bits = numpy.unpackbits(Bytes)
print(Bytes, Bits)
print(type(Bytes[0]), type(Bits[0]))