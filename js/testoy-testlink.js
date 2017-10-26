function getTestCaseIds(){
    element = document.getElementById('statusTableBody');
    count = element.childElementCount;
    var arr = [];
    for(var i=0; i<count; i++){
       full_name = element.children[i].getElementsByTagName('td')[0].innerHTML;
        regx = /^PLT\d+/gi;
        match_ret = full_name.match(regx);
        if(match_ret){
            arr.push(match_ret[0]);
        }
    }
    var ret = arr.map(function(key){return key.replace(/PLT/, 'PLT#-')});
    return ret;
}

function consistXmlBody(idArr){
    doc = document.implementation.createDocument("", "", null);

    var resultsNode = doc.createElement('results');

    for(var i=0; i<idArr.length; i++){
        var testCaseNode = doc.createElement('testcase');
        testCaseNode.setAttribute('external_id', idArr[i]);
        var resultNode = doc.createElement('result');
        var resultText = doc.createTextNode('p');
        resultNode.appendChild(resultText);
        var noteNode = doc.createElement('notes');
        testCaseNode.appendChild(resultNode);
        testCaseNode.appendChild(noteNode);
        resultsNode.appendChild(testCaseNode);
    }

    doc.appendChild(resultsNode);
    return doc;
}

function getXmlStringContent(docObj){
    var xmlString = new XMLSerializer().serializeToString(docObj);
    var xmlContent = 'data:text/xml;charset=utf-8,<?xml version="1.0" encoding="UTF-8"?>\n';
    xmlContent += xmlString;
    return xmlContent;
}

function formatXml(xml) {
    var formatted = '';
    var reg = /(>)(<)(\/*)/g;
    xml = xml.replace(reg, '$1\r\n$2$3');
    var pad = 0;
    jQuery.each(xml.split('\r\n'), function(index, node) {
        var indent = 0;
        if (node.match( /.+<\/\w[^>]*>$/ )) {
            indent = 0;
        } else if (node.match( /^<\/\w/ )) {
            if (pad != 0) {
                pad -= 1;
            }
        } else if (node.match( /^<\w([^>]*[^\/])?>.*$/ )) {
            indent = 1;
        } else {
            indent = 0;
        }

        var padding = '';
        for (var i = 0; i < pad; i++) {
            padding += '  ';
        }

        formatted += padding + node + '\r\n';
        pad += indent;
    });

    return formatted;
}

function downloadXmlFile(xmlContent){
    var encodedUri = encodeURI(xmlContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "my_data2.xml");
    document.body.appendChild(link);
    link.click();
}


//Step 1. get test case id and status 
var case_ids = getTestCaseIds();
//Step 2. generate xml string
var xmlString = consistXmlBody(case_ids);
xmlString = getXmlStringContent(xmlString);
xmlString = formatXml(xmlString);
//Step 3. download this xml file
downloadXmlFile(xmlString);