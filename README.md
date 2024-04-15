# UQAC_API

L'objectif du projet de session est de développer et déployer une application Web responsable du paiement de commandes Internet.

Le projet consiste à développer une application Web responsable de prendre des commandes Internet. Cette application devra répondre à une API REST, mais devra également être utilisée à travers des pages HTMLs.

##

### Équipe

- [Nolwenn TREUST - TREN21620200]()
- [Sophie BERTRAND - BERS15580400]()

##

```
.
├── README.md
├── htmlcov
│   ├── coverage_html.js
│   ├── d_869ccebe1c6d09d3___init___py.html
│   ├── d_869ccebe1c6d09d3_models_py.html
│   ├── d_869ccebe1c6d09d3_services_py.html
│   ├── d_869ccebe1c6d09d3_view_py.html
│   ├── favicon_32.png
│   ├── index.html
│   ├── keybd_closed.png
│   ├── keybd_open.png
│   ├── status.json
│   └── style.css
├── img
│   ├── cart_empty.png
│   ├── cart_fill.png
│   ├── landing_page.png
│   ├── order_failed.png
│   ├── order_success.png
│   ├── payment.png
│   ├── shipping.png
│   └── test_cov.png
├── inf349.py
├── instance
│   └── database.sqlite
├── orders_products
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   ├── view.py
│   └── payment_tasks.py   
├── static
│   ├── css
│   │   └── style.css
│   └── js
│       └── script.js
├── templates
│   └── index.html
└── tests
    ├── conftest.py
    ├── test_functionnal.py
    ├── test_integration.py
    └── test_unit.py

10 directories, 34 files
```

##

### Exigences

- Python 3.6+
- Flask 1.11+
- peewee 3.17
- pytest 8.1.1
- pytest-cov 4.1.0
- selenium 4.1.0
- requests 2.26.0
- redis 5.0.3
- rq 1.16.1
- psycopg2 2.9.9

Utilisation de la librairie _requests_ à la place de _urllib_ pour l'API.

##

### Démarrer le projet

Initialisation de la base données:

```bash
FLASK_DEBUG=True FLASK_APP=inf349 flask init-db
```

Lancement du serveur Flask

```bash
FLASK_DEBUG=True FLASK_APP=inf349 flask run
```

Docker : 

```bash
docker compose up -d 
```

Construction de l'image Docker :

```bash
docker compose build -t api8inf349 .
```

Lancement de l'image Docker :

```bash
docker run --network=uqac_api_app-network api8inf349:latest 
```

Dans un autre terminal, initialisation de la base de données :

```bash
docker exec -it <container_id> flask init-db
```

Lancement du worker Redis :

```bash
docker exec -it <container_id> rq worker
```

##

### Tests

```bash
python -m pytest --cov=orders_products
```

ou

```bash
python -m pytest --cov-report=html --cov=orders_products
```

##

### Screenshots

![alt text](./img/test_cov.png)

![alt text](./img/landing_page.png)

![alt text](./img/cart_empty.png)

![alt text](./img/cart_fill.png)

![alt text](./img/shipping.png)

![alt text](./img/payment.png)

![alt text](./img/order_success.png)

![alt text](./img/order_failed.png)
