from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.cache import patch_vary_headers


class SeparateAdminSessionMiddleware(SessionMiddleware):
    """
    Separates Django Admin sessions from normal frontend sessions.

    FRONTEND:
        sessionid

    ADMIN:
        admin_sessionid
    """

    ADMIN_COOKIE_NAME = "admin_sessionid"

    def _is_admin_request(self, request):
        return request.path.startswith("/admin/")

    def process_request(self, request):
        """
        Load the appropriate session depending on the URL.
        """

        if self._is_admin_request(request):

            session_key = request.COOKIES.get(
                self.ADMIN_COOKIE_NAME
            )

        else:

            session_key = request.COOKIES.get(
                settings.SESSION_COOKIE_NAME
            )

        request.session = self.SessionStore(session_key)

    def process_response(self, request, response):
        """
        Save the correct session and send the correct cookie.
        """

        try:
            accessed = request.session.accessed
            modified = request.session.modified
            empty = request.session.is_empty()

        except AttributeError:
            return response

        if not accessed:
            return response

        patch_vary_headers(
            response,
            ("Cookie",)
        )

        # =====================================================
        # DETERMINE COOKIE
        # =====================================================

        if self._is_admin_request(request):

            cookie_name = self.ADMIN_COOKIE_NAME

            cookie_path = "/admin/"

        else:

            cookie_name = settings.SESSION_COOKIE_NAME

            cookie_path = settings.SESSION_COOKIE_PATH

        # =====================================================
        # DELETE EMPTY SESSION
        # =====================================================

        if empty:

            if cookie_name in request.COOKIES:

                response.delete_cookie(
                    cookie_name,
                    path=cookie_path,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                    samesite=settings.SESSION_COOKIE_SAMESITE,
                )

            return response

        # =====================================================
        # SAVE SESSION
        # =====================================================

        if modified or settings.SESSION_SAVE_EVERY_REQUEST:

            if request.session.session_key is None:

                request.session.save()

            else:

                try:

                    request.session.save()

                except Exception:

                    request.session.create()

            # =================================================
            # SESSION COOKIE SETTINGS
            # =================================================

            if settings.SESSION_EXPIRE_AT_BROWSER_CLOSE:

                max_age = None

            else:

                max_age = settings.SESSION_COOKIE_AGE

            # =================================================
            # SET COOKIE
            # =================================================

            response.set_cookie(
                cookie_name,
                request.session.session_key,

                max_age=max_age,

                domain=settings.SESSION_COOKIE_DOMAIN,

                path=cookie_path,

                secure=settings.SESSION_COOKIE_SECURE,

                httponly=settings.SESSION_COOKIE_HTTPONLY,

                samesite=settings.SESSION_COOKIE_SAMESITE,
            )

        return response