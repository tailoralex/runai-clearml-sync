from api_clients import runai_api, clearml_api
from runai_projects import CreateProjects
from project_settings import ProjectSettings


class ClearRunSync:
    def __init__(self,
                 tenant_name: str,
                 cluster_id: str,
                 client_id: str,
                 client_secret: str,
                 runai_base_url: str,
                 deserved_gpus: float,
                 interactive_jobs_time_limit: int,
                 verify_cert: bool,
                 default_user: str,
                 delete_projects: bool,
                 dry_run: bool):

        self.runai_client = runai_api.RunaiClient(tenant_name=tenant_name,
                                                  cluster_id=cluster_id,
                                                  client_id=client_id,
                                                  client_secret=client_secret,
                                                  runai_base_url=runai_base_url,
                                                  verify_cert=verify_cert,
                                                  default_user=default_user)
        self.project_settings = ProjectSettings(deserved_gpus,
                                                interactive_jobs_time_limit,
                                                delete_projects,
                                                dry_run)
        self.clear_client = clearml_api.ClearMLClient()

    def sync(self):
        CreateProjects(runai_client=self.runai_client,
                       projects_dict=self.clear_client.get_projects(),
                       project_settings=self.project_settings).sync()


