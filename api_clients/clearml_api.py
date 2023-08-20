from clearml.backend_api.session.client import APIClient
import re
import consts


class ClearMLClient:
    def __init__(self):
        self.client = APIClient()
        self.clearml_projects = self.client.projects.get_all()
        self.department_project_list = {}
        self.build_project_list()

    def get_projects(self):
        print(self.department_project_list)
        return self.department_project_list

    def build_project_list(self):
        for proj in self.clearml_projects:
            if len(proj.name.split("/")) == 1:
                department = self._rfc_complient(proj.name)
                self.department_project_list[department] = self.get_sub_project_list(proj.name)

    def get_sub_project_list(self, main_proj):
        project_list = []
        all_sub_projects = [p.name for p in self.clearml_projects if main_proj == p.name.split("/")[0]]
        for sub_project in all_sub_projects:
            sub_proj = sub_project.split("/")
            if len(sub_proj) == 2:
                rfc_project = f'{self._rfc_complient(main_proj)}-{self._rfc_complient(sub_proj[1])}'
                if rfc_project[-1] == "-":
                    rfc_project = rfc_project[:-1]
                project_list.append(rfc_project)
        return project_list

    def _rfc_complient(self, project):
        return re.sub(r"[^a-zA-Z0-9]+", "-", project).lower()

