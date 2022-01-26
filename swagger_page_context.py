SWAGGER_CONFIG = {
    'title': 'TTIA ESTOP Restful API',
    'uiversion': 3,
    'specs_route': '/docs/'
}

SWAGGER_CONTEXT = {
    "swagger": "2.0",
    "info": {
        "title": "TTIA ESTOP http server",
        "description": "API for controlling TTIA ESTOP service",
        "contact": {
            "responsibleOrganization": "Askey",
            "responsibleDeveloper": "Howard",
            "email": "howard1_hsu@askey.com.tw",
        },
        "version": "0.1.1"
    },
    "host": "127.0.0.1:5000",
    "schemes": [
        "http",
        "https"
    ],
}
