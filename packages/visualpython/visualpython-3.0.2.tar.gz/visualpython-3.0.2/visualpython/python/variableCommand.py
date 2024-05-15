"""
Search Variables
"""

_VP_NOT_USING_VAR = ['_html', '_nms', 'NamespaceMagics', '_Jupyter', 'In', 'Out', 'exit', 'quit', 'get_ipython']
_VP_NOT_USING_TYPES = ['module', 'function', 'builtin_function_or_method', 'instance', '_Feature', 'type', 'ufunc']

def _vp_load_instance(var=''):
    """
    load Variables with dir(globals)
    """
    # _VP_NOT_USING_VAR = ['_html', '_nms', 'NamespaceMagics', '_Jupyter', 'In', 'Out', 'exit', 'quit', 'get_ipython']
    varList = []
    query = ''
    result = {}
    if var == '':
        varList = sorted(globals())
        # result = { 'type': 'NoneType', 'list': [{'name': v, 'type': type(eval(v)).__name__} for v in _vp_vars if (not v.startswith('_')) and (v not in _VP_NOT_USING_VAR)] }
        result = {'type': 'NoneType', 'list': []}
    else:
        varList = dir(eval(var))
        query = var + '.'

        varType = type(eval(var)).__name__
        # result = { 'type': type(eval(var)).__name__, 'list': [{'name': v, 'type': type(eval(var + '.' + v)).__name__} for v in _vp_vars if (not v.startswith('_')) and (v not in _VP_NOT_USING_VAR)] }
        if varType == 'module':
            varName = eval(var).__name__
            result = {'type': type(eval(var)).__name__, 'name': varName, 'list': []}
        else:
            result = {'type': type(eval(var)).__name__, 'list': []}

    tmpList = []
    for v in varList:
        try:
            if (not v.startswith('_')) and (v not in _VP_NOT_USING_VAR):
                tmpList.append({'name': v, 'type': type(eval(query + v)).__name__ })
        except Exception as e:
            continue
    result['list'] = tmpList

    return result

def _vp_get_type(var=None):
    """
    get type name
    """
    return str(type(var).__name__)


def _vp_get_variables_list(types, exclude_types=[], allow_module=False):
    """
    Get Variable list in types
    """
    # notUsingVariables = ['_html', '_nms', 'NamespaceMagics', '_Jupyter', 'In', 'Out', 'exit', 'quit', 'get_ipython']
    # notUsingTypes = ['module', 'function', 'builtin_function_or_method', 'instance', '_Feature', 'type', 'ufunc']
    not_using_types = _VP_NOT_USING_TYPES

    varList = []
    searchList = globals()
    if (type(types) == list) and (len(types) > 0):
        varList = [{'varName': v, 'varType': type(eval(v)).__name__, 'varInfo': _vp_get_variable_info(eval(v))} for v in searchList if (not v.startswith('_')) & (v not in _VP_NOT_USING_VAR) & (type(eval(v)).__name__ not in exclude_types) & (type(eval(v)).__name__ in types)]
    else:
        if allow_module == True:
            not_using_types.remove('module')
        varList = [{'varName': v, 'varType': type(eval(v)).__name__, 'varInfo': _vp_get_variable_info(eval(v))} for v in searchList if (not v.startswith('_')) & (v not in _VP_NOT_USING_VAR) & (type(eval(v)).__name__ not in exclude_types) & (type(eval(v)).__name__ not in not_using_types)]

    return varList

def _vp_get_variable_info(v):
    """
    Get Variable's detailed information
    """
    if type(v).__name__ == 'ndarray':
        return {'ndim': v.ndim}
    return {}

def _vp_get_sweetviz_list():
    """
    Get sweetviz variable list
    """
    varList = _vp_get_variables_list(['DataframeReport'])
    result = []
    for v in varList:
        title = eval(v['varName']).source_name
        result.append({ 'varName': v['varName'], 'title': title })
    return result

def _vp_get_profiling_list():
    """
    Get profiling variable list
    """
    varList = _vp_get_variables_list(['ProfileReport'])
    result = []
    for v in varList:
        title = eval(v['varName']).get_description()['analysis']['title']
        result.append({ 'varName': v['varName'], 'title': title })
    return result

import numpy as _vp_np
import random as _vp_rd
def _vp_sample(data, sample_cnt):
    """
    Sampling data
    """
    data_type = type(data).__name__
    sample_cnt = len(data) if len(data) < sample_cnt else sample_cnt

    if data_type == 'DataFrame':
        return data.sample(sample_cnt, random_state=0)
    elif data_type == 'Series':
        return data.sample(sample_cnt, random_state=0).reset_index(drop=True)
    elif data_type == 'ndarray':
        return data[_vp_np.random.choice(data.shape[0], sample_cnt, replace=False)]
    elif data_type == 'list':
        return _vp_rd.choices(data, k=sample_cnt)
    return data

def _vp_check_module_loaded(fname_list):
    """
    Check if this module is loaded
    """
    result = []
    for fname in fname_list:
        if fname in globals():
            result.append(True)
        else:
            result.append(False)
    return result

def _vp_check_package_list(pack_list):
    """
    Check package info : name, version, path
    """
    import importlib as _vp_ilib
    import warnings
    _pack_info = {}
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for pack in pack_list:
            try:
                _vp_pack = _vp_ilib.import_module(pack)
                _vp_ilib.reload(_vp_pack)
                _pack_info[pack] = { 'name': _vp_pack.__name__, 'installed': True, 'version': _vp_pack.__version__, 'path': _vp_pack.__path__ }
            except:
                _pack_info[pack] = { 'name': pack, 'installed': False }
    return _pack_info