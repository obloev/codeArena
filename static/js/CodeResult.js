langs = {
    '50': 'x-csrc',
    '71': 'x-python',
    '62': 'x-java',
    '63': 'javascript',
    '54': 'x-c++src',
    '51': 'x-csharp',
    '67': 'x-pascal',
    '78': 'x-kotlin',
    '68': 'x-php',
}

let editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
    lineNumbers: true,
    mode: 'text/' + langs['{{ submission.lang_id }}'],
    theme: 'ayu-dark',
    tabSize: 4,
    indentUnit: 4,
    readOnly: true,
    autocorrect: true
});