import { QoS } from "aws-crt/dist/common/mqtt"
import { io } from "aws-iot-device-sdk-v2"
import { Logger } from "phnodelayer"
import Conf from "../common/conf"
import MQTT from "../common/iot"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        let mq: MQTT = null
        try {
            const cert = `
        -----BEGIN CERTIFICATE-----
MIIDWTCCAkGgAwIBAgIUHvgOnGVaKMmbi92BjxrDMj6gX+cwDQYJKoZIhvcNAQEL
BQAwTTFLMEkGA1UECwxCQW1hem9uIFdlYiBTZXJ2aWNlcyBPPUFtYXpvbi5jb20g
SW5jLiBMPVNlYXR0bGUgU1Q9V2FzaGluZ3RvbiBDPVVTMB4XDTIxMDExMzA2MzM0
M1oXDTQ5MTIzMTIzNTk1OVowHjEcMBoGA1UEAwwTQVdTIElvVCBDZXJ0aWZpY2F0
ZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALP2zL6IwWBHJsznZ88G
knHHZ0NE9BnvRAlV65OUcZID+ZtA7/e+OnsiwBdAmXxC5a+bVMZ9MYvne+CBkoCP
KdqiG2U7kBe8z0wzkjDaEfhUCTGtWlVMtrFGmHAdC0Gf6XM2EkpybEA/LpXESTUb
wvZu+ctmIf5ADMIa6+cmL7Bwk6ZPwDtQ2cqHCz0eCSwsIDO3cm1P0GPbsJGNjCJ8
k5o3pHi0UMa1qIycAK+ShRtJoV/0adY8qgVdCPwKtk/EeGgiU3AD60eE2tk5W15p
V91NakftDviQFoURjFpV2OK0R1OE3fWzyOV26fyqo+qiuKYXJQjETHlT5yu43lNu
AJsCAwEAAaNgMF4wHwYDVR0jBBgwFoAUoInftUCoD5td8Yzu3HhpJfdwfiowHQYD
VR0OBBYEFM5ZORZngjxxBavV55rbNjVVlPOeMAwGA1UdEwEB/wQCMAAwDgYDVR0P
AQH/BAQDAgeAMA0GCSqGSIb3DQEBCwUAA4IBAQCk0//NXzqXPusrwfj7bzcpXHfE
+h4pGjNEnoHTjIqStpGBCo8DXCiWBY6yFuCJeOlg+UPpvAeta56Z6gR62TY+VntU
f72Sso8r78FQJFCENtmgIrNAG1T9pUORPugsvyjdQsN2PvAAimfx1bnK+HazMY0L
Mckz3Fucwz12tX6Kqh7QgsqhbPScE6dlJbnc04fh9dKHkijQ9JGjWhcLDdNNe+g4
B4lFMDgZB4w40xhFSlvffPfNVDqM7H6m36dZc/RPKhRsGlrni5Lqjd5f0eODyQzT
01PiNSufcGvAwsSAZw82gNFFhmN6BnPWqitDa7Wf4Y7oRx2UXD1xckm6iiQt
-----END CERTIFICATE-----
        `
            const key = `
        -----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAs/bMvojBYEcmzOdnzwaSccdnQ0T0Ge9ECVXrk5RxkgP5m0Dv
9746eyLAF0CZfELlr5tUxn0xi+d74IGSgI8p2qIbZTuQF7zPTDOSMNoR+FQJMa1a
VUy2sUaYcB0LQZ/pczYSSnJsQD8ulcRJNRvC9m75y2Yh/kAMwhrr5yYvsHCTpk/A
O1DZyocLPR4JLCwgM7dybU/QY9uwkY2MInyTmjekeLRQxrWojJwAr5KFG0mhX/Rp
1jyqBV0I/Aq2T8R4aCJTcAPrR4Ta2TlbXmlX3U1qR+0O+JAWhRGMWlXY4rRHU4Td
9bPI5Xbp/Kqj6qK4phclCMRMeVPnK7jeU24AmwIDAQABAoIBAH9tgNplMTAAEZxD
OoEf8S/5dsfuGj4G6pEFsrIkCSrP/70MBR7SJsyr9YJBbqzLHaHzhdqqKRwcQ93b
QaYgOQ2jfWx3+Xalbc9SMPDAaLsCniP70JvXnwD1sNip6B+GoKHApsDqNnZjhpPr
kb62Mp2WRO/eGLHUHnSO5X0dz+TJEL+bbjmKjnZUluj1W0Jbdf57jZ9tL4DRT0IB
KNSHTXvEyz+NI1Cv3jbT+Duy+QqsCDEBVgRdS7oUpam/FJO9AwcRL3INFPhkc263
N49Ex6nFFtWdLqQrTAQWBa4WOwLeuF/taKV0+K93gmtzHhDLTtyFYvTuQx6+EVGK
Zbnm+SkCgYEA6t+k7fqudva/x/W4scLnuvdIT7dEgKrgAheRQyHVj3Kuow/hhO94
dZrcXhr4lO/tJ7DIB3sO3MFyGcQaNVTESbSHNH9KvVJWBzgXisBiHatmE1zuabN8
vxhshf74W5PaZsD/v10OitkvNclUtJjzp/gIv/KjoBur5H6ZDs9eMe0CgYEAxCbF
k/VqggZHCFSbVOiBMUZr9+ySYDkNmWVKTXCNJKFrHyoTL/Jirf1Cw/PW7n/ylBpx
EPtUug3kINmAXBHQdvgfG/zUWVDjqzl+JqnMg5dElYXCNZVX1c2a4YnG+QYWhqGB
ILiOTanGFdypIlIq0QTMcjyC4WASUN8S1BZnS6cCgYBFeeZVpwOYmSDdy2fY3Wii
u6cePX37+Y/Nzp7fltCPYEMcZQQ2yId/clGhXKUPmXEzfm2NGO+qiWZxDLsb73ko
vEgKVWUMX6Cm/gaouoPLdvn43FKB3eAWvujLMkLRBAlkv85nEuXMWLZIWMe/rEbW
9t3PubyBDe5o5rHr2ZdpeQKBgQCUmU7bPXQX1wufGwGmPJILM29+HkHyFabgy+ST
cC3tT0BpFqX8j+MELraS3rq4akPqwXFgzRat8PIflMbyeSh1yJlAybRRib9Aq0iP
n9lo44M4x2GO2Hn3ZlDshkUvyNXt3pKFqGteGL0RON8FOjxnpvv/myoH9ZFKpQSN
mf9dRwKBgBKPdZWI/ZcJPSPZsIR3jPl8VxTIDMmX4x28FzNaVBK15+1XmWjNXXsu
TkbsVZNKHBvi/VsW/EUBoW2FWi/5xuU7Kwm609DsWHfWT2N3GWCMbDcLgsVIPc92
LL32dd/WzNfwq+xSTOASzwNY1TBfT1TEDdBVuKK1L4If8E8AeB52
-----END RSA PRIVATE KEY-----
        `
            const ca = `
            -----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
        `
            mq = new MQTT()
            await mq.setClientId("001").setCleanSession(false)
                .setClientBootstrap(new io.ClientBootstrap()).setConfigBuilder(cert, key, ca)
                .setEndPoint(Conf.endpoint).build()
            await mq.open()
            const message = "啦啦啦啦阿拉啦啦啦拉拉😋"
            await mq.publish("test/1", QoS.AtLeastOnce, message)
            return {body: {message}, statusCode: 200}
        } catch (e) {
            Logger.error(e)
        } finally {
            if (mq) {
                await mq.close()
            }
        }
    }
}
