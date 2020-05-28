function RC4(plain, key) {
    function swap(S, i, j) {
        let S0 = S.toString();
        let t = S[i];
        S[i] = S[j];
        S[j] = t;
        add_process('<a style=\'color: blue\'>Swap</a><br>' + S0 + '<br>' + S.toString());
        return S;
    }

    function convert_ascii(text) {
        let result_arr = [];
        let result = "";
        for (let i=0; i<text.length; ++i) {
            result = result.concat(text[i].charCodeAt(0).toString());
            result_arr.push(text[i].charCodeAt(0));
        }
        add_process('<a style=\'color: blue\'>Convert</a><br>' + text + '<br>' + result);
        return result_arr;
    }

    function init(key) {
        let S = [], T = [];
        for (let i=0; i<256; ++i) {
            S.push(i);
            T.push(key[i % key.length]);
        }
        add_process('<a style=\'color: red\'>Init</a><br>' + S.toString() + '<br>' + T.toString());
        let j = 0;
        for (let i=0; i<256; ++i) {
            j = (j + S[i] + T[i]) % 256;
            add_process('i = ' + i.toString() + ', j = ' + j.toString());
            S = swap(S, i, j);
        }
        add_process('End Init: ' + S.toString());
        return [S, T];
    }

    function stream_gen(S, l) {
        let i = 0, j = 0, K = [];
        add_process('<a style=\'color: red\'>Stream Generation</a>');
        for (let n=0; n<l; ++n) {
            i = (i + 1) % 256;
            j = (j + S[i]) % 256;
            add_process('i = ' + i.toString() + ', j = ' + j.toString());
            S = swap(S, i, j);
            let t = (S[i] + S[j]) % 256;
            add_process('t = ' + t);
            K.push(S[t]);
        }
        add_process('K = [' + K.toString() + ']');
        return K;
    }

    function xor(text1, text2) {
        let result = "";
        for (let i=0; i<text1.length; ++i) {
            let x = (text1[i] ^ text2[i]).toString(2);
            let l = x.length;
            for (let j=0; j<8-l; ++j)
                x = '0'.concat(x);
            result = result.concat(x);
        }
        let l = result.length % 4;
        for (let i=0; i<l; ++i)
            result = '0'.concat(result);
        add_process('<a style=\'color: blue\'>XOR</a><br>' + text1.toString() + '<br>' + text2.toString() + '<br>' + result);
        return result;
    }

    function convert(text) {
        let result = "";
        let arr = [];
        t1 = BIN_TABLE;
        t2 = HEX_TABLE;
        for (let i=0; i<text.length; i+=4)
            arr.push(text[i].concat(text[i+1], text[i+2], text[i+3]));
        for (let i=0; i<arr.length; ++i) {
            let n = t1.indexOf(arr[i]);
            result = result.concat(t2[n]);
        }
        add_process('<a style=\'color: blue\'>Convert</a><br>' + text + '<br>' + result);
        return result;
    }

    let p = convert_ascii(plain);
    let k = convert_ascii(key);
    let ST = init(k);
    let K = stream_gen(ST[0], p.length);
    let result = xor(p, K);
    result = convert(result);
    console.log(result);
    return result;
}
