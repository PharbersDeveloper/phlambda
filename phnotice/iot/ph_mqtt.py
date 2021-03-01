import uuid
from iot.ph_iot import PhIOT
from awscrt import io as awscrtio
from awscrt import mqtt
from awsiot import mqtt_connection_builder


class PhMQTT(PhIOT):

    def __init__(self, endpoint, cert, key, ca, clean_session, keep_alive):
        self.client_id = str(uuid.uuid4())
        self._connection = None
        self._endpoint = endpoint
        self._cert = cert
        self._key = key
        self._ca = ca
        self._clean_session = clean_session
        self._keep_alive_secs = keep_alive

        event_loop_group = awscrtio.EventLoopGroup(1)
        host_resolver = awscrtio.DefaultHostResolver(event_loop_group)
        client_bootstrap = awscrtio.ClientBootstrap(event_loop_group, host_resolver)
        self._client_bootstrap = client_bootstrap

    def build(self):
        self._connection = mqtt_connection_builder.mtls_from_bytes(
            cert_bytes=self._cert.encode("utf-8"),
            pri_key_bytes=self._key.encode("utf-8"),
            ca_bytes=self._ca.encode("utf-8"),
            endpoint=self._endpoint,
            client_id=self.client_id,
            client_session=self._clean_session,
            keep_alive_secs=self._keep_alive_secs,
            client_bootstrap=self._client_bootstrap
        )

    def open(self):
        connect_future = self._connection.connect()
        connect_future.result()

    def close(self):
        disconnect_future = self._connection.disconnect()
        disconnect_future.result()

    def publish(self, topic, message, qos=mqtt.QoS.AT_LEAST_ONCE):
        self._connection.publish(topic=topic, payload=message, qos=qos)
