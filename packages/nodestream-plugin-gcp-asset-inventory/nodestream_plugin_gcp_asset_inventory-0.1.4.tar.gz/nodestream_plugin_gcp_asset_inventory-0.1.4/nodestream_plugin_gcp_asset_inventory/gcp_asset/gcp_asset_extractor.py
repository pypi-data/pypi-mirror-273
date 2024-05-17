from nodestream.pipeline import Extractor
from google.cloud import asset_v1


class GcpAssetExtractor(Extractor):
    def __init__(self, project_id: str):
        self.project_id = project_id

    async def extract_records(self):
        client = asset_v1.AssetServiceClient()

        project_resource = f"projects/{self.project_id}"

        # Initialize request argument(s)
        request = asset_v1.ListAssetsRequest(
            parent=project_resource,
        )

        # Make the request
        page_result = client.list_assets(request=request)

        # Handle the response
        for asset in page_result:
            newObj = {"name": asset.name, "asset_type": asset.asset_type}
            yield newObj
