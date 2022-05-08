from azure.storage.blob import BlobServiceClient, ContentSettings
import requests
import json
import os
from datetime import datetime
import uuid
import azure.functions as func


class EndpointsClient:
    def __init__(self, working_path):
        self.uuid = str(uuid.uuid4())
        self.main_page = "main.html"
        self.out_path = "artifacts"
        self.artifacts_path = working_path + "/" + self.out_path
        self.main_page_path = working_path + "/" + self.main_page
        if not os.path.exists(self.artifacts_path):
            os.mkdir(self.artifacts_path)
        self.clear()

    def clear(self):
        self.sorted_url_list = {}
        self.url_list = None

    def get_o365_endpoints(self):
        """
        Get Office 365 endpoints IP addresses
        """
        self.clear()
        office_response = requests.get(
            "https://endpoints.office.com/endpoints/worldwide?clientrequestid={}".format(
                self.uuid
            )
        )
        self.url_list = office_response.json()
        urls = []
        for key in self.url_list:
            if "urls" in key:
                urls.append(key["urls"])
                self.urls_output = urls
        urls_json_list = json.loads(json.dumps(self.urls_output))
        flat_list = [item for sublist in urls_json_list for item in sublist]
        return flat_list

    def export_locally(self, prepend_value=""):
        """
        Store obtained data locally
        """
        with open(
            f"{self.artifacts_path}/{prepend_value}.txt", "w"
        ) as out_file:
            for key in self.get_o365_endpoints():
                out_file.write("%s\n" % key)

    def new_main_page(self):
        """
        Generate main webpage
        """
        artifacts_files = os.listdir(self.artifacts_path)
        artifacts_files.sort(reverse=True)
        main_page_content = (
            "<html>\n<head>\n</head>\n<body>\n Generated date:<br>"
            + str(datetime.now())
            + "<br><br>Generated list:<br>"
        )
        for item in artifacts_files:
            print(item)
            main_page_content = (
                main_page_content
                + '<a href="'
                + self.out_path
                + "/"
                + item
                + '" download>'
                + item
                + "</href>\n <br>"
            )
        main_page_content += "</body></html>"
        with open(self.main_page_path, "w") as out_file:
            out_file.write("%s" % main_page_content)

    def upload_main_page(self):
        """
        Upload main webpage
        """
        self.upload_file(self.main_page_path, self.main_page)

    def upload(self, source, dest):
        """
        Upload a file or directory to a path inside the container
        """
        if os.path.isdir(source):
            self.upload_dir(source, dest)
        else:
            self.upload_file(source, dest)

    def upload_file(self, source, dest):
        """
        Upload a single file to a path inside the container
        """
        content_settings = ContentSettings(content_type="text/html")
        print(f"Uploading {source} to {dest}")
        with open(source, "rb") as data:
            self.client.upload_blob(
                name=dest, data=data, content_settings=content_settings, overwrite=True
            )

    def upload_dir(self, source="", dest=""):
        """
        Upload a directory to a path inside the container
        """
        if not source:
            source = self.artifacts_path
        prefix = "" if dest == "" else dest + "/"
        prefix += os.path.basename(source) + "/"
        for root, dirs, files in os.walk(source):
            for name in files:
                dir_part = os.path.relpath(root, source)
                dir_part = "" if dir_part == "." else dir_part + "/"
                file_path = os.path.join(root, name)
                blob_path = prefix + dir_part + name
                self.upload_file(file_path, blob_path)

    def download(self, source, dest):
        """
        Download a file or directory to a path on the local filesystem
        """
        if not dest:
            raise Exception("A destination must be provided")
        blobs = self.ls_files(source, recursive=True)
        if blobs:
            # if source is a directory, dest must also be a directory
            if not source == "" and not source.endswith("/"):
                source += "/"
            if not dest.endswith("/"):
                dest += "/"
            # append the directory name from source to the destination
            dest += os.path.basename(os.path.normpath(source)) + "/"
            blobs = [source + blob for blob in blobs]
            for blob in blobs:
                blob_dest = dest + os.path.relpath(blob, source)
                self.download_file(blob, blob_dest)
        else:
            self.download_file(source, dest)

    def download_file(self, source, dest):
        """
        Download a single file to a path on the local filesystem
        """
        # dest is a directory if ending with '/' or '.', otherwise it's a file
        if dest.endswith("."):
            dest += "/"
        blob_dest = dest + os.path.basename(source) if dest.endswith("/") else dest
        print(f"Downloading {source} to {blob_dest}")
        os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
        bc = self.client.get_blob_client(blob=source)
        with open(blob_dest, "wb") as file:
            data = bc.download_blob()
            file.write(data.readall())

    def ls_files(self, path, recursive=False):
        """
        List files under a path, optionally recursively
        """
        if not path == "" and not path.endswith("/"):
            path += "/"
        blob_iter = self.client.list_blobs(name_starts_with=path)
        files = []
        for blob in blob_iter:
            relative_path = os.path.relpath(blob.name, path)
            if recursive or not "/" in relative_path:
                files.append(relative_path)
        return files


test = EndpointsClient(working_path=".").export_locally(prepend_value="urls")