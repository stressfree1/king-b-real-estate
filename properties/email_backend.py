from django.core.mail.backends.smtp import EmailBackend
import smtplib
import ssl


class CustomSMTPEmailBackend(EmailBackend):

    def open(self):

        if self.connection:
            return False

        try:
            # =====================================================
            # SSL SMTP - PORT 465
            # =====================================================
            if self.use_ssl:

                self.connection = smtplib.SMTP_SSL(
                    self.host,
                    self.port,
                    timeout=self.timeout,
                    context=self.ssl_context,
                )

            # =====================================================
            # NORMAL SMTP - PORT 25 / 587
            # =====================================================
            else:

                self.connection = smtplib.SMTP(
                    self.host,
                    self.port,
                    timeout=self.timeout,
                )

                # =================================================
                # STARTTLS - PORT 587
                # =================================================
                if self.use_tls:

                    self.connection.starttls(
                        keyfile=self.ssl_keyfile,
                        certfile=self.ssl_certfile,
                        context=self.ssl_context,
                    )

            # =====================================================
            # SMTP LOGIN
            # =====================================================
            if self.username and self.password:

                self.connection.login(
                    self.username,
                    self.password,
                )

            return True

        except OSError:
            if not self.fail_silently:
                raise

            return False

        except smtplib.SMTPException:
            if not self.fail_silently:
                raise

            return False

    def close(self):

        if self.connection is None:
            return

        try:
            try:
                self.connection.quit()

            except (ssl.SSLError, smtplib.SMTPServerDisconnected):
                self.connection.close()

        except OSError:
            if not self.fail_silently:
                raise

        finally:
            self.connection = None