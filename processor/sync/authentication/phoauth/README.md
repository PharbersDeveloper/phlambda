# OAuth 核心代码

## 概要

### 什么是OAuth！

**OAuth不是一项技术，他不需要特定语言才能实现。**

OAuth是一种“协议”说协议我个人感觉不是很喜欢，我个人更喜欢用规则这个词去描述什么是OAuth。

OAuth这套规则其实是有版本之分，最初OAuth 1.x因为有严重的逻辑漏洞，后面才诞生了OAuth2.0，这套核心代码是以OAuth2.0的规则去抽象编写。

## 支持模式

**本项目支持模式：**

- password (密码模式)
- authorization code (授权码模式)
- implicit (简单模式，我们自己的登录页面使用的是这种同时加入了授权码模式)第三方只能使用前2种
- client credentials (客户端模式，未实现)
- refresh token (刷新token)
- revoke token (单独的撤销没做，只做了跟刷新后的旧的token撤销)

```password```

![密码模式](https://tva1.sinaimg.cn/large/e6c9d24ely1h4d6z8vbvrj20m70bat9c.jpg)

> （A）用户向客户端提供用户名和密码。
>
> （B）客户端将用户名和密码发给认证服务器，向后者请求令牌。
>
> （C）认证服务器确认无误后，向客户端提供访问令牌。



```authorization code```

![授权码模式](https://tva1.sinaimg.cn/large/e6c9d24ely1h4d6xyji5dj20l80epdgs.jpg)

> （A）用户访问客户端，后者将前者导向认证服务器。
>
> （B）用户选择是否给予客户端授权。
>
> （C）假设用户给予授权，认证服务器将用户导向客户端事先指定的"重定向URI"（redirection URI），同时附上一个授权码。
>
> （D）客户端收到授权码，附上早先的"重定向URI"，向认证服务器申请令牌。这一步是在客户端的后台的服务器上完成的，对用户不可见。
>
> （E）认证服务器核对了授权码和重定向URI，确认无误后，向客户端发送访问令牌（access token）和更新令牌（refresh token）。



```implicit```

![简化模式](https://tva1.sinaimg.cn/large/e6c9d24ely1h4d73d9slej20in0fxwfe.jpg)

> （A）客户端将用户导向认证服务器。
>
> （B）用户决定是否给于客户端授权。
>
> （C）假设用户给予授权，认证服务器将用户导向客户端指定的"重定向URI"，并在URI的Hash部分包含了访问令牌。
>
> （D）浏览器向资源服务器发出请求，其中不包括上一步收到的Hash值。
>
> （E）资源服务器返回一个网页，其中包含的代码可以获取Hash值中的令牌。
>
> （F）浏览器执行上一步获得的脚本，提取出令牌。
>
> （G）浏览器将令牌发给客户端。



```client credentials```

![客户端模式](https://tva1.sinaimg.cn/large/e6c9d24ely1h4d74o5baaj20ma0530sx.jpg)

> （A）客户端向认证服务器进行身份认证，并要求一个访问令牌。
>
> （B）认证服务器确认无误后，向客户端提供访问令牌。







## 实现原理

自己看代码抽象，熟悉OOP的应该会很快看懂~

## 学习官网

官网  [OAuth 2.0 — OAuth](https://oauth.net/2/)

中文  [理解OAuth 2.0 - 阮一峰的网络日志 (ruanyifeng.com)](
