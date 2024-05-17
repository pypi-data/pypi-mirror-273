"""Main Class for GitLab Builds data collection"""

import os
import time
import json
import gitlab
import requests
import pandas as pd
from typing import Optional

from tqdm import tqdm
from glbuild import constants
from glbuild.utils import utils
from glbuild.collector import progress
from requests.exceptions import ChunkedEncodingError
from urllib3.exceptions import InsecureRequestWarning


# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)  # type: ignore


class GitLabBuild:
    """GitLabBuild Class."""

    def __init__(
        self,
        token: str,
        projects: list[int],
        base_url: str = constants.GITLAB_BASE_URL,
        api_version: int = 4,
        ssl_verify: bool = False,
    ) -> None:
        """Constructor.

        Params
        ------
            base_url(str): GitLab instance base URL. Defaults to https://gitlab.com
            token(str): GitLab Personal Access Token.
        """
        self.base_url: str = base_url
        self.token: str = token
        self.api_version: int = api_version
        self.ssl_verify: bool = ssl_verify
        self.projects = projects
        self.gl = gitlab.Gitlab(
            url=base_url,
            private_token=token,
            api_version=api_version,
            ssl_verify=ssl_verify,
        )
        self.progress = progress.Progress(projects=projects)

    def get(self, datapath: str) -> bool:
        """Get historical build jobs metadata and logs from projects into path.

        Params
        ------
            projects(list[int]|int): Single of List of projects ID.
            path(str): Directory for output.
        """
        # Create directories if necessary
        for path in [datapath, f"{datapath}/logs/"]:
            utils.ensure_path(path)

        for path in [f"{datapath}/logs/{id}" for id in self.projects]:
            utils.ensure_path(path)

        for project_id in self.progress.load_unprocessed():
            self.__get_project_data(project_id, datapath)
            self.progress.set_processed(project_id)
            time.sleep(1)
        return True

    ###################################
    #         Project Methods         #
    ###################################

    def __get_project_data(
        self, project_id: int, datapath: str, only_failures: bool = True
    ):
        """Collect jobs metadata and logs for a GitLab project."""
        print(f"\nProcessing project with id {project_id}")

        # get all metadata of jobs.
        jobs = self.__get_jobs_metadata(project_id, datapath=datapath)
        print(f"{len(jobs)} jobs found for collection.")

        # download the logs
        progress_bar = tqdm(jobs, ncols=120)
        for job in progress_bar:
            if only_failures:
                if job["status"] != "failed":
                    continue

            job_log_file = f"{datapath}/logs/{project_id}/{job['id']}.log"
            # if job log file is already collected, next.
            if os.path.isfile(job_log_file):
                continue
            # else get and save logs
            logs = self.__retrieve_job_logs(project_id, job["id"])
            utils.to_file(logs, job_log_file)

        # close progress bar
        progress_bar.close()

    ###################################
    #           Job Methods           #
    ###################################

    def __get_jobs_metadata(self, project_id: int, datapath: str):
        """Get jobs for project (or download) and save to datapath.

        project_id(int): ID of the project.
        datapath(str): Base directory where to save the collected data.
        """
        jobs_filepath = f"{datapath}/jobs_{project_id}.json"
        project = self.gl.projects.get(int(project_id), lazy=True)

        # read already collected json jobs
        old_jobs = utils.json_to_list(jobs_filepath)
        if old_jobs is None:
            # read entire history records
            jobs = self.__get_all_jobs(project)
        else:
            # read new records efficiently
            old_jobs = pd.DataFrame(old_jobs)
            last_collected_job_id: int = old_jobs["id"].max()

            page: int = 1
            jobs_df: pd.DataFrame = pd.DataFrame(
                self.__get_jobs_by_page(project=project, page=page)
            )
            # collect only new record
            while last_collected_job_id not in jobs_df["id"].to_list():
                page = page + 1
                jobs_df = pd.concat(
                    [
                        jobs_df,
                        pd.DataFrame(
                            self.__get_jobs_by_page(project=project, page=page)
                        ),
                    ],
                    ignore_index=True,
                )

            # merge new records to old ones
            jobs_df = pd.concat([jobs_df, old_jobs], ignore_index=True).drop_duplicates(
                subset=["id"]
            )
            print(f"{jobs_df.shape[0] - old_jobs.shape[0]} additionnal jobs found.")
            jobs = jobs_df.to_dict(orient="records")

        # save jobs json data
        with open(jobs_filepath, mode="w", encoding="utf-8") as f:
            json.dump(jobs, f)
        return jobs

    def __get_all_jobs(self, project) -> list[dict]:
        """Get list of all jobs for a project using python-gitlab."""
        return [
            json.loads(job.to_json())
            for job in project.jobs.list(all=True, retry_transient_errors=True)
        ]

    def __get_jobs_by_page(
        self, project, page: int, per_page: int = constants.JOBS_PER_PAGE
    ) -> list[dict]:
        """Get list of jobs on a given page for a project using python-gitlab."""
        return [
            json.loads(job.to_json())
            for job in project.jobs.list(
                per_page=per_page, page=page, retry_transient_errors=True
            )
        ]

    def __retrieve_job_logs(
        self, project_id: str | int, job_id: str | int
    ) -> Optional[str]:
        """Get job textual log data from API.

        Returns
        -------
            (str | None): Log data textual content. None if no logs available (e.g., for canceled jobs).
        """
        headers = {
            "PRIVATE-TOKEN": self.token,
        }
        url = f"{self.base_url}/api/v4/projects/{project_id}/jobs/{job_id}/trace"
        try:
            response = requests.get(
                url,
                headers=headers,
                verify=self.ssl_verify,
                timeout=constants.HTTP_REQUESTS_TIMEOUT,
            )
            return response.text
        except ChunkedEncodingError:
            # Empty log
            return None
