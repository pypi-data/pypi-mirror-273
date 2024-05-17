from pygff import GFF, StepInfo, GFFInfo
from struct import unpack
import numpy as np
import hashlib
import multiprocessing as mp
import threading
import zlib
import os

from ._util import (
    __special_tag,
    __my_software_version,
    __old_storage_software_version,
    _voxel_type_id_to_type,
)

__all__ = ["load"]


def __load_int(bytes, length, signed=True):
    """Loads a signed / unsiged ( *signed* => True/False ) integer of *length* bytes from *bytes*."""
    return int.from_bytes(bytes.read(length), byteorder="little", signed=signed)


def __load_int32(bytes):
    return __load_int(bytes, 4)


def __load_int64(bytes):
    return __load_int(bytes, 8)


def __load_uint64(bytes):
    return __load_int(bytes, 8, signed=False)


def __load_double(bytes):
    return unpack("<d", bytes.read(8))[0]


def __load_float(bytes):
    return unpack("<f", bytes.read(4))[0]


def __load_string(bytes):
    """Deserialize UTF-8 encoded variable length string from *bytes*."""
    size = __load_uint64(bytes)
    return bytes.read(size).decode("utf-8")


def __load_step_info(bytes):
    """Deserialize StepInfo object."""
    equidistant = __load_int32(bytes) != 0
    number_of_timepoints = __load_int64(bytes)

    le_double = np.dtype(np.double)
    le_double = le_double.newbyteorder("<")
    centers = np.frombuffer(bytes.read(8 * number_of_timepoints), le_double)
    widths = np.frombuffer(bytes.read(8 * number_of_timepoints), le_double)

    return StepInfo(equidistant, centers, widths)


def __load_header(bytes):
    """Load and parse header information which is returned as a dictionary."""
    tag = __load_int32(bytes)
    if tag != __special_tag():
        raise ValueError("Invalid header magic.")

    # Populate dictionary with values from header
    header = {}
    version = __load_int32(bytes)  # Version of writing program

    header["file_version"] = version

    required_version = __load_int32(bytes)
    if __my_software_version() < required_version:
        raise ValueError("Data format too new.")
    header_bytes = __load_int64(bytes)

    header["dimX"] = __load_int64(bytes)
    header["dimY"] = __load_int64(bytes)
    header["dimZ"] = __load_int64(bytes)

    header["vX"] = __load_double(bytes)
    header["vY"] = __load_double(bytes)
    header["vZ"] = __load_double(bytes)

    header["voxel_sizes"] = np.array([header["vX"], header["vY"], header["vZ"]])

    voxel_type = __load_int32(bytes)
    voxel_type_numpy = _voxel_type_id_to_type()

    if not (voxel_type in voxel_type_numpy):
        raise ValueError("Invalid voxel type identifier '{}'".format(voxel_type))

    header["voxel_type"] = voxel_type_numpy[voxel_type]

    header["has_scale"] = __load_int(bytes, 1, False) > 0
    header["intensity_scale"] = __load_float(bytes)
    header["intensity_offset"] = __load_float(bytes)

    le_double = np.dtype(np.double)
    le_double = le_double.newbyteorder("<")
    header["rotation"] = np.reshape(
        np.frombuffer(bytes.read(8 * 9), le_double), [3, 3], order="C"
    )
    header["translation"] = np.reshape(
        np.frombuffer(bytes.read(8 * 3), le_double), [3, 1], order="C"
    )

    header["times"] = __load_step_info(bytes)
    header["channels"] = __load_step_info(bytes)

    header["dimT"] = max(header["times"].len(), 1)
    header["dimC"] = max(header["channels"].len(), 1)

    compression_methods = {0: "raw", 1: "zlib"}

    compression_method = __load_int32(bytes)
    if not compression_method in compression_methods:
        raise ValueError(
            "Unknown compression method id ({})".format(compression_method)
        )

    header["compression_method"] = compression_methods[compression_method]
    header["compression_level"] = __load_int32(bytes)

    tag = __load_int32(bytes)
    if tag != __special_tag():
        raise ValueError("Invalid header end magic ({}).".format(tag))

    remaining_bytes = header_bytes - bytes.tell()
    if remaining_bytes < 0:
        raise ValueError(
            "Header too small. {} remaining bytes.".format(remaining_bytes)
        )
    elif remaining_bytes > 0:
        bytes.read(remaining_bytes)  # Read until end of header

    return header


