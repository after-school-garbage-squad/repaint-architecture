from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.network import Armor
from diagrams.gcp.compute import Run, Functions
from diagrams.gcp.database import SQL, Datastore
from diagrams.gcp.storage import Storage
from diagrams.gcp.operations import Monitoring
from diagrams.gcp.analytics import Pubsub
from diagrams.firebase.grow import Messaging
from diagrams.firebase.base import Firebase
from diagrams.generic.device import Mobile, Tablet
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.monitoring import Grafana
from diagrams.programming.framework import Flutter, React
from diagrams.programming.language import Python, Rust
from diagrams.onprem.network import Nginx


def drawArchitecture(is_service=False):
    with Cluster("Client"):
        visitor_mobile = Mobile("Visitor") if not is_service else Flutter("Visitor")
        admin_tablet = Tablet("Admin") if not is_service else React("Admin")

    with Cluster("Google Cloud"):
        armor = Armor("Armor")

        with Cluster("Back-end API"):
            backend_run = Run("Back-end API") if not is_service else Rust("Back-end API")
            backend_sql = SQL("Backend DB") if not is_service else PostgreSQL("Backend DB")
            backend_nosql = Datastore("Backend Palette DB")

        with Cluster("Image Manage"):
            image_nginx_run = Run("Image Proxy") if not is_service else Nginx("Image Proxy")
            image_auth_run = Run("Image Auth") if not is_service else Python("Image Auth")
            image_manage_db = SQL("Image Manage DB") if not is_service else PostgreSQL("Image Manage DB")
            image_storage = Storage("Image storage")

        with Cluster("Image Processing"):
            image_clustering_func = Functions("Image clustering") if not is_service else Python("Image clustering")
            image_gen_func = Functions("Image generation") if not is_service else Python("Image generation")
            image_pubsub = Pubsub("Image pub/sub")

        with Cluster("Monitoring"):
            system_grafana_run = Run("System grafana") if not is_service else Grafana("System grafana")
            monitoring = Monitoring("Cloud Monitoring")

        with Cluster("Event monitoring"):
            event_grafana_run = Run("Event grafana") if not is_service else Grafana("Event grafana")
            user_grafana_func = Functions("Add user operation") if not is_service else Python("Add user operation")
            event_log_nosql = Datastore("Event log DB")

    with Cluster("Firebase"):
        analytics = Firebase("Analytics")
        fcm = Messaging("FCM")

    visitor_mobile >> armor
    admin_tablet >> armor

    armor >> backend_run
    armor >> event_grafana_run
    armor >> image_nginx_run

    backend_run >> backend_sql
    backend_run >> backend_nosql
    backend_run >> fcm >> visitor_mobile
    backend_run >> event_log_nosql

    backend_run >> user_grafana_func >> event_grafana_run
    event_log_nosql >> event_grafana_run

    backend_run >> image_pubsub
    image_pubsub >> image_clustering_func >> image_storage
    image_pubsub >> image_gen_func >> image_storage

    image_nginx_run >> image_storage
    image_nginx_run >> image_auth_run
    image_auth_run >> image_manage_db
    backend_run >> image_auth_run

    monitoring >> system_grafana_run
    analytics >> system_grafana_run

    def drawMonitoring():
        backend_run >> monitoring
        backend_sql >> monitoring
        backend_nosql >> monitoring
        image_nginx_run >> monitoring
        image_auth_run >> monitoring
        image_storage >> monitoring
        image_clustering_func >> monitoring
        image_gen_func >> monitoring
        image_pubsub >> monitoring
        event_log_nosql >> monitoring

    visitor_mobile >> analytics


with Diagram("GCP Architecture", filename="docs/architecture/imgs/gcp_architecture", show=False):
    drawArchitecture()

with Diagram("Service Architecture", filename="docs/architecture/imgs/service_architecture", show=False):
    drawArchitecture(is_service=True)
