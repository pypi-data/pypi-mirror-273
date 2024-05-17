"""shared_ndarray2 - Provides the SharedNDArray class that streamlines the use of NumPy
ndarrays with multiprocessing.shared_memory.
"""

from __future__ import annotations

from multiprocessing.managers import SharedMemoryManager
from multiprocessing.shared_memory import SharedMemory
from typing import Any, Generic, SupportsIndex, Tuple, Type, TypeVar, Union, overload

import numpy as np
from numpy._typing._array_like import _ArrayLikeInt_co
from numpy.typing import NDArray

VALID_SHARED_TYPES = (np.number, np.bool_, np.datetime64, np.timedelta64)
"""Any NumPy scalar type with a fixed number of bytes per element (for runtime type
checking)."""

ShareableT = TypeVar(
    "ShareableT", bound=Union[np.number, np.bool_, np.datetime64, np.timedelta64]
)
"""Any NumPy scalar type with a fixed number of bytes per element (for static type
checking)."""


class SharedNDArray(Generic[ShareableT]):
    """Class to keep track of and retrieve the data in a shared array

    Attributes
    ----------
    shm
        `SharedMemory` object containing the data of the array
    shape
        Shape of the NumPy array
    dtype
        Numpy `dtype` for the NumPy array to be represented in shared memory.

    A `SharedNDArray` object may be created either directly with a preallocated shared
    memory object plus the type and shape of the numpy array it represents:

    >>> from multiprocessing.shared_memory import SharedMemory
    >>> import numpy as np
    >>> from shared_ndarray2 import SharedNDArray
    >>> x = np.array([1, 2, 3])
    >>> shm = SharedMemory(name="x", create=True, size=x.nbytes)
    >>> arr = SharedNDArray(shm, x.shape, x.dtype)
    >>> arr[:] = x[:]  # copy x into the array
    >>> print(arr[:])
    [1 2 3]
    >>> shm.close()
    >>> shm.unlink()

    Or using a `SharedMemoryManager` either from an existing array or from arbitrary shape
    and type:

    >>> from multiprocessing.managers import SharedMemoryManager
    >>> mem_mgr = SharedMemoryManager()
    >>> mem_mgr.start()  # Better yet, use SharedMemoryManager context manager
    >>> arr = SharedNDArray.from_shape(mem_mgr, x.shape, x.dtype)
    >>> arr[:] = x[:]  # copy x into the array
    >>> print(arr[:])
    [1 2 3]
    >>> # -or in one step-
    >>> arr = SharedNDArray.from_array(mem_mgr, x)
    >>> print(arr[:])
    [1 2 3]

    `SharedNDArray` does not subclass `numpy.ndarray` but rather generates an ndarray
    on-the-fly in `get()`, which is used in `__getitem__()` and `__setitem__()`. Thus to
    access the data and/or use any ndarray methods `arr.get()` or `arr[index_or_slice]`
    must be used. For example:

    >>> arr.max()  # ERROR: SharedNDArray has no `max` method.
    Traceback (most recent call last):
        ....
    AttributeError: SharedNDArray object has no attribute 'max'. To access NumPy ndarray object use .get() method.
    >>> arr.get().max()  # (or arr[:].max())  OK: This gets an ndarray on which we can operate
    3
    >>> y = np.zeros(3)
    >>> y[:] = arr  # ERROR: Cannot broadcast-assign a SharedNDArray to ndarray `y`
    Traceback (most recent call last):
        ...
    ValueError: setting an array element with a sequence.
    >>> y[:] = arr[:]  # OK: This gets an ndarray that can be copied element-wise to `y`
    >>> mem_mgr.shutdown()
    """

    shm: SharedMemory
    # shape: Tuple[int, ...]  # is a property
    dtype: np.dtype[ShareableT]

    def __init__(
        self,
        shm: Union[SharedMemory, str],
        shape: Tuple[int, ...],
        dtype: Union[Type[ShareableT], np.dtype[ShareableT]],
    ):
        """Initialize a SharedNDArray object from existing shared memory, object shape,
        and dtype.

        To initialize a SharedNDArray object from a memory manager and data or shape, use
        the `from_array()` or `from_shape()` classmethods.

        Parameters
        ----------
        shm
            Either a `multiprocessing.shared_memory.SharedMemory` object or a name for
            connecting to an existing block of shared memory (using SharedMemory
            constructor)
        shape
            Shape of the NumPy array to be represented in the shared memory
        dtype
            Data type for the NumPy array to be represented in shared memory. Any NumPy
            scalar type with a fixed size or dtype of a scalar type with a fixed size is
            acceptable. See `shared_ndarray2.VALID_SHARED_TYPES` and
            https://numpy.org/doc/stable/user/basics.types.html.

        Raises
        ------
        ValueError
            The SharedMemory size (number of bytes) does not match the product of the
            shape and dtype itemsize.
        """
        if isinstance(shm, str):
            shm = SharedMemory(name=shm, create=False)
        self.dtype = np.dtype(dtype)
        if not issubclass(self.dtype.type, VALID_SHARED_TYPES):
            raise TypeError(f"dtype must be one of {VALID_SHARED_TYPES}")
        if shm.size != self.dtype.itemsize * np.prod(shape):
            raise ValueError(
                "The SharedMemory object shm must have the same size as the product of"
                " the size of the dtype and the shape."
            )
        self.shm = shm
        self._shape: Tuple[int, ...] = shape

    def __repr__(self):
        # Like numpy's ndarray repr
        cls_name = self.__class__.__name__
        nspaces = len(cls_name) + 1
        array_repr = str(self.get())
        array_repr = array_repr.replace("\n", "\n" + " " * nspaces)
        return f"{cls_name}({array_repr}, dtype={self.dtype})"

    @classmethod
    def from_array(
        cls,
        mem_mgr: SharedMemoryManager,
        arr: NDArray[ShareableT],
    ) -> SharedNDArray[ShareableT]:
        """Create a SharedNDArray from a SharedMemoryManager and an existing numpy array.

        Parameters
        ----------
        mem_mgr
            Running `multiprocessing.managers.SharedMemoryManager` instance from which to
            create the SharedMemory for the SharedNDArray
        arr
            NumPy `ndarray` object to copy into the created SharedNDArray upon
            initialization.
        """
        # Simply use from_shape() to create the SharedNDArray and copy the data into it.
        shared_arr = cls.from_shape(mem_mgr, arr.shape, arr.dtype)
        shared_arr[:] = arr[:]
        return shared_arr

    @classmethod
    def from_shape(
        cls,
        mem_mgr: SharedMemoryManager,
        shape: Tuple[int, ...],
        dtype: Union[Type[ShareableT], np.dtype[ShareableT]],
    ) -> SharedNDArray[ShareableT]:
        """Create a SharedNDArray directly from a SharedMemoryManager

        Parameters
        ----------
        mem_mgr
            SharedMemoryManager instance that has been started
        shape
            Shape of the array
        dtype
            Data type for the NumPy array to be represented in shared memory. Any NumPy
            scalar type with a fixed size is acceptable. See
            `shared_ndarray2.VALID_SHARED_TYPES` and
            https://numpy.org/doc/stable/user/basics.types.html.
        """
        nbytes = int(np.prod(shape) * np.dtype(dtype).itemsize)
        shm = mem_mgr.SharedMemory(nbytes)
        return cls(shm=shm, shape=shape, dtype=dtype)

    @property
    def shape(self) -> Tuple[int, ...]:
        return self._shape

    @shape.setter
    def shape(self, shp: Tuple[int, ...]):
        """Ensure the provided shape is compatible with the data"""
        # Try to reshape using ndarray. Will raise a ValueError if the shape is invalid
        self._shape = self.get().reshape(shp).shape

    def get(self) -> NDArray[ShareableT]:
        """Get a numpy array with access to the shared memory"""
        return np.ndarray(self.shape, dtype=self.dtype, buffer=self.shm.buf)

    # ###
    # Relevant __getitem__() overloads copied from numpy.__init__.pyi:ndarray.__getitem__
    # ###
    @overload
    def __getitem__(
        self,
        key: Union[
            NDArray[np.integer[Any]],
            NDArray[np.bool_],
            Tuple[Union[NDArray[np.integer[Any]], NDArray[np.bool_]], ...],
        ],
    ) -> NDArray[ShareableT]: ...

    @overload
    def __getitem__(
        self, key: Union[SupportsIndex, Tuple[SupportsIndex, ...]]
    ) -> Any: ...

    @overload
    def __getitem__(
        self,
        key: Union[
            None,
            slice,
            ellipsis,
            SupportsIndex,
            _ArrayLikeInt_co,
            Tuple[Union[None, slice, ellipsis, SupportsIndex, _ArrayLikeInt_co], ...],
        ],
    ) -> NDArray[ShareableT]: ...

    def __getitem__(self, key):
        """Get data from the shared array

        Equivalent to SharedNDArray.get()[key]
        """
        return self.get()[key]

    def __setitem__(self, key, value):
        """Set values in the shared array

        Equivalent to SharedNDArray.get()[key] = value
        """
        self.get()[key] = value

    @property
    def ndim(self) -> int:
        return len(self.shape)

    def __getattr__(self, name):
        extra_err_txt = (
            " To access NumPy ndarray object use .get() method."
            if hasattr(np.ndarray, name)
            else ""
        )

        raise AttributeError(
            f"SharedNDArray object has no attribute '{name}'.{extra_err_txt}"
        )

    def __del__(self):
        if hasattr(self, "shm"):  # Prevent pytest warning...?
            self.shm.close()


