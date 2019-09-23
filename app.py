import gevent.monkey  # isort:skip

gevent.monkey.patch_all()  # noqa

from babylon.application import connexion, core

core.core.initialise_global(config=core.config.EnvironmentConfig())

app = connexion.core.Application(
    config=connexion.config.EnvironmentConfig(
        swagger_dir="swagger/", api_spec="dbzr-projects-audit.yaml"
    )
)

application = app.wsgi

if __name__ == "__main__":
    app.run()
