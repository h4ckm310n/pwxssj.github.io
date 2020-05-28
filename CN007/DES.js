let IP_TABLE = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7];

let IP_I_TABLE = [40, 8, 48, 16, 56, 24, 64, 32,
                  39, 7, 47, 15, 55, 23, 63, 31,
                  38, 6, 46, 14, 54, 22, 62, 30,
                  37, 5, 45, 13, 53, 21, 61, 29,
                  36, 4, 44, 12, 52, 20, 60, 28,
                  35, 3, 43, 11, 51, 19, 59, 27,
                  34, 2, 42, 10, 50, 18, 58, 26,
                  33, 1, 41, 9, 49, 17, 57, 25];

let EP_TABLE = [32, 1, 2, 3, 4, 5,
                4, 5, 6, 7, 8, 9,
                8, 9, 10, 11, 12, 13,
                12, 13, 14, 15, 16, 17,
                16, 17, 18, 19, 20, 21,
                20, 21, 22, 23, 24, 25,
                24, 25, 26, 27, 28, 29,
                28, 29, 30, 31, 32, 1];

let P_TABLE = [16, 7, 20, 21, 29, 12, 28, 17,
               1, 15, 23, 26, 5, 18, 31, 10,
               2, 8, 24, 14, 32, 27, 3, 9,
               19, 13, 30, 6, 22, 11, 4, 25];

let S1 = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
          [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
          [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
          [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]];

let S2 = [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
          [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
          [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
          [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]];

let S3 = [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
          [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
          [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
          [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]];

let S4 = [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
          [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
          [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
          [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]];

let S5 = [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
          [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
          [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
          [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]];

let S6 = [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
          [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
          [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
          [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]];

let S7 = [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
          [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
          [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
          [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]];

let S8 = [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
          [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
          [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
          [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]];

let SBOX_TABLE = [S1, S2, S3, S4, S5, S6, S7, S8];

let PC1_TABLE = [57, 49, 41, 33, 25, 17, 9,
                 1, 58, 50, 42, 34, 26, 18,
                 10, 2, 59, 51, 43, 35, 27,
                 19, 11, 3, 60, 52, 44, 36,
                 63, 55, 47, 39, 31, 23, 15,
                 7, 62, 54, 46, 38, 30, 22,
                 14, 6, 61, 53, 45, 37, 29,
                 21, 13, 5, 28, 20, 12, 4];

let PC2_TABLE = [14, 17, 11, 24, 1, 5, 3, 28,
                 15, 6, 21, 10, 23, 19, 12, 4,
                 26, 8, 16, 7, 27, 20, 13, 2,
                 41, 52, 31, 37, 47, 55, 30, 40,
                 51, 45, 33, 48, 44, 49, 39, 56,
                 34, 53, 46, 42, 50, 36, 29, 32];

let HEX_TABLE = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'];
let BIN_TABLE = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
                 '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111'];

let SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1];


function DES(plain, key) {
    function split(text) {
        let l = text.slice(0, text.length/2), r = text.slice(text.length/2, text.length);
        add_process('<a style=\'color: blue\'>Split</a>' + '<br>' + l + '<br>' + r);
        return [l, r];
    }

    function permutation(text, table, name) {
        let text2 = "";
        for (let i=0; i<table.length; ++i) {
            text2 = text2.concat(text[table[i]-1]);
        }
        add_process('<a style=\'color: blue\'>' + name + '</a><br>' + text + '<br>' + text2);
        return text2;
    }

    function shift(text, n) {
        let text2 = "";
        for (let i=n; i<text.length; ++i)
            text2 = text2.concat(text[i]);
        for (let i=0; i<n; ++i)
            text2 = text2.concat(text[i]);
        add_process('<a style=\'color: blue\'>Shift</a> ' + n.toString() + '<br>' + text + '<br>' + text2);
        return text2;
    }

    function swap(text) {
        let text2 = "";
        for (let i=32; i<64; ++i)
            text2 = text2.concat(text[i]);
        for (let i=0; i<32; ++i)
            text2 = text2.concat(text[i]);
        add_process('<a style=\'color: blue\'>Swap</a><br>' + text + '<br>' + text2);
        return text2
    }

    function xor(text1, text2) {
        let result = "";
        for (let i=0; i<text1.length; ++i) {
            if (text1[i] == text2[i])
                result = result.concat('0');
            else
                result = result.concat('1');
        }
        add_process('<a style=\'color: blue\'>XOR</a><br>' + text1 + '<br>' + text2 + '<br>' + result);
        return result;
    }

    function sbox(text) {
        let result = "";
        for (let i=0; i<8; ++i) {
            let x = i * 6;
            let r = parseInt(text[x].concat(text[x+5]), 2);
            let c = parseInt(text.slice(x+1, x+5), 2);
            result = result.concat(BIN_TABLE[SBOX_TABLE[i][r][c]]);
        }
        add_process('<a style=\'color: blue\'>SBOX</a><br>' + text + '<br>' + result);
        return result;
    }

    function round(text, k, round_i) {
        add_process('<a style=\'color: red\'>Round: ' + round_i.toString() + '</a>');
        let sp = split(text);
        let l = sp[0], r = sp[1];
        let f = F(r, k);
        let result = xor(l, f);
        result = r.concat(result);
        add_process('<br>');
        return result;
    }

    function F(r, k) {
        let ep = permutation(r, EP_TABLE, 'EP');
        let x = xor(ep, k);
        let s = sbox(x);
        let result = permutation(s, P_TABLE, 'P');
        return result;
    }

    function convert(text, mode) {
        let result = "";
        let arr = [];
        let t1 = null, t2 = null;
        if (mode === 2) {
            t1 = HEX_TABLE;
            t2 = BIN_TABLE;
            for (let i=0; i<text.length; ++i)
                arr.push(text[i]);
        }
        else {
            t1 = BIN_TABLE;
            t2 = HEX_TABLE;
            for (let i=0; i<text.length; i+=4)
                arr.push(text[i].concat(text[i+1], text[i+2], text[i+3]));
        }
        for (let i=0; i<arr.length; ++i) {
            let n = t1.indexOf(arr[i]);
            result = result.concat(t2[n]);
        }
        add_process('<a style=\'color: blue\'>Convert</a><br>' + text + '<br>' + result);
        return result;
    }

    let k = permutation(convert(key, 2), PC1_TABLE, 'PC1');
    let p = permutation(convert(plain, 2), IP_TABLE, 'IP');
    let spk = split(k);
    let round_result = p;
    for (let i=0; i<16; ++i) {
        let sn = SHIFT_TABLE[i];
        let lk = shift(spk[0], sn);
        let rk = shift(spk[1], sn);
        let k = permutation(lk.concat(rk), PC2_TABLE, 'PC2');
        round_result = round(round_result, k, i+1);
        spk = [lk, rk];
    }
    let cipher_bin = permutation(swap(round_result), IP_I_TABLE, 'IP-1');
    let result = convert(cipher_bin, 16);
    console.log(result);
    return result;
}

