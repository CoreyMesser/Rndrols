import connexion

from logger import LoggerService

ls = LoggerService()
_log = ls.get_logger()


def app_run():
    _log.info("___RndRolls starting___")
    try:
        app = connexion.App(__name__, port=8080, specification_dir='api/')
        app.add_api('openapi.yaml', arguments={'title': 'Random Rolls'})
        app.run()
        _log.info("___API SERVER STARTED___")

    except Exception as e:
        _log.error(f"[ERROR] RndRolls failed to start due to: {e}")


if __name__ == '__main__':
    app_run()
