import time
import uuid

import consts
from api_clients import runai_api, clearml_api
from project_settings import ProjectSettings


class CreateProjects:
    def __init__(self, runai_client, projects_dict, project_settings):
        self.runai_client = runai_client
        self.clearml_projects_dict = projects_dict
        self.project_settings = project_settings
        self.runai_projects = self.runai_client.get_all_projects()
        self.runai_departments = self.runai_client.get_all_departments()
        self.runai_users = self.runai_client.get_all_users()
        self._user_exists()
        if not self.project_settings.dry_run:
            self.default_user_id = self.get_default_user_id()

    def sync(self):
        for clearml_main_project in self.clearml_projects_dict.keys():
            if self._department_exists(clearml_main_project):
                print(f'Department {clearml_main_project} exists, skipping')
            else:
                print(f'Creating Department for ClearML project {clearml_main_project}')
                if not self.project_settings.dry_run:
                    self._create_department(clearml_main_project)
            self.create_projects(clearml_main_project)
        if self.project_settings.delete_projects:
            self.delete_non_existing()

    def create_projects(self, department):
        for clearml_project in self.clearml_projects_dict[department]:
            if self._project_exists(clearml_project):
                print(f"Project {clearml_project} exists, skipping...")
            else:
                print(f"Creating project {clearml_project}")
                if not self.project_settings.dry_run:
                    department_id = self.get_department_id(department)
                    self._create_project(clearml_project, department_id)

    def _create_department(self, department):
        payload = self.build_department_body(department)
        self.runai_client.create_department(payload)
        print(f"Department {department} created successfully")
        self.runai_departments = self.runai_client.get_all_departments()

    def _create_project(self, project, department_id):
        payload = self.build_project_body(project, department_id)
        new_project = self.runai_client.create_project(payload)
        #self.runai_client.update_project(new_project["id"], payload)
        print(f"Project {project} created successfully")

    def _department_exists(self, department_name):
        return department_name in [p["name"] for p in self.runai_departments]

    def _project_exists(self, project_name):
        return project_name in [p["name"] for p in self.runai_projects]

    def get_department_id(self, department):
        return [d["id"] for d in self.runai_departments if d["name"] == department][0]

    def delete_non_existing(self):
        for project in self.runai_projects:
            if project["name"] not in sum(self.clearml_projects_dict.values(), []):
                print(f'Project {project["name"]} doesn\'t exists in ClearML anymore, deleting')
                if not self.project_settings.dry_run:
                    self.runai_client.delete_project(project["id"])

    def _user_exists(self):
        if self.runai_client.default_user not in [u["name"] for u in self.runai_users]:
            print(f"User name not found creating {self.runai_client.default_user}")
            if not self.project_settings.dry_run:
                self.runai_client.create_user(self.build_user_body(self.runai_client.default_user))
            time.sleep(2)
        else:
            print(f"User {self.runai_client.default_user} exists")

    def get_default_user_id(self):
        return [u["userId"] for u in self.runai_users if u["name"] == self.runai_client.default_user][0]

    def build_department_body(self, department_name):
        return {
            "name": department_name,
            "deservedGpus": self.project_settings.deserved_gpus*3,
            "allowOverQuota": True,
            "maxAllowedGpus": self.project_settings.deserved_gpus*3
        }

    def build_user_body(self, user_email: str) -> dict:
        return {
            "entityType": "app",
            "roles": ["researcher", "viewer"],
            "permittedClusters": [self.runai_client.cluster_id],
            "name": user_email,
            "password": consts.PASSWORD,
            "email": user_email,
            "permitAllClusters": False,
            "needToChangePassword": False
        }


def build_project_body(self, project_name, department_id):
    return {
        "name": project_name,
        "departmentId": department_id,
        "deservedGpus": self.project_settings.deserved_gpus,
        "clusterUuid": self.runai_client.cluster_id,
        "nodeAffinity": {
            "train": {
                "affinityType": "no_limit",
                "selectedTypes": []
            },
            "interactive": {
                "affinityType": "no_limit",
                "selectedTypes": []
            }
        },
        "permissions": {
            "users": [self.default_user_id],
            "groups": [],
            "applications": []
        },
        "gpuOverQuotaWeight": consts.OVER_QUOTA_WEIGHT,
        "maxAllowedGpus": -1,
        "swapEnabled": False,
        "resources": {
            "gpu": {
                "deserved": self.project_settings.deserved_gpus,
                "maxAllowed": -1,
                "overQuotaWeight": consts.OVER_QUOTA_WEIGHT
            },
            "cpu": {},
            "memory": {}
        }
    }
