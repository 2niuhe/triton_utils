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
