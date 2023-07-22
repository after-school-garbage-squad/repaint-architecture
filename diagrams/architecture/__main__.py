from diagrams import Diagram, Cluster
from diagrams.gcp.network import Armor
from diagrams.gcp.compute import AppEngine, Run, Functions
from diagrams.gcp.database import SQL
from diagrams.gcp.storage import Storage
from diagrams.gcp.operations import Monitoring
from diagrams.firebase.grow import Messaging
from diagrams.firebase.base import Firebase
from diagrams.generic.device import Mobile, Tablet

with Diagram("GCP Architecture", filename="imgs/gcp_architecture.png", show=False):
    
    with Cluster("Client"):
        visitor_mobile = Mobile("Visitor")
        admin_tablet = Tablet("Admin")

    with Cluster("Google Cloud"):
        armor = Armor("Armor")
        backend_app = AppEngine("Back-end API")
        event_grafana_run = Run("Event grafana")
        user_grafana_func = Functions("Add user operation")
        system_grafana_run = Run("System grafana")
        backend_sql = SQL("Backend DB")
        storage = Storage("Image storage")
        monitoring = Monitoring("Cloud Monitoring")
        fcm = Messaging("FCM")
        analytics = Firebase("Analytics")
        image_reg_run = Run("Image recognition")
        image_gen_run = Run("Image generation")


    armor >> backend_app
    backend_app >> backend_sql
    backend_sql >> event_grafana_run
    backend_app >> user_grafana_func >> event_grafana_run
    monitoring >> system_grafana_run
    visitor_mobile >> analytics
    admin_tablet >> analytics
    backend_app >> fcm >> visitor_mobile
    analytics >> system_grafana_run
    backend_app >> image_reg_run >> storage
    backend_app >> image_gen_run
    storage >> image_gen_run >> backend_app
    backend_app >> monitoring
    backend_sql >> monitoring
    image_reg_run >> monitoring
    image_gen_run >> monitoring
    storage >> monitoring
    visitor_mobile >> armor
    admin_tablet >> armor
