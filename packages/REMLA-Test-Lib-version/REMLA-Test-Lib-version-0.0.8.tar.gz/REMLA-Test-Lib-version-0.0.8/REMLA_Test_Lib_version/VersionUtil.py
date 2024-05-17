
import os

class VersionUtil:
    @staticmethod
    def get_version():
        # Get the version from the VERSION file
        with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as version_file:
            return version_file.read().strip()    
    

if __name__ == "__main__":
    print(VersionUtil.get_version())
