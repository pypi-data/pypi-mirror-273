from nodestream.pipeline import Extractor
from google.cloud import asset_v1


class GcpPolicyExtractor(Extractor):
    def __init__(self, project_id: str):
        self.project_id = project_id

    async def extract_records(self):
        client = asset_v1.AssetServiceClient()

        project_resource = f"projects/{self.project_id}"

        # Initialize request argument(s)
        request = asset_v1.SearchAllIamPoliciesRequest(
            scope = project_resource
        )

        page_result = client.search_all_iam_policies(request=request)

        # Handle the response
        for asset in page_result:
            
            assetName = asset.resource
            policy = asset.policy
            bindings = policy.bindings
            
            for binding in bindings: 
                role = binding.role
                role = role.replace('roles/', '')
                role = role.replace('.', '_')
                role = role.upper()
                
                for member in binding.members:
                    splitMember = member.split(":")
                    if len(splitMember) > 1:
                        memberName = splitMember[1]
                        tag = splitMember[0]
                    else:
                        memberName = member
                    newObj = {"asset_name": assetName, "role": role, "member_name": memberName, "tag": tag}
                    yield newObj