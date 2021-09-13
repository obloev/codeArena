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

var editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
    lineNumbers: true,
    mode: 'text/x-python',
    theme: 'ayu-dark',
    tabSize: 4,
    indentUnit: 4,
    readOnly: false,
    autocorrect: true
});

function changeLang(){
    editor.setOption('mode', 'text/' + langs[document.getElementById('langu').value]);
}