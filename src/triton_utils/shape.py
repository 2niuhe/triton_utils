import ctypes

import torch
import triton
import triton.language as tl


@triton.jit
def get_1d_offest(size, n_prev_chunks):
    return n_prev_chunks * size + tl.arange(0, size)


@triton.jit
def get_2d_offset(offs_0, offs_1, stride_0, stride_1=1):
    return tl.expand_dims(offs_0, 1) * stride_0 + tl.expand_dims(offs_1, 0) * stride_1


@triton.jit
def get_1d_mask(offs, max):
    return offs < max


@triton.jit
def get_2d_mask(offs_0, offs_1, max_0, max_1):
    return (tl.expand_dims(offs_0, 1) < max_0) & (tl.expand_dims(offs_1, 0) < max_1)


def print_internal(t: torch.Tensor):
    print(
        torch.frombuffer(
            ctypes.string_at(t.data_ptr(), t.storage().nbytes()), dtype=t.dtype
        )
    )


# # load
# Copied from https://github.com/UmerHA/triton_util/blob/main/triton_util/coding.py
@triton.jit
def load_1d(ptr, sz: tl.constexpr, n, max, stride=1):
    """Chunk 1d vector (defined by ptr) into 1d grid, where each chunk has size sz.
    Load the nth chunk. Ie, load [n*sz,...,(n+1)*sz-1]."""
    offs = get_1d_offest(sz, n)
    mask = get_1d_mask(offs, max)
    return tl.load(ptr + offs, mask)


@triton.jit
def load_full_1d(ptr, sz: tl.constexpr, stride=1):
    """Load 1d block [0,...,sz-1]"""
    offs = get_1d_offest(sz)
    mask = get_1d_mask(offs, sz)
    return tl.load(ptr + offs, mask)


@triton.jit
def load_2d(
    ptr,
    sz0: tl.constexpr,
    sz1: tl.constexpr,
    n0,
    n1,
    max0,
    max1,
    stride0=None,
    stride1=1,
):
    """Chunk 2d matrix (defined by ptr) into 2d grid, where each chunk has size (sz0,sz1).
    Load the (n0,n1)th chunk. Ie, load [n0*sz0,...,(n0+1)*sz0-1] x [n1*sz1,...,(n1+1)*sz1-1].
    """
    stride0 = stride0 or sz1
    offs0 = get_1d_offest(sz0, n0)
    offs1 = get_1d_offest(sz1, n1)
    offs = get_2d_offset(offs0, offs1, stride0, stride1)
    mask = get_2d_mask(offs0, offs1, max0, max1)
    return tl.load(ptr + offs, mask)


@triton.jit
def load_full_2d(ptr, sz0: tl.constexpr, sz1: tl.constexpr, stride0=None, stride1=1):
    """Load 2d block [0,...,sz0-1] x [0,...,sz1-1]"""
    stride0 = stride0 or sz1
    offs = get_2d_offset(tl.arange(0, sz0), tl.arange(0, sz1), stride0, stride1)
    mask = get_2d_mask(tl.arange(0, sz0), tl.arange(0, sz1), sz0, sz1)
    return tl.load(ptr + offs, mask)


# # store


@triton.jit
def store_1d(vals, ptr, sz: tl.constexpr, n, max, stride=1):
    """Store 1d block into nth chunk of vector (defined by ptr), where each chunk has size sz"""
    offs = get_1d_offest(sz, n)
    mask = get_1d_mask(offs, max)
    tl.store(ptr + offs, vals, mask)


@triton.jit
def store_full_1d(vals, ptr, sz: tl.constexpr, stride=1):
    """Store 1d block into vector (defined by ptr)"""
    offs = get_1d_offest(sz)
    mask = get_1d_mask(offs, sz)
    tl.store(ptr + offs, vals, mask)


@triton.jit
def store_2d(
    vals,
    ptr,
    sz0: tl.constexpr,
    sz1: tl.constexpr,
    n0,
    n1,
    max0,
    max1,
    stride0=None,
    stride1=1,
):
    """Store 2d block into (n0,n1)th chunk of matrix (defined by ptr), where each chunk has size (sz0, sz1)"""
    stride0 = stride0 or sz1
    offs0 = get_1d_offest(sz0, n0)
    offs1 = get_1d_offest(sz1, n1)
    offs = get_2d_offset(offs0, offs1, stride0, stride1)
    mask = get_2d_mask(offs0, offs1, max0, max1)
    tl.store(ptr + offs, vals, mask)


@triton.jit
def store_full_2d(
    vals, ptr, sz0: tl.constexpr, sz1: tl.constexpr, stride0=None, stride1=1
):
    """Store 2d block into matrix (defined by ptr)"""
    stride0 = stride0 or sz1
    offs = get_2d_offset(tl.arange(0, sz0), tl.arange(0, sz1), stride0, stride1)
    mask = get_2d_mask(tl.arange(0, sz0), tl.arange(0, sz1), sz0, sz1)
    tl.store(ptr + offs, vals, mask)
