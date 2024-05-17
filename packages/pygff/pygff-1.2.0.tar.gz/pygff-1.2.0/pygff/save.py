from struct import pack
import numpy as np
import hashlib
import multiprocessing as mp
import threading
import zlib
import pathlib
from .GFF import GFF
from os import PathLike
from typing import Union

from ._util import (
    __special_tag,
    __my_software_version,
    _voxel_type_id_to_type,
)

__all__ = ["save"]


def __default_compression_level():
    return 5


def __save_uint8(bytes, i):
    bytes.write(pack("<B", i))


def __save_int32(bytes, i):
    bytes.write(pack("<i", i))


def __save_int64(bytes, i):
    bytes.write(pack("<q", i))


def __save_uint64(bytes, ui):
    bytes.write(pack("<Q", ui))


def __save_double(bytes, d):
    bytes.write(pack("<d", d))


def __save_float(bytes, f):
    bytes.write(pack("<f", f))


def __save_string(bytes, s):
    """Serialize string into UTF-8 encoded variable length string"""
    s_encoded = s.encode("utf-8")
    __save_uint64(bytes, len(s_encoded))
    bytes.write(s_encoded)


def __save_step_info(bytes, step_info):
    """Serialize StepInfo object."""

    if len(step_info.centers) != len(step_info.widths):
        raise ValueError(
            "Centers ({}) and widths ({}) lengths are not equal.".format(
                len(step_info.centers), len(step_info.widths)
            )
        )

    if step_info.equidistant:
        __save_int32(bytes, 1)
    else:
        __save_int32(bytes, 0)

    __save_int64(bytes, len(step_info.centers))

    le_double = np.dtype(np.double)
    le_double = le_double.newbyteorder("<")

    centers = np.array(step_info.centers, dtype=le_double)
    widths = np.array(step_info.widths, dtype=le_double)

    bytes.write(centers.tobytes("C"))
    bytes.write(widths.tobytes("C"))


class ByteArrayWriteInterface:
    """Wrap bytearray to allow use in functions that use the "write" function to append bytes."""

    def __init__(self):
        self.ba = bytearray()

    def write(self, bytes):
        self.ba.extend(bytes)

    def size(self):
        return len(self.ba)

    def get(self):
        return self.ba


def __get_header_bytes(gff):
    """Serialize information into wrapper, so we know how many bytes are stored therein."""
    header_bytes = ByteArrayWriteInterface()

    if not 0 < len(gff.shape) <= 5:
        raise ValueError(
            f"GFF shape ({gff.shape}) must be 1, 2, 3, 4, or 5 dimensional."
        )

    # header order: X, Y, Z
    __save_int64(header_bytes, int(gff.shape[4]))
    __save_int64(header_bytes, int(gff.shape[3]))
    __save_int64(header_bytes, int(gff.shape[2]))

    vX, vY, vZ = gff.info.voxel_sizes

    __save_double(header_bytes, float(vX))
    __save_double(header_bytes, float(vY))
    __save_double(header_bytes, float(vZ))

    # find and store id for voxel type
    voxel_types_numpy = _voxel_type_id_to_type()
    voxel_type = np.dtype(gff.dtype)
    store_id = 0
    for id, type in voxel_types_numpy.items():
        if voxel_type == type:
            store_id = id
    if store_id == 0:
        raise ValueError("Could not determine voxel type from GFF.")

    __save_int32(header_bytes, store_id)

    scale = float(gff.info.intensity_scale)
    offset = float(gff.info.intensity_offset)

    if scale != 1.0 and offset != 0.0:
        __save_uint8(header_bytes, 1)
    else:
        __save_uint8(header_bytes, 0)

    __save_float(header_bytes, scale)
    __save_float(header_bytes, offset)

    affine = gff.info.affine

    rotation = np.matmul(np.diag(np.reciprocal(gff.info.voxel_sizes)), affine[0:3, 0:3])
    translation = affine[0:3, 3]

    le_double = np.dtype(np.double)
    le_double = le_double.newbyteorder("<")
    header_bytes.write(rotation.astype(le_double, "C").tobytes("C"))
    header_bytes.write(translation.astype(le_double, "C").tobytes("C"))

    __save_step_info(header_bytes, gff.info.times)
    __save_step_info(header_bytes, gff.info.channels)

    compression_methods = {"raw": 0, "zlib": 1}

    # Hardcode to use zlib compression on store
    compression_method = "zlib"  # header.get('compression_method', 'zlib')

    # if not compression_method in compression_methods:
    #    raise ValueError("Unknown compression method '{}'".format(compression_method))

    __save_int32(header_bytes, compression_methods[compression_method])
    # __save_int32(header_bytes, int(header.get('compression_level', 5)))
    __save_int32(header_bytes, __default_compression_level())
    __save_int32(header_bytes, __special_tag())  # Header end tag

    return header_bytes


