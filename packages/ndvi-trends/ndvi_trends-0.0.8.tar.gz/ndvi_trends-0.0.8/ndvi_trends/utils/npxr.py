from copy import deepcopy
from functools import wraps
import numpy as np
import xarray as xr


#
# CONSTANTS
#
NP_ARRAY_TYPE = 'array'
DATA_ARRAY_TYPE = 'data_array'
DATASET_TYPE = 'dataset'
REINDEX_DROP_INIT = 'drop_init'
REINDEX_DROP_LAST = 'drop_last'


#
# DECORATORS
#
def npxr(func):
    """ npxr

    decorator for functions that take in and return
    numpy arrays to extend their behavior to xarray.

    IMPORTANT NOTE:
        * deocorated functions must have the first argument be "data" of type np.array.
        * deocorated functions must return a np.array

    Usage:

    ```python
    @npxr
    def plus1(arr):
        return arr + 1

    ds_plus_1 = plus1(ds, data_var='blah', return_data_var='boom')    # returns xr.Dataset
    da_plus_1 = plus1(ds.blah)                                        # returns xr.DataArray
    np_plus_1 = plus1(ds.blah.data)                                   # returns np.ndarray
    ```

    Args:
        data_var (str|None):
            [only used for xr.dataset] if exists update
            the named data_var. if falsey: if only 1
            data_var exists use that data_var, otherwise
            throw error.
        result_data_var (str):
            [only used for xr.dataset] name of resulting data-var.
            if None defaults (and overwrites) <data_var>
        result_prefix (str):
            [only used for xr.dataset] ignored if <result_data_var>,
            sets <result_data_var> = <result_prefix>_<data_var>
        result_suffix (str):
            [only used for xr.dataset] ignored if <result_data_var>,
            sets <result_data_var> = <data_var>_<result_suffix>
        return_data_var (bool):
            [only useful for xr.dataset] if True return data as tuple (data, <result_data_var>)
        reindex (bool|'drop_init'|'drop_last'):
            if input and output arrays are of different lengths:
                if <reindex>  is True or 'drop_init': drop initial values to make the
                    coordinates align
                else if <reindex>  is 'drop_last': drop the ending values to make the
                    coordinates align
                else:
                    throw error
    Returns:
        decorated function that accepts xr.dataset/data_array as well as np.ndarray
    """
    @wraps(func)
    def _func(*args,
            data_var=None,
            result_data_var=None,
            result_prefix=None,
            result_suffix=None,
            return_data_var=False,
            reindex=False,
            **kwargs):
        data = deepcopy(kwargs.pop('data', None) or args[0])
        da, coords, data_object_type, data_var, result_data_var = _preprocess_xarray_data(
            data,
            data_var,
            result_data_var,
            result_prefix,
            result_suffix)
        values = func(da, *args[1:], **kwargs)
        data = _postprocess_xarray_data(
            values,
            coords,
            data,
            data_object_type,
            result_data_var,
            reindex)
        if return_data_var:
            return data, result_data_var
        else:
            return data
    return _func


#
# METHODS
#
def sequencer(data, data_var=None, result_data_vars=None, func_list=[], args_list=[]):
    """ run a sequence of npxr-decorated methods

    Args:
        data (np.array|xr.data_array|xr.dataset):
        data_var (str):
            if data is xr.dataset, name of data_var to use as input data
        result_data_vars (None|str|list):
            if None: overwrite input data
            if str: assign final output to name <result_data_vars>
            if list: keep all intermediate results named with elements of <result_data_vars>
        func_list (list[functions]):
            ordered list of functions to execute
        args_list (list):
            list of arguments for aligned function. an element "<args>" should be
                - False: to skip this function
                - a tuple such that, `args, kwargs = <args>` and func(data, *args, **kwargs)
                - a list such that, `args = <args>` and func(data, *args)
                - a dict such that, `kwargs = <args>` and func(data, **kwargs)
                - otherswise, such that, func(data, <args>)

    Returns:
        output data (and possibly intermediate steps) after processing through sequence.
        form will be the same as type as the input data (np.array|xr.data_array|xr.dataset)
    """
    args_list, data_vars = _process_sequence_args(
        data_var,
        args_list,
        result_data_vars,
        len(func_list))
    for i, (func, args) in enumerate(zip(func_list, args_list)):
        if args is not False:
            data_var, result_data_var = data_vars[i:i + 2]
            args, kwargs = _process_sequence_function_args(args)
            data = func(data, *args, data_var=data_var, result_data_var=result_data_var, **kwargs)
    return data


