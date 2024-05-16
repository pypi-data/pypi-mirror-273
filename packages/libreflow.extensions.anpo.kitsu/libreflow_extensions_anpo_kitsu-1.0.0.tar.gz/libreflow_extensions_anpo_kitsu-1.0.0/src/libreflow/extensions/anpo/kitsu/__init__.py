import re
from kabaret import flow
from libreflow.baseflow.asset import AssetCollection, AssetFamily, AssetType, AssetTypeCollection


from . import _version
__version__ = _version.get_versions()['version']

class CreateKitsuFamilyAssets(flow.Action):

    ICON = ('icons.libreflow', 'kitsu')

    skip_existing = flow.SessionParam(False).ui(editor='bool')
    update_tasks = flow.SessionParam(True).ui(editor='bool')
    update_default_files = flow.SessionParam(True).ui(editor='bool')

    _type = flow.Parent(3)
    _family = flow.Parent()

    def get_buttons(self):
        return ['Create assets', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        skip_existing = self.skip_existing.get()
        update_tasks = self.update_tasks.get()
        update_default_files = self.update_default_files.get()
        type_name = self._type.code.get()
        if not type_name:
            type_name = self._type.name()
            print(f"[KITSU] Asset Type {type_name} - code undefined -> name will be used")

        assets_data = self.root().project().kitsu_api().get_assets_data(type_name)
        if assets_data is None:
            print(f"[KITSU] Warning - Asset type {type_name} not found on Kitsu")
            return

        type_name = self._type.name()
        family_name = self._family.name()
        # Filter assets by family
        assets_data = [ad for ad in assets_data \
            if ad['data'].get('category', type_name) == family_name]

        for data in assets_data:
            code = data['name']
            name = code.replace('-','_')
            if self._family.assets.has_mapped_name(name):
                if skip_existing:
                    continue

                a = self._family.assets[name]
            else:
                print(f'[KITSU] Asset Type {type_name} - Create asset {name.ljust(20)} (code: {code})')
                a = self._family.assets.add(name)
                a.code.set(code)
            if not update_tasks:
                continue
            
            print(f'[KITSU] Asset {name} - update tasks')
            a.ensure_tasks()
            if not update_default_files:
                continue

            for t in a.tasks.mapped_items():
                print(f'[KITSU] Asset {name} - {t.name()}: update files')
                t.create_dft_files.files.update()
                t.create_dft_files.run(None)
        
        self._family.assets.touch()

class CreateKitsuAssetFamilies(flow.Action):

    ICON = ('icons.libreflow', 'kitsu')

    skip_existing = flow.SessionParam(False).ui(editor='bool')
    update_assets = flow.SessionParam(False).ui(editor='bool')
    update_tasks = flow.SessionParam(True).ui(editor='bool')
    update_default_files = flow.SessionParam(True).ui(editor='bool')

    _type = flow.Parent()

    def get_buttons(self):
        return ['Create families', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return

        skip_existing = self.skip_existing.get()
        update_assets = self.update_assets.get()
        update_tasks = self.update_tasks.get()
        update_default_files = self.update_default_files.get()
        type_name = self._type.code.get()
        if not type_name:
            type_name = self._type.name()
            print(f"[KITSU] Asset Type {type_name} - code undefined -> name will be used")

        assets_data = self.root().project().kitsu_api().get_assets_data(type_name)
        if assets_data is None:
            print(f"[KITSU] Warning - Asset type {type_name} not found on Kitsu")
            return

        family_kitsu_names = [ad['data'].get('category', self._type.name()) \
            for ad in assets_data]
        family_kitsu_names = sorted(set(family_kitsu_names))
        family_names = [re.sub(r'[\.-]', '_', name) \
            for name in family_kitsu_names]

        for i, name in enumerate(family_names):
            kitsu_name = family_kitsu_names[i]
            if self._type.asset_families.has_mapped_name(name):
                if skip_existing:
                    continue

                af = self._type.asset_families[name]
            else:
                print(f'[KITSU] Asset Type {self._type.name()} - Create family {name.ljust(20)} (code: {kitsu_name})')
                af = self._type.asset_families.add(name)
                af.code.set(kitsu_name)

            if not update_assets:
                continue

            print(f'[KITSU] Asset Family - {self._type.name()}/{name}: update assets')
            af.create_assets.skip_existing.set(skip_existing)
            af.create_assets.update_tasks.set(update_tasks)
            af.create_assets.update_default_files.set(update_default_files)
            af.create_assets.run('Create assets')

class CreateKitsuAssetTypes(flow.Action):

    ICON = ('icons.libreflow', 'kitsu')

    skip_existing = flow.SessionParam(False).ui(editor='bool')
    update_asset_families = flow.SessionParam(False).ui(editor='bool')
    update_assets = flow.SessionParam(False).ui(editor='bool')
    update_tasks = flow.SessionParam(True).ui(editor='bool')
    update_default_files = flow.SessionParam(True).ui(editor='bool')

    _asset_types = flow.Parent()

    def get_buttons(self):
        return ['Create asset types', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        asset_types_data = self.root().project().kitsu_api().get_asset_types_data()
        update_assets = self.update_assets.get()
        update_asset_families = self.update_asset_families.get()
        update_tasks = self.update_tasks.get()
        update_default_files = self.update_default_files.get()
        skip_existing = self.skip_existing.get()

        for data in asset_types_data:
            kitsu_name = data['name']
            type_name = kitsu_name.lower() # special case: asset type names are in lowercase right now
            type_name = type_name.replace('-','_')

            if type_name == 'x':
                continue

            # Ensure asset type
            if not self._asset_types.has_mapped_name(type_name):
                print(f'[KITSU] Asset Type - Create {type_name} (code: {kitsu_name})')
                at = self._asset_types.add(type_name)
                at.code.set(kitsu_name)
            elif not skip_existing:
                at = self._asset_types[type_name]
            else:
                continue
            
            if not update_asset_families:
                continue

            print(f'[KITSU] Asset Type - {type_name}: update families')
            at.create_asset_families.skip_existing.set(skip_existing)
            at.create_asset_families.update_assets.set(update_assets)
            at.create_asset_families.update_tasks.set(update_tasks)
            at.create_asset_families.update_default_files.set(update_default_files)
            at.create_asset_families.run('Create families')
        
        self._asset_types.touch()


def create_kitsu_asset_actions(parent):
    if isinstance(parent, AssetType):
        r = flow.Child(CreateKitsuAssetFamilies)
        r.name = "create_asset_families"
        r.index = None
        return r
    elif isinstance(parent, AssetFamily):
        r = flow.Child(CreateKitsuFamilyAssets)
        r.name = "create_assets"
        r.index = None
        return r
    elif isinstance(parent, AssetTypeCollection):
        r = flow.Child(CreateKitsuAssetTypes)
        r.name = "create_asset_types" # override base action
        r.index = None
        return r
    elif isinstance(parent, AssetCollection):
        # Dummy relation to disable base action
        r = flow.Child(flow.SessionObject)
        r.name = "create_assets"
        r.index = None
        r.ui(hidden=True)
        return r

def install_extensions(session):
    return {
        "kitsu.sync": [
            create_kitsu_asset_actions
        ]
    }
