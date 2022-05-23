def _crc8(data: bytes) -> bytes:
  crc = 0

  for byte in data:
    crc ^= byte
    for _ in range(8):
      if crc & 0x01:
        crc = (crc >> 1) ^ 0x8C
      else:
        crc >>= 1
    crc &= 0xFF
  return bytes([crc])