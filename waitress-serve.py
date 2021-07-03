from waitress import serve
import application
serve(application.application, host="0.0.0.0", port="5000",url_scheme='https')