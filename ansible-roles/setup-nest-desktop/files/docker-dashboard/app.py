from flask import Flask, render_template, request, redirect
import docker

app = Flask(__name__)
base_url = "/docker/"
app.config["APPLICATION_ROOT"] = base_url

client = docker.client.from_env()

configs = {
    'jupyter-lab': {
        'image': 'docker-registry.ebrains.eu/nest/nest-simulator:3.4',
        'kwargs': {
            'detach': True,
            'environment': ["NEST_CONTAINER_MODE=jupyterlab"],
            'name': 'jupyter-lab',
            'ports': {'8080/tcp': 8080},
        }
    },
    'nest-desktop': {
        'image': 'docker-registry.ebrains.eu/nest/nest-desktop:3.2',
        'kwargs': {
            'detach': True,
            'name': 'nest-desktop',
            'ports': {'54286/tcp': 54286},
        }
    },
    'nest-simulator': {
        'image': 'docker-registry.ebrains.eu/nest/nest-simulator:3.4',
        'kwargs': {
            'detach': True,
            'environment': ["NEST_CONTAINER_MODE=nest-server"],
            'name': 'nest-simulator',
            'ports': {'52425/tcp': 52425},
        }
    }
}

@app.route('/', methods=['GET', ])
def home():
    return redirect(base_url + 'containers')

@app.route('/containers', methods=['GET', ])
def containers():
    containers = client.containers.list()
    return render_template('containers.html', base_url=base_url, containers=containers)

@app.route('/api/containers/prune', methods=['GET', ])
def container_prune():
    return client.containers.prune()

@app.route('/container/<container_id>/logs', methods=['GET', ])
def container_logs(container_id):
    container = client.containers.get(container_id)
    logs = container.logs()
    return render_template('logs.html', base_url=base_url, id=container_id, logs=logs.decode("utf-8"))

@app.route('/api/container/<container_id>/restart', methods=['GET', ])
def container_restart(container_id):
    container = client.containers.get(container_id)
    container.restart()
    return container.status

@app.route('/api/container/<container_id>/status', methods=['GET', ])
def container_status(container_id):
    container = client.containers.get(container_id)
    return container.status

@app.route('/api/container/<container_id>/stop', methods=['GET', ])
def container_stop(container_id):
    container = client.containers.get(container_id)
    container.stop()
    client.containers.prune()
    return container.status

@app.route('/api/container/<image_name>/run', methods=['GET', ])
def image_run(image_name):
    config = configs[image_name]
    container = client.containers.run(config['image'], **config['kwargs'])
    return container.status

@app.route('/images', methods=['GET', ])
def images():
    images = client.images.list()
    imagesData = []
    for image in images:
        if len(image.tags) > 0:
            short_id = image.short_id.split(':')[1]
            name = image.tags[0].split(':')[0]
            label = name.split('/')[-1]
            tag = image.tags[0].split(':')[1]
            imagesData.append({'short_id': short_id, 'label': label, 'name': name, 'tag':tag})
    return render_template('images.html', base_url=base_url, images=imagesData)


app.run(port=5000)