def __load_dict(bytes):
    """Deserialize a dictionary from *bytes*."""
    n = __load_int64(bytes)
    dict = {}
    for _ in range(n):
        key = __load_string(bytes)
        value = __load_string(bytes)
        dict[key] = value
    return dict


def __load_metas(bytes):
    """Deserialize meta information tuples ( name, dictionary ) from *bytes*."""
    meta_count = __load_int32(bytes)

    metas = {}
    for _ in range(meta_count):
        name = __load_string(bytes)
        dict = __load_dict(bytes)
        metas[name] = dict

    return metas


def __load_compressed_slices(raw_bytes, bytes, header):
    """Loads compressed representation of slices.
    Does not do any decompression or hashing of the compressed slices.
    """
    slice_count = header["dimZ"] * header["dimT"] * header["dimC"]
    slice_count_file = __load_uint64(bytes)
    if slice_count != slice_count_file:
        raise ValueError(
            "Computed number of slices ({}) does not match advertised number of slices ({})".format(
                slice_count, slice_count_file
            )
        )
    le_int64 = np.dtype(np.int64)
    le_int64 = le_int64.newbyteorder("<")
    slice_starts = np.frombuffer(bytes.read(8 * slice_count), le_int64)

    slice_lengths_count = __load_uint64(bytes)
    if slice_count != slice_lengths_count:
        raise ValueError(
            "Computed number of slices ({}) does not match advertised number of slices ({})".format(
                slice_count, slice_lengths_count
            )
        )
    slice_lengths = np.frombuffer(bytes.read(8 * slice_count), le_int64)

    old_position = raw_bytes.tell()

    # Memory mapped view of file, so that we can defer actual reading of the file to the decompression / checksumming threads
    mapped = np.memmap(raw_bytes, dtype=np.ubyte, mode="r", offset=old_position)

    compressed_slices = []

    offset = 0

    for i in range(slice_count):
        # Support for old storage format which did not store proper slice offsets
        if header["file_version"] <= __old_storage_software_version():
            length = int(mapped[offset : offset + 8].view(dtype=np.uint64)[0])
            offset += 8
            if length != slice_lengths[i]:
                raise ValueError(
                    "Slice length mismatch. ({}) ({})".format(length, slice_lengths[i])
                )
        else:
            offset = int(slice_starts[i])
            length = int(slice_lengths[i])
        slice = mapped[offset : offset + length].view()
        offset += length
        compressed_slices.append(slice)

    raw_bytes.seek(old_position + offset, os.SEEK_SET)

    return compressed_slices


class HashingBytes:
    """Directly update hash with read bytes."""

    def __init__(self, bytes):
        self.bytes = bytes
        self.hash = hashlib.sha256()

    def read(self, num_bytes):
        read_bytes = self.bytes.read(num_bytes)
        self.hash.update(read_bytes)
        return read_bytes

    def tell(self):
        return self.bytes.tell()

    def digest(self):
        return self.hash.digest()

    def update(self, bytes):
        self.hash.update(bytes)


def __compute_slice_hash_and_decompress(
    hashes, indices, compressed_slices, output_data_view, decompress
):
    """Decompress slices and compute their compressed hash as specified in `indices`."""

    bytes_per_element = np.dtype(output_data_view.dtype).itemsize
    elements_per_slice = (
        output_data_view.shape[0]
        * output_data_view.shape[1]
        * output_data_view.shape[2]
    )
    bytes_per_slice = bytes_per_element * elements_per_slice

    # Each slice is 2D, but may be at a different time point or channel.
    # The canonical order is: slices in Z -> slices in T -> slices in C
    # Thus we can load into output_data.view as (dimC * dimT * dimZ, dimY, dimX) and later reshape the data

    for i in indices:
        hash = hashlib.sha256()
        hash.update(memoryview(compressed_slices[i]))
        hashes[i] = hash.digest()

        if decompress:
            local_slice_view = np.frombuffer(
                zlib.decompress(
                    memoryview(compressed_slices[i]), bufsize=bytes_per_slice
                ),
                dtype=output_data_view.dtype,
            )
        else:  # copy raw uncompressed data
            local_slice_view = np.frombuffer(
                memoryview(compressed_slices[i]), dtype=output_data_view.dtype
            )

        # shape local_slice_view from 1D decompressed buffer to slice
        output_data_view[i, :, :] = local_slice_view.reshape(
            (output_data_view.shape[1], output_data_view.shape[2])
        )


