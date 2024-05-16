import requests
import os
from pathlib import Path
from constants import STANDARD_CONST, CONST
import tarfile

class Installer:
    # __slots__ = 
    def __init__(self, doc: str, globals: dict) -> None:
        self.source, self.repo, release = doc.strip().split("\n")
        
        # self._get_repo_url()
        # self._get_release(release)
        self.is_latest = release == 'latest'
        
        # recognized constants (to be filled)
        self.FILES = []
        self.ROOT = ""
        self.DRIVE = ""
        
        # getting all user set variables
        for k, v in globals.items():
            if k in STANDARD_CONST:
                self.__dict__[k] = v
        
        # getting default values if not given by the user
        for k in (set(CONST.keys()) - set(self.__dict__.keys())):
            self.__dict__[k] = CONST[k]
        
        self.INSTALL_FOLDER = globals.get("INSTALL_FOLDER", self.repo)
    

    def install(self, path=None):
        if not path:
            if os.environ.get('os') == "Windows_NT":
                install_path = Path(self.DRIVE, "", self.INSTALL_FOLDER)
                print(install_path)
                # !os.makedirs(root, exist_ok=True)
                
                # downloading project from github to temp folder
                #! temp: Path = Path(os.environ['temp']) / self.repo / f"{self.release_name}.tar.gz"
                temp: Path = Path(os.environ['temp']) / self.repo / f"v1.2.0.tar.gz"
                print(temp)
                os.makedirs(temp.parent, exist_ok=True)

                # !with open(temp, 'wb') as file:
                #     resp = requests.get(self.archive_url)
                #     if resp.status_code == 200:
                #         file.write(resp.content)

                # with open(temp, 'rb') as tar:
                #     tar = tarfile.TarFile()
                #     print(tar.getmember())
                #     print(tar.getnames())
                
                with tarfile.open(temp, 'r:gz') as tar:
                    names = tar.getnames()
                    base = Path(names[0])
                    root = (base / self.ROOT)
                    root = root.as_posix()
                    root_len = len(root)
                    files = []

                    for file in self.FILES:
                        file = f"{root}/{file}"
                        if file in names:
                            files.append(file)

                    if not self.FILES:
                        files = [file for file in names if file.startswith(root)]
                    
                    # print(root_len)
                    for file in files:
                        # print(install_path / file[root_len+1:])
                        file_path = install_path / file[root_len+1:]
                        print(os.path.dirname(file_path), file_path)
                        # print(file)
                        # print(file_path)
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(file_path, "wb") as ifile:
                            ifile.write(tar.extractfile(file).read())


        

    
    def _get_repo_url(self):
        if self.source == "github":
            url = f"https://github.com/{self.repo}"
            resp = requests.head(url)
            if resp.status_code == 200:
                self.repo_url = url
            else:
                raise Exception(f"Repository Not Found: {url}")

    
    def _get_release(self, release="latest"):
        if self.source == "github":
            release_url = f"{self.repo_url}/releases/{release}"
            resp = requests.head(release_url)
            if 200 <= resp.status_code < 400:
                self.release_url = release_url if resp.status_code < 300 else resp.headers.get("location")
            else:
                raise Exception("Release Not Found")
            
            self.release_name = self.release_url.split("/")[-1]
            
            if self.release_name == "releases":
                raise Exception("Release Not Found")

            self.archive_url = f"{self.repo_url}/archive/refs/tags/{self.release_name}.tar.gz"

