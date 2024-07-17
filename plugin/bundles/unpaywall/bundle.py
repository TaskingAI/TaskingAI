from bundle_dependency import *


class Unpaywall(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        # todo The unpaywall api is not needed for now.
        pass
