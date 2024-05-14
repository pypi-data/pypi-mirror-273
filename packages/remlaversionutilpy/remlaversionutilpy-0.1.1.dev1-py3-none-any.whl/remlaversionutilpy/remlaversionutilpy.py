import pkg_resources

class VersionUtil:
    @classmethod
    def get_version(cls):
        try:
            # Try to retrieve version from package metadata
            version = pkg_resources.get_distribution('remlaversionutilpy').version
        except pkg_resources.DistributionNotFound:
            # If package metadata is not available, fallback to a default version
            version = 'Version Unknown'
        return version

if __name__ == "__main__":
    print(VersionUtil.get_version())
