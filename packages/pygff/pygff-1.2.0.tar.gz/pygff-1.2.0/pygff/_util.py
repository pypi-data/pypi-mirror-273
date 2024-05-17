import numpy as np


def __special_tag():
    """Header magic that marks the begin of the file and the end of the old header. Stored as 32bit signed integer."""
    return 772824


## From reference implementation:
# VoxelTypeUNKNOWN = 0, // Types need to be incrementally numbered
# VoxelTypeCHAR,        // 1
# VoxelTypeUCHAR,       // 2
# VoxelTypeSHORT,       // 3
# VoxelTypeUSHORT,      // 4
# VoxelTypeINT,         // 5
# VoxelTypeUINT,        // 6
# VoxelTypeFLOAT,       // 7
# VoxelTypeDOUBLE,      // 8
# VoxelTypeINT64,       // 9
# VoxelTypeUINT64,      // 10
# VoxelTypeUCHAR3,      // 11 # NOT SUPPORTED
# VoxelTypeUCHAR4,      // 12 # NOT SUPPORTED
# VoxelTypeDOUBLE3,     // 13 # NOT SUPPORTED
# VoxelTypeHALF,        // 14


def _voxel_type_id_to_type():
    voxel_type_numpy = {
        1: np.int8,
        2: np.uint8,
        3: np.int16,
        4: np.uint16,
        5: np.int32,
        6: np.uint32,
        7: np.float32,
        8: np.float64,
        9: np.int64,
        10: np.uint64,
        14: np.float16,
    }
    return voxel_type_numpy


def __old_storage_software_version():
    """Software version until ( inclusive ) which storage of slices was broken."""
    return int.from_bytes([0, 5, 0, 7], byteorder="little", signed=False)


def __my_software_version():
    """Software version bytes interpreted as 32bit unsigned integer."""
    return int.from_bytes([0, 5, 0, 8], byteorder="little", signed=False)
