// ==UserScript==
// @name         Is_Case_Recorded
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  this script will send request to check if test case recorded in Capillary
// @author       Jack Zheng
// @match        http://testoy.mo.sap.corp:8080/testoy/status/*
// @grant        GM_registerMenuCommand
// @grant	     GM_xmlhttpRequest
// ==/UserScript==

GM_registerMenuCommand('Is Case Recorded', main);

var capillaryReqeustUrl = "http://capillary.mo.sap.corp:8080/api/v1/testcases/by-case-id?mode=intelligent&caseIds=";

function getTestoyCaseResultMap(){
	element = document.getElementById('statusTableBody');
    count = element.childElementCount;
    var id_exit_map = new Map();
    for(var i=0; i<count; i++){
        var childNode = element.children[i];
        full_name = childNode.getElementsByTagName('td')[0].innerHTML;
        regx = /^PLT\d+/gi;
        match_ret = full_name.match(regx);
        if(match_ret){
            case_id = match_ret[0].replace(/PLT/, "PLT#-");
            if(isCaseRecorded(encodeURIComponent(case_id)))
			{
				// 't' for case record exit and f for not
				id_exit_map.set(case_id, "t");
			}else{
				id_exit_map.set(case_id, "f");
			}
        }
    }
    return id_exit_map;
}

function isCaseRecorded(case_id){
	var requestUrl = capillaryReqeustUrl + case_id;
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", capillaryReqeustUrl + case_id, false);
    xmlHttp.send(null);
    if(xmlHttp.status == 200){
        return "true";
    }else{
        return "";
    }
}

function consistXmlBody(map){
    doc = document.implementation.createDocument("", "", null);

    var resultsNode = doc.createElement('results');

    for(var [key, value] of map.entries()){
        var testCaseNode = doc.createElement('testcase');
        testCaseNode.setAttribute('external_id', key);
        var resultNode = doc.createElement('result');
        var resultText = doc.createTextNode(value);
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
	link.setAttribute("download", window.location.host.split('.')[0] + "_is_case_recorded.xml");
	document.body.appendChild(link);
    link.click();
}

function main(){
    //Step 1. get test case id and status
    var retMap = getTestoyCaseResultMap();
    //Step 2. generate xml string
    var xmlString = consistXmlBody(retMap);
    xmlString = getXmlStringContent(xmlString);
    xmlString = formatXml(xmlString);
    //Step 3. download this xml file
    downloadXmlFile(xmlString);
}

