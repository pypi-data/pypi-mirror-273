from kabaret import flow
from kabaret.flow.object import _Manager
from libreflow.baseflow.asset import AssetFamilyCollection
from libreflow.flows.default.flow.asset import AssetType, Assets


def assets_families_map(parent):
    if isinstance(parent, AssetType):
        if parent.name() == 'templates':
            r = flow.Child(AssetFamilyCollection).injectable().ui(
                expanded=True, hidden=True, default_height=600
            )
        else:
            r = flow.Child(AssetFamilyCollection).injectable().ui(
                expanded=True, show_filter=True, default_height=600
            )
        r.name = 'asset_families'
        return r


def assets_map(parent):
    if isinstance(parent, AssetType):
        if parent.name() == 'templates':
            r = flow.Child(Assets).ui(
                expanded=True, show_filter=True, default_height=600
            )
        else:
            r = flow.Child(Assets).ui(
                expanded=True, hidden=True, default_height=600
            )
        r.name = 'assets'
        return r


def install_extensions(session):
    return {
        "ui": [
            assets_families_map,
            assets_map
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']
