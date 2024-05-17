"""shared_ndarray2 - Provides the SharedNDArray class that streamlines the use of NumPy ndarrays with
multiprocessing.shared_memory.
"""

from .shared_ndarray import (
    VALID_SHARED_TYPES,
    ShareableT,
    SharedNDArray,
    from_array,
    from_shape,
)
from .version import __version__
