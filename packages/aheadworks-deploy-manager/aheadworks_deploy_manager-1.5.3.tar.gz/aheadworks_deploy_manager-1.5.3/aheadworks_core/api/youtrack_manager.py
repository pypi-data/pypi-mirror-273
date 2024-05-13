import requests

class YoutrackManager:
    base = ''
    api_base = ''
    token = ''

    def __init__(self, cloud, token):
        self.base = f"https://{cloud}.youtrack.cloud"
        self.api_base = f"https://{cloud}.youtrack.cloud/api"
        self.token = token

    def get_issue_url(self, idReadable):
        return f"{self.base}/issue/{idReadable}"

    def find_issues_by_tags(self, tags):
        tags_query = ""
        for t in tags:
            tags_query += f"tag: {{{t}}} "
        api_endpoint = f"{self.api_base}/issues?fields=id,idReadable,tags(name),project(name)&query={tags_query}"
        r = requests.get(url=api_endpoint, headers=self._get_headers())
        return r.json()

    def close_issue(self, task_id):
        api_endpoint = f"{self.api_base}/commands"
        data = {"query": "Fixed", "issues": [{"id": task_id}]}
        r = requests.post(url=api_endpoint, headers=self._get_headers(), json=data)

    def reassign(self, task_id, assign_to):
        api_endpoint = f"{self.api_base}/commands"
        data = {"query": "for " + assign_to, "issues": [{"id": task_id}]}
        r = requests.post(url=api_endpoint, headers=self._get_headers(), json=data)

    def add_comment(self, task_id, text):
        api_endpoint = f"{self.api_base}/issues/{task_id}/comments?fields=id,name,author(id,name)"
        r = requests.post(url=api_endpoint, headers=self._get_headers(), json={"text": text})

    def add_attachments_to_task(self, task_id, files):
        api_endpoint = f"{self.api_base}/issues/{task_id}/attachments?fields=id,name,author(id,name),created,updated,size,mimeType,extension,charset,metaData,url"
        headers = { "Authorization": f"Bearer {self.token}" }
        r = requests.post(url=api_endpoint, headers=headers, files=files)

    def _get_headers(self):
        return {
            "Content-Type":"application/json",
            "Accept": "application/json",
            "Cache-Control": "no-cache",
            "Authorization": f"Bearer {self.token}"
        } 