def from_shape(
    mem_mgr: SharedMemoryManager,
    shape: Tuple[int, ...],
    dtype: Union[Type[ShareableT], np.dtype[ShareableT]],
) -> SharedNDArray[ShareableT]:
    """Create a SharedNDArray directly from a SharedMemoryManager

    Parameters
    ----------
    mem_mgr
        SharedMemoryManager instance that has been started
    shape
        Shape of the array
    dtype
        Data type for the NumPy array to be represented in shared memory. Any NumPy scalar
        type with a fixed size is acceptable. See `shared_ndarray2.VALID_SHARED_TYPES` and
        https://numpy.org/doc/stable/user/basics.types.html.
    """
    nbytes = int(np.prod(shape) * np.dtype(dtype).itemsize)
    shm = mem_mgr.SharedMemory(nbytes)
    return SharedNDArray(shm=shm, shape=shape, dtype=dtype)


def from_array(
    mem_mgr: SharedMemoryManager, arr: NDArray[ShareableT]
) -> SharedNDArray[ShareableT]:
    """Create a SharedNDArray from a SharedMemoryManager and an existing numpy array.

    Parameters
    ----------
    mem_mgr
        Running `multiprocessing.managers.SharedMemoryManager` instance from which to
        create the SharedMemory for the SharedNDArray
    arr
        NumPy `ndarray` object to copy into the created SharedNDArray upon initialization.
    """
    # Simply use from_shape() to create the SharedNDArray and copy the data into it.
    shared_arr = from_shape(mem_mgr, arr.shape, arr.dtype)
    shared_arr[:] = arr[:]
    return shared_arr
