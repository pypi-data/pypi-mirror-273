from nodestream.project import Project, ProjectPlugin


class GcpAssetInventoryPlugin(ProjectPlugin):
    def activate(self, project: Project) -> None:
        project.add_plugin_scope_from_pipeline_resources(
            name="gcp_asset_inventory", package="nodestream_plugin_gcp_asset_inventory"
        )