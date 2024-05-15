/*
 *    Project Name    : Visual Python
 *    Description     : GUI-based Python code generator
 *    File Name       : com_generator_v2.js
 *    Author          : Black Logic
 *    Note            : Generator for library options
 *    License         : GNU GPLv3 with Visual Python special exception
 *    Date            : 2021. 12. 17
 *    Change Date     :
 */
define([
    'vp_base/js/com/com_util',
    'vp_base/js/com/com_makeDom',
    'vp_base/js/com/component/SuggestInput',
    'vp_base/js/com/component/VarSelector2',
    'vp_base/js/com/component/DataSelector',
    'vp_base/js/com/component/MultiSelector',
    'vp_base/js/com/component/FileNavigation'
], function (com_util, com_makeDom, SuggestInput, VarSelector2, DataSelector, MultiSelector, FileNavigation) {
    /**
     * show result after code executed
     */
    var _VP_SHOW_RESULT = true;

    const _VP_COMP_TYPE_LABEL = {
        '1dlen': '1D Length',
        '2dlen': '2D Length',
        '3dlen': '3D Length',
        '1darr': '1D Array',
        '2darr': '2D Array',
        'ndarr': 'ND Array',
        'scalar': 'Scalar Value',
        'param': 'Param Value',
        'dtype': 'Dtype',
        'bool_checkbox': 'Boolean',
        'bool_select': 'Select Boolean',
        'option_select': 'Select option',
        'option_suggest': 'Input option',
        'data_select': 'Select data',
        'var_select': 'Select Variable',
        'var_multi': 'Select N-Variables',
        'col_select': 'Select Column',
        'col_multi': 'Select Columns',
        'textarea': 'Input textarea',
        'input_number': 'Input number',
        'input_text': 'Input text', 
        'input': 'Input value',
        'file_save': 'Select file',
        'file_load': 'Select file'
    }

    const _VP_BOOL_OPTIONS = [
        { label: 'Select option...', value: ''},
        { label: 'True', value: 'True' },
        { label: 'False', value: 'False' }
    ]

    const _VP_NP_DTYPES = [
        {
            name: 'Default',
            value: ''
        },
        {
            name: 'None',
            value: 'None'
        },
        {
            name: 'Int8',
            value: 'np.int8'
        },
        {
            name: 'Int16',
            value: 'np.int16'
        },
        {
            name: 'Int32',
            value: 'np.int32'
        },
        {
            name: 'Int64',
            value: 'np.int64'
        },
        {
            name: 'Intp',
            value: 'np.intp'
        },
        {
            name: 'uInt8',
            value: 'np.uint8'
        },
        {
            name: 'uInt16',
            value: 'np.uint16'
        },
        {
            name: 'uInt32',
            value: 'np.uint32'
        },
        {
            name: 'uInt64',
            value: 'np.uint64'
        },
        {
            name: 'Float16',
            value: 'np.float16'
        },
        {
            name: 'Float32',
            value: 'np.float32'
        },
        {
            name: 'Float64',
            value: 'np.float64'
        },
        {
            name: 'Bool',
            value: 'np.bool'
        },
        {
            name: 'String',
            value: 'np.string_'
        }
    ];

     /**
     * Generate page interface based on package configuration
     * @param {Component} pageThis
     * @param {*} package 
     * @param {Object} state [optional]
     * @param {String} parent [optional] parent selector as string
     */
    var vp_showInterfaceOnPage = function(pageThis, package, state={}, parent='') {

        // generate input variable tag
        var tblInput = $(pageThis.wrapSelector() + (parent!==''?(' ' + parent):'') + ' #vp_inputOutputBox table tbody');
        // generate option variable tag
        var tblOption = $(pageThis.wrapSelector() + (parent!==''?(' ' + parent):'') + ' #vp_optionBox table tbody');

        package.options && package.options.forEach(function(o, i) {
            var obj = JSON.parse(JSON.stringify(o));
            let newTag = vp_createTag(pageThis, obj, state);
            if (obj.required === true || obj.output === true) {
                tblInput.append(newTag);
            } else {
                tblOption.append(newTag);
            }
        });

        // TODO: userOption
        if (package.code.includes('${etc}')) {
            
        }

        bindMultiSelector(pageThis);
        bindAutoComponentEvent(pageThis);
    }

    /**
     * Generate tag using type
     * @param {String} selector
     * @param {Object} obj 
     * @param {Object} state
     */
    var vp_createTag = function(pageThis, obj, state) {
        // TR tag & TD label tag
        var tblRow = $('<tr></tr>')
        var tblLabel = $('<td></td>');
        var tblContent = $('<td></td>');

        
        let { name, label, component, required, output } = obj;
        let value = state[name];
        
        var requiredFontStyle = '';
        if (required === true) {
            requiredFontStyle = 'vp-bold vp-orange-text';
        } else if (output === true) {
            requiredFontStyle = 'vp-bold';
        }
        var lblTag = $(`<label class="vp-bold">${label || com_util.optionToLabel(name)}</label>`).attr({
            'for': name,
            'class': requiredFontStyle,
            'title': '(' + name + ')'
        });
        $(tblLabel).append(lblTag);

        let componentType = 'input';
        if (component) {
            if (component.length == 1) {
                componentType = component[0];
            } else {
                let compSlct = $('<select></select>').attr({
                    'class': 'vp-select vp-state vp-auto-component-selector',
                    'id': name + '_type'
                });
                compSlct.data('obj', obj);
                let defaultCompIdx = 0;
                component.forEach((comp, idx) => {
                    let compLabel = _VP_COMP_TYPE_LABEL[comp];
                    let option = $(`<option>${compLabel}</option>`).attr({
                        'index': idx,
                        'value': comp
                    });
                    // set as previous data 
                    if (state[name + '_type'] != undefined) {
                        // set as saved value
                        if (state[name + '_type'] == comp) {
                            $(option).attr({
                                'selected':'selected'
                            });
                            defaultCompIdx = idx;
                        }
                    }
                    compSlct.append(option);
                });
                tblContent.append(compSlct);
                // set default component type
                componentType = component[defaultCompIdx];
            }
        }
        // render content
        let contentTag = $('<div class="vp-auto-component-content"></div>');
        contentTag.append(renderContent(pageThis, componentType, obj, state));
        tblContent.append(contentTag);
        
        tblRow.append(tblLabel);
        tblRow.append(tblContent);
        
        return tblRow;
    }

    var renderContent = function(pageThis, componentType, obj, state={}) {
        let content = '';
        let value = state[obj.name];
        if (value == undefined) {
            if (obj.value != undefined) {
                value = obj.value;
            } else if (obj.default != undefined) {
                value = obj.default;
            } else {
                value = '';
            }
        } else {
            obj.value = value;
        }
        // create as component type
        switch (componentType) {
            case '1dlen':
                content = render1dLen(pageThis, obj, state);
                break;
            case '2dlen':
                content = render2dLen(pageThis, obj, state);
                break;
            case '3dlen':
                content = render3dLen(pageThis, obj, state);
                break;
            case '1darr':
                content = render1dArr(pageThis, obj, state);
                break;
            case '2darr':
                content = render2dArr(pageThis, obj, state);
                break;
            case 'ndarr':
                content = renderNdArr(pageThis, obj, state);
                break;
            case 'scalar':
                content = renderScalar(pageThis, obj, state);
                break;
            case 'param':
                content = renderParam(pageThis, obj, state);
                break;
            case 'dtype':
                content = renderDtypeSelector(pageThis, obj, state);
                break;
            case 'tabblock':
                content = renderTabBlock(pageThis, obj, state);
                break;
            case 'bool_checkbox':
                content = $(`<input type="checkbox" id="${obj.name}" class="vp-checkbox"/>`);
                if (value != undefined) {
                    // set as saved value
                    $(content).attr({
                        'checked': value
                    });
                }
                break;
            case 'bool_select':
                // True False select box
                var optSlct = $(`<select id="${obj.name}" class="vp-select vp-state"></select>`);
                _VP_BOOL_OPTIONS.forEach((opt, idx) => {
                    var option = $(`<option>${opt.label}${obj.default==opt.value?' (default)':''}</option>`).attr({
                        // 'id':opt,
                        'index':obj.index,
                        'name':obj.name,
                        // 'value':(obj.default==opt.value?'':opt.value)
                        'value':opt.value
                    });
                    // cell metadata test
                    if (value != undefined && obj.value != undefined) {
                        // set as saved value
                        if (value == opt.value) {
                            $(option).attr({
                                'selected':'selected'
                            });
                        }
                    } else {
                        // set default value
                        // if (value == opt.default) {
                        //     $(option).attr({
                        //         'selected':'selected'
                        //     });
                        // }
                    }
                    optSlct.append(option);
                });
                content = optSlct;
                break;
            case 'option_select':
                var optSlct = $('<select></select>').attr({
                    'class':'vp-select option-select vp-state',
                    'id':obj.name,
                    'title': (obj.help==undefined?'':obj.help),
                });
                obj.options.forEach((opt, idx, arr) => {
                    var label = (obj.options_label != undefined? obj.options_label[idx]:opt);
                    let isDefault = false;
                    if (obj.required != true && obj.default != undefined && obj.default == opt) {
                        isDefault = true;
                        label += ' (default)';
                    }
                    var option = $(`<option>${label}</option>`).attr({
                        // 'id':opt,
                        'index':obj.index,
                        'name':obj.name,
                        'value':(isDefault? '': opt)
                    });
                    // saved data
                    if ((value == opt)
                        || ((value == undefined || value == '') && isDefault)) {
                        // set as saved value
                        $(option).attr({
                            'selected':'selected'
                        });
                    }
                    optSlct.append(option);
                });
                content = optSlct;
                break;
            case 'option_suggest':
                // suggest input tag
                // 1. Target Variable
                var suggestInput = new SuggestInput();
                suggestInput.setComponentID(obj.name);
                suggestInput.addClass('vp-input vp-state');
                suggestInput.setSuggestList(function() { return obj.options; });
                suggestInput.setNormalFilter(obj.useFilter == undefined?false:obj.useFilter);
                suggestInput.setValue(value);
                if (obj.placeholder != undefined) {
                    suggestInput.setPlaceholder(obj.placeholder);
                }
                if (obj.required === true) {
                    suggestInput.addAttribute('required', true);
                }
                suggestInput.setSelectEvent(function(selectedValue) {
                    // trigger change
                    $(pageThis.wrapSelector('#' + obj.name)).val(selectedValue);
                    $(pageThis.wrapSelector('#' + obj.name)).trigger('change');
                });
                content = $(suggestInput.toTagString());
                break;
            case 'data_select':
                let dataSelector = new DataSelector({
                    pageThis: pageThis, 
                    id: obj.name,
                    type: obj.comp_type || 'data',
                    allowDataType: obj.var_type, 
                    placeholder: obj.placeholder || 'Select data',
                    value: value,
                    columnSelection: obj.columnSelection || 'multiple', // single / multiple
                    returnFrameType: obj.returnFrameType || '',         // '' / DataFrame / Series
                    required: obj.required === true
                });
                content = $(dataSelector.toTagString());
                break;
            case 'var_select':
                // suggest input tag
                var tag = $('<input/>').attr({
                    type: 'text',
                    id: obj.name,
                    class: 'vp-input vp-state',
                    placeholder: obj.placeholder || 'Select data',
                    required: obj.required === true,
                    title: (obj.help==undefined?'':obj.help),
                });
                vp_generateVarSuggestInput(pageThis.wrapSelector(), obj);
                content = tag;
                break;
            case 'var_multi':
                // select tag with multiple selection
                var tag = $('<select></select>').attr({
                    'id': obj.name,
                    'class': 'vp-select var-multi vp-state',
                    // multiple selection true
                    'multiple': true,
                    'title': (obj.help==undefined?'':obj.help),
                });
                vp_generateVarSelect(tag, obj.var_type, obj.value);
                content = tag;
                break;
            case 'col_select':
                var tag = $('<input/>').attr({
                    'type': 'text',
                    'id': obj.name,
                    'class': 'vp-input vp-state',
                    'title': (obj.help==undefined?'':obj.help),
                });
                content = tag;
                break;
            case 'col_multi':
                var tag1 = $('<div></div>').attr({
                    'id': obj.name + '_auto_comp',
                    'class': 'vp-auto-multi-column',
                    'data-id': obj.name,
                    'data-target': obj.comp_target || 'i0',
                    'style': 'height: 150px;',
                    'title': (obj.help==undefined?'':obj.help),
                });
                var tag2 = $('<input/>').attr({
                    type: 'hidden',
                    id: obj.name,
                    class: 'vp-input vp-state',
                })
                var tag = $('<div></div>').append(tag1).append(tag2);
                content = tag;
                break;
            case 'textarea':
                var textarea = $(`<textarea id="${obj.name}" class="vp-textarea vp-state">${(obj.default==undefined?'':obj.default)}</textarea>`);
                // cell metadata test
                if (value != undefined) {
                    // set as saved value
                    textarea.val(value);
                }
                content = textarea;
                break;
            case 'input_number':
                var input = $('<input/>').attr({
                    type: 'number',
                    class: 'vp-input vp-state',
                    id: obj.name,
                    placeholder: (obj.placeholder==undefined?'Input Number':obj.placeholder),
                    value: (obj.default==undefined?'':obj.default),
                    title: (obj.help==undefined?'':obj.help),
                    required: obj.required === true
                });
                if (obj.step != undefined) {
                    $(input).attr({ 'step': obj.step });
                }
                if (obj.min != undefined) {
                    $(input).attr({ 'min': obj.min });
                }
                if (obj.max != undefined) {
                    $(input).attr({ 'max': obj.max });
                }
                // cell metadata test
                if (value != undefined) {
                    // set as saved value
                    $(input).attr({
                        'value': value
                    });
                }
                content = input;
                break;
            case 'file-save':
                var input = $('<input/>').attr({
                    type: 'text',
                    class: 'vp-input input-single vp-state',
                    id: obj.name,
                    placeholder: (obj.placeholder==undefined?'Input Data':obj.placeholder),
                    value: (obj.default==undefined?'':obj.default),
                    title: (obj.help==undefined?'':obj.help),
                    required: obj.required == true
                });
                // cell metadata test
                if (value != undefined) {
                    // set as saved value
                    $(input).attr({
                        'value': value
                    });
                }
                var fileBrowerButton = $(`<div class="vp-file-browser-button" data-parent="${obj.name}"></div>`);
                var div = $('<div></div>');
                div.append(input);
                div.append(fileBrowerButton);

                $(document).off('click', pageThis.wrapSelector(`.vp-file-browser-button[data-parent="${obj.name}"]`));
                $(document).on('click', pageThis.wrapSelector(`.vp-file-browser-button[data-parent="${obj.name}"]`), function() {
                    let fileNavi = new FileNavigation({
                        type: 'save',
                        extensions: (obj.fileExtension==undefined?[]:[obj.fileExtension]),
                        finish: function(filesPath, status, error) {
                            let {file, path} = filesPath[0];
    
                            // set text
                            $(pageThis.wrapSelector('#' + obj.name)).data('file', file);
                            $(pageThis.wrapSelector('#' + obj.name)).val(path);
                        }
                    });
                    fileNavi.open();
                });
                content = div;
                break;
            case 'file-open':
                var input = $('<input/>').attr({
                    type: 'text',
                    class: 'vp-input input-single vp-state',
                    id: obj.name,
                    placeholder: (obj.placeholder==undefined?'Input Data':obj.placeholder),
                    value: (obj.default==undefined?'':obj.default),
                    title: (obj.help==undefined?'':obj.help),
                    required: obj.required == true
                });
                // cell metadata test
                if (value != undefined) {
                    // set as saved value
                    $(input).attr({
                        'value': value
                    });
                }
                var fileBrowerButton = $(`<div class="vp-file-browser-button" data-parent="${obj.name}"></div>`);
                var div = $('<div></div>');
                div.append(input);
                div.append(fileBrowerButton);

                $(document).off('click', pageThis.wrapSelector(`.vp-file-browser-button[data-parent="${obj.name}"]`));
                $(document).on('click', pageThis.wrapSelector(`.vp-file-browser-button[data-parent="${obj.name}"]`), function() {
                    let fileNavi = new FileNavigation({
                        type: 'open',
                        extensions: (obj.fileExtension==undefined?[]:[obj.fileExtension]),
                        finish: function(filesPath, status, error) {
                            let {file, path} = filesPath[0];
    
                            // set text
                            $(pageThis.wrapSelector('#' + obj.name)).data('file', file);
                            $(pageThis.wrapSelector('#' + obj.name)).val(path);
                        }
                    });
                    fileNavi.open();
                });
                content = div;
                break;
            case 'table':
                // break;
            // default : input_single
            default:
                var input = $('<input/>').attr({
                    type: 'text',
                    class: 'vp-input input-single vp-state',
                    id: obj.name,
                    placeholder: (obj.placeholder==undefined?'Input Data':obj.placeholder),
                    value: (obj.default==undefined?'':obj.default),
                    title: (obj.help==undefined?'':obj.help),
                    required: obj.required == true
                });
                // cell metadata test
                if (value != undefined) {
                    // set as saved value
                    $(input).attr({
                        'value': value
                    });
                }
                content = input;
                break;
        }

        return content;
    }

    /**
     * Generate suggest input
     * @param {object} obj
     */
    var vp_generateVarSuggestInput = function(divTag, obj) {
        var types = obj.varType;
        var defaultValue = obj.value;
        if (obj.value == undefined && obj.default != undefined) {
            defaultValue = obj.default;
        }

        if (types == undefined) {
            types = [];
        }

        // Include various index types for Index type
        var INDEX_TYPES = ['RangeIndex', 'CategoricalIndex', 'MultiIndex', 'IntervalIndex', 'DatetimeIndex', 'TimedeltaIndex', 'PeriodIndex', 'Int64Index', 'UInt64Index', 'Float64Index'];
        // Include various groupby types for Groupby type
        var GROUPBY_TYPES = ['DataFrameGroupBy', 'SeriesGroupBy']
        if (types && types.indexOf('Index') >= 0) {
            types = types.concat(INDEX_TYPES);
        }
        if (types && types.indexOf('GroupBy') >= 0) {
            types = types.concat(GROUPBY_TYPES);
        }

        vpKernel.getDataList(types).then((resultObj) => {
            let { result, type, msg } = resultObj;
            var varList = JSON.parse(result);
            varList = varList.map(function(v) {
                return { label: v.varName, value: v.varName, dtype: v.varType };
            });
            // 1. Target Variable
            var suggestInput = new SuggestInput();
            suggestInput.setComponentID(obj.name);
            suggestInput.addClass('vp-input vp-state');
            suggestInput.setSuggestList(function() { return varList; });
            suggestInput.setNormalFilter(false);
            suggestInput.setValue(defaultValue);
            if (obj.required === true) {
                suggestInput.addAttribute('required', true);
            }
            if (obj.placeholder != undefined) {
                suggestInput.setPlaceholder(obj.placeholder);
            }
            suggestInput.setSelectEvent(function(selectedValue) {
                // trigger change
                $(divTag + ' #' + obj.name).val(selectedValue);
                $(divTag + ' #' + obj.name).trigger('change');
            });
            $(divTag + ' #' + obj.name).replaceWith(function() {
                return suggestInput.toTagString();
            });
        }).catch(err => {
            vpLog.display(VP_LOG_TYPE.ERROR, 'Error on generating var suggest input', err);
        });
    }

    /**
     * Generate variable select tag
     * @param {object} tag 
     * @param {Array<string>} types 
     * @param {string} defaultValue 
     */
    var vp_generateVarSelect = function(tag, types, defaultValue = '') {
        // Include various index types for Index type
        var INDEX_TYPES = ['RangeIndex', 'CategoricalIndex', 'MultiIndex', 'IntervalIndex', 'DatetimeIndex', 'TimedeltaIndex', 'PeriodIndex', 'Int64Index', 'UInt64Index', 'Float64Index'];
        // Include various groupby types for Groupby type
        var GROUPBY_TYPES = ['DataFrameGroupBy', 'SeriesGroupBy']
        if (types.indexOf('Index') >= 0) {
            types = types.concat(INDEX_TYPES);
        }
        if (types.indexOf('GroupBy') >= 0) {
            types = types.concat(GROUPBY_TYPES);
        }

        vpKernel.getDataList(types).then(function(resultObj) {
            let { result, type, msg } = resultObj;
            var jsonVars = result.replace(/'/gi, `"`);
            var varList = JSON.parse(jsonVars);
            
            // option tags
            varList.forEach(listVar => {
                if (types.includes(listVar.varType) && listVar.varName[0] !== '_') {
                    var option = document.createElement('option');
                    $(option).attr({
                        'value':listVar.varName,
                        'text':listVar.varName,
                        'data-type':listVar.varType
                    });
                    // cell metadata test : defaultValue as selected
                    if (listVar.varName == defaultValue) {
                        $(option).prop('selected', true);
                    }
                    option.append(document.createTextNode(listVar.varName));
                    $(tag).append(option);
                }
            });

            // val-multi(select multiple) value list registration
            var classname = $(tag).attr('class');
            if (classname == 'var-multi') {
                $(tag).val(defaultValue);
            }

            // trigger change
            $(tag).trigger('change');
        }).catch(err => {
            vpLog.display(VP_LOG_TYPE.ERROR, 'Error on generating var selector', err);
        });
    }

    /**
     * Get tag value
     * @param {Object} pageThis parent this object
     * @param {Object} obj      state object to get tag value 
     * @param {string} parent   parent selector as string
     * @returns {string}        tag's value
     */
    var vp_getTagValue = function(pageThis, obj, parent='') {
        var value = '';
        let componentType = 'input';
        if (obj.component && obj.component.length == 1) {
            componentType = obj.component[0];
        } else {
            componentType = $(pageThis.wrapSelector(parent + ' #' + obj.name + '_type')).val();
        }
        switch (componentType) {
            case 'option_radio':
                var input = $(pageThis.wrapSelector(parent + " input[name='"+obj.name+"']:checked")).val();
                // same as default
                if (input == obj.default) break;
                value = input;
                break;
            case 'option_checkbox':
                let checked = $(pageThis.wrapSelector(parent + " input[name='"+obj.name+"']:checked")).val();

                for (var i = 0; i < checked.length; i++) {
                    value += "'" + $(checked[i]).val() + "',";
                }
                value = value.substr(0, value.length-1);
                break;
            case 'bool_checkbox':
                let isChecked = $(pageThis.wrapSelector(parent + ' #'+obj.name)).prop('checked');
                value = isChecked?'True':'False';
                break;
            case 'var_multi':
                let multiValue = $(pageThis.wrapSelector(parent + ' #'+obj.name)).val();
                if (multiValue && multiValue.length > 0) {
                    value = multiValue.join(', ');
                } else {
                    value = '';
                }
                break;
            case 'input_multi':
            case 'bool_select':
            case 'data_select':
            case 'var_select':
            case 'col_select':
            case 'dtype':
                value = $(pageThis.wrapSelector(parent + ' #'+obj.name)).val();
                break;
            case 'col_multi':
                let colList = pageThis.autoGen[obj.name].getDataList();
                pageThis.state[obj.name] = colList.map(data => { return data.code });
                value = colList.map(data => { return data.code }).join(',');
                if (colList.length == 0) {
                    value = '';
                } else if (colList.length > 0) {
                    value = '[' + value + ']';
                }
                $(pageThis.wrapSelector('#'+obj.name)).val(value);
                break;
            case 'file-open':
            case 'file-save':
            case 'table':
            case 'option_select':
            case 'option_suggest':
            case 'input_number':
            default:
                var input = $(pageThis.wrapSelector(parent + ' #'+obj.name)).val();
                // same as default
                if (input == obj.default) break;
                value = input;
        }
        return value;
    }

    /**
     * Generate code
     * @param {Object} pageThis
     * @param {Object} package 
     * @param {Object} state      [optional]
     * @param {string} etcOptions [optional] userOptionCode addition ex) ", test='TEST'"
     * @param {string} parent     [optional] parent selector as string
     * @returns {string} generated code / if error, null
     */
    var vp_codeGenerator = function(pageThis, package, state = {}, etcOptions = '', parent='') {
        var code = package.code;
        
        try {
            package.options && package.options.forEach(function(v, i) {
                var val = state[v.name];
                if (val == undefined || val == '' || val == v.default) {
                    if (pageThis) {
                        val = vp_getTagValue(pageThis, v, parent=parent);
                    }
                }
                var id = '${' + v.name + '}';
                if (val == undefined || val.trim() == '') {
                    if (v.required == true) {
                        // throw new Error("'" + v.label + "' is required.");
                    }
                    // if no value, replace it
                    code = code.split(id).join('');
                } else {
                    // text quotation
                    if (v.type == 'text' 
                        || (v.component != undefined && (v.component.includes('file-open') || v.component.includes('file-save')))) {
                        val = "'"+val+"'";
                    } 
                    // code completion
                    if (v.code != undefined) {
                        val = v.code.split(id).join(val);
                    }
                    // code completion 2
                    if (v.usePair == true) {
                        if (v.pairKey) {
                            val = ', ' + v.pairKey + '=' + val;
                        } else {
                            val = ', ' + v.name + '=' + val;
                        }
                    }
                    // code completion 3
                    if (v.component != undefined && v.componentCode != undefined) {
                        let autoSelector = state[v.name + '_type'];
                        let compIdx = v.component.indexOf(autoSelector);
                        if (compIdx < 0) {
                            compIdx = 0;
                        }
                        let compCode = v.componentCode[compIdx];
                        if (compCode != '') {
                            val = compCode.split(id).join(val);
                        }
                    }
                    code = code.split(id).join(val);
                }
            });

            // additional userOptionCode
            code = code.split('${etc}').join(etcOptions);

            // () prevent code: (, ${v})
            code = code.split('(, ').join('(');

            // prevent code: no allocation variable ( = pd.DataFrame())
            if (code.startsWith(' = ')) {
                code = code.substr(3);
            } 
            // prevent code: without allocation code (${o0} = code)
            let outputCodeMatch = code.match(/^\$\{.+\} = /);
            if (outputCodeMatch) {
                let matchLength = outputCodeMatch[0].length;
                let matchStartIdx = outputCodeMatch['index'];
                code = code.substr(matchStartIdx + matchLength);
            }
            // show_result 
            // get output variables
            if (_VP_SHOW_RESULT && package.options) {
                var outputOptList = package.options.filter(x => x.output === true);
                var outputStr = '';
                if (pageThis) {
                    outputOptList.forEach(opt => {
                        outputStr += (outputStr !== ''?', ':'') + vp_getTagValue(pageThis, opt);
                    })
                }
                if (outputStr != '') {
                    code += '\n'+ outputStr;
                }
            }


        } catch (e) {
            vpLog.display(VP_LOG_TYPE.ERROR, 'com_generator v2 code generation error ' + e.message);
            return null;
        }
        return code;
    }

    /**
     * Bind columns source function
     * @param {object} pageThis
     * @param {object} targetId 
     * @param {array} columnInputIdList 
     * @param {string} tagType input / select (tag type)
     * @param {array/boolean} columnWithEmpty boolean array or value to decide whether select tag has empty space
     * @param {array/boolean} columnWithIndex boolean array or value to decide whether select tag has index option
     * Usage : 
     *  $(document).on('change', this.wrapSelector('#dataframe_tag_id'), function() {
     *      pdGen.vp_bindColumnSource(that, 'dataframe_tag_id', ['column_input_id'], 'select', false, false);
     *  });
     */
    var vp_bindColumnSource = function(pageThis, targetId, columnInputIdList, tagType="input", columnWithEmpty=false, columnWithIndex=false) {
        var varName = pageThis.state[targetId];
        if (varName === '') {
            // reset with no source
            columnInputIdList && columnInputIdList.forEach(columnInputId => {
                let defaultValue = pageThis.state[columnInputId];
                if (defaultValue === null || defaultValue === undefined) {
                    defaultValue = '';
                }
                if (tagType == 'input') {
                    var suggestInputX = new SuggestInput();
                    suggestInputX.setComponentID(columnInputId);
                    suggestInputX.addClass('vp-input vp-state');
                    suggestInputX.setNormalFilter(false);
                    suggestInputX.setValue(defaultValue);
                    $(pageThis.wrapSelector('#' + columnInputId)).replaceWith(function() {
                        return suggestInputX.toTagString();
                    });
                } else {
                    // option tags
                    var tag = $('<select></select>').attr({
                        'id': columnInputId,
                        'class': 'vp-select vp-state'
                    });
                    $(pageThis.wrapSelector('#' + columnInputId)).replaceWith(function() {
                        return $(tag);
                    });
                }
            });
            return ;
        }
        // get result and show on detail box
        vpKernel.getColumnList(varName).then(function(resultObj) {
            try {
                let { result, type, msg } = resultObj;
                var { list } = JSON.parse(result);

                // check if it needs to add index option
                let addIndex = false;
                if (Array.isArray(columnWithIndex)) {
                    addIndex = columnWithIndex[idx];
                } else {
                    addIndex = columnWithIndex;
                }
                if (addIndex == true) {
                    list = [
                        {value: varName + '.index', label: 'index'},
                        ...list
                    ]
                }

                // check if it needs to add empty option
                let addEmpty = false;
                if (Array.isArray(columnWithEmpty)) {
                    addEmpty = columnWithEmpty[idx];
                } else {
                    addEmpty = columnWithEmpty;
                }
                if (addEmpty == true) {
                    list = [
                        {value: '', label: 'Select option...'},
                        ...list
                    ]
                }

                // columns using suggestInput
                columnInputIdList && columnInputIdList.forEach((columnInputId, idx) => {
                    let defaultValue = pageThis.state[columnInputId];
                    if (defaultValue === null || defaultValue === undefined) {
                        defaultValue = '';
                    }
                    // create tag
                    if (tagType == 'input') {
                        var suggestInputX = new SuggestInput();
                        suggestInputX.setComponentID(columnInputId);
                        suggestInputX.addClass('vp-input vp-state');
                        suggestInputX.setPlaceholder("column name");
                        suggestInputX.setSuggestList(function() { return list; }); //FIXME:
                        suggestInputX.setNormalFilter(false);
                        suggestInputX.setValue(defaultValue);
                        $(pageThis.wrapSelector('#' + columnInputId)).replaceWith(function() {
                            return suggestInputX.toTagString();
                        });
                    } else {
                        var tag = $('<select></select>').attr({
                            'id': columnInputId,
                            'class': 'vp-select vp-state'
                        });
                        // make tag
                        list.forEach((listVar, idx) => {
                            var option = document.createElement('option');
                            $(option).attr({
                                'value':listVar.value,
                                'text':listVar.label,
                                'data-type':listVar.dtype
                            });
                            // cell metadata test : defaultValue as selected
                            if (listVar.value === defaultValue) {
                                $(option).prop('selected', true);
                            }
                            option.append(document.createTextNode(listVar.label));
                            $(tag).append(option);
                        });
                        $(pageThis.wrapSelector('#' + columnInputId)).replaceWith(function() {
                            return $(tag);
                        });
                        $(pageThis.wrapSelector('#' + columnInputId)).trigger('change');
                    }
                }).catch(function(err) {
                    vpLog.display(VP_LOG_TYPE.ERROR, 'com_generator - bindColumnSource error ', err)
                });
                
                
            } catch (e) {
                vpLog.display(VP_LOG_TYPE.ERROR, 'com_generator - bindColumnSource: not supported data type. ', e);
            }
        });
    }

    //========================================================================
    // Render components
    //========================================================================
    var render1dLen = function(pageThis, obj, state) {
        state = {
            [obj.name]: '',
            ...state
        };
        return $(`<div class="vp-numpy-style-flex-row">
            <div class="vp-numpy-style-flex-row" style="margin-right:10px;">
                <span class="vp-numpy-style-flex-column-center mr5">
                    Length
                </span>
                <input type="text" id="${obj.name}" value="${state[obj.name]}" class="vp-input vp-state" style="width:200px;" placeholder="Input Number">
            </div>
        </div>`)
    }

    var render2dLen = function(pageThis, obj, state) {
        state = {
            [obj.name + '_row']: '',
            [obj.name + '_col']: '',
            ...state
        }
        return $(`<div class="vp-numpy-style-flex-row">
            <div class="vp-numpy-style-flex-row" style="margin-right:10px;">
                <span class="vp-numpy-style-flex-column-center" style="margin-right:5px;">
                    Row
                </span>
                <input type="text" id="${obj.name}_row" data-id="${obj.name}" value="${state[obj.name+'_row']}" class="vp-input vp-state vp-numpy-2dlen-item" style="width:150px;" placeholder="Number">
            </div>
            <div class="vp-numpy-style-flex-row" style="margin-right:10px;">
                <span class="vp-numpy-style-flex-column-center" style="margin-right:5px;">
                    Col
                </span>
                <input type="text" id="${obj.name}_col" data-id="${obj.name}"  value="${state[obj.name+'_col']}" class="vp-input vp-state vp-numpy-2dlen-item" style="width:150px;" placeholder="Number">
            </div>
            <input type="hidden" class="vp-state" id="${obj.name}" value="${state[obj.name]}">
        </div>`);
    }

    var render3dLen = function(pageThis, obj, state) {
        state = {
            [obj.name + '_plane']: '',
            [obj.name + '_row']: '',
            [obj.name + '_col']: '',
            ...state
        }
        return $(`<div class="vp-numpy-style-flex-row">
            <div class="vp-numpy-style-flex-row" style="margin-right:10px;">
                <span class="vp-numpy-style-flex-column-center" style="margin-right:5px;">
                    Plane
                </span>
                <input type="text" id="${obj.name}_plane" data-id="${obj.name}" value="${state[obj.name+'_plane']}" class="vp-input vp-state vp-numpy-3dlen-item" style="width:150px;" placeholder="Number">
            </div>
            <div class="vp-numpy-style-flex-row" style="margin-right:10px;">
                <span class="vp-numpy-style-flex-column-center" style="margin-right:5px;">
                    Row
                </span>
                <input type="text" id="${obj.name}_row" data-id="${obj.name}" value="${state[obj.name+'_row']}" class="vp-input vp-state vp-numpy-3dlen-item" style="width:150px;" placeholder="Number">
            </div>
            <div class="vp-numpy-style-flex-row" style="margin-right:10px;">
                <span class="vp-numpy-style-flex-column-center" style="margin-right:5px;">
                    Col
                </span>
                <input type="text" id="${obj.name}_col" data-id="${obj.name}"  value="${state[obj.name+'_col']}" class="vp-input vp-state vp-numpy-3dlen-item" style="width:150px;" placeholder="Number">
            </div>
            <input type="hidden" class="vp-state" id="${obj.name}" value="${state[obj.name]}">
        </div>`);
    }

    var render1dArr = function(pageThis, obj, state) {
        let arrKey = obj.name + '_1darr';
        let arrState = [ 0 ];
        let value = `[${arrState.join(',')}]`;
        if (state[arrKey] == undefined) {
            pageThis.setState({ [arrKey]: arrState });
            pageThis.setState({ [obj.name]: value});
        } else {
            arrState = state[arrKey];
            value = `[${arrState.join(',')}]`;
        }

        let contentTag = $(`<div class="vp-numpy-1darr-box"></div>`);
        $(contentTag).attr({
            'data-id': obj.name
        });
        contentTag.data('obj', obj);
        // Length setting
        contentTag.append($(`<div class="vp-numpy-style-flex-row-center">
            <div style="margin:0 5px;">
                <span>Length : </span>
                <input class="vp-input vp-numpy-1darr-set-num" style="width:50px;"
                    value="${arrState.length}" type="number">
            </div>
            <button class="vp-button vp-numpy-1darr-set">
                Set
            </button>
            <input type="hidden" class="vp-state" id="${obj.name}" value="${value}">
        </div>`));
        // Array Items
        let arrItems = $(`<div class="vp-numpy-style-flex-row-wrap vp-numpy-1darr-item-box"></div>`);
        arrState.forEach((item, idx) => {
            arrItems.append(render1dArrItem(idx, item));
        });
        contentTag.append(arrItems);
        // add button
        contentTag.append($(`<button class="vp-button vp-numpy-1darr-add">+ Add</button>`));
        return contentTag;
    }

    var render1dArrItem = function(idx, value=0) {
        return $(`<div class="vp-numpy-style-flex-column" style="margin-top:10px;;margin-bottom:10px;">
            <div class="text-center" style="margin-top:10px;;margin-bottom:10px;">
                ${idx}
            </div>
            <input class="vp-input vp-numpy-1darr-item" style="width:40px;" type="text" data-idx="${idx}" value="${value}">
            <button class="vp-button vp-numpy-1darr-del" style="width:40px;">
                x
            </button>
        </div>`);
    }

    var render2dArr = function(pageThis, obj, state) {
        let arrKey = obj.name + '_2darr';
        let arrState = [[0]];
        let value = `[[0]]`;
        if (state[arrKey] == undefined) {
            pageThis.setState({ [arrKey]: arrState });
            pageThis.setState({ [obj.name]: value});
        } else {
            arrState = state[arrKey];
            value = `[${arrState.map(ele => '[' + ele.join(',') + ']').join(',')}]`;
        }

        let contentTag = $(`<div class="vp-numpy-2darr-box"></div>`);
        $(contentTag).attr({
            'data-id': obj.name
        });
        contentTag.data('obj', obj);
        // Length setting
        let rowLength = arrState.length;
        let colLength = 0;
        if (arrState.length > 0) {
            colLength = Math.max(...arrState.map(ele => ele.length));
        }
        contentTag.append(`<div class="vp-numpy-style-flex-row-center">
            <div style="margin:0 5px;">
                <span>Row : </span>
                <input class="vp-input vp-numpy-2darr-set-row" style="width:50px;" value="${rowLength}" type="text">
            </div>
            <div style="margin:0 5px;">
                <span>Col : </span>
                <input class="vp-input vp-numpy-2darr-set-col" style="width:50px;" value="${colLength}" type="text">
            </div>
            <button class="vp-button vp-numpy-2darr-set">Set</button>
            <input type="hidden" class="vp-state" id="${obj.name}" value="${value}">
        </div>`)
        // Array Items
        let arrItems = $(`<div class="vp-numpy-style-flex-column vp-numpy-2darr-item-box"></div>`);
        arrState.forEach((item, idx) => {
            arrItems.append(render2dArrItem(idx, item));
        });
        contentTag.append(arrItems);
        // row add button
        contentTag.append($(`<button class="vp-button vp-numpy-2darr-row-add" style="width: 100%;">+ Row</button>`));
        return contentTag;
    }

    var render2dArrItem = function(rowIdx, item) {
        let arrRowBox = $(`<div class="vp-numpy-arrayEditor-row-block vp-numpy-style-flex-row vp-numpy-box-border"></div>`);
        let arrRows = $(`<div class="vp-numpy-style-flex-row" style="width: 80%; margin-top:5px; margin-bottom:5px;"></div>`);
        // row index
        arrRows.append($(`<div class="vp-numpy-style-flex-column-center vp-bold vp-numpy-2darr-row" data-idx="${rowIdx}" style="width: 10%;">
            ${rowIdx}
        </div>`))
        // columns
        let arrColBox = $(`<div class="vp-numpy-style-flex-column" style="width: 90%;"></div>`);
        let arrCols = $(`<div class="vp-numpy-array-row-container vp-numpy-style-flex-row-wrap" style="width:100%;"></div>`);
        item.forEach((col, idx) => {
            arrCols.append($(`<div class="vp-numpy-style-flex-column" style="margin-top:5px">
                <span class="vp-numpy-style-flex-row-center vp-bold">
                    ${idx}
                </span>
                <input class="vp-input vp-numpy-2darr-item" style="width:40px;" value="${col}" data-rowidx="${rowIdx}" data-idx="${idx}" type="text">
                <button class="vp-button vp-numpy-2darr-col-del" style="width:40px;" title="Delete column">
                    x
                </button>
            </div>`));
        });
        arrColBox.append(arrCols);
        arrRows.append(arrColBox);
        arrRowBox.append(arrRows);
        // col add button
        arrRowBox.append($(`<div class="vp-numpy-style-flex-column-center" style="width:10%;">
            <button class="vp-button vp-numpy-2darr-col-add" style="width: 100%;height:40px;max-height:80px;" title="Add column">+</button>
        </div>`));
        // row delete button
        arrRowBox.append($(`<div class="vp-numpy-style-flex-column-center" style="width:10%;">
            <button class="vp-button vp-numpy-2darr-row-del" style="width: 100%;height:40px;max-height:80px;" title="Delete row">x</button>
        </div>`));
        return arrRowBox;
    }

    var renderNdArr = function(pageThis, obj, state) {
        let arrKey = obj.name + '_ndarr';
        let arrState = [ '' ];
        let value = `${arrState.join(',')}`;
        if (state[arrKey] == undefined) {
            pageThis.setState({ [arrKey]: arrState });
            pageThis.setState({ [obj.name]: value});
        } else {
            arrState = state[arrKey];
            value = `${arrState.join(',')}`;
        }

        let contentTag = $(`<div class="vp-numpy-ndarr-box"></div>`);
        $(contentTag).attr({
            'data-id': obj.name
        });
        contentTag.data('obj', obj);
        // Array Items
        let arrItems = $(`<div class="vp-numpy-style-flex-row-between-wrap vp-scrollbar" style="max-height: 200px; overflow: auto;"></div>`);
        arrState.forEach((item, idx) => {
            arrItems.append($(`<div class="vp-numpy-style-flex-row">
                <div class="vp-numpy-style-flex-column-center vp-bold mr5 w10">
                    ${idx + 1}
                </div>
                <input class="vp-numpy-input vp-numpy-ndarr-item" data-idx="${idx}" value="${item}" type="text" placeholder="Value">
                <button class="vp-button vp-numpy-ndarr-del w30">x</button>
            </div>`));
        });
        contentTag.append(arrItems);
        // add button
        contentTag.append($(`<button class="vp-button vp-numpy-ndarr-add w30">+</button>`));
        return contentTag;
    }

    var renderScalar = function(pageThis, obj, state) {
        let placeholder = 'Input Scalar';
        if (obj.placeholder) {
            placeholder = obj.placeholder;
        }
        return $(`<input class="vp-input vp-state" id="${obj.name}" placeholder="${placeholder}" value="${state[obj.name]}"/>`);
    }

    var renderParam = function(pageThis, obj, defaultValue) {
        let placeholder = 'Input Param';
        if (obj.placeholder) {
            placeholder = obj.placeholder;
        }
        return $(`<input class="vp-input vp-state" id="${obj.name}" placeholder="${placeholder}" value="${state[obj.name]}"/>`);
    }

    var renderDtypeSelector = function(pageThis, obj, defaultValue) {
        let slctTag = $('<select></select>').attr({
            class: 'vp-select vp-state',
            id: obj.name
        });
        _VP_NP_DTYPES.forEach(dtypeObj => {
            let { name, value } = dtypeObj;
            let option = $(`<option>${name}</option>`).attr({
                'value': value
            });
            if (value != undefined && value == defaultValue) {
                $(option).attr({
                    'selected':'selected'
                });
            }
            slctTag.append(option);
        });
        return slctTag;
    }

    var renderTabBlock = function(pageThis, obj, defaultValue) {
        return $('<input value="tabblock"/>');
    }

    var bindMultiSelector = function(pageThis) {
        //====================================================================
        // for column multi selector
        //====================================================================
        $(pageThis.wrapSelector('.vp-auto-multi-column')).each((idx, tag) => {
            let compId = tag.id;
            let id = $(tag).data('id');
            let targetId = $(tag).data('target');
            let colSelector = new MultiSelector(
                pageThis.wrapSelector('#' + compId), 
                { 
                    mode: 'columns', parent: (pageThis.state[targetId] || ''), selectedList: pageThis.state[compId],
                    change: function(type, list) {
                        let value = list.map(data => { return data.code }).join(',');
                        if (list.length == 0) {
                            value = '';
                        } else if (list.length > 0) {
                            value = '[' + value + ']';
                        }
                        pageThis.state[compId] = list.map(data => { return data.code });
                        pageThis.state[id] = value;
                        $(pageThis.wrapSelector('#'+id)).val(value);
                    }
                }
            );
            pageThis.autoGen = {
                [id]: colSelector,
                ...pageThis.autoGen
            };
            $(pageThis.wrapSelector('#' + targetId)).on('change', function() {
                let targetVariable = $(this).val();
                let colSelector = new MultiSelector(
                    pageThis.wrapSelector('#' + compId), 
                    { 
                        mode: 'columns', parent: targetVariable, selectedList: pageThis.state[compId],
                        change: function(type, list) {
                            let value = list.map(data => { return data.code }).join(',');
                            if (list.length == 0) {
                                value = '';
                            } else if (list.length > 0) {
                                value = '[' + value + ']';
                            }
                            pageThis.state[compId] = list.map(data => { return data.code });
                            pageThis.state[id] = value;
                            $(pageThis.wrapSelector('#'+id)).val(value);
                        }
                    },
                );
                pageThis.autoGen = {
                    [id]: colSelector,
                    ...pageThis.autoGen
                };
            });
            
        });
    }

    var bindAutoComponentEvent = function(pageThis) {
        let selector = pageThis.wrapSelector();
        // Auto-component selector
        $(selector).on('change', '.vp-auto-component-selector', function() {
            let contentTag = $(this).parent().find('.vp-auto-component-content');
            let newType = $(this).val();
            let obj = $(this).data('obj');
            $(contentTag).html(renderContent(pageThis, newType, obj, pageThis.getState()));
        }); 

        //====================================================================
        // Event for 2dLen
        //====================================================================
        $(selector).on('change', '.vp-numpy-2dlen-item', function() {
            let id = $(this).data('id');
            let newValue = pageThis.getState(id+'_row') + ',' + pageThis.getState(id+'_col');
            $(pageThis.wrapSelector('#' + id)).val(newValue);
            $(pageThis.wrapSelector('#' + id)).trigger('change');
        }); 

        //====================================================================
        // Event for 3dLen
        //====================================================================
        $(selector).on('change', '.vp-numpy-3dlen-item', function() {
            let id = $(this).data('id');
            let newValue = pageThis.getState(id+'_plane') + ',' + pageThis.getState(id+'_row') + ',' + pageThis.getState(id+'_col');
            $(pageThis.wrapSelector('#' + id)).val(newValue);
            $(pageThis.wrapSelector('#' + id)).trigger('change');
        }); 

        //====================================================================
        // Event for 1dArr
        //====================================================================
        $(selector).on('click', '.vp-numpy-1darr-set', function() {
            let id = $(this).closest('.vp-numpy-1darr-box').data('id');
            let arrId = id + '_1darr';
            let len = $(this).parent().find('.vp-numpy-1darr-set-num').val();
            // update state
            let state = Array(parseInt(len)).fill(0);
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: `[${state.join(',')}]` });
            // re-render
            let obj = $(this).closest('.vp-numpy-1darr-box').data('obj');
            $(this).closest('.vp-numpy-1darr-box').replaceWith(function() {
                return render1dArr(pageThis, obj, pageThis.getState());
            });
        }); 

        $(selector).on('click', '.vp-numpy-1darr-del', function() {
            let id = $(this).closest('.vp-numpy-1darr-box').data('id');
            let arrId = id + '_1darr';
            let idx = $(this).parent().find('.vp-numpy-1darr-item').data('idx');
            // update state
            let state = pageThis.getState(arrId);
            state.splice(idx, 1);
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: `[${state.join(',')}]` });
            // re-render
            let obj = $(this).closest('.vp-numpy-1darr-box').data('obj');
            $(this).closest('.vp-numpy-1darr-box').replaceWith(function() {
                return render1dArr(pageThis, obj, pageThis.getState());
            });
        });

        $(selector).on('click', '.vp-numpy-1darr-add', function() {
            let id = $(this).closest('.vp-numpy-1darr-box').data('id');
            let arrId = id + '_1darr';
            let idx = 0;
            // update state
            let state = pageThis.getState(arrId);
            if (!state) {
                state = [];
            } else {
                idx = state.length;
            }
            state.push(0);
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: `[${state.join(',')}]` });
            // re-render
            let obj = $(this).closest('.vp-numpy-1darr-box').data('obj');
            $(this).closest('.vp-numpy-1darr-box').replaceWith(function() {
                return render1dArr(pageThis, obj, pageThis.getState());
            });
        });

        $(selector).on('change', '.vp-numpy-1darr-item', function() {
            let id = $(this).closest('.vp-numpy-1darr-box').data('id');
            let arrId = id + '_1darr';
            let idx = $(this).data('idx');
            let value = $(this).val();
            // update state
            let state = pageThis.getState(arrId);
            state[idx] = value;
            let code = `[${state.join(',')}]`;
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: code });
            $(pageThis.wrapSelector('#'+id)).val(code);
        });

        //====================================================================
        // Event for 2dArr
        //====================================================================
        $(selector).on('click', '.vp-numpy-2darr-set', function() {
            let id = $(this).closest('.vp-numpy-2darr-box').data('id');
            let arrId = id + '_2darr';
            let row = $(this).parent().find('.vp-numpy-2darr-set-row').val();
            let col = $(this).parent().find('.vp-numpy-2darr-set-col').val();
            // update state
            let state = Array(parseInt(row));
            for (let i = 0; i < state.length; i++) {
                state[i] = Array(parseInt(col)).fill(0);
            }
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: `[${state.map(ele => '[' + ele.join(',') + ']').join(',')}]` });
            // re-render
            let obj = $(this).closest('.vp-numpy-2darr-box').data('obj');
            $(this).closest('.vp-numpy-2darr-box').replaceWith(function() {
                return render2dArr(pageThis, obj, pageThis.getState());
            });
        }); 

        $(selector).on('click', '.vp-numpy-2darr-row-del', function() {
            let id = $(this).closest('.vp-numpy-2darr-box').data('id');
            let arrId = id + '_2darr';
            let idx = $(this).parent().parent().find('.vp-numpy-2darr-row').data('idx');
            // update state
            let state = pageThis.getState(arrId);
            state.splice(idx, 1);
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: `[${state.map(ele => '[' + ele.join(',') + ']').join(',')}]` });
            // re-render
            let obj = $(this).closest('.vp-numpy-2darr-box').data('obj');
            $(this).closest('.vp-numpy-2darr-box').replaceWith(function() {
                return render2dArr(pageThis, obj, pageThis.getState());
            });
        });

        $(selector).on('click', '.vp-numpy-2darr-row-add', function() {
            let id = $(this).closest('.vp-numpy-2darr-box').data('id');
            let arrId = id + '_2darr';
            // update state
            let state = pageThis.getState(arrId);
            if (!state) {
                state = [];
            }
            state.push([0]);
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: `[${state.map(ele => '[' + ele.join(',') + ']').join(',')}]` });
            // re-render
            let obj = $(this).closest('.vp-numpy-2darr-box').data('obj');
            $(this).closest('.vp-numpy-2darr-box').replaceWith(function() {
                return render2dArr(pageThis, obj, pageThis.getState());
            });
        });

        $(selector).on('click', '.vp-numpy-2darr-col-del', function() {
            let id = $(this).closest('.vp-numpy-2darr-box').data('id');
            let arrId = id + '_2darr';
            let rowIdx = $(this).parent().parent().find('.vp-numpy-2darr-item').data('rowidx');
            let idx = $(this).parent().find('.vp-numpy-2darr-item').data('idx');
            // update state
            let state = pageThis.getState(arrId);
            state[rowIdx].splice(idx, 1);
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: `[${state.map(ele => '[' + ele.join(',') + ']').join(',')}]` });
            // re-render
            let obj = $(this).closest('.vp-numpy-2darr-box').data('obj');
            $(this).closest('.vp-numpy-2darr-box').replaceWith(function() {
                return render2dArr(pageThis, obj, pageThis.getState());
            });
        });

        $(selector).on('click', '.vp-numpy-2darr-col-add', function() {
            let id = $(this).closest('.vp-numpy-2darr-box').data('id');
            let arrId = id + '_2darr';
            let rowIdx = $(this).parent().parent().find('.vp-numpy-2darr-item').data('rowidx');
            // update state
            let state = pageThis.getState(arrId);
            if (!state) {
                state = Array(rowIdx + 1);
                for (let i = 0; i < state.length; i++) {
                    state[i] = [];
                }
            }
            state[rowIdx].push(0);
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: `[${state.map(ele => '[' + ele.join(',') + ']').join(',')}]` });
            // re-render
            let obj = $(this).closest('.vp-numpy-2darr-box').data('obj');
            $(this).closest('.vp-numpy-2darr-box').replaceWith(function() {
                return render2dArr(pageThis, obj, pageThis.getState());
            });
        });

        $(selector).on('change', '.vp-numpy-2darr-item', function() {
            let id = $(this).closest('.vp-numpy-2darr-box').data('id');
            let arrId = id + '_2darr';
            let rowIdx = $(this).data('rowidx');
            let idx = $(this).data('idx');
            let value = $(this).val();
            // update state
            let state = pageThis.getState(arrId);
            state[rowIdx][idx] = value;
            let code = `[${state.map(ele => '[' + ele.join(',') + ']').join(',')}]`;
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: code });
            $(pageThis.wrapSelector('#'+id)).val(code);
        });

        //====================================================================
        // Event for ndArr
        //====================================================================
        $(selector).on('click', '.vp-numpy-ndarr-del', function() {
            let id = $(this).closest('.vp-numpy-ndarr-box').data('id');
            let arrId = id + '_ndarr';
            let idx = $(this).parent().find('.vp-numpy-ndarr-item').data('idx');
            // update state
            let state = pageThis.getState(arrId);
            state.splice(idx, 1);
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: `${state.join(',')}` });
            // re-render
            let obj = $(this).closest('.vp-numpy-ndarr-box').data('obj');
            $(this).closest('.vp-numpy-ndarr-box').replaceWith(function() {
                return renderNdArr(pageThis, obj, pageThis.getState());
            });
        });

        $(selector).on('click', '.vp-numpy-ndarr-add', function() {
            let id = $(this).closest('.vp-numpy-ndarr-box').data('id');
            let arrId = id + '_ndarr';
            let idx = 0;
            // update state
            let state = pageThis.getState(arrId);
            if (!state) {
                state = [ ];
            } else {
                idx = state.length;
            }
            state.push(0);
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: `${state.join(',')}` });
            // re-render
            let obj = $(this).closest('.vp-numpy-ndarr-box').data('obj');
            $(this).closest('.vp-numpy-ndarr-box').replaceWith(function() {
                return renderNdArr(pageThis, obj, pageThis.getState());
            });
        });

        $(selector).on('change', '.vp-numpy-ndarr-item', function() {
            let id = $(this).closest('.vp-numpy-ndarr-box').data('id');
            let arrId = id + '_ndarr';
            let idx = $(this).data('idx');
            let value = $(this).val();
            // update state
            let state = pageThis.getState(arrId);
            state[idx] = value;
            let code = `${state.join(',')}`;
            pageThis.setState({ [arrId]: state });
            pageThis.setState({ [id]: code });
            $(pageThis.wrapSelector('#'+id)).val(code);
        });

        //====================================================================
        // Event for tabBlock
        //====================================================================
    }

    return {
        vp_showInterfaceOnPage: vp_showInterfaceOnPage,
        renderContent: renderContent,
        vp_codeGenerator: vp_codeGenerator,
        vp_generateVarSelect: vp_generateVarSelect,
        vp_getTagValue: vp_getTagValue,
        vp_bindColumnSource: vp_bindColumnSource
    };
});