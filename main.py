from goprocam import GoProCamera, constants
import json
from datetime import datetime, timedelta
import os

class File:
    def __init__(self, data) -> None:
        self.filename = data["n"]
        self.date = datetime.fromtimestamp(int(data["cre"]))
        self.size_bytes = int(data["s"])

class GoproMedia:
    def __init__(self, gopro: GoProCamera.GoPro) -> None:
        self.gopro = gopro
        data = json.loads(self.gopro.listMedia(media_array=True))["media"][0]
        self.files = [File(f) for f in data["fs"]]
        self.directory = data["d"]
    
    def download_files_newer(self, dt: datetime = datetime.today(), directory: str = "download"):
        files_newer = [f for f in self.files if f.date >= dt]
        for i, f in enumerate(files_newer):
            date_str = f.date.strftime("%d-%m-%Y-%a")
            out_dir = os.path.join(directory, date_str)
            out_filename = f"{date_str}_{f.date.strftime('%H:%M')}_{i}.{f.filename.split('.')[-1].lower()}"
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            out_path = os.path.join(out_dir, out_filename)
            if os.path.exists(out_path):
                print(f"Skipping {out_path}")
            else:
                print(f"Downloading {(f.size_bytes / 2**20):.02f} MiB to {out_path}: ", end="")
                self.gopro.downloadMedia(self.directory, f.filename, out_path)


goproCamera = GoProCamera.GoPro()
media = GoproMedia(goproCamera)
media.download_files_newer(datetime.today() - timedelta(days=5))


