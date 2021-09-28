import webview                                      # type: ignore


def get_redirect_html(filename: str) -> str:
    with open(filename) as fh:
        doc = fh.read()
    return doc


filename = 'pjisocial/html/redirect.html'
redirect = 'https://google.com'
html = get_redirect_html(filename)
redirect_html = html.format(redirect)
webview.create_window('Redirect', html=redirect_html)
webview.start()


# Create Flask page with the needed JS
# Create Python object for interacting with Flask page
# Log into Facebook:
#   * response_type = code%20token
#   * pass the python object to pywebview
#   * redirect on login to the Fask page
# Grab the token from the Flask page

# See:
# https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow
# https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow#confirm