def __save_header(bytes, gff):
    """Save header information to bytes object"""

    __save_int32(bytes, __special_tag())  # Store header magic
    __save_int32(bytes, __my_software_version())  # Format version of writing program
    __save_int32(
        bytes, __my_software_version()
    )  # Required format version for reader of this file

    header_bytes = __get_header_bytes(gff)

    # Store header size to file
    # 3 * 4 = 12 bytes before header size, 8 bytes for header size itself
    __save_int64(bytes, header_bytes.size() + 12 + 8)
    bytes.write(header_bytes.get())


def __save_dict(bytes, dict):
    """Serialize a dictionary to *bytes*."""
    __save_int64(bytes, len(dict))
    for key, value in dict.items():
        __save_string(bytes, key)
        __save_string(bytes, value)


def __save_metas(bytes, metas):
    """Serialize meta information (dictionary of dictionaries) to *bytes*."""
    __save_int32(bytes, len(metas))

    for key, value in metas.items():
        __save_string(bytes, key)
        __save_dict(bytes, value)


class HashingBytes:
    """Directly update hash with written bytes."""

    def __init__(self, bytes):
        self.bytes = bytes
        self.hash = hashlib.sha256()

    def write(self, bytes):
        self.bytes.write(bytes)
        self.hash.update(bytes)

    def tell(self):
        return self.bytes.tell()

    def digest(self):
        return self.hash.digest()

    def update(self, bytes):
        self.hash.update(bytes)


def __compute_slice_hash_and_compress(hashes, indices, compressed_slices, slice_view):
    """Compress slices and compute their compressed hash as specified in *indices*."""

    for i in indices:
        bytes = np.ascontiguousarray(slice_view[i, :, :]).view(dtype=np.uint8)

        hash = hashlib.sha256()
        compressor = zlib.compressobj(
            __default_compression_level(),
            wbits=15,
            memLevel=9,
            strategy=zlib.Z_DEFAULT_STRATEGY,
        )
        compressed = bytearray()

        chunk_size = 512**2
        for offset in range(0, len(bytes), chunk_size):
            rem = min(len(bytes) - offset, chunk_size)

            chunk = memoryview(bytes)[offset : offset + rem]
            compressed_chunk = compressor.compress(chunk)
            compressed.extend(compressed_chunk)
            hash.update(compressed_chunk)

        compressed_chunk = compressor.flush()
        compressed.extend(compressed_chunk)
        hash.update(compressed_chunk)

        compressed_slices[i] = compressed
        hashes[i] = hash.digest()


def __get_compressed_slices_and_hashes(gff):
    slice_count = gff.shape[0] * gff.shape[1] * gff.shape[2]  # dimC * dimT * dimZ
    if slice_count <= 0 or len(gff.shape) < 3:
        raise ValueError(
            "Invalid shape: {}\nAt least 3 dimensions are required.".format(gff.shape)
        )

    # reshape 5D to 3D for compression and storage
    slices = np.reshape(gff, (slice_count, gff.shape[3], gff.shape[4]))

    num_cpus = max(int(mp.cpu_count()), 1)
    task_size = slice_count
    num_cpus = min(task_size, num_cpus)

    hashes = [0] * task_size
    compressed_slices = [None] * task_size

    slice_view = slices.view()

    threads = []
    for i in range(num_cpus):
        local_indices = range(
            task_size * i // num_cpus, task_size * (i + 1) // num_cpus
        )
        thread = threading.Thread(
            target=__compute_slice_hash_and_compress,
            args=(hashes, local_indices, compressed_slices, slice_view),
        )
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    return compressed_slices, hashes


