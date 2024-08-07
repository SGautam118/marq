from prometheus_client import start_http_server, Gauge
import docker
import time

# Create a Docker client
client = docker.from_env()

# Create a Prometheus gauge metric
container_status = Gauge('docker_container_status', 'Docker container status', ['container_name'])

def collect_metrics():
    containers = client.containers.list(all=True)
    for container in containers:
        status = 1 if container.status == 'running' else 0
        container_status.labels(container.name).set(status)

if __name__ == '__main__':
    start_http_server(8000)  # Start Prometheus exporter
    while True:
        collect_metrics()
        time.sleep(10)
