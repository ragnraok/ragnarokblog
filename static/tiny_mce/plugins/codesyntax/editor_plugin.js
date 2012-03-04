tinymce.create('tinymce.plugins.CodeSyntaxPlugin', {
    createControl: function(n, cm) {
        switch (n) {
            case 'codeformat':
                var mlb = cm.createListBox('codeformat', {
                    title: 'Format Code',
                    onselect: function(v) {
                        var content = new String(tinyMCE.activeEditor.selection.getContent());
                        content = content.replace(/<(p)([^>]*)>/g, '');
                        content = content.replace(/<\/(p)>/g, '');
                        //content = content.replace(/\/(&nbsp;)/g, '\n\r');

                            tinyMCE.activeEditor.selection.setContent('<pre id=\'code\' name=code class="' + v + '">' + content + '</pre>');
                    }
                });

                // Add some values to the list box
                mlb.add('C#', 'brush:csharp;');
                mlb.add('Html', 'brush:xhtml;');
                mlb.add('Xml/Xsl', 'brush:xml;');
                mlb.add('VB.Net', 'brush:vbnet;');
                mlb.add('SQL', 'brush:sql;');
                mlb.add('CSS', 'brush:css;');
                mlb.add('JavaScript', 'brush:jscript;');
                mlb.add('Python', 'brush:python;');
                mlb.add('Cpp', 'brush:cpp;')


                // Return the new listbox instance
                return mlb;
        }

        return null;
    },

    getInfo: function() {
        return {
            longname: 'Code Syntax Plugin',
            author: 'Jacobus Meintjes',
            authorurl: 'http://www.phoenixcode.net',
            infourl: 'http://alexgorbatchev.com/wiki/SyntaxHighlighter',
            version: '1.0'
        };
    }
});

    // Register plugin with a short name
    tinymce.PluginManager.add('codesyntax', tinymce.plugins.CodeSyntaxPlugin);
