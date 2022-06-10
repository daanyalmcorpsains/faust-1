from faust.auth import (
    GSSAPICredentials,
    SASLCredentials,
    SSLCredentials,
)

from faust.types.auth import CredentialsT
from typing import (Any, Mapping)
from faust.exceptions import ImproperlyConfigured


class BrokerCredentialsMixin:

    def __init__(self):
        pass

    def get_auth_credentials(self, client=None) -> Mapping:

        credentials = self.app.conf.broker_credentials
        ssl_context = self.app.conf.ssl_context

        if credentials is not None:
            if isinstance(credentials, SSLCredentials):
                return {
                    'security_protocol': credentials.protocol.value,
                    'ssl_context': credentials.context,
                }
            elif isinstance(credentials, SASLCredentials):
                return {
                    'security_protocol': credentials.protocol.value,
                    'sasl_mechanism': credentials.mechanism.value,
                    'sasl_plain_username': credentials.username,
                    'sasl_plain_password': credentials.password,
                    'ssl_context': credentials.ssl_context,
                }
            elif isinstance(credentials, GSSAPICredentials):
                return {
                    'security_protocol': credentials.protocol.value,
                    'sasl_mechanism': credentials.mechanism.value,
                    'sasl_kerberos_service_name':
                        credentials.kerberos_service_name,
                    'sasl_kerberos_domain_name':
                        credentials.kerberos_domain_name,
                    'ssl_context': credentials.ssl_context,
                }
            else:
                raise ImproperlyConfigured(
                    f'{client} does not support {credentials}')
        elif ssl_context is not None:
            return {
                'security_protocol': 'SSL',
                'ssl_context': ssl_context,
            }
        elif client == 'aiokafka':
            return {'security_protocol': 'PLAINTEXT'}
        else:
            return None
