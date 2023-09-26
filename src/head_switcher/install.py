import mimetypes
import warnings


def install_to_flask(frontend_assets, app, index_html_file='index.html'):
    from flask import Response
    if index_html_file not in frontend_assets:
        warnings.warn(f'{index_html_file} not in the provided frontend_assets')

    @app.route('/', defaults={'path': ''})
    @app.route("/<string:path>")
    @app.route('/<path:path>')
    def catch_all(path):
        fp = path
        if fp not in frontend_assets:
            # due to frontend routing, we need to serve content index.html of non static asset url.
            if index_html_file not in frontend_assets:
                return '', 404
            fp = index_html_file

        mime_type, _ = mimetypes.guess_type(fp)
        content_bytes = frontend_assets[fp]
        if mime_type is None:
            mime_type = 'application/octet-stream'
        return Response(content_bytes, content_type=mime_type)