def __get_offsets(compressed_slices):
    """Computes byte offsets into compressed slices"""
    offsets = np.roll(
        np.cumsum(np.array([len(x) for x in compressed_slices], dtype=np.int64)), 1
    )
    offsets[0] = 0
    # Add 8 byte offsets for each compressed slice to account for C++ legacy offsets
    offsets = np.add(offsets, np.array(range(1, len(offsets) + 1)) * 8)
    return offsets


def __save_bytes_like(bytes, gff):
    hashing_bytes = HashingBytes(bytes)

    # ensure gff is 5D with shape (c, t, z, y, x)
    if len(gff.shape) == 1:
        gff = np.reshape(gff, (1, 1, 1, 1, gff.shape[0]))
    elif len(gff.shape) == 2:
        gff = np.reshape(gff, (1, 1, 1, gff.shape[0], gff.shape[1]))
    elif len(gff.shape) == 3:
        gff = np.reshape(gff, (1, 1, gff.shape[0], gff.shape[1], gff.shape[2]))
    elif len(gff.shape) == 4:
        gff = np.reshape(
            gff, (1, gff.shape[0], gff.shape[1], gff.shape[2], gff.shape[3])
        )
    gff.info._correct_times_and_channels(gff.shape)

    __save_header(hashing_bytes, gff)
    __save_metas(hashing_bytes, gff.info.meta)

    compressed_slices, slice_hashes = __get_compressed_slices_and_hashes(gff)

    # slice_count
    __save_uint64(hashing_bytes, len(compressed_slices))

    offsets = __get_offsets(compressed_slices)

    le_int64 = np.dtype(np.int64)
    le_int64 = le_int64.newbyteorder("<")

    # Write slice_starts
    hashing_bytes.write(memoryview(offsets.astype(dtype=le_int64).view(dtype=np.uint8)))

    # slice_lengths_count
    __save_uint64(hashing_bytes, len(compressed_slices))

    # Write slice_lengths
    hashing_bytes.write(
        memoryview(
            np.array([len(slice) for slice in compressed_slices])
            .astype(dtype=le_int64)
            .view(dtype=np.uint8)
        )
    )

    # Write slices
    for compressed_slice in compressed_slices:
        # Store slice size for compatibility with legacy C++ code
        __save_uint64(bytes, len(compressed_slice))
        bytes.write(compressed_slice)

    for slice_hash in slice_hashes:
        hashing_bytes.update(slice_hash)

    # hash_name
    __save_string(hashing_bytes, "sha256")

    file_size_until_here = hashing_bytes.tell()
    __save_int64(hashing_bytes, file_size_until_here)

    file_digest = hashing_bytes.digest()
    __save_uint64(bytes, len(file_digest))
    bytes.write(file_digest)

    # Signal nonexisting timestamp
    __save_string(bytes, "No Timestamp")


def save(path_or_byteslike: Union[str, bytes, PathLike], gff: GFF):
    """Saves a GFF object as a .gff/.segff file."""

    write, tell = [getattr(path_or_byteslike, x, None) for x in ["write", "tell"]]
    if callable(write) and callable(tell):  # bytes
        __save_bytes_like(path_or_byteslike, gff)
    else:  # filepath
        if pathlib.Path(path_or_byteslike).suffix == ".segff":
            gff.info.set_class_dict({})
            gff = gff.astype(np.uint8)
        with open(path_or_byteslike, "wb") as f:
            __save_bytes_like(f, gff)
