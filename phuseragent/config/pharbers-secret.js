(($) => {

	$.PhSigV4AWSClientFactory = () => {
		const AWS_SHA_256 = 'AWS4-HMAC-SHA256';
		const AWS4_REQUEST = 'aws4_request';
		const AWS4 = 'AWS4';
		const X_AMZ_DATE = 'x-amz-date';
		const X_AMZ_SECURITY_TOKEN = 'x-amz-security-token';
		const HOST = 'host';
		const AUTHORIZATION = 'Authorization';

		function hash(value) {
			return CryptoJS.SHA256(value);
		}

		function hexEncode(value) {
			return value.toString(CryptoJS.enc.Hex);
		}

		function hmac(secret, value) {
			return CryptoJS.HmacSHA256(value, secret, { asBytes: true });
		}

		function buildCanonicalRequest(method, path, queryParams, headers, payload) {
			return method + '\n' +
				buildCanonicalUri(path) + '\n' +
				buildCanonicalQueryString(queryParams) + '\n' +
				buildCanonicalHeaders(headers) + '\n' +
				buildCanonicalSignedHeaders(headers) + '\n' +
				hexEncode(hash(payload));
		}

		function hashCanonicalRequest(request) {
			return hexEncode(hash(request));
		}

		function buildCanonicalUri(uri) {
			return encodeURI(uri);
		}

		function buildCanonicalQueryString(queryParams) {
			if (Object.keys(queryParams).length < 1) {
				return '';
			}

			let sortedQueryParams = [];
			for (const property in queryParams) {
				if (queryParams.hasOwnProperty(property)) {
					sortedQueryParams.push(property);
				}
			}
			sortedQueryParams.sort();

			let canonicalQueryString = '';
			for (let i = 0; i < sortedQueryParams.length; i++) {
				canonicalQueryString += sortedQueryParams[i] + '=' + fixedEncodeURIComponent(queryParams[sortedQueryParams[i]]) + '&';
			}
			return canonicalQueryString.substr(0, canonicalQueryString.length - 1);
		}

		function fixedEncodeURIComponent(str) {
			return encodeURIComponent(str).replace(/[!'()*]/g, function (c) {
				return '%' + c.charCodeAt(0).toString(16).toUpperCase();
			});
		}

		function buildCanonicalHeaders(headers) {
			let canonicalHeaders = '';
			let sortedKeys = [];
			for (const property in headers) {
				if (headers.hasOwnProperty(property)) {
					sortedKeys.push(property);
				}
			}
			sortedKeys.sort();

			for (let i = 0; i < sortedKeys.length; i++) {
				canonicalHeaders += sortedKeys[i].toLowerCase() + ':' + headers[sortedKeys[i]] + '\n';
			}
			return canonicalHeaders;
		}

		function buildCanonicalSignedHeaders(headers) {
			let sortedKeys = [];
			for (const property in headers) {
				if (headers.hasOwnProperty(property)) {
					sortedKeys.push(property.toLowerCase());
				}
			}
			sortedKeys.sort();

			return sortedKeys.join(';');
		}

		function buildStringToSign(datetime, credentialScope, hashedCanonicalRequest) {
			return AWS_SHA_256 + '\n' +
				datetime + '\n' +
				credentialScope + '\n' +
				hashedCanonicalRequest;
		}

		function buildCredentialScope(datetime, region, service) {
			return datetime.substr(0, 8) + '/' + region + '/' + service + '/' + AWS4_REQUEST
		}

		function calculateSigningKey(secretKey, datetime, region, service) {
			return hmac(hmac(hmac(hmac(AWS4 + secretKey, datetime.substr(0, 8)), region), service), AWS4_REQUEST);
		}

		function calculateSignature(key, stringToSign) {
			return hexEncode(hmac(key, stringToSign));
		}

		function buildAuthorizationHeader(accessKey, credentialScope, headers, signature) {
			return AWS_SHA_256 + ' Credential=' + accessKey + '/' + credentialScope + ', SignedHeaders=' + buildCanonicalSignedHeaders(headers) + ', Signature=' + signature;
		}

		const PhSigV4AWSClientObject = {};
		PhSigV4AWSClientObject.newClient = function (config) {

			let awsSigV4Client = {};
			if (config.accessKey === undefined || config.secretKey === undefined) {
				return awsSigV4Client;
			}
			awsSigV4Client.accessKey = $.PhSigV4ClientUtils().assertDefined(config.accessKey, 'accessKey');
			awsSigV4Client.secretKey = $.PhSigV4ClientUtils().assertDefined(config.secretKey, 'secretKey');
			awsSigV4Client.sessionToken = config.sessionToken;
			awsSigV4Client.serviceName = $.PhSigV4ClientUtils().assertDefined(config.serviceName, 'serviceName');
			awsSigV4Client.region = $.PhSigV4ClientUtils().assertDefined(config.region, 'region');
			awsSigV4Client.endpoint = $.PhSigV4ClientUtils().assertDefined(config.endpoint, 'endpoint');

			awsSigV4Client.makeRequest = function (request) {
				const verb = $.PhSigV4ClientUtils().assertDefined(request.verb, 'verb');
				const path = $.PhSigV4ClientUtils().assertDefined(request.path, 'path');
				let queryParams = $.PhSigV4ClientUtils().copy(request.queryParams);
				if (queryParams === undefined) {
					queryParams = {};
				}
				let headers = $.PhSigV4ClientUtils().copy(request.headers);
				if (headers === undefined) {
					headers = {};
				}

				//If the user has not specified an override for Content type the use default
				if (headers['Content-Type'] === undefined) {
					headers['Content-Type'] = config.defaultContentType;
				}

				//If the user has not specified an override for Accept type the use default
				if (headers['Accept'] === undefined) {
					headers['Accept'] = config.defaultAcceptType;
				}

				let body = $.PhSigV4ClientUtils().copy(request.body);
				if (body === undefined || verb === 'GET') { // override request body and set to empty when signing GET requests
					body = '';
				} else {
					body = JSON.stringify(body);
				}

				//If there is no body remove the content-type header so it is not included in SigV4 calculation
				if (body === '' || body === undefined || body === null) {
					delete headers['Content-Type'];
				}

				const datetime = new Date().toISOString().replace(/\.\d{3}Z$/, 'Z').replace(/[:\-]|\.\d{3}/g, '');
				headers[X_AMZ_DATE] = datetime;
				headers[HOST] = "2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn";

				const canonicalRequest = buildCanonicalRequest(verb, path, queryParams, headers, body);
				const hashedCanonicalRequest = hashCanonicalRequest(canonicalRequest);
				const credentialScope = buildCredentialScope(datetime, awsSigV4Client.region, awsSigV4Client.serviceName);
				const stringToSign = buildStringToSign(datetime, credentialScope, hashedCanonicalRequest);
				const signingKey = calculateSigningKey(awsSigV4Client.secretKey, datetime, awsSigV4Client.region, awsSigV4Client.serviceName);
				const signature = calculateSignature(signingKey, stringToSign);
				headers[AUTHORIZATION] = buildAuthorizationHeader(awsSigV4Client.accessKey, credentialScope, headers, signature);
				if (awsSigV4Client.sessionToken !== undefined && awsSigV4Client.sessionToken !== '') {
					headers[X_AMZ_SECURITY_TOKEN] = awsSigV4Client.sessionToken;
				}
				delete headers[HOST];

				let url = config.endpoint + path;
				const queryString = buildCanonicalQueryString(queryParams);
				if (queryString !== '') {
					url += '?' + queryString;
				}

				//Need to re-attach Content-Type if it is not specified at this point
				if (headers['Content-Type'] === undefined) {
					headers['Content-Type'] = config.defaultContentType;
				}

				return {
					method: verb,
					url: url,
					headers: headers,
					data: body,
					timeout: 30000
				};
			};

			return awsSigV4Client;
		};
		return PhSigV4AWSClientObject;
	};

	$.PhSigV4ClientUtils = () => {
		const ClientUtils = {
			assertDefined: function (object, name) {
				if (object === undefined) {
					throw name + ' must be defined';
				} else {
					return object;
				}
			},
			assertParametersDefined: function (params, keys, ignore) {
				if (keys === undefined) {
					return;
				}
				if (keys.length > 0 && params === undefined) {
					params = {};
				}
				for (let i = 0; i < keys.length; i++) {
					if (!this.contains(ignore, keys[i])) {
						this.assertDefined(params[keys[i]], keys[i]);
					}
				}
			},
			parseParametersToObject: function (params, keys) {
				if (params === undefined) {
					return {};
				}
				let object = {};
				for (let i = 0; i < keys.length; i++) {
					object[keys[i]] = params[keys[i]];
				}
				return object;
			},
			contains: function (a, obj) {
				if (a === undefined) { return false; }
				let i = a.length;
				while (i--) {
					if (a[i] === obj) {
						return true;
					}
				}
				return false;
			},
			copy: function (obj) {
				if (null == obj || "object" != typeof obj) return obj;
				const copy = obj.constructor();
				for (const attr in obj) {
					if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
				}
				return copy;
			},
			mergeInto: function (baseObj, additionalProps) {
				if (null == baseObj || "object" != typeof baseObj) return baseObj;
				const merged = baseObj.constructor();
				for (const attr in baseObj) {
					if (baseObj.hasOwnProperty(attr)) merged[attr] = baseObj[attr];
				}
				if (null == additionalProps || "object" != typeof additionalProps) return baseObj;
				for (attr in additionalProps) {
					if (additionalProps.hasOwnProperty(attr)) merged[attr] = additionalProps[attr];
				}
				return merged;
			}
		}

		return ClientUtils;
	}

	$.PhUriTemplate = () => {
		function isFunction(fn) {
			return typeof fn == 'function';
		}

		function isEmptyObject(obj) {
			for (var name in obj) {
				return false;
			}
			return true;
		}

		function extend(base, newprops) {
			for (var name in newprops) {
				base[name] = newprops[name];
			}
			return base;
		}

		function CachingContext(context) {
			this.raw = context;
			this.cache = {};
		}

		CachingContext.prototype.get = function (key) {
			var val = this.lookupRaw(key);
			var result = val;

			if (isFunction(val)) { // check function-result-cache
				var tupple = this.cache[key];
				if (tupple !== null && tupple !== undefined) {
					result = tupple.val;
				} else {
					result = val(this.raw);
					this.cache[key] = { key: key, val: result };
				}
			}
			return result;
		};

		CachingContext.prototype.lookupRaw = function (key) {
			return CachingContext.lookup(this, this.raw, key);
		};

		CachingContext.lookup = function (me, context, key) {
			var result = context[key];
			if (result !== undefined) {
				return result;
			} else {
				var keyparts = key.split('.');
				var i = 0, keysplits = keyparts.length - 1;
				for (i = 0; i < keysplits; i++) {
					var leadKey = keyparts.slice(0, keysplits - i).join('.');
					var trailKey = keyparts.slice(-i - 1).join('.');
					var leadContext = context[leadKey];
					if (leadContext !== undefined) {
						return CachingContext.lookup(me, leadContext, trailKey);
					}
				}
				return undefined;
			}
		};


		function UriTemplate(set) {
			this.set = set;
		}

		UriTemplate.prototype.expand = function (context) {
			var cache = new CachingContext(context);
			var res = "";
			var i = 0, cnt = this.set.length;
			for (i = 0; i < cnt; i++) {
				res += this.set[i].expand(cache);
			}
			return res;
		};

		function Literal(txt) {
			this.txt = txt;
		}

		Literal.prototype.expand = function () {
			return this.txt;
		};



		var RESERVEDCHARS_RE = new RegExp("[:/?#\\[\\]@!$&()*+,;=']", "g");
		function encodeNormal(val) {
			return encodeURIComponent(val).replace(RESERVEDCHARS_RE, function (s) { return escape(s); });
		}

		function encodeReserved(val) {
			return encodeURI(val);
		}


		function addUnNamed(name, key, val) {
			return key + (key.length > 0 ? "=" : "") + val;
		}

		function addNamed(name, key, val, noName) {
			noName = noName || false;
			if (noName) { name = ""; }

			if (!key || key.length === 0) {
				key = name;
			}
			return key + (key.length > 0 ? "=" : "") + val;
		}

		function addLabeled(name, key, val, noName) {
			noName = noName || false;
			if (noName) { name = ""; }

			if (!key || key.length === 0) {
				key = name;
			}
			return key + (key.length > 0 && val ? "=" : "") + val;
		}


		var simpleConf = {
			prefix: "", joiner: ",", encode: encodeNormal, builder: addUnNamed
		};
		var reservedConf = {
			prefix: "", joiner: ",", encode: encodeReserved, builder: addUnNamed
		};
		var fragmentConf = {
			prefix: "#", joiner: ",", encode: encodeReserved, builder: addUnNamed
		};
		var pathParamConf = {
			prefix: ";", joiner: ";", encode: encodeNormal, builder: addLabeled
		};
		var formParamConf = {
			prefix: "?", joiner: "&", encode: encodeNormal, builder: addNamed
		};
		var formContinueConf = {
			prefix: "&", joiner: "&", encode: encodeNormal, builder: addNamed
		};
		var pathHierarchyConf = {
			prefix: "/", joiner: "/", encode: encodeNormal, builder: addUnNamed
		};
		var labelConf = {
			prefix: ".", joiner: ".", encode: encodeNormal, builder: addUnNamed
		};

		function Expression(conf, vars) {
			extend(this, conf);
			this.vars = vars;
		}

		Expression.build = function (ops, vars) {
			var conf;
			switch (ops) {
				case '': conf = simpleConf; break;
				case '+': conf = reservedConf; break;
				case '#': conf = fragmentConf; break;
				case ';': conf = pathParamConf; break;
				case '?': conf = formParamConf; break;
				case '&': conf = formContinueConf; break;
				case '/': conf = pathHierarchyConf; break;
				case '.': conf = labelConf; break;
				default: throw "Unexpected operator: '" + ops + "'";
			}
			return new Expression(conf, vars);
		};

		Expression.prototype.expand = function (context) {
			var joiner = this.prefix;
			var nextjoiner = this.joiner;
			var buildSegment = this.builder;
			var res = "";
			var i = 0, cnt = this.vars.length;

			for (i = 0; i < cnt; i++) {
				var varspec = this.vars[i];
				varspec.addValues(context, this.encode, function (key, val, noName) {
					var segm = buildSegment(varspec.name, key, val, noName);
					if (segm !== null && segm !== undefined) {
						res += joiner + segm;
						joiner = nextjoiner;
					}
				});
			}
			return res;
		};

		var UNBOUND = {};

		function Buffer(limit) {
			this.str = "";
			if (limit === UNBOUND) {
				this.appender = Buffer.UnboundAppend;
			} else {
				this.len = 0;
				this.limit = limit;
				this.appender = Buffer.BoundAppend;
			}
		}

		Buffer.prototype.append = function (part, encoder) {
			return this.appender(this, part, encoder);
		};

		Buffer.UnboundAppend = function (me, part, encoder) {
			part = encoder ? encoder(part) : part;
			me.str += part;
			return me;
		};

		Buffer.BoundAppend = function (me, part, encoder) {
			part = part.substring(0, me.limit - me.len);
			me.len += part.length;

			part = encoder ? encoder(part) : part;
			me.str += part;
			return me;
		};


		function arrayToString(arr, encoder, maxLength) {
			var buffer = new Buffer(maxLength);
			var joiner = "";

			var i = 0, cnt = arr.length;
			for (i = 0; i < cnt; i++) {
				if (arr[i] !== null && arr[i] !== undefined) {
					buffer.append(joiner).append(arr[i], encoder);
					joiner = ",";
				}
			}
			return buffer.str;
		}

		function objectToString(obj, encoder, maxLength) {
			var buffer = new Buffer(maxLength);
			var joiner = "";
			var k;

			for (k in obj) {
				if (obj.hasOwnProperty(k)) {
					if (obj[k] !== null && obj[k] !== undefined) {
						buffer.append(joiner + k + ',').append(obj[k], encoder);
						joiner = ",";
					}
				}
			}
			return buffer.str;
		}

		function simpleValueHandler(me, val, valprops, encoder, adder) {
			var result;

			if (valprops.isArr) {
				result = arrayToString(val, encoder, me.maxLength);
			} else if (valprops.isObj) {
				result = objectToString(val, encoder, me.maxLength);
			} else {
				var buffer = new Buffer(me.maxLength);
				result = buffer.append(val, encoder).str;
			}

			adder("", result);
		}

		function explodeValueHandler(me, val, valprops, encoder, adder) {
			if (valprops.isArr) {
				var i = 0, cnt = val.length;
				for (i = 0; i < cnt; i++) {
					adder("", encoder(val[i]));
				}
			} else if (valprops.isObj) {
				var k;
				for (k in val) {
					if (val.hasOwnProperty(k)) {
						adder(k, encoder(val[k]));
					}
				}
			} else {
				adder("", encoder(val));
			}
		}

		function valueProperties(val) {
			var isArr = false;
			var isObj = false;
			var isUndef = true;

			if (val !== null && val !== undefined) {
				isArr = (val.constructor === Array);
				isObj = (val.constructor === Object);
				isUndef = (isArr && val.length === 0) || (isObj && isEmptyObject(val));
			}

			return { isArr: isArr, isObj: isObj, isUndef: isUndef };
		}


		function VarSpec(name, vhfn, nums) {
			this.name = unescape(name);
			this.valueHandler = vhfn;
			this.maxLength = nums;
		}

		VarSpec.build = function (name, expl, part, nums) {
			var valueHandler, valueModifier;

			if (!!expl) {
				valueHandler = explodeValueHandler;
			} else {
				valueHandler = simpleValueHandler;
			}

			if (!part) {
				nums = UNBOUND;
			}

			return new VarSpec(name, valueHandler, nums);
		};

		VarSpec.prototype.addValues = function (context, encoder, adder) {
			var val = context.get(this.name);
			var valprops = valueProperties(val);
			if (valprops.isUndef) { return; } // ignore empty values
			this.valueHandler(this, val, valprops, encoder, adder);
		};

		var VARSPEC_RE = /([^*:]*)((\*)|(:)([0-9]+))?/;

		var match2varspec = function (m) {
			var name = m[1];
			var expl = m[3];
			var part = m[4];
			var nums = parseInt(m[5], 10);

			return VarSpec.build(name, expl, part, nums);
		};

		var LISTSEP = ",";

		var TEMPL_RE = /(\{([+#.;?&\/])?(([^.*:,{}|@!=$()][^*:,{}$()]*)(\*|:([0-9]+))?(,([^.*:,{}][^*:,{}]*)(\*|:([0-9]+))?)*)\})/g;

		var match2expression = function (m) {
			var expr = m[0];
			var ops = m[2] || '';
			var vars = m[3].split(LISTSEP);
			var i = 0, len = vars.length;
			for (i = 0; i < len; i++) {
				var match;
				if ((match = vars[i].match(VARSPEC_RE)) === null) {
					throw "unexpected parse error in varspec: " + vars[i];
				}
				vars[i] = match2varspec(match);
			}

			return Expression.build(ops, vars);
		};


		var pushLiteralSubstr = function (set, src, from, to) {
			if (from < to) {
				var literal = src.substr(from, to - from);
				set.push(new Literal(literal));
			}
		};

		var parse = function (str) {
			var lastpos = 0;
			var comp = [];

			var match;
			var pattern = TEMPL_RE;
			pattern.lastIndex = 0; // just to be sure
			while ((match = pattern.exec(str)) !== null) {
				var newpos = match.index;
				pushLiteralSubstr(comp, str, lastpos, newpos);

				comp.push(match2expression(match));
				lastpos = pattern.lastIndex;
			}
			pushLiteralSubstr(comp, str, lastpos, str.length);

			return new UriTemplate(comp);
		};
		return parse
	}

	const factory = $.PhSigV4AWSClientFactory();
	const utils = $.PhSigV4ClientUtils();
	const template = $.PhUriTemplate();

	const key = CryptoJS.enc.Utf8.parse("1234123412ABCDEF");  //十六位十六进制数作为密钥
	const iv = CryptoJS.enc.Utf8.parse('ABCDEF1234123412');   //正常情况由后端返回十六位十六进制数作为密钥偏移量
	const client_id = $('#client_id').val().replace(/\s+/g, "")
	const callback = $("#redirect_uri").val()
	const state = CryptoJS.MD5(`${client_id}${new Date().getTime()}`).toString()
	$("#secret").remove()
	//解密方法
	function Decrypt(word) {
		let encryptedHexStr = CryptoJS.enc.Hex.parse(word);
		let srcs = CryptoJS.enc.Base64.stringify(encryptedHexStr);
		let decrypt = CryptoJS.AES.decrypt(srcs, key, { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
		let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
		return decryptedStr.toString();
	}

	//加密方法
	// function Encrypt(word) {
	// 	let srcs = CryptoJS.enc.Utf8.parse(word);
	// 	let encrypted = CryptoJS.AES.encrypt(srcs, key, { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
	// 	return encrypted.ciphertext.toString().toUpperCase();
	// }

	const config = {
		accessKey: Decrypt('B963100A6E95D5C7EDC8E27DFDD1C7658B4951449C5D91D620EC3604C6F3221A'),
		secretKey: Decrypt('F0480FDD9E4E8705E1A5E1DDCC716EA6B1B197CE50B7930A009F5C543F2EEEC08A54D72D52567AD613B92FF73135152F'),
		sessionToken: '',
		region: 'cn-northwest-1',
		apiKey: undefined,
		defaultContentType: 'application/vnd.api+json',
		defaultAcceptType: 'application/vnd.api+json'
	};

	const invokeUrl = 'https://2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn/v0';
	const endpoint = /(^https?:\/\/[^\/]+)/g.exec(invokeUrl)[1];
	const pathComponent = invokeUrl.substring(endpoint.length);

	const sigV4ClientConfig = {
		accessKey: config.accessKey,
		secretKey: config.secretKey,
		sessionToken: config.sessionToken,
		serviceName: 'execute-api',
		region: config.region,
		endpoint: endpoint,
		defaultContentType: config.defaultContentType,
		defaultAcceptType: config.defaultAcceptType
	};

	function hexEncode(value) {
		return value.toString(CryptoJS.enc.Hex)
	}

	function sha256(value) {
		return hexEncode(CryptoJS.SHA256(value).toString())
	}

	function tips(type, value) {
		$('#alert').empty()
		$('#alert').append(`<div class="alert alert-${type}"><a href="#" class="close" data-dismiss="alert">&times;</a><strong>${type}! </strong>${value}</div>`)
		setTimeout(function () {
			$('#alert').empty()
		}, 5000)
		return;
	}

	$('#authSubmit').click(async () => {
		function isEqRe(key, value) {
			return value.indexOf(key) !== -1
		}
		const isNullRe = /^\s*$/g
		const account = $('#account').val().replace(/\s+/g, "")
		const password = $('#password').val()
		// const client_secret = $('#client_secret').val().replace(/\s+/g, "")

		// TODO: || isNullRe.test(client_secret) || isEqRe("{{client_secret}}", client_secret)
		// TODO: 这边只能验证client_id 和 secret是否为空，具体验证是否合法交由逻辑层
		if (isNullRe.test(client_id) || isEqRe("{{client_id}}", client_id)) {
			tips("warning", "client_id illegal input");
			return;
		}
		if (isNullRe.test(account) || isNullRe.test(password)) {
			tips("warning", "Input box is required");
		} else {
			const result = await login(account, sha256(password), client_id)
			if (result === undefined || result.status !== 200) {
				const msg = result === undefined ? 'An unknown error' : result.data.message
				tips("danger", msg);
			} else {
				console.info("Result", result)
			}
		}
	})

	async function send(client, params, keys) {
		axios.interceptors.response.use(response => {
			return response;
		}, (err) => { // 这里是返回状态码不为200时候的错误处理
			return Promise.resolve(err);
		})
		const req = {
			verb: 'get'.toUpperCase(),
			path: pathComponent + template('/oauth/{edp}').expand(utils.parseParametersToObject(params, ['edp'])),
			headers: utils.parseParametersToObject(params, ['Accept']),
			queryParams: utils.parseParametersToObject(params, keys),
			body: {},
			timeout: 30000
		};
		let request = client.makeRequest(req)
		return await axios(request)
	}

	async function login(accout, password) {
		const client = factory.newClient(sigV4ClientConfig)

		async function oauthLogin(data) {
			const params = {
				edp: "login",
				Accept: "application/json",
				email: data.account,
				password: data.password
			}
			const result = await send(client, params, ['email', 'password'])
			console.log(result)
			return result
		}

		async function authorization(oauthLoginResult) {
			const params = {
				edp: "authorization",
				Accept: "application/json",
				client_id: client_id,
				response_type: "code",
				user_id: oauthLoginResult.data.uid,
				redirect_uri: callback,
				state
			}
			const result = await send(client, params, ['client_id', 'response_type', 'user_id', 'redirect_uri', 'state'])
			console.log(result)
			const authorizationParams = {}

			for (const item of result.data.split('&')) {
				const obj = item.split('=')
				authorizationParams[obj[0]] = obj[1]
			}
			if (authorizationParams.state !== state) {
				tips("danger", "parameter error");
				return
			}
			console.log(authorizationParams)
			const callBackParm = [
				`client_id=${client_id}`,
				`code=${authorizationParams.code}`,
				`redirect_uri=${authorizationParams.redirect_uri}`,
				`grant_type=authorization_code`,
				`state=${authorizationParams.state}`].join("&")
			window.location = `${callback}?${callBackParm}`
		}

		const registerFuncs = registerFunc(authorization, registerFunc(oauthLogin, []));

		console.log(registerFuncs);
		return await runListFun({
			account: accout,
			password: password
		}, registerFuncs);
	}

	function registerFunc(func, merge) {
		merge.push(func);
		return merge;
	}

	// 链式调用Fun
	async function runListFun(data, funcs) {
		let result = data;
		for (const func of funcs) {
			result = await func(result)
			if (result.data === undefined) {
				return result.response;
			}
		}
		return result;
	}

})(jQuery)