import requests
from decouple import config

from apps.correos.domain.entities.correo import Correo
from apps.correos.domain.interfaces.proveedor_correo import ProveedorCorreo


class GraphProvider(ProveedorCorreo):
    @staticmethod
    def obtener_token() -> str:
        url = f"https://login.microsoftonline.com/{config('MS_TENANT_ID')}/oauth2/v2.0/token"

        data = {
            "client_id": config("MS_CLIENT_ID"),
            "client_secret": config("MS_CLIENT_SECRET"),
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        }

        response = requests.post(url, data=data, timeout=30)
        response.raise_for_status()
        return response.json()["access_token"]

    @staticmethod
    def normalizar_correos(correos):
        if not correos:
            return []
        if isinstance(correos, str):
            correos = [correos]
        return [str(c).strip() for c in correos if str(c).strip()]

    def enviar(self, correo: Correo) -> dict:
        token = self.obtener_token()
        url = f"https://graph.microsoft.com/v1.0/users/{config('MS_SENDER_EMAIL')}/sendMail"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        destinatarios = self.normalizar_correos(correo.destinatarios)
        cc = self.normalizar_correos(correo.cc)
        bcc = self.normalizar_correos(correo.bcc)

        if not destinatarios:
            raise Exception("Debe existir al menos un destinatario principal")

        message = {
            "subject": correo.asunto,
            "body": {
                "contentType": "HTML",
                "content": correo.contenido_html,
            },
            "toRecipients": [
                {"emailAddress": {"address": email}} for email in destinatarios
            ],
        }

        if cc:
            message["ccRecipients"] = [
                {"emailAddress": {"address": email}} for email in cc
            ]

        if bcc:
            message["bccRecipients"] = [
                {"emailAddress": {"address": email}} for email in bcc
            ]

        if correo.attachments:
            message["attachments"] = correo.attachments

        payload = {
            "message": message,
            "saveToSentItems": True,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        return {
            "ok": True,
            "mensaje": "Correo enviado correctamente",
            "status_code_graph": response.status_code,
        }