# SPES-server
Autori: Luca Gregori & Alessandro Wood

## Installazione

### Requisiti

- **Python 3.9.7**
- **PostgreSQL 14.1**
- **Redis 6.2.6**

Si consiglia in via preliminare di configurare un nuovo virtual enviroment (venv) per python. \
Ciò può essere fatto con le seguenti modalità:
1) all'interno della cartella del progetto eseguire:
```bash
python3 -m venv venv
source venv/bin/activate
```
- Se si è da Ubuntu e il primo comando fallisce, installare il pacchetto:
```bash
sudo apt install python3-venv
```
2) Una volta attivato il nuovo virtual enviroment, per installare tutte le dipendenze eseguire il seguente comando:
```bash
pip install -r requirements.txt 
```
### /src/openapi_server/config.yml
In questo file yaml sono racchiuse le principali configurazioni riguardanti il DB usato dalla libreria ORM _SQLAlchemy_ e _redis_.

Se si desidera non eseguire SQL da file allo startup del server porre ***startup_sql_path*** uguale a **null**.
Si specifica inoltre che in caso di malconfigurazione di redis non verranno sollevate eccezioni allo startup del server ma bensi durante le chiamate API relative alla sessione.
```yaml
db:
  url: "postgresql://root:root@localhost/spes"
  drop_on_startup: false
  startup_sql_path: "startup.sql"
redis:
  host: "localhost"
  port: 6379
  db: 1
  password: "eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81"

```

## Avvio del server
```bash
cd src/openapi_server
uvicorn main:app --host 0.0.0.0 --port 8080
```
Per visualizzare la documentazione/testare le chiamate API navigare a:
http://localhost:8080/docs.

Se si desidera invece visionare la documentazione in formato json (standard openapi) navigare a http://localhost:8080/openapi.json

### Running with Docker (non testato)

To run the server on a Docker container, please execute the following from the root directory:

```bash
docker-compose up --build
```

## Guida alla struttura del progetto
### Descrizione packages
- **apis** contiene le classi che si occupano di implementare le chiamate API.
- **database**  contiene le classi che definiscono i modelli ORM del DB.
- **models**   contiene le classi che definiscono i modelli per le request e response HTTP.
- **services** contiene le classi che si occupano di prepare le response, interagendo con il livello sottostante, ovvero le repositories.
- **repositories** contiene le classi che definiscono le query per interrogare il database.
- **utils** contiene funzioni di utilità, come quelle per generare una password random e lo username.
### containers.py
Questo script contiene la classe Container che definisce configurazioni varie e definizioni di classi singleton.

Se si desidera aggiungere nuovi servizi API definite in un nuovo script, aggiungere quest'ultimo alla lista dei modules.
```python
wiring_config = containers.WiringConfiguration(
        modules=["apis.pf_api", "apis.report_api", "apis.wallet_api", "apis.auth_api", "security_api"])
```
A questo aggiungere per qualsiasi chiamata definita in questo nuovo script il decoratore *@inject* (per iniettare le dipendeze)
e dunque definire come parametro della funzione il servizio singleton che si intende usare usare.
```python
@router.post(...)
@inject
async def add_citizenship_by_pf_id(...,
    person_service: PersonService = Depends(Provide[Container.person_service])):
    pass
```
Tali servizi sono sempre definiti come classi singleton all'interno della classe Container.

``` python
person_service = providers.Factory(
        PersonService,
        person_repository=person_repository,
    )
```

Con lo stesso principio vengono definite come classi singleton anche i repository, che sono passati come argomenti agli oggetti Service.
```python
report_repository = providers.Factory(
        ReportRepository,
        session_factory=db.provided.session,
    )
```

## Installazioni extra
Qui sono definiti i docker compose per postgress e redis.
```dockerfile
version: '3.0'

services:
  postgres:
    container_name: postgres_container
    image: postgres
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      PGDATA: /data/postgres
    volumes:
       - postgres:/data/postgres
    ports:
      - "5432:5432"
    networks:
      - postgres
    restart: unless-stopped
  
  pgadmin:
    container_name: pgadmin_container
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: pgadmin4@pgadmin.org
      PGADMIN_DEFAULT_PASSWORD: root
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    volumes:
       - pgadmin:/var/lib/pgadmin

    ports:
      - "5050:80"
    networks:
      - postgres
    restart: unless-stopped

networks:
  postgres:
    driver: bridge

volumes:
    postgres:
    pgadmin:
```
```dockerfile
version: '3.8'
services:
  cache:
    image: redis
    restart: always
    ports:
      - '6379:6379'
    command: redis-server --save 20 1 --loglevel warning --requirepass eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81
    volumes: 
      - cache:/data
volumes:
  cache:
    driver: local
```
