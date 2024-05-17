# shared-ndarray2  <!-- omit in toc -->

`SharedNDArray` encapsulates a NumPy `ndarray` interface for using shared memory in
multiprocessing, using `multiprocessing.shared_memory` in Python 3.8+.

- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Similar Projects](#similar-projects)
- [Usage](#usage)
  - [Creation](#creation)
    - [`SharedNDArray()`](#sharedndarray)
    - [`SharedNDArray.from_shape()` or `shared_ndarray.from_shape()`](#sharedndarrayfrom_shape-or-shared_ndarrayfrom_shape)
    - [`SharedNDArray.from_array()` or `shared_ndarray.from_array()`](#sharedndarrayfrom_array-or-shared_ndarrayfrom_array)
  - [Using like `np.ndarray`](#using-like-npndarray)
  - [Releasing Shared Memory](#releasing-shared-memory)
  - [`.lock` attribute](#lock-attribute)
  - [Typed SharedNDArray](#typed-sharedndarray)

## Quick Start

```python
import multiprocessing
from multiprocessing.managers import SharedMemoryManager

import numpy as np

from shared_ndarray2 import SharedNDArray


def process_data(arr: SharedNDArray):
    # Work with data
    arr[:] += 1


with SharedMemoryManager() as mem_mgr:
    arr = SharedNDArray.from_array(mem_mgr, np.arange(1024))
    p = multiprocessing.Process(target=process_data, args=(arr,))
    p.start()
    p.join()
    assert np.all(arr[:] == np.arange(1, 1025))
```

## Requirements

- Python 3.8+
- NumPy 1.21+

## Similar Projects

- [SharedArray](https://pypi.org/project/SharedArray/) - POSIX-only. Quite a different
  paradigm, uses pre-Python 3.8 memory-sharing constructs, requires building a C module
  with `gcc`.
- [shared-ndarray](https://pypi.org/project/shared-ndarray/) - POSIX-only. Similar (uses
  NumPy ndarray `buffer` arg), uses pre-Python 3.8 memory-sharing constructs (requires
  `posix_ipc`).

## Usage

### Creation

There are three methods for constructing a `SharedNDArray`.

#### `SharedNDArray()`

To create a `SharedNDArray` object from existing shared memory that represents a NumPy
array, use the regular constructor providing _shape_ and _dtype_, either with an existing
`multiprocessing.SharedMemory` object or the name of one:

```python
shm = SharedMemory(create=True, size=1024)
arr = SharedNDArray(shm, (1024,), np.uint8)
# -or-
arr = SharedNDArray(shm.name, (1024,), np.uint8)
```

#### `SharedNDArray.from_shape()` or `shared_ndarray.from_shape()`

This method allocates shared memory managed by a SharedMemoryManager to represent a NumPy
`ndarray` with some _shape_ and _dtype_.

```python
with SharedMemoryManager as mem_mgr:
    arr = SharedNDArray.from_shape(mem_mgr, (3, 1024, 1024), dtype=np.uint16)
    # ... Use arr with e.g. multiprocessing.Pool or multiprocess.Process
    # ... Be sure process instances join/terminate before exiting SharedMemoryManager context manager
```

<div style="font-size: small; margin-left: 4em">

Note: _`shared_ndarray.from_shape()` is a standlone function and correctly types the
`SharedNDArray`, whereas the classmethod might (in mypy) or might not (in pyright)_

</div>

#### `SharedNDArray.from_array()` or `shared_ndarray.from_array()`

This method allocates shared memory managed by a SharedMemoryManager to represent a some
provided NumPy `ndarray` and copies that ndarray into the shared memory

```python
x = np.arange(100.0).reshape(2, 2, 25)
with SharedMemoryManager as mem_mgr:
    arr = SharedNDArray.from_array(mem_mgr, x)
    assert np.all(arr[:] == x[:])
    # ... Use arr as above...
```

<div style="font-size: small; margin-left: 4em">

Note: _`shared_ndarray.from_array()` is a standlone function and correctly types the
`SharedNDArray`, whereas the classmethod might (in mypy) or might not (in pyright)_

</div>

### Using like `np.ndarray`

The point of `SharedNDArray` is to remove the boilerplate of creating shared memory,
passing around shapes and dtypes and reconstructing `np.ndarray` objects. `SharedNDArray`
does this last step with its `.get()` method, which creates a `np.ndarray` on-the-fly
using the shared memory buffer. The `__getitem__()` and `__setitem__()` methods use the
`.get()` method to get the np.ndarray to access the data, so multi-dimensional indexing
and slicing work the same as with an `ndarray`. Other `np.ndarray` methods are not
directly implemented but may be accessed by first calling `.get()`, e.g.
`arr.get().mean()`.

### Releasing Shared Memory

`SharedNDArray` implements a `__del__()` method that calls the
[`.close()`](https://docs.python.org/3/library/multiprocessing.shared_memory.html#multiprocessing.shared_memory.SharedMemory.close)
method on the `SharedMemory` when the instance is destroyed (i.e. at process exit). When
the shared memory is unlinked in the parent process (either manually with
[`shm.unlink()`](https://docs.python.org/3/library/multiprocessing.shared_memory.html#multiprocessing.shared_memory.SharedMemory.unlink)
or by exiting a `SharedMemoryManager` context manager) the shared_memory is properly
released. However if a sub-process is not joined or terminated before the shared memory is
unlinked a warning will be emitted about "`leaked shared_memory objects to clean up at
shutdown`".

### `.lock` attribute

The `__init__()`, `from_shape()`, and `from_array()` methods may be given a `lock=True`
argument that will also create a `multiprocessing.Lock` object and include it in the
`SharedNDArray`, accesible as the `.lock` attribute. It should be noted, however, that it
doesn't work well to pass a `multiprocessing.Lock` as an argument to a
`multiprocessing.Pool` function, for reasons described
[here](https://stackoverflow.com/questions/25557686/python-sharing-a-lock-between-processes#comment72803059_25558333).
Thus by default `.lock` is set to `None`.

### Typed SharedNDArray

`SharedNDArray` is able to be typed with NumPy types. When using the `from_array()`
constructor, it is also able to inherit the type of the `ndarray` if it is typed using
`numpy.typing.NDArray` (new in NumPy 1.21). Typing information does not pass through with
slicing (`__getitem__`), however.

```python
x: npt.NDArray[np.int_] = np.arange(1024)
arr = SharedNDArray(mem_mgr, x)  # type of x is SharedNDArray[int_]
arr2 = arr[:]  # arr2 is typing.Any
```
