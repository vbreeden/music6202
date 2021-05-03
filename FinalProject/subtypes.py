from dataclasses import dataclass, field

@dataclass
class Subtype:
    subtype_bitrate_map = {
        'PCM_U8':    8,  # Unsigned 8 bit data (WAV and RAW only)
        'PCM_16':    16,  # Signed 16 bit data
        'PCM_24':    24,  # Signed 24 bit data      
        'FLOAT':     32,  # 32 bit float data
        'DOUBLE':    64  # 64 bit float data
    }
    bitrate_subtype_map = {
            '8'  :'PCM_U8', # Signed 8 bit data
            '16' :'PCM_16',  # Signed 16 bit data
            '24' :'PCM_24',  # Signed 24 bit data
            '32' :'FLOAT',  # 32 bit float data
            '64' :'DOUBLE' # 64 bit float data     
    }
    def get_bit_rate(self, subtype):
        return self.subtype_bitrate_map[subtype] 
        
    def get_subtype(self, bitrate):
        return self.bitrate_subtype_map[str(bitrate)] 



