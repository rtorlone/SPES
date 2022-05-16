from fastapi_mail import MessageSchema, FastMail


class EmailService:
    """
    Classe che definisce il servizio per l'invio delle email.

    """

    def __init__(self, fast_email: FastMail) -> None:
        self._fast_email: FastMail = fast_email

    def send_credentials(self, dest: str, username: str, password: str) -> None:
        """
        Invia un email contente le credenziali d'accesso a SPES.

        dest: email del destinatario
        username: username da inviare
        password: password da inviare
        """
        subject = "Benvenuto in SPES!"
        template = f"""
                    
                    Queste sono le tue credenziali:
                    Username: {username}
                    Password: {password}
                    
                """
        message = MessageSchema(
            subject=subject,
            recipients=[dest],
            body=template,
            subtype=None
        )

        return self._fast_email.send_message(message)
