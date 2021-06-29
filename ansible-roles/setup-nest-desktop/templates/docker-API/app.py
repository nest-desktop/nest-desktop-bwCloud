from flask import Flask, request
import docker

app = Flask(__name__)
client = docker.client.from_env()


@app.route('/containers', methods=['GET', ])
def containers():
    return client.containers.list()


# @app.route('/containers/id', methods=['GET', ])
# def containers_id():
#     return [container.id for container in client.containers.list()]
#
#
# @app.route('/containers/short_id', methods=['GET', ])
# def containers_short_id():
#     return [container.short_id for container in client.containers.list()]
#
#
# @app.route('/containers/name', methods=['GET', ])
# def containers_name():
#     return [container.name for container in client.containers.list()]


# @app.route('/container/<name>/logs', methods=['GET', ])
# def container_logs(name):
#     container = client.containers.get(name)
#     return '<pre>' + container.logs().decode() + '</pre>'


@app.route('/container/<name>/restart', methods=['GET', ])
def container_restart(name):
    container = client.containers.get(name)
    container.restart()
    return 'Container {} restarted.\n'.format(name)


@app.route('/container/<name>/status', methods=['GET', ])
def container_status(name):
    container = client.containers.get(name)
    return 'Status of container {}: {}.\n'.format(name, container.status)


@app.route('/container/<name>/stop', methods=['GET', ])
def container_stop(name):
    container = client.containers.get(name)
    container.stop()
    return 'Container {} stopped.\n'.format(name)

@app.route('/images', methods=['GET', ])
def images():
    return client.images.list()

#
# @app.route('/images/id', methods=['GET', ])
# def images_id():
#     return [image.id for image in client.images.list()]
#
#
# @app.route('/images/short_id', methods=['GET', ])
# def images_short_id():
#     return [image.short_id for image in client.images.list()]


@app.route('/image/<name>/start', methods=['GET', ])
def image_start(name):
    image = client.images.get(name)
    port = request.args.get('port')
    container = client.containers.run(image,
                                      detach=True,
                                      name=request.args.get('name'),
                                      ports={'{}/tcp'.format(port): port}
                                      )
    return 'Container {} started.\n'.format(name)


app.run(port=5001)
