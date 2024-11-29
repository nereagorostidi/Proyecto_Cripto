import ascon
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

class EchoClient(LineReceiver):
    end = b"Bye-bye!"

    def _init_(self):
        # Generar parámetros y claves Diffie-Hellman
        self.parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
        self.private_key = self.parameters.generate_private_key()
        self.public_key = self.private_key.public_key()
        self.shared_key = None

        # Datos para encriptar
        self.nonce = b'qc\xb3\x0bJ\x92\xaf{\xee\r\x1a\x94d\x04o\xf8'
        self.associatedData = b"SENSOR"
        self.dataTemperature = b"1,3,12,24,29,42,100"

    def connectionMade(self):
        """Cuando conecta el cliente al servidor, envía su clave pública."""
        print("SENDING CLIENT PUBLIC KEY TO SERVER")
        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.sendLine(public_key_pem)

    def lineReceived(self, line):
        """Procesa las respuestas del servidor."""
        print(f"Received data from server: {line[:50]}...")  # Muestra los primeros 50 bytes

        if line.startswith(b"-----BEGIN PUBLIC KEY-----"):
            print("RECEIVED SERVER PUBLIC KEY")
            # Recibir la clave pública del servidor
            server_public_key = serialization.load_pem_public_key(line, backend=default_backend())
            # Generar la clave compartida usando la clave pública del servidor
            self.shared_key = self.private_key.exchange(server_public_key)

            print("Now I have the shared key and will send data!")

            # Cifrar datos con ASCON usando la clave compartida
            encryptedTemp = ascon.ascon_encrypt(
                key=self.shared_key[:16],  # Usar los primeros 16 bytes como clave para ASCON
                nonce=self.nonce,
                associateddata=self.associatedData,
                plaintext=self.dataTemperature,
                variant="Ascon-128"
            )
            print("Encrypted Data: ", encryptedTemp)

            # Enviar los datos cifrados al servidor
            self.sendLine(encryptedTemp)

        if line == self.end:
            self.transport.loseConnection()


class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def _init_(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        self.done.callback(None)


def main(reactor):
    """Función principal para iniciar la conexión del cliente."""
    factory = EchoClientFactory()
    reactor.connectTCP("localhost", 8080, factory)  # Asegúrate de que el servidor esté escuchando en el puerto 8080
    return factory.done


if _name_ == "_main_":
    task.react(main)
