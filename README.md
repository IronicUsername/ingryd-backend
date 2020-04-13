# ingryd-backend

## Project setup
Start the service:
```sh
docker-compose up --force-recreate --build -d
```


## Development

### Environment parameters:
* `DB_HOST`: The host of the postgres database server.
* `DB_NAME`: The database name of the postgres database server.
* `DB_USER`: The user of the postgres database server.
* `DB_PASS`: The password of the user of the postgres database server.
* `LOG_CONSOLE`: If set to `1`, it gives you human readable logs, if set to `0` it prints json logs (only for development purposes)
