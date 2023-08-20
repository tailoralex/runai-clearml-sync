import argparse
from ClearRunSync import ClearRunSync

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tenant_name', required=True)
    parser.add_argument('--cluster_id', required=True)
    parser.add_argument('--client_id', required=True)
    parser.add_argument('--client_secret', required=True)
    parser.add_argument('--runai_base_url', default="https://app.run.ai", help="default: 'https://app.run.ai'")

    parser.add_argument('--deserved_gpus', default=2, help="deserved GPUs for every new project (default: 2)")
    parser.add_argument('--interactive_jobs_time_limit', default=0,
                        help="Limit duration of interactive jobs in seconds (default: '43200' - 12 hours)")
    parser.add_argument("--no_certificate_verification", default=False, action="store_true")
    parser.add_argument("--default_user", default="api@run.ai",
                        help="Default username that will be assigned to newly created projects (default: api@run.ai)")
    parser.add_argument("--delete_projects", default=False, action="store_true",
                        help="Turn on if you want to delete projects that are no longer present inn clearml")
    parser.add_argument("--dry-run", default=False, action="store_true",
                        help="Run the script without doing any actions")

    args = parser.parse_args()
    ClearRunSync(
                #runai
                tenant_name=args.tenant_name,
                cluster_id=args.cluster_id,
                client_id=args.client_id,
                client_secret=args.client_secret,
                runai_base_url=args.runai_base_url,
                default_user=args.default_user,
                #project attributes
                interactive_jobs_time_limit=args.interactive_jobs_time_limit,
                deserved_gpus=args.deserved_gpus,
                verify_cert=not args.no_certificate_verification,
                delete_projects=args.delete_projects,
                dry_run=args.dry_run
    ).sync()
