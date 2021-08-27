import xbmc
import base64

from resources.lib import js2py

def translate(encoded_ajax):
    js_code = '''
    function trans(f){
	var g = f.replace(/[a-zA-Z]/g, function(a) {
		    return String.fromCharCode(("Z" >= a ? 90 : 122) >= (a = a.charCodeAt(0) + 13) ? a : a - 26)
	    })
	   return g;
    }
    '''
    js_code2 = '''
    function translate(f){
    for (var g = decodeURIComponent(f), k = [], l = 0; l < g.length; l++) {
            var m = g.charCodeAt(l);
            k[l] = 33 <= m && 126 >= m ? String.fromCharCode(33 + (m + 14) % 94) : String.fromCharCode(m)
        }
    g = k.join("");

    return g;
    }
    '''
    trans = js2py.eval_js(js_code)
    halfDecodedAjax = trans(encoded_ajax)
    translate = js2py.eval_js(js_code2)
    decodedAjax = translate(base64.b64decode(halfDecodedAjax).decode())

    return decodedAjax

def getKey():
    js = 'Math.round(new Date / 1E3)'
    key = js2py.eval_js(js)
    xbmc.log("Key: %s" %key,2)
    return key
