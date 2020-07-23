(function(t) {
    var u = "", a = 0, h = [], z = [], A = 0, w = 0, o = [], v = [], p = true;
    function f() {
        return Math.round(Math.random() * 4294967295)
    }
    function k(E, F, B) {
        if (!B || B > 4) {
            B = 4
        }
        var C = 0;
        for (var D = F; D < F + B; D++) {
            C <<= 8;
            C |= E[D]
        }
        return (C & 4294967295) >>> 0
    }
    function b(C, D, B) {
        C[D + 3] = (B >> 0) & 255;
        C[D + 2] = (B >> 8) & 255;
        C[D + 1] = (B >> 16) & 255;
        C[D + 0] = (B >> 24) & 255
    }
    function y(E) {
        if (!E) {
            return ""
        }
        var B = "";
        for (var C = 0; C < E.length; C++) {
            var D = Number(E[C]).toString(16);
            if (D.length == 1) {
                D = "0" + D
            }
            B += D
        }
        return B
    }
    function x(C) {
        var D = "";
        for (var B = 0; B < C.length; B += 2) {
            D += String.fromCharCode(parseInt(C.substr(B, 2), 16))
        }
        return D
    }
    function c(E, B) {
        if (!E) {
            return ""
        }
        if (B) {
            E = m(E)
        }
        var D = [];
        for (var C = 0; C < E.length; C++) {
            D[C] = E.charCodeAt(C)
        }
        return y(D)
    }
    function m(E) {
        var D, F, C = [], B = E.length;
        for (D = 0; D < B; D++) {
            F = E.charCodeAt(D);
            if (F > 0 && F <= 127) {
                C.push(E.charAt(D))
            } else {
                if (F >= 128 && F <= 2047) {
                    C.push(String.fromCharCode(192 | ((F >> 6) & 31)), String.fromCharCode(128 | (F & 63)))
                } else {
                    if (F >= 2048 && F <= 65535) {
                        C.push(String.fromCharCode(224 | ((F >> 12) & 15)), String.fromCharCode(128 | ((F >> 6) & 63)), String.fromCharCode(128 | (F & 63)))
                    }
                }
            }
        }
        return C.join("")
    }
    function j(D) {
        h = new Array(8);
        z = new Array(8);
        A = w = 0;
        p = true;
        a = 0;
        var B = D.length;
        var E = 0;
        a = (B + 10) % 8;
        if (a != 0) {
            a = 8 - a
        }
        o = new Array(B + a + 10);
        h[0] = ((f() & 248) | a) & 255;
        for (var C = 1; C <= a; C++) {
            h[C] = f() & 255
        }
        a++;
        for (var C = 0; C < 8; C++) {
            z[C] = 0
        }
        E = 1;
        while (E <= 2) {
            if (a < 8) {
                h[a++] = f() & 255;
                E++
            }
            if (a == 8) {
                r()
            }
        }
        var C = 0;
        while (B > 0) {
            if (a < 8) {
                h[a++] = D[C++];
                B--
            }
            if (a == 8) {
                r()
            }
        }
        E = 1;
        while (E <= 7) {
            if (a < 8) {
                h[a++] = 0;
                E++
            }
            if (a == 8) {
                r()
            }
        }
        return o
    }
    function s(F) {
        var E = 0;
        var C = new Array(8);
        var B = F.length;
        v = F;
        if (B % 8 != 0 || B < 16) {
            return null
        }
        z = n(F);
        a = z[0] & 7;
        E = B - a - 10;
        if (E < 0) {
            return null
        }
        for (var D = 0; D < C.length; D++) {
            C[D] = 0
        }
        o = new Array(E);
        w = 0;
        A = 8;
        a++;
        var G = 1;
        while (G <= 2) {
            if (a < 8) {
                a++;
                G++
            }
            if (a == 8) {
                C = F;
                if (!g()) {
                    return null
                }
            }
        }
        var D = 0;
        while (E != 0) {
            if (a < 8) {
                o[D] = (C[w + a] ^ z[a]) & 255;
                D++;
                E--;
                a++
            }
            if (a == 8) {
                C = F;
                w = A - 8;
                if (!g()) {
                    return null
                }
            }
        }
        for (G = 1; G < 8; G++) {
            if (a < 8) {
                if ((C[w + a] ^ z[a]) != 0) {
                    return null
                }
                a++
            }
            if (a == 8) {
                C = F;
                w = A;
                if (!g()) {
                    return null
                }
            }
        }
        return o
    }
    function r() {
        for (var B = 0; B < 8; B++) {
            if (p) {
                h[B] ^= z[B]
            } else {
                h[B] ^= o[w + B]
            }
        }
        var C = l(h);
        for (var B = 0; B < 8; B++) {
            o[A + B] = C[B] ^ z[B];
            z[B] = h[B]
        }
        w = A;
        A += 8;
        a = 0;
        p = false
    }
    function l(B) {
        var C = 16;
        var H = k(B, 0, 4);
        var G = k(B, 4, 4);
        var J = k(u, 0, 4);
        var I = k(u, 4, 4);
        var F = k(u, 8, 4);
        var E = k(u, 12, 4);
        var D = 0;
        var K = 2654435769 >>> 0;
        while (C-- > 0) {
            D += K;
            D = (D & 4294967295) >>> 0;
            H += ((G << 4) + J) ^ (G + D) ^ ((G >>> 5) + I);
            H = (H & 4294967295) >>> 0;
            G += ((H << 4) + F) ^ (H + D) ^ ((H >>> 5) + E);
            G = (G & 4294967295) >>> 0
        }
        var L = new Array(8);
        b(L, 0, H);
        b(L, 4, G);
        return L
    }
    function n(B) {
        var C = 16;
        var H = k(B, 0, 4);
        var G = k(B, 4, 4);
        var J = k(u, 0, 4);
        var I = k(u, 4, 4);
        var F = k(u, 8, 4);
        var E = k(u, 12, 4);
        var D = 3816266640 >>> 0;
        var K = 2654435769 >>> 0;
        while (C-- > 0) {
            G -= ((H << 4) + F) ^ (H + D) ^ ((H >>> 5) + E);
            G = (G & 4294967295) >>> 0;
            H -= ((G << 4) + J) ^ (G + D) ^ ((G >>> 5) + I);
            H = (H & 4294967295) >>> 0;
            D -= K;
            D = (D & 4294967295) >>> 0
        }
        var L = new Array(8);
        b(L, 0, H);
        b(L, 4, G);
        return L
    }
    function g() {
        var B = v.length;
        for (var C = 0; C < 8; C++) {
            z[C] ^= v[A + C]
        }
        z = n(z);
        A += 8;
        a = 0;
        return true
    }
    function q(F, E) {
        var D = [];
        if (E) {
            for (var C = 0; C < F.length; C++) {
                D[C] = F.charCodeAt(C) & 255
            }
        } else {
            var B = 0;
            for (var C = 0; C < F.length; C += 2) {
                D[B++] = parseInt(F.substr(C, 2), 16)
            }
        }
        return D
    }
    t.TEA = {encrypt: function(E, D) {
            var C = q(E, D);
            var B = j(C);
            return y(B)
        },enAsBase64: function(G, F) {
            var E = q(G, F);
            var D = j(E);
            var B = "";
            for (var C = 0; C < D.length; C++) {
                B += String.fromCharCode(D[C])
            }
            return btoa(B)
        },decrypt: function(D) {
            var C = q(D, false);
            var B = s(C);
            return y(B)
        },initkey: function(B, C) {
            u = q(B, C)
        },bytesToStr: x,strToBytes: c,bytesInStr: y,dataFromStr: q};
    var d = {};
    d.PADCHAR = "=";
    d.ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    d.getbyte = function(D, C) {
        var B = D.charCodeAt(C);
        if (B > 255) {
            throw "INVALID_CHARACTER_ERR: DOM Exception 5"
        }
        return B
    };
    d.encode = function(F) {
        if (arguments.length != 1) {
            throw "SyntaxError: Not enough arguments"
        }
        var C = d.PADCHAR;
        var H = d.ALPHA;
        var G = d.getbyte;
        var E, I;
        var B = [];
        F = "" + F;
        var D = F.length - F.length % 3;
        if (F.length == 0) {
            return F
        }
        for (E = 0; E < D; E += 3) {
            I = (G(F, E) << 16) | (G(F, E + 1) << 8) | G(F, E + 2);
            B.push(H.charAt(I >> 18));
            B.push(H.charAt((I >> 12) & 63));
            B.push(H.charAt((I >> 6) & 63));
            B.push(H.charAt(I & 63))
        }
        switch (F.length - D) {
            case 1:
                I = G(F, E) << 16;
                B.push(H.charAt(I >> 18) + H.charAt((I >> 12) & 63) + C + C);
                break;
            case 2:
                I = (G(F, E) << 16) | (G(F, E + 1) << 8);
                B.push(H.charAt(I >> 18) + H.charAt((I >> 12) & 63) + H.charAt((I >> 6) & 63) + C);
                break
        }
        return B.join("")
    };
    if (!window.btoa) {
        window.btoa = d.encode
    }
})(window);
RSA = function() {
    function h(z, t) {
        return new au(z, t)
    }
    function aj(aC, aD) {
        var t = "";
        var z = 0;
        while (z + aD < aC.length) {
            t += aC.substring(z, z + aD) + "\n";
            z += aD
        }
        return t + aC.substring(z, aC.length)
    }
    function u(t) {
        if (t < 16) {
            return "0" + t.toString(16)
        } else {
            return t.toString(16)
        }
    }
    function ah(aD, aG) {
        if (aG < aD.length + 11) {
            uv_alert("Message too long for RSA");
            return null
        }
        var aF = new Array();
        var aC = aD.length - 1;
        while (aC >= 0 && aG > 0) {
            var aE = aD.charCodeAt(aC--);
            aF[--aG] = aE
        }
        aF[--aG] = 0;
        var z = new af();
        var t = new Array();
        while (aG > 2) {
            t[0] = 0;
            while (t[0] == 0) {
                z.nextBytes(t)
            }
            aF[--aG] = t[0]
        }
        aF[--aG] = 2;
        aF[--aG] = 0;
        return new au(aF)
    }
    function N() {
        this.n = null;
        this.e = 0;
        this.d = null;
        this.p = null;
        this.q = null;
        this.dmp1 = null;
        this.dmq1 = null;
        this.coeff = null
    }
    function q(z, t) {
        if (z != null && t != null && z.length > 0 && t.length > 0) {
            this.n = h(z, 16);
            this.e = parseInt(t, 16)
        } else {
            uv_alert("Invalid RSA public key")
        }
    }
    function Y(t) {
        return t.modPowInt(this.e, this.n)
    }
    function r(aC) {
        var t = ah(aC, (this.n.bitLength() + 7) >> 3);
        if (t == null) {
            return null
        }
        var aD = this.doPublic(t);
        if (aD == null) {
            return null
        }
        var z = aD.toString(16);
        if ((z.length & 1) == 0) {
            return z
        } else {
            return "0" + z
        }
    }
    N.prototype.doPublic = Y;
    N.prototype.setPublic = q;
    N.prototype.encrypt = r;
    var ay;
    var ak = 244837814094590;
    var ab = ((ak & 16777215) == 15715070);
    function au(z, t, aC) {
        if (z != null) {
            if ("number" == typeof z) {
                this.fromNumber(z, t, aC)
            } else {
                if (t == null && "string" != typeof z) {
                    this.fromString(z, 256)
                } else {
                    this.fromString(z, t)
                }
            }
        }
    }
    function j() {
        return new au(null)
    }
    function b(aE, t, z, aD, aG, aF) {
        while (--aF >= 0) {
            var aC = t * this[aE++] + z[aD] + aG;
            aG = Math.floor(aC / 67108864);
            z[aD++] = aC & 67108863
        }
        return aG
    }
    function aA(aE, aJ, aK, aD, aH, t) {
        var aG = aJ & 32767, aI = aJ >> 15;
        while (--t >= 0) {
            var aC = this[aE] & 32767;
            var aF = this[aE++] >> 15;
            var z = aI * aC + aF * aG;
            aC = aG * aC + ((z & 32767) << 15) + aK[aD] + (aH & 1073741823);
            aH = (aC >>> 30) + (z >>> 15) + aI * aF + (aH >>> 30);
            aK[aD++] = aC & 1073741823
        }
        return aH
    }
    function az(aE, aJ, aK, aD, aH, t) {
        var aG = aJ & 16383, aI = aJ >> 14;
        while (--t >= 0) {
            var aC = this[aE] & 16383;
            var aF = this[aE++] >> 14;
            var z = aI * aC + aF * aG;
            aC = aG * aC + ((z & 16383) << 14) + aK[aD] + aH;
            aH = (aC >> 28) + (z >> 14) + aI * aF;
            aK[aD++] = aC & 268435455
        }
        return aH
    }
    if (ab && (navigator.appName == "Microsoft Internet Explorer")) {
        au.prototype.am = aA;
        ay = 30
    } else {
        if (ab && (navigator.appName != "Netscape")) {
            au.prototype.am = b;
            ay = 26
        } else {
            au.prototype.am = az;
            ay = 28
        }
    }
    au.prototype.DB = ay;
    au.prototype.DM = ((1 << ay) - 1);
    au.prototype.DV = (1 << ay);
    var ac = 52;
    au.prototype.FV = Math.pow(2, ac);
    au.prototype.F1 = ac - ay;
    au.prototype.F2 = 2 * ay - ac;
    var ag = "0123456789abcdefghijklmnopqrstuvwxyz";
    var ai = new Array();
    var ar, x;
    ar = "0".charCodeAt(0);
    for (x = 0; x <= 9; ++x) {
        ai[ar++] = x
    }
    ar = "a".charCodeAt(0);
    for (x = 10; x < 36; ++x) {
        ai[ar++] = x
    }
    ar = "A".charCodeAt(0);
    for (x = 10; x < 36; ++x) {
        ai[ar++] = x
    }
    function aB(t) {
        return ag.charAt(t)
    }
    function C(z, t) {
        var aC = ai[z.charCodeAt(t)];
        return (aC == null) ? -1 : aC
    }
    function aa(z) {
        for (var t = this.t - 1; t >= 0; --t) {
            z[t] = this[t]
        }
        z.t = this.t;
        z.s = this.s
    }
    function p(t) {
        this.t = 1;
        this.s = (t < 0) ? -1 : 0;
        if (t > 0) {
            this[0] = t
        } else {
            if (t < -1) {
                this[0] = t + DV
            } else {
                this.t = 0
            }
        }
    }
    function c(t) {
        var z = j();
        z.fromInt(t);
        return z
    }
    function y(aG, z) {
        var aD;
        if (z == 16) {
            aD = 4
        } else {
            if (z == 8) {
                aD = 3
            } else {
                if (z == 256) {
                    aD = 8
                } else {
                    if (z == 2) {
                        aD = 1
                    } else {
                        if (z == 32) {
                            aD = 5
                        } else {
                            if (z == 4) {
                                aD = 2
                            } else {
                                this.fromRadix(aG, z);
                                return
                            }
                        }
                    }
                }
            }
        }
        this.t = 0;
        this.s = 0;
        var aF = aG.length, aC = false, aE = 0;
        while (--aF >= 0) {
            var t = (aD == 8) ? aG[aF] & 255 : C(aG, aF);
            if (t < 0) {
                if (aG.charAt(aF) == "-") {
                    aC = true
                }
                continue
            }
            aC = false;
            if (aE == 0) {
                this[this.t++] = t
            } else {
                if (aE + aD > this.DB) {
                    this[this.t - 1] |= (t & ((1 << (this.DB - aE)) - 1)) << aE;
                    this[this.t++] = (t >> (this.DB - aE))
                } else {
                    this[this.t - 1] |= t << aE
                }
            }
            aE += aD;
            if (aE >= this.DB) {
                aE -= this.DB
            }
        }
        if (aD == 8 && (aG[0] & 128) != 0) {
            this.s = -1;
            if (aE > 0) {
                this[this.t - 1] |= ((1 << (this.DB - aE)) - 1) << aE
            }
        }
        this.clamp();
        if (aC) {
            au.ZERO.subTo(this, this)
        }
    }
    function Q() {
        var t = this.s & this.DM;
        while (this.t > 0 && this[this.t - 1] == t) {
            --this.t
        }
    }
    function s(z) {
        if (this.s < 0) {
            return "-" + this.negate().toString(z)
        }
        var aC;
        if (z == 16) {
            aC = 4
        } else {
            if (z == 8) {
                aC = 3
            } else {
                if (z == 2) {
                    aC = 1
                } else {
                    if (z == 32) {
                        aC = 5
                    } else {
                        if (z == 4) {
                            aC = 2
                        } else {
                            return this.toRadix(z)
                        }
                    }
                }
            }
        }
        var aE = (1 << aC) - 1, aH, t = false, aF = "", aD = this.t;
        var aG = this.DB - (aD * this.DB) % aC;
        if (aD-- > 0) {
            if (aG < this.DB && (aH = this[aD] >> aG) > 0) {
                t = true;
                aF = aB(aH)
            }
            while (aD >= 0) {
                if (aG < aC) {
                    aH = (this[aD] & ((1 << aG) - 1)) << (aC - aG);
                    aH |= this[--aD] >> (aG += this.DB - aC)
                } else {
                    aH = (this[aD] >> (aG -= aC)) & aE;
                    if (aG <= 0) {
                        aG += this.DB;
                        --aD
                    }
                }
                if (aH > 0) {
                    t = true
                }
                if (t) {
                    aF += aB(aH)
                }
            }
        }
        return t ? aF : "0"
    }
    function T() {
        var t = j();
        au.ZERO.subTo(this, t);
        return t
    }
    function an() {
        return (this.s < 0) ? this.negate() : this
    }
    function I(t) {
        var aC = this.s - t.s;
        if (aC != 0) {
            return aC
        }
        var z = this.t;
        aC = z - t.t;
        if (aC != 0) {
            return aC
        }
        while (--z >= 0) {
            if ((aC = this[z] - t[z]) != 0) {
                return aC
            }
        }
        return 0
    }
    function l(z) {
        var aD = 1, aC;
        if ((aC = z >>> 16) != 0) {
            z = aC;
            aD += 16
        }
        if ((aC = z >> 8) != 0) {
            z = aC;
            aD += 8
        }
        if ((aC = z >> 4) != 0) {
            z = aC;
            aD += 4
        }
        if ((aC = z >> 2) != 0) {
            z = aC;
            aD += 2
        }
        if ((aC = z >> 1) != 0) {
            z = aC;
            aD += 1
        }
        return aD
    }
    function w() {
        if (this.t <= 0) {
            return 0
        }
        return this.DB * (this.t - 1) + l(this[this.t - 1] ^ (this.s & this.DM))
    }
    function at(aC, z) {
        var t;
        for (t = this.t - 1; t >= 0; --t) {
            z[t + aC] = this[t]
        }
        for (t = aC - 1; t >= 0; --t) {
            z[t] = 0
        }
        z.t = this.t + aC;
        z.s = this.s
    }
    function Z(aC, z) {
        for (var t = aC; t < this.t; ++t) {
            z[t - aC] = this[t]
        }
        z.t = Math.max(this.t - aC, 0);
        z.s = this.s
    }
    function v(aH, aD) {
        var z = aH % this.DB;
        var t = this.DB - z;
        var aF = (1 << t) - 1;
        var aE = Math.floor(aH / this.DB), aG = (this.s << z) & this.DM, aC;
        for (aC = this.t - 1; aC >= 0; --aC) {
            aD[aC + aE + 1] = (this[aC] >> t) | aG;
            aG = (this[aC] & aF) << z
        }
        for (aC = aE - 1; aC >= 0; --aC) {
            aD[aC] = 0
        }
        aD[aE] = aG;
        aD.t = this.t + aE + 1;
        aD.s = this.s;
        aD.clamp()
    }
    function n(aG, aD) {
        aD.s = this.s;
        var aE = Math.floor(aG / this.DB);
        if (aE >= this.t) {
            aD.t = 0;
            return
        }
        var z = aG % this.DB;
        var t = this.DB - z;
        var aF = (1 << z) - 1;
        aD[0] = this[aE] >> z;
        for (var aC = aE + 1; aC < this.t; ++aC) {
            aD[aC - aE - 1] |= (this[aC] & aF) << t;
            aD[aC - aE] = this[aC] >> z
        }
        if (z > 0) {
            aD[this.t - aE - 1] |= (this.s & aF) << t
        }
        aD.t = this.t - aE;
        aD.clamp()
    }
    function ad(z, aD) {
        var aC = 0, aE = 0, t = Math.min(z.t, this.t);
        while (aC < t) {
            aE += this[aC] - z[aC];
            aD[aC++] = aE & this.DM;
            aE >>= this.DB
        }
        if (z.t < this.t) {
            aE -= z.s;
            while (aC < this.t) {
                aE += this[aC];
                aD[aC++] = aE & this.DM;
                aE >>= this.DB
            }
            aE += this.s
        } else {
            aE += this.s;
            while (aC < z.t) {
                aE -= z[aC];
                aD[aC++] = aE & this.DM;
                aE >>= this.DB
            }
            aE -= z.s
        }
        aD.s = (aE < 0) ? -1 : 0;
        if (aE < -1) {
            aD[aC++] = this.DV + aE
        } else {
            if (aE > 0) {
                aD[aC++] = aE
            }
        }
        aD.t = aC;
        aD.clamp()
    }
    function F(z, aD) {
        var t = this.abs(), aE = z.abs();
        var aC = t.t;
        aD.t = aC + aE.t;
        while (--aC >= 0) {
            aD[aC] = 0
        }
        for (aC = 0; aC < aE.t; ++aC) {
            aD[aC + t.t] = t.am(0, aE[aC], aD, aC, 0, t.t)
        }
        aD.s = 0;
        aD.clamp();
        if (this.s != z.s) {
            au.ZERO.subTo(aD, aD)
        }
    }
    function S(aC) {
        var t = this.abs();
        var z = aC.t = 2 * t.t;
        while (--z >= 0) {
            aC[z] = 0
        }
        for (z = 0; z < t.t - 1; ++z) {
            var aD = t.am(z, t[z], aC, 2 * z, 0, 1);
            if ((aC[z + t.t] += t.am(z + 1, 2 * t[z], aC, 2 * z + 1, aD, t.t - z - 1)) >= t.DV) {
                aC[z + t.t] -= t.DV;
                aC[z + t.t + 1] = 1
            }
        }
        if (aC.t > 0) {
            aC[aC.t - 1] += t.am(z, t[z], aC, 2 * z, 0, 1)
        }
        aC.s = 0;
        aC.clamp()
    }
    function G(aK, aH, aG) {
        var aQ = aK.abs();
        if (aQ.t <= 0) {
            return
        }
        var aI = this.abs();
        if (aI.t < aQ.t) {
            if (aH != null) {
                aH.fromInt(0)
            }
            if (aG != null) {
                this.copyTo(aG)
            }
            return
        }
        if (aG == null) {
            aG = j()
        }
        var aE = j(), z = this.s, aJ = aK.s;
        var aP = this.DB - l(aQ[aQ.t - 1]);
        if (aP > 0) {
            aQ.lShiftTo(aP, aE);
            aI.lShiftTo(aP, aG)
        } else {
            aQ.copyTo(aE);
            aI.copyTo(aG)
        }
        var aM = aE.t;
        var aC = aE[aM - 1];
        if (aC == 0) {
            return
        }
        var aL = aC * (1 << this.F1) + ((aM > 1) ? aE[aM - 2] >> this.F2 : 0);
        var aT = this.FV / aL, aS = (1 << this.F1) / aL, aR = 1 << this.F2;
        var aO = aG.t, aN = aO - aM, aF = (aH == null) ? j() : aH;
        aE.dlShiftTo(aN, aF);
        if (aG.compareTo(aF) >= 0) {
            aG[aG.t++] = 1;
            aG.subTo(aF, aG)
        }
        au.ONE.dlShiftTo(aM, aF);
        aF.subTo(aE, aE);
        while (aE.t < aM) {
            aE[aE.t++] = 0
        }
        while (--aN >= 0) {
            var aD = (aG[--aO] == aC) ? this.DM : Math.floor(aG[aO] * aT + (aG[aO - 1] + aR) * aS);
            if ((aG[aO] += aE.am(0, aD, aG, aN, 0, aM)) < aD) {
                aE.dlShiftTo(aN, aF);
                aG.subTo(aF, aG);
                while (aG[aO] < --aD) {
                    aG.subTo(aF, aG)
                }
            }
        }
        if (aH != null) {
            aG.drShiftTo(aM, aH);
            if (z != aJ) {
                au.ZERO.subTo(aH, aH)
            }
        }
        aG.t = aM;
        aG.clamp();
        if (aP > 0) {
            aG.rShiftTo(aP, aG)
        }
        if (z < 0) {
            au.ZERO.subTo(aG, aG)
        }
    }
    function P(t) {
        var z = j();
        this.abs().divRemTo(t, null, z);
        if (this.s < 0 && z.compareTo(au.ZERO) > 0) {
            t.subTo(z, z)
        }
        return z
    }
    function M(t) {
        this.m = t
    }
    function X(t) {
        if (t.s < 0 || t.compareTo(this.m) >= 0) {
            return t.mod(this.m)
        } else {
            return t
        }
    }
    function am(t) {
        return t
    }
    function L(t) {
        t.divRemTo(this.m, null, t)
    }
    function J(t, aC, z) {
        t.multiplyTo(aC, z);
        this.reduce(z)
    }
    function aw(t, z) {
        t.squareTo(z);
        this.reduce(z)
    }
    M.prototype.convert = X;
    M.prototype.revert = am;
    M.prototype.reduce = L;
    M.prototype.mulTo = J;
    M.prototype.sqrTo = aw;
    function D() {
        if (this.t < 1) {
            return 0
        }
        var t = this[0];
        if ((t & 1) == 0) {
            return 0
        }
        var z = t & 3;
        z = (z * (2 - (t & 15) * z)) & 15;
        z = (z * (2 - (t & 255) * z)) & 255;
        z = (z * (2 - (((t & 65535) * z) & 65535))) & 65535;
        z = (z * (2 - t * z % this.DV)) % this.DV;
        return (z > 0) ? this.DV - z : -z
    }
    function g(t) {
        this.m = t;
        this.mp = t.invDigit();
        this.mpl = this.mp & 32767;
        this.mph = this.mp >> 15;
        this.um = (1 << (t.DB - 15)) - 1;
        this.mt2 = 2 * t.t
    }
    function al(t) {
        var z = j();
        t.abs().dlShiftTo(this.m.t, z);
        z.divRemTo(this.m, null, z);
        if (t.s < 0 && z.compareTo(au.ZERO) > 0) {
            this.m.subTo(z, z)
        }
        return z
    }
    function av(t) {
        var z = j();
        t.copyTo(z);
        this.reduce(z);
        return z
    }
    function R(t) {
        while (t.t <= this.mt2) {
            t[t.t++] = 0
        }
        for (var aC = 0; aC < this.m.t; ++aC) {
            var z = t[aC] & 32767;
            var aD = (z * this.mpl + (((z * this.mph + (t[aC] >> 15) * this.mpl) & this.um) << 15)) & t.DM;
            z = aC + this.m.t;
            t[z] += this.m.am(0, aD, t, aC, 0, this.m.t);
            while (t[z] >= t.DV) {
                t[z] -= t.DV;
                t[++z]++
            }
        }
        t.clamp();
        t.drShiftTo(this.m.t, t);
        if (t.compareTo(this.m) >= 0) {
            t.subTo(this.m, t)
        }
    }
    function ao(t, z) {
        t.squareTo(z);
        this.reduce(z)
    }
    function B(t, aC, z) {
        t.multiplyTo(aC, z);
        this.reduce(z)
    }
    g.prototype.convert = al;
    g.prototype.revert = av;
    g.prototype.reduce = R;
    g.prototype.mulTo = B;
    g.prototype.sqrTo = ao;
    function k() {
        return ((this.t > 0) ? (this[0] & 1) : this.s) == 0
    }
    function A(aH, aI) {
        if (aH > 4294967295 || aH < 1) {
            return au.ONE
        }
        var aG = j(), aC = j(), aF = aI.convert(this), aE = l(aH) - 1;
        aF.copyTo(aG);
        while (--aE >= 0) {
            aI.sqrTo(aG, aC);
            if ((aH & (1 << aE)) > 0) {
                aI.mulTo(aC, aF, aG)
            } else {
                var aD = aG;
                aG = aC;
                aC = aD
            }
        }
        return aI.revert(aG)
    }
    function ap(aC, t) {
        var aD;
        if (aC < 256 || t.isEven()) {
            aD = new M(t)
        } else {
            aD = new g(t)
        }
        return this.exp(aC, aD)
    }
    au.prototype.copyTo = aa;
    au.prototype.fromInt = p;
    au.prototype.fromString = y;
    au.prototype.clamp = Q;
    au.prototype.dlShiftTo = at;
    au.prototype.drShiftTo = Z;
    au.prototype.lShiftTo = v;
    au.prototype.rShiftTo = n;
    au.prototype.subTo = ad;
    au.prototype.multiplyTo = F;
    au.prototype.squareTo = S;
    au.prototype.divRemTo = G;
    au.prototype.invDigit = D;
    au.prototype.isEven = k;
    au.prototype.exp = A;
    au.prototype.toString = s;
    au.prototype.negate = T;
    au.prototype.abs = an;
    au.prototype.compareTo = I;
    au.prototype.bitLength = w;
    au.prototype.mod = P;
    au.prototype.modPowInt = ap;
    au.ZERO = c(0);
    au.ONE = c(1);
    var o;
    var W;
    var ae;
    function d(t) {
        W[ae++] ^= t & 255;
        W[ae++] ^= (t >> 8) & 255;
        W[ae++] ^= (t >> 16) & 255;
        W[ae++] ^= (t >> 24) & 255;
        if (ae >= O) {
            ae -= O
        }
    }
    function V() {
        d(new Date().getTime())
    }
    if (W == null) {
        W = new Array();
        ae = 0;
        var K;
        if (navigator.appName == "Netscape" && navigator.appVersion < "5" && window.crypto && window.crypto.random) {
            var H = window.crypto.random(32);
            for (K = 0; K < H.length; ++K) {
                W[ae++] = H.charCodeAt(K) & 255
            }
        }
        while (ae < O) {
            K = Math.floor(65536 * Math.random());
            W[ae++] = K >>> 8;
            W[ae++] = K & 255
        }
        ae = 0;
        V()
    }
    function E() {
        if (o == null) {
            V();
            o = aq();
            o.init(W);
            for (ae = 0; ae < W.length; ++ae) {
                W[ae] = 0
            }
            ae = 0
        }
        return o.next()
    }
    function ax(z) {
        var t;
        for (t = 0; t < z.length; ++t) {
            z[t] = E()
        }
    }
    function af() {
    }
    af.prototype.nextBytes = ax;
    function m() {
        this.i = 0;
        this.j = 0;
        this.S = new Array()
    }
    function f(aE) {
        var aD, z, aC;
        for (aD = 0; aD < 256; ++aD) {
            this.S[aD] = aD
        }
        z = 0;
        for (aD = 0; aD < 256; ++aD) {
            z = (z + this.S[aD] + aE[aD % aE.length]) & 255;
            aC = this.S[aD];
            this.S[aD] = this.S[z];
            this.S[z] = aC
        }
        this.i = 0;
        this.j = 0
    }
    function a() {
        var z;
        this.i = (this.i + 1) & 255;
        this.j = (this.j + this.S[this.i]) & 255;
        z = this.S[this.i];
        this.S[this.i] = this.S[this.j];
        this.S[this.j] = z;
        return this.S[(z + this.S[this.i]) & 255]
    }
    m.prototype.init = f;
    m.prototype.next = a;
    function aq() {
        return new m()
    }
    var O = 256;
    function U(aD, aC, z) {
        aC = "F20CE00BAE5361F8FA3AE9CEFA495362FF7DA1BA628F64A347F0A8C012BF0B254A30CD92ABFFE7A6EE0DC424CB6166F8819EFA5BCCB20EDFB4AD02E412CCF579B1CA711D55B8B0B3AEB60153D5E0693A2A86F3167D7847A0CB8B00004716A9095D9BADC977CBB804DBDCBA6029A9710869A453F27DFDDF83C016D928B3CBF4C7";
        z = "3";
        var t = new N();
        t.setPublic(aC, z);
        return t.encrypt(aD)
    }
    return {rsa_encrypt: U}
}();
Encryption =function() {
    var hexcase = 1;
    var b64pad = "";
    var chrsz = 8;
    var mode = 32;

    function md5(s) {
        return hex_md5(s)
    }
    function hex_md5(s) {
        return binl2hex(core_md5(str2binl(s), s.length * chrsz))
    }
    function str_md5(s) {
        return binl2str(core_md5(str2binl(s), s.length * chrsz))
    }
    function hex_hmac_md5(key, data) {
        return binl2hex(core_hmac_md5(key, data))
    }
    function b64_hmac_md5(key, data) {
        return binl2b64(core_hmac_md5(key, data))
    }
    function str_hmac_md5(key, data) {
        return binl2str(core_hmac_md5(key, data))
    }
    function core_md5(x, len) {
        x[len >> 5] |= 128 << ((len) % 32);
        x[(((len + 64) >>> 9) << 4) + 14] = len;
        var a = 1732584193;
        var b = -271733879;
        var c = -1732584194;
        var d = 271733878;
        for (var i = 0; i < x.length; i += 16) {
            var olda = a;
            var oldb = b;
            var oldc = c;
            var oldd = d;
            a = md5_ff(a, b, c, d, x[i + 0], 7, -680876936);
            d = md5_ff(d, a, b, c, x[i + 1], 12, -389564586);
            c = md5_ff(c, d, a, b, x[i + 2], 17, 606105819);
            b = md5_ff(b, c, d, a, x[i + 3], 22, -1044525330);
            a = md5_ff(a, b, c, d, x[i + 4], 7, -176418897);
            d = md5_ff(d, a, b, c, x[i + 5], 12, 1200080426);
            c = md5_ff(c, d, a, b, x[i + 6], 17, -1473231341);
            b = md5_ff(b, c, d, a, x[i + 7], 22, -45705983);
            a = md5_ff(a, b, c, d, x[i + 8], 7, 1770035416);
            d = md5_ff(d, a, b, c, x[i + 9], 12, -1958414417);
            c = md5_ff(c, d, a, b, x[i + 10], 17, -42063);
            b = md5_ff(b, c, d, a, x[i + 11], 22, -1990404162);
            a = md5_ff(a, b, c, d, x[i + 12], 7, 1804603682);
            d = md5_ff(d, a, b, c, x[i + 13], 12, -40341101);
            c = md5_ff(c, d, a, b, x[i + 14], 17, -1502002290);
            b = md5_ff(b, c, d, a, x[i + 15], 22, 1236535329);
            a = md5_gg(a, b, c, d, x[i + 1], 5, -165796510);
            d = md5_gg(d, a, b, c, x[i + 6], 9, -1069501632);
            c = md5_gg(c, d, a, b, x[i + 11], 14, 643717713);
            b = md5_gg(b, c, d, a, x[i + 0], 20, -373897302);
            a = md5_gg(a, b, c, d, x[i + 5], 5, -701558691);
            d = md5_gg(d, a, b, c, x[i + 10], 9, 38016083);
            c = md5_gg(c, d, a, b, x[i + 15], 14, -660478335);
            b = md5_gg(b, c, d, a, x[i + 4], 20, -405537848);
            a = md5_gg(a, b, c, d, x[i + 9], 5, 568446438);
            d = md5_gg(d, a, b, c, x[i + 14], 9, -1019803690);
            c = md5_gg(c, d, a, b, x[i + 3], 14, -187363961);
            b = md5_gg(b, c, d, a, x[i + 8], 20, 1163531501);
            a = md5_gg(a, b, c, d, x[i + 13], 5, -1444681467);
            d = md5_gg(d, a, b, c, x[i + 2], 9, -51403784);
            c = md5_gg(c, d, a, b, x[i + 7], 14, 1735328473);
            b = md5_gg(b, c, d, a, x[i + 12], 20, -1926607734);
            a = md5_hh(a, b, c, d, x[i + 5], 4, -378558);
            d = md5_hh(d, a, b, c, x[i + 8], 11, -2022574463);
            c = md5_hh(c, d, a, b, x[i + 11], 16, 1839030562);
            b = md5_hh(b, c, d, a, x[i + 14], 23, -35309556);
            a = md5_hh(a, b, c, d, x[i + 1], 4, -1530992060);
            d = md5_hh(d, a, b, c, x[i + 4], 11, 1272893353);
            c = md5_hh(c, d, a, b, x[i + 7], 16, -155497632);
            b = md5_hh(b, c, d, a, x[i + 10], 23, -1094730640);
            a = md5_hh(a, b, c, d, x[i + 13], 4, 681279174);
            d = md5_hh(d, a, b, c, x[i + 0], 11, -358537222);
            c = md5_hh(c, d, a, b, x[i + 3], 16, -722521979);
            b = md5_hh(b, c, d, a, x[i + 6], 23, 76029189);
            a = md5_hh(a, b, c, d, x[i + 9], 4, -640364487);
            d = md5_hh(d, a, b, c, x[i + 12], 11, -421815835);
            c = md5_hh(c, d, a, b, x[i + 15], 16, 530742520);
            b = md5_hh(b, c, d, a, x[i + 2], 23, -995338651);
            a = md5_ii(a, b, c, d, x[i + 0], 6, -198630844);
            d = md5_ii(d, a, b, c, x[i + 7], 10, 1126891415);
            c = md5_ii(c, d, a, b, x[i + 14], 15, -1416354905);
            b = md5_ii(b, c, d, a, x[i + 5], 21, -57434055);
            a = md5_ii(a, b, c, d, x[i + 12], 6, 1700485571);
            d = md5_ii(d, a, b, c, x[i + 3], 10, -1894986606);
            c = md5_ii(c, d, a, b, x[i + 10], 15, -1051523);
            b = md5_ii(b, c, d, a, x[i + 1], 21, -2054922799);
            a = md5_ii(a, b, c, d, x[i + 8], 6, 1873313359);
            d = md5_ii(d, a, b, c, x[i + 15], 10, -30611744);
            c = md5_ii(c, d, a, b, x[i + 6], 15, -1560198380);
            b = md5_ii(b, c, d, a, x[i + 13], 21, 1309151649);
            a = md5_ii(a, b, c, d, x[i + 4], 6, -145523070);
            d = md5_ii(d, a, b, c, x[i + 11], 10, -1120210379);
            c = md5_ii(c, d, a, b, x[i + 2], 15, 718787259);
            b = md5_ii(b, c, d, a, x[i + 9], 21, -343485551);
            a = safe_add(a, olda);
            b = safe_add(b, oldb);
            c = safe_add(c, oldc);
            d = safe_add(d, oldd)
        }
        if (mode == 16) {
            return Array(b, c)
        } else {
            return Array(a, b, c, d)
        }
    }
    function md5_cmn(q, a, b, x, s, t) {
        return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s), b)
    }
    function md5_ff(a, b, c, d, x, s, t) {
        return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t)
    }
    function md5_gg(a, b, c, d, x, s, t) {
        return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t)
    }
    function md5_hh(a, b, c, d, x, s, t) {
        return md5_cmn(b ^ c ^ d, a, b, x, s, t)
    }
    function md5_ii(a, b, c, d, x, s, t) {
        return md5_cmn(c ^ (b | (~d)), a, b, x, s, t)
    }
    function core_hmac_md5(key, data) {
        var bkey = str2binl(key);
        if (bkey.length > 16) {
            bkey = core_md5(bkey, key.length * chrsz)
        }
        var ipad = Array(16), opad = Array(16);
        for (var i = 0; i < 16; i++) {
            ipad[i] = bkey[i] ^ 909522486;
            opad[i] = bkey[i] ^ 1549556828
        }
        var hash = core_md5(ipad.concat(str2binl(data)), 512 + data.length * chrsz);
        return core_md5(opad.concat(hash), 512 + 128)
    }
    function safe_add(x, y) {
        var lsw = (x & 65535) + (y & 65535);
        var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
        return (msw << 16) | (lsw & 65535)
    }
    function bit_rol(num, cnt) {
        return (num << cnt) | (num >>> (32 - cnt))
    }
    function str2binl(str) {
        var bin = Array();
        var mask = (1 << chrsz) - 1;
        for (var i = 0; i < str.length * chrsz; i += chrsz) {
            bin[i >> 5] |= (str.charCodeAt(i / chrsz) & mask) << (i % 32)
        }
        return bin
    }
    function binl2str(bin) {
        var str = "";
        var mask = (1 << chrsz) - 1;
        for (var i = 0; i < bin.length * 32; i += chrsz) {
            str += String.fromCharCode((bin[i >> 5] >>> (i % 32)) & mask)
        }
        return str
    }
    function binl2hex(binarray) {
        var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
        var str = "";
        for (var i = 0; i < binarray.length * 4; i++) {
            str += hex_tab.charAt((binarray[i >> 2] >> ((i % 4) * 8 + 4)) & 15) + hex_tab.charAt((binarray[i >> 2] >> ((i % 4) * 8)) & 15)
        }
        return str
    }
    function binl2b64(binarray) {
        var tab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        var str = "";
        for (var i = 0; i < binarray.length * 4; i += 3) {
            var triplet = (((binarray[i >> 2] >> 8 * (i % 4)) & 255) << 16) | (((binarray[i + 1 >> 2] >> 8 * ((i + 1) % 4)) & 255) << 8) | ((binarray[i + 2 >> 2] >> 8 * ((i + 2) % 4)) & 255);
            for (var j = 0; j < 4; j++) {
                if (i * 8 + j * 6 > binarray.length * 32) {
                    str += b64pad
                } else {
                    str += tab.charAt((triplet >> 6 * (3 - j)) & 63)
                }
            }
        }
        return str
    }
    function hexchar2bin(str) {
        var arr = [];
        for (var i = 0; i < str.length; i = i + 2) {
            arr.push("\\x" + str.substr(i, 2))
        }
        arr = arr.join("");
        eval("var temp = '" + arr + "'");
        return temp
    }
    function __monitor(mid, probability) {
        if (Math.random() > (probability || 1)) {
            return
        }
        try {
            var url = location.protocol + "//ui.ptlogin2.qq.com/cgi-bin/report?id=" + mid;
            var s = document.createElement("img");
            s.src = url
        } catch (e) {
        }
    }
    function getEncryption(password, salt, vcode, isMd5) {
        vcode = vcode || "";
        password = password || "";
        var md5Pwd = isMd5 ? password : md5(password), h1 = hexchar2bin(md5Pwd), s2 = md5(h1 + salt), rsaH1 = RSA.rsa_encrypt(h1), rsaH1Len = (rsaH1.length / 2).toString(16), hexVcode = TEA.strToBytes(vcode.toUpperCase(), true), vcodeLen = Number(hexVcode.length / 2).toString(16);
        while (vcodeLen.length < 4) {
            vcodeLen = "0" + vcodeLen
        }
        while (rsaH1Len.length < 4) {
            rsaH1Len = "0" + rsaH1Len
        }
        TEA.initkey(s2);
        var saltPwd = TEA.enAsBase64(rsaH1Len + rsaH1 + TEA.strToBytes(salt) + vcodeLen + hexVcode);
        TEA.initkey("");

        return saltPwd.replace(/[\/\+=]/g, function(a) {
            return {"/": "-","+": "*","=": "_"}[a]
        })
    }
    function getRSAEncryption(password, vcode, isMd5) {
        var str1 = isMd5 ? password : md5(password);
        var str2 = str1 + vcode.toUpperCase();
        var str3 = RSA.rsa_encrypt(str2);
        return str3
    }
    function get_hash(qq, ptwebqq){
        x = qq;
        K = ptwebqq;
        x += "";
        for (var N = [], T = 0; T < K.length; T++)
            N[T % 4] ^= K.charCodeAt(T);
        var U = ["EC", "OK"]
          , V = [];
        V[0] = x >> 24 & 255 ^ U[0].charCodeAt(0);
        V[1] = x >> 16 & 255 ^ U[0].charCodeAt(1);
        V[2] = x >> 8 & 255 ^ U[1].charCodeAt(0);
        V[3] = x & 255 ^ U[1].charCodeAt(1);
        U = [];
        for (T = 0; T < 8; T++)
            U[T] = T % 2 == 0 ? N[T >> 1] : V[T >> 1];
        N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
        V = "";
        for (T = 0; T < U.length; T++) {
            V += N[U[T] >> 4 & 15];
            V += N[U[T] & 15]
        }
        return V

    }
    return {getEncryption: getEncryption,getRSAEncryption: getRSAEncryption,md5: md5, get_hash:get_hash}
}();

//result = Encryption.getEncryption("test pwd", "\x00\x00\x00\x00\x54\x38\x3c\x58", "!abf")
//console.log(result)
