import ascon
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory

class EchoServer(Protocol):
    def _init_(self):
        # Generar parámetros Diffie-Hellman (DH clásico) para el servidor
        self.parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
        self.private_key = self.parameters.generate_private_key()
        self.public_key = self.private_key.public_key()
        self.shared_key = None

        self.nonce = b'qc\xb3\x0bJ\x92\xaf{\xee\r\x1a\x94d\x04o\xf8'
        self.associated_data = b"SENSOR"

    def connectionMade(self):
        """Cuando un cliente se conecta, enviamos nuestra clave pública."""
        print("Cliente conectado. Enviando clave pública del servidor...")
        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.transport.write(public_key_pem)

    def dataReceived(self, data):
        """Procesamos la clave pública del cliente y generamos la clave compartida."""
        print(f"Recibido del cliente: {data[:50]}...")

        try:
            if data.startswith(b"-----BEGIN PUBLIC KEY-----"):
                print("Recibida clave pública del cliente.")
                client_public_key = serialization.load_pem_public_key(data, backend=default_backend())
                
                # Generar la clave compartida utilizando Diffie-Hellman (DH clásico)
                self.shared_key = self.private_key.exchange(client_public_key)
                print("Clave compartida generada:", self.shared_key.hex())

                # Enviar nuestra clave pública al cliente
                public_key_pem = self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                self.transport.write(public_key_pem)
                print("Clave pública del servidor enviada al cliente.")

            elif self.shared_key and len(data) > 0:
                print("Recibiendo datos cifrados del cliente...")
                # Desencriptar los datos con la clave compartida
                decrypted = ascon.ascon_decrypt(
                    key=self.shared_key[:16],  # Usamos los primeros 16 bytes de la clave compartida
                    nonce=self.nonce,
                    associateddata=self.associated_data,
                    ciphertext=data,
                    variant="Ascon-128"
                )
                print("Datos descifrados:", decrypted.decode())

        except Exception as e:
            print(f"Error procesando datos: {e}")

class EchoServerFactory(Factory):
    def buildProtocol(self, addr):
        return EchoServer()

reactor.listenTCP(8080, EchoServerFactory())  # Asegúrate de que el puerto 8080 esté libre
print("Servidor escuchando en el puerto 8080...")
reactor.run()