def __compute_slice_hashes_and_decompress(compressed_slices, output_data, decompress):
    """Decompress all slices and compute their compressed hash using multiple threads."""

    num_cpus = max(
        int(2 * mp.cpu_count()), 1
    )  # oversubscription of threads for IO-bounded networks
    task_size = len(compressed_slices)
    num_cpus = min(task_size, num_cpus)

    hashes = [0] * task_size

    target_shape = output_data.shape

    # reshape output data by concatenating last three dimensions
    output_data = np.reshape(
        output_data,
        (
            output_data.shape[0] * output_data.shape[1] * output_data.shape[2],
            output_data.shape[3],
            output_data.shape[4],
        ),
    )

    threads = []
    for i in range(num_cpus):
        # assign slice indices to thread
        local_indices = range(
            task_size * i // num_cpus, task_size * (i + 1) // num_cpus
        )
        thread = threading.Thread(
            target=__compute_slice_hash_and_decompress,
            args=(
                hashes,
                local_indices,
                compressed_slices,
                output_data.view(),
                decompress,
            ),
        )
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    # reshape back to 5D
    output_data = np.reshape(output_data, target_shape)

    return hashes


def __load_bytes_like(bytes):
    hashing_bytes = HashingBytes(bytes)

    header = __load_header(hashing_bytes)
    metas = __load_metas(hashing_bytes)

    # loads list of sequentially compressed 2D slices in "canonical" order (Z -> T -> C)
    compressed_slices = __load_compressed_slices(bytes, hashing_bytes, header)

    # we adopt Numpy's shape order where the fastest growing index (x) is at the last position
    data_shape = (
        header["dimC"],
        header["dimT"],
        header["dimZ"],
        header["dimY"],
        header["dimX"],
    )

    header["meta"] = metas

    # Generate affine transformation matrix
    affine = np.identity(4, dtype=np.double)
    affine[0:3, 0:3] = np.matmul(np.diag(header["voxel_sizes"]), header["rotation"])
    affine[0:3, 3] = np.reshape(header["translation"], (3))
    header["affine"] = affine

    # allocate empty ndarray for loading
    empty_array = np.ndarray(data_shape, dtype=header["voxel_type"])
    info = GFFInfo(
        header["meta"],
        header["affine"],
        header["voxel_sizes"],
        header["intensity_scale"],
        header["intensity_offset"],
        header["times"],
        header["channels"],
    )
    # TODO: validate header against shape
    output_gff = GFF(empty_array, info)

    # load data and compute hashes
    slice_hashes = __compute_slice_hashes_and_decompress(
        compressed_slices, output_gff.view(), header["compression_method"] == "zlib"
    )

    for slice_hash in slice_hashes:
        hashing_bytes.update(slice_hash)

    # validate hash
    hash_name = __load_string(hashing_bytes)
    if hash_name.lower() != "sha256":
        raise ValueError("Unknown hash configuration. ({})".format(hash_name))

    file_size_until_here = bytes.tell()
    file_size_until_here_reference = __load_int64(hashing_bytes)
    if file_size_until_here != file_size_until_here_reference:
        raise ValueError(
            "File size mismatch. Expected {}, got {}".format(
                file_size_until_here, file_size_until_here_reference
            )
        )

    digest_size = __load_uint64(bytes)
    file_digest = np.frombuffer(bytes.read(digest_size), np.uint8)

    if memoryview(file_digest) != hashing_bytes.digest():
        raise ValueError(
            "Mismatch between hashes:\nFile   :\t\t{}\nComputed:\t\t{}".format(
                memoryview(file_digest).tobytes().hex(), hashing_bytes.hash.hexdigest()
            )
        )

    time_stamp_type = __load_string(bytes)
    if time_stamp_type.lower() == "timestamp":
        time_stamp_digest_length = __load_uint64(bytes)
        time_stamp_digest = bytes.read(
            time_stamp_digest_length
        )  # TODO: Optionally verify timestamp

    return output_gff


def load(path_or_byteslike):
    """Load a .gff file from path or as bytes. Returns GFF object."""
    read, tell = [getattr(path_or_byteslike, x, None) for x in ["read", "tell"]]
    if callable(read) and callable(tell):
        return __load_bytes_like(path_or_byteslike)
    else:
        with open(path_or_byteslike, "rb") as f:
            return __load_bytes_like(f)
