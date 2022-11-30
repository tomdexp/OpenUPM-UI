import subprocess
from events import Events


class InstallationProcess:
    def __init__(self, package_name, folder_path, installation_complete):
        self.package_name = package_name
        self.folder_path = folder_path
        self.installation_complete = installation_complete
        self.installation_log = ""
        self.CallBackEvents = Events()

    def apply_defaults(self):
        self.package_name = "com.default"
        self.folder_path = "folder/default"
        self.installation_complete = False
        self.print_log("Applied defaults to InstallationProcess object.")

    def install(self):
        self.print_log("Installing " + self.package_name + " into " + self.folder_path)
        self.print_log("Checking if Node.js is installed...")
        obj = subprocess.run("node -v", shell=True, capture_output=True)
        node_version = obj.stdout.decode("utf-8")
        node_version_number = node_version.split("v")[1]
        node_version_major = str(node_version_number.split(".")[0])
        node_version_minor = str(node_version_number.split(".")[1])
        node_version_total = int(node_version_major + node_version_minor)
        if obj.returncode != 0:
            self.print_log("Node.js is not installed! Please install Node.js and try again.")
            return
        if node_version_total < 1418:
            self.print_log("Node.js version is too old! Please update Node.js to at least v14.18 or above and try again.")
            return
        self.print_log("Node.js version: " + node_version_number)
        self.print_log("Checking if npm is installed...")
        obj = subprocess.run("npm -v", shell=True, capture_output=True)
        if obj.returncode != 0:
            self.print_log("npm is not installed! Please install npm and try again.")
            return
        self.print_log("npm version: " + obj.stdout.decode("utf-8"))
        self.print_log("Checking if OpenUPM CLI is installed...")
        obj = subprocess.run("openupm -V", shell=True, capture_output=True)
        if obj.returncode != 0:
            self.print_log("OpenUPM CLI is not installed! Automatically installing OpenUPM CLI, please wait...")
            subprocess.run("npm install -g openupm-cli", shell=True, capture_output=True)
            self.print_log("OpenUPM CLI installed!")
        else:
            self.print_log("OpenUPM CLI version: " + obj.stdout.decode("utf-8"))
        self.print_log("Installing package...")
        obj = subprocess.run(
            'openupm --chdir "{path}" add {pkg}'.format(path=self.folder_path, pkg=self.package_name),
            shell=True, capture_output=True)
        self.print_log("Package installed!")
        self.print_log(obj.stdout.decode("utf-8"))
        self.print_log(obj.stderr.decode("utf-8"))
        self.installation_complete = True
        self.CallBackEvents.on_installation_complete()

    def print_log(self, value):
        print(value)
        self.installation_log += "[LOG] " + value + "\n"
        self.CallBackEvents.on_log(value)

    def __str__(self):
        return "InstallationProcess(package_name=" + self.package_name + ", folder_path=" + self.folder_path + ", installation_complete=" + str(
            self.installation_complete) + ")"