#
# INTERNEL
#
def _get_data_var_names(data_var_names, data_var, result_data_var, result_prefix, result_suffix):
    """
    - if not <data_var> extract from data_var_names[0] or raise exception
    - if not <result_data_var> create from [data_var, result_prefix, result_suffix]
    Returns:
        tuple (data_var, result_data_var)
    """
    if not data_var:
        if len(data_var_names) > 1:
            err = (
                'ndvi_trends.utils.npxr._get_data_var_names: '
                '<data_var> required if multiple data_vars exist '
                f'(data_vars={data_var_names})'
            )
            raise ValueError(err)
        else:
            data_var = data_var_names[0]
    if not result_data_var:
        result_data_var = data_var
        if result_prefix:
            result_data_var = f'{result_prefix}_{result_data_var}'
        if result_suffix:
            result_data_var = f'{result_data_var}_{result_suffix}'
    return data_var, result_data_var


def _preprocess_xarray_data(
        data,
        data_var=None,
        result_data_var=None,
        result_prefix=None,
        result_suffix=None):
    """
    Args:
        data (xr.dataset|xr.data_array): data to process
        data_var (str|None):
            only used for xr.dataset. if exists update
            the named data_var. if falsey: if only 1
            data_var exists use that data_var, otherwise
            throw error.

    Returns:
        tuple (data, datatype, result_data_var)
    """
    if isinstance(data, xr.Dataset):
        data_var, result_data_var = _get_data_var_names(
            list(data.keys()),
            data_var,
            result_data_var,
            result_prefix,
            result_suffix)
        data_object_type = DATASET_TYPE
        da = data[data_var]
        coords = da.coords
    else:
        da = data
        if isinstance(data, np.ndarray):
            data_object_type = NP_ARRAY_TYPE
            result_data_var = None
            coords = None
        else:
            data_object_type = DATA_ARRAY_TYPE
            if not result_data_var:
                result_data_var = da.name
            da.name = result_data_var
            coords = da.coords
    return da, coords, data_object_type, data_var, result_data_var


def _postprocess_xarray_data(
        values,
        coords,
        data,
        data_object_type,
        result_data_var,
        reindex=False):
    """
    Returns:
        * if data_object_type is DATASET_TYPE:
            - return a xr.dataset with values assigned to the <result_data_var> data-var
        * otherwise: return da <np.array|xr.data_array>
        * if <return_data_var> return tuple (<xr.dataset>, <result_data_var>)
    """
    if data_object_type == NP_ARRAY_TYPE:
        return values
    else:
        coords = _reindex_coords(reindex, coords, len(values))
        da = xr.DataArray(values, coords=coords)
        if data_object_type == DATASET_TYPE:
            data[result_data_var] = da
            return data
        else:
            return da


def _reindex_coords(reindex, coords, len_out):
    cname = list(coords)[0]
    cvals = coords[cname]
    len_coord = len(cvals)
    len_diff = len_coord - len_out
    if len_diff > 0:
        if reindex == REINDEX_DROP_LAST:
            cvals = cvals.isel({cname: slice(None, -len_diff)})
        elif reindex in [True, REINDEX_DROP_INIT]:
            cvals = cvals.isel({cname: slice(len_diff, None)})
        else:
            err = (
                'ndvi_trends.utils.npxr._reindex_coords: '
                f'if coords lengths do not match ({len_coord}, {len_out}) '
                f'<reindex> must be one of [True, {REINDEX_DROP_INIT}, {REINDEX_DROP_LAST}] '
            )
            raise ValueError(err)
    return {cname: cvals}


def _process_sequence_function_args(args):
    """ process arguments for functions in sequencer `func_list`

    converts element of `args_list` to args-kwargs pair for function

    Args:
        args (tuple|list|dict|object|`falsey`): element to convert

    Returns:
        (tuple) args, kwargs
    """
    if isinstance(args, tuple):
        args, kwargs = args
    elif isinstance(args, list):
        args, kwargs = args, {}
    elif isinstance(args, dict):
        args, kwargs = {}, args
    elif args:
        args, kwargs = [args], {}
    else:
        args, kwargs = [], {}
    return args, kwargs


def _process_sequence_args(data_var, args_list, result_data_vars, len_funcs):
    """ process arguments for sequencer

    Args:
        data_var (str): name of initial data_var
        args_list (list): list of arguments for functions
        result_data_vars (list|str|None|False):
            see docs for `sequencer`
        len_funcs (int): number of functions in sequence

    Returns:
        (tuple) args_list, data_vars
    """
    if not isinstance(result_data_vars, list):
        result_data_vars = [result_data_vars]
    len_args = len(args_list)
    len_rdvars = len(result_data_vars)
    if len_funcs != len_args:
        if len_funcs > len_args:
            args_list = args_list + [None] * (len_funcs - len_args)
        else:
            err = (
                'ndvi_trends.utils.npxr._process_sequence_args'
                'number of functions must be greater than the number of function-args'
            )
            raise ValueError(err)
    if len_funcs != len_rdvars:
        if len_rdvars == 1:
            result_data_vars = result_data_vars * (len_funcs)
        else:
            err = (
                'ndvi_trends.utils.npxr._process_sequence_args'
                'number of result_data_vars must be 0, 1 or the number of functions'
            )
            raise ValueError(err)
    data_vars = [data_var] + result_data_vars
    return args_list, data_vars
