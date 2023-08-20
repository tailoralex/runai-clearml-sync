class ProjectSettings:
    def __init__(self, deserved_gpu, interactive_jobs_time_limit, delete_projects, dry_run):
        self.deserved_gpus = deserved_gpu
        self.interactive_jobs_time_limit = interactive_jobs_time_limit
        self.delete_projects = delete_projects
        self.dry_run = dry_run