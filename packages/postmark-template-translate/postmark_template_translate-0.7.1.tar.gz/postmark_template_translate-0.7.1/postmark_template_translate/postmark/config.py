from postmarker.core import PostmarkClient

class PostmarkService:
    def __init__(self, server_token):
        self.client = PostmarkClient(server_token=server_token)

    def get_template(self, template_id):
        try:
            template = self.client.templates.get(template_id)
            return template.HtmlBody
        except Exception as e:
            print(f"Error al obtener la plantilla: {e}")
            return None

    def send_translated_email(self, template_id, model, language, from_email, to_email, message_stream):
        from postmark_template_translate.translate.translate import translate_html
        
        html = self.get_template(template_id)
        if not html:
            print("Error: No se pudo obtener la plantilla.")
            return
        
        translated_html = translate_html(html, dest_lang=language)
        
        for key, value in model.items():
            placeholder = f"{{{{{key}}}}}"
            translated_html = translated_html.replace(placeholder, str(value))

        try:
            self.client.emails.send(
                From=from_email,
                To=to_email,
                Subject="Your translated email subject here",
                HtmlBody=translated_html,
                MessageStream=message_stream
            )
            print("Correo enviado correctamente.")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

# Exporta una función para crear una instancia del servicio
def configure(server_token):
    return PostmarkService(server_token=server_token)
