import struct
import hashlib
import time
import ctypes
from pwn import *

binary_path = "./times"
elf = ELF(binary_path)

libs = elf.libs
libc_path = None
for path in libs:
    if 'libc.so.6' in path:
        libc_path = path
        break

if libc_path is None:
    print("libc 경로를 찾을 수 없습니다.")
    exit()

print(f"바이너리가 사용하는 libc 경로: {libc_path}")

libc = ctypes.CDLL(libc_path)
rand = libc.rand
rand.restype = ctypes.c_int
srand = libc.srand
srand.argtypes = [ctypes.c_uint]

unk_4020 = bytes([
    0x66, 0x0C, 0x4C, 0x86, 0xA6, 0x2C, 0x1C, 0x9C,
    0x1C, 0x66, 0x1C, 0x2C, 0x9C, 0x6C, 0xA6, 0xCC,
    0xA6, 0x6C, 0x6C, 0xAC, 0xA6, 0xA6, 0x86, 0x4C,
    0x2C, 0x46, 0xEC, 0x8C, 0xEC, 0x46, 0x8C, 0x9C,
    0x4C, 0xEC, 0xC6, 0x66, 0x4C, 0x46, 0x86, 0x4C
])

def sub_174A(a1):
    n = a1
    n = ((n & 0x55555555) << 1) | ((n >> 1) & 0x55555555)
    n = ((n & 0x33333333) << 2) | ((n >> 2) & 0x33333333)
    n = ((n & 0x0F0F0F0F) << 4) | ((n >> 4) & 0x0F0F0F0F)
    n = ((n & 0x00FF00FF) << 8) | ((n >> 8) & 0x00FF00FF)
    n = (n << 16) | (n >> 16)
    return n & 0xFFFFFFFF

def reverse_process(unk_4020, word_4048_values):
    v12 = len(unk_4020)
    s_transformed = bytearray(unk_4020)
    current_time = int(time.time())
    time_range = range(current_time - 3600, current_time + 1)
    for seed in time_range:
        for word_4048 in word_4048_values:
            srand(seed)
            v4 = rand()
            v7 = v4 + rand()
            md5_input = struct.pack('<I', v7)
            v15 = hashlib.md5(md5_input).digest()
            s = bytearray(s_transformed)
            for i in range(v12):
                idx = i
                s[idx] ^= v15[(4 * i) % 16]
                s[idx] ^= v15[(4 * i + 1) % 16]
                s[idx] ^= v15[(4 * i + 2) % 16]
                s[idx] ^= v15[(4 * i + 3) % 16]
            for j in range(v12 // 2):
                idx = j * 2
                word = struct.unpack('<H', s[idx:idx+2])[0]
                word ^= word_4048
                s[idx:idx+2] = struct.pack('<H', word)
            srand(seed)
            v5 = rand()
            v7 = v5 + rand()
            md5_input = struct.pack('<I', v7)
            v15 = hashlib.md5(md5_input).digest()
            for k in range(v12):
                idx = k
                s[idx] ^= v15[(4 * k) % 16]
                s[idx] ^= v15[(4 * k + 1) % 16]
                s[idx] ^= v15[(4 * k + 2) % 16]
                s[idx] ^= v15[(4 * k + 3) % 16]
            for m in range(v12 // 4):
                idx = m * 4
                dword = struct.unpack('<I', s[idx:idx+4])[0]
                dword = sub_174A(dword)
                s[idx:idx+4] = struct.pack('<I', dword)
            try:
                recovered_str = s.decode('utf-8')
                if all(32 <= ord(c) <= 126 for c in recovered_str):
                    print(f"시드 {seed}, word_4048 {word_4048}에서 복원된 문자열: {recovered_str}")
                    return recovered_str.encode('utf-8')  # 문자열을 바이트로 변환
            except UnicodeDecodeError:
                continue
    
    print("복원에 실패했습니다.")
    return None

recovered_str = reverse_process(unk_4020, [0x4D2, 0x0])