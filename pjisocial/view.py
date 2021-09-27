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
