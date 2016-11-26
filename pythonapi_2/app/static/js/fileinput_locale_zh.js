/*!
 * FileInput Spanish (Latin American) Translations
 *
 * This file must be loaded after 'fileinput.js'. Patterns in braces '{}', or
 * any HTML markup tags in the messages must not be converted or translated.
 *
 * @see http://github.com/kartik-v/bootstrap-fileinput
 *
 * NOTE: this file must be saved in UTF-8 encoding.
 */
(function ($) {
    "use strict";
    $.fn.fileinput.locales.es = {
    		fileSingle: '单个文件',
            filePlural: '多个文件',
            browseLabel: '选择文件 &hellip;',
            removeLabel: '删除文件',
            removeTitle: '删除选中文件',
            cancelLabel: '取消',
            cancelTitle: '取消上传',
            uploadLabel: '上传',
            uploadTitle: '上传选中文件',
            msgSizeTooLarge: '文件 "{name}" (<b>{size} KB</b>) 超过最大允许 <b>{maxSize} KB</b>. 请重新上传！',
            msgFilesTooLess: '文件数量必须大于 <b>{n}</b> {files} ，请重新上传！',
            msgFilesTooMany: '已选择的文件数量 <b>({n})</b> 超过最大允许限制： <b>{m}</b>. 请重新上传！',
            msgFileNotFound: '文件 "{name}" 未找到!',
            msgFileSecured: '安全限制防止读取文件"{name}"！',
            msgFileNotReadable: '文件"{name}" 无法读取！',
            msgFilePreviewAborted: '预览文件"{name}"时出错.',
            msgFilePreviewError: '读取文件 "{name}"时出错',
            msgInvalidFileType: '文件 "{name}"的类型无效. 只有 "{types}" 文件类型被支持！',
            msgInvalidFileExtension: '文件 "{name}"的无效扩展名. 只有 "{extensions}" 文件被支持！',
            msgValidationError: '文件上传错误',
            msgLoading: '加载文件 {index} 的 {files} ',
            msgProgress: '加载文件 {index} 的 {files} - {name} - {percent}% 完成.',
            msgSelected: '选中{n}个文件',
            msgFoldersNotAllowed: '选择或者拖拽中有 {n} 文件夹需要被跳过',
            dropZoneTitle: '选择或者拖拽上传文件'
    };

    $.extend($.fn.fileinput.defaults, $.fn.fileinput.locales.es);
})(window.jQuery);
