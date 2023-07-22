from diagrams import Diagram, Cluster
from diagrams.gcp.network import Armor
from diagrams.gcp.compute import AppEngine, Run, Functions
from diagrams.gcp.database import SQL, Datastore
from diagrams.gcp.storage import Storage
from diagrams.gcp.operations import Monitoring
from diagrams.firebase.grow import Messaging
from diagrams.firebase.base import Firebase
from diagrams.generic.device import Mobile, Tablet

with Diagram("GCP Architecture", filename="imgs/gcp_architecture", show=False):
    with Cluster("Client"):
        visitor_mobile = Mobile("Visitor")
        admin_tablet = Tablet("Admin")

    with Cluster("Google Cloud"):
        armor = Armor("Armor")

        with Cluster("Back-end API"):
            backend_app = AppEngine("Back-end API")
            backend_sql = SQL("Backend DB")
            backend_nosql = Datastore("Backend Palette DB")

        with Cluster("Image Manage"):
            image_manage_run = Run("Image Manage System")
            image_manage_db = SQL("Image Manage DB")
            image_storage = Storage("Image storage")

        with Cluster("Image Processing"):
            image_clustering_run = Run("Image clustering")
            image_gen_run = Run("Image generation")

        with Cluster("Monitoring"):
            system_grafana_run = Run("System grafana")
            monitoring = Monitoring("Cloud Monitoring")

        with Cluster("Event monitoring"):
            event_grafana_run = Run("Event grafana")
            user_grafana_func = Functions("Add user operation")

    with Cluster("Firebase"):
        analytics = Firebase("Analytics")
        fcm = Messaging("FCM")

    visitor_mobile >> armor
    admin_tablet >> armor

    armor >> backend_app
    armor >> event_grafana_run
    armor >> image_manage_run

    backend_app >> backend_sql
    backend_app >> backend_nosql
    backend_app >> fcm >> visitor_mobile

    backend_app >> user_grafana_func >> event_grafana_run
    backend_sql >> event_grafana_run

    backend_app >> image_clustering_run >> image_storage
    admin_tablet >> image_gen_run >> image_storage

    image_manage_run >> image_manage_db
    image_manage_run >> image_storage

    monitoring >> system_grafana_run
    analytics >> system_grafana_run

    backend_app >> monitoring
    backend_sql >> monitoring
    backend_nosql >> monitoring
    image_manage_run >> monitoring
    image_storage >> monitoring
    image_clustering_run >> monitoring
    image_gen_run >> monitoring

    visitor_mobile >> analytics
