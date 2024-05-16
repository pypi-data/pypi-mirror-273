import os
import re
import glob
import time
from kabaret import flow
from kabaret.app import resources
from libreflow.baseflow.file import GenericRunAction
from libreflow.baseflow.task import Task
from .build_utils import wrap_python_expr

from . import _version
__version__ = _version.get_versions()['version']


class AssetStatus(flow.values.ChoiceValue):

    CHOICES = ["NotAvailable", "Downloadable", "Available"]


class LayoutDependency(flow.Object):

    _parent = flow.Parent()
    _shot = flow.Parent(3)
    
    asset_type = flow.Computed(store_value=False)
    asset_family = flow.Computed(store_value=False)
    asset_code = flow.Computed(store_value=False)
    asset_number = flow.Computed(store_value=False)
    asset_path = flow.Computed(store_value=False)
    asset_oid = flow.Computed(store_value=False)
    asset_file_oid = flow.Computed(store_value=False)
    asset_revision_oid = flow.Computed(store_value=False)
    available = flow.Computed(store_value=False)

    def compute_child_value(self, child_value):
        asset_data = self._parent.asset_data(self.name())

        if child_value is self.asset_type:
            child_value.set(asset_data['asset_type'])
        elif child_value is self.asset_family:
            child_value.set(asset_data['asset_family'])
        elif child_value is self.asset_number and 'asset_number' in asset_data:
            child_value.set(asset_data['asset_number'])
        elif child_value is self.asset_oid:
            if self.name() == "animatic":
                oid = self._shot.oid()
            else:
                asset_type = self.asset_type.get()
                asset = None
                asset_family = self.asset_family.get()
                asset_name = self.name()
                oid = self.root().project().oid() + f"/asset_types/{asset_type}/asset_families/{asset_family}/assets/{asset_name}"
                if not self.root().session().cmds.Flow.exists(oid): # ensure asset exists
                    self.root().session().log_warning(f'Scene Builder - undefined asset {oid}')
                    oid = None
            child_value.set(oid)
        elif child_value is self.asset_file_oid:
            asset_type = self.asset_type.get()
            asset_oid = self.asset_oid.get()

            if asset_oid is not None:
                asset = self.root().get_object(asset_oid)
            else:
                child_value.set(None)
                return

            file_name = self._parent.asset_type_file_name(asset_type)
            files = self._parent.files_from_asset_type(asset, asset_type)
            
            if files is None or not files.has_mapped_name(file_name):
                child_value.set(None)
            else:
                child_value.set(files[file_name].oid())
        elif child_value is self.asset_code:
            oid = self.asset_oid.get()
            if oid is None:
                child_value.set(None)
            else:
                asset = self.root().get_object(oid)
                child_value.set(asset.code.get())
        elif child_value is self.asset_revision_oid:
            asset_file_oid = self.asset_file_oid.get()
            
            if asset_file_oid:
                file = self.root().get_object(asset_file_oid)
                rev = file.get_head_revision()

                if rev and rev.exists():
                    child_value.set(rev.oid())
                else:
                    child_value.set(None)
            else:
                child_value.set(None)
        elif child_value is self.asset_path:
            asset_revision_oid = self.asset_revision_oid.get()
            asset_type = self.asset_type.get()

            if not asset_revision_oid:
                child_value.set(None)
            else:
                rev = self.root().get_object(asset_revision_oid)
                if not rev.exists():
                    child_value.set(None)
                else:
                    child_value.set(rev.get_path())
        elif child_value is self.available:
            asset_path = self.asset_path.get()

            if self.asset_revision_oid.get():
                child_value.set("Available")
            elif self.asset_file_oid.get():
                child_value.set("Downloadable")
            else:
                child_value.set("NotAvailable")


class LayoutDependencies(flow.DynamicMap):
    _task = flow.Parent(2)
    _shot = flow.Parent(4)
    _sequence = flow.Parent(6)
    _updated = flow.BoolParam(False)

    def __init__(self, parent, name):
        super(LayoutDependencies, self).__init__(parent, name)
        self._assets_data_time = time.time()
        self._assets_data = None

    def mapped_names(self, page_num=0, page_size=None):
        if not self._assets_data or time.time() - self._assets_data_time > 30.0:
            self._assets_data = self._get_assets_data()
            self._assets_data_time = time.time()

        return list(self._assets_data.keys())

    def _get_assets_data(self):
        kitsu_api = self.root().project().kitsu_api()
        kitsu_casting = kitsu_api.get_shot_casting(self._shot.name(), self._sequence.name())
        casting = dict()
        
        # Kitsu assets
        for asset in kitsu_casting:
            asset_name = asset['asset_name']
            asset_type = asset['asset_type_name']
            asset_family = kitsu_api.get_asset_data(asset_name)['data'].get('category', asset_type.lower())

            casting[asset_name.replace('-', '_')] = dict(
                asset_type=asset_type.lower(),
                asset_family=asset_family.lower(),
                asset_number=asset['nb_occurences']
            )

        # Animatic
        casting['animatic'] = dict(
            asset_type='animatic',
            asset_family='',
        )
        
        return casting

    def asset_data(self, asset_name):
        return self._assets_data[asset_name]

    @classmethod
    def mapped_type(cls):
        return LayoutDependency

    def columns(self):
        return ["Name", "Type", "Family", "Revision"]
    
    def asset_type_file_name(self, asset_type):
        return {
            "sets": "layers",
            "animals": "rigging_blend",
            "characters": "rigging_blend",
            "props": "rigging_blend",
            "animatic": "animatic_mov",
        }[asset_type]
    
    def files_from_asset_type(self, asset, asset_type):
        if asset_type == 'sets' and asset.tasks.has_mapped_name('design'):
            return asset.tasks['design'].files
        elif asset_type == 'animatic':
            return self._task.files
        elif asset.tasks.has_mapped_name('rigging'):
            return asset.tasks['rigging'].files
        else:
            return None
    
    def _fill_row_cells(self, row, item):
        row["Name"] = item.name()
        row["Type"] = item.asset_type.get()
        row["Family"] = item.asset_family.get()
        
        rev_oid = item.asset_revision_oid.get()
        rev_name = rev_oid.split("/")[-1] if rev_oid else ""
        row["Revision"] = rev_name
    
    def _fill_row_style(self, style, item, row):
        icon_by_status = {
            "NotAvailable": ("icons.libreflow", "cross-mark-on-a-black-circle-background-colored"),
            "Downloadable": ("icons.libreflow", "exclamation-sign-colored"),
            "Available": ("icons.libreflow", "checked-symbol-colored"),
        }
        style["icon"] = icon_by_status[item.available.get()]


class BuildBlenderScene(GenericRunAction):
    ICON = ('icons.libreflow', 'blender')

    _task = flow.Parent()
    _shot = flow.Parent(3)
    _sequence = flow.Parent(5)

    dependencies = flow.Child(LayoutDependencies).ui(expanded=True)

    def runner_name_and_tags(self):
        return 'Blender', []
    
    def get_run_label(self):
        return "Build scene"

    def get_buttons(self):
        # Make build action behave as base RunAction by default
        return RunAction.get_buttons(self)

    def needs_dialog(self):
        return True

    def extra_env(self):
        return {
            "ROOT_PATH": self.root().project().get_root()
        }
    
    def target_file_extension(self):
        return 'blend'

    def get_template_path(self, filename):
        file_mapped_name = filename.replace('.', '_')
        template_path = resources.get("file_templates", "template.blend")
        mng = self.root().project().get_task_manager()
        if not mng.default_tasks.has_mapped_name(self._task.name()): # check default task
            print(f'Scene Builder - no default task {self._task.name()} -> use default template')
            return template_path

        default_task = mng.default_tasks[self._task.name()]
        if not default_task.files.has_mapped_name(file_mapped_name): # check default file
            print(f'Scene Builder - default task {self._task.name()} has no default file {filename} -> use default template')
            return template_path

        default_file = default_task.files[file_mapped_name]
        template_oid = default_file.template_file.get()
        if template_oid is None or not self.root().session().cmds.Flow.exists(template_oid): # check file template
            print(f'Scene Builder -  template of {self._task.name()}/{filename} is undefined -> use default template')
            return template_path

        template = self.root().get_object(template_oid)
        if template is None: # check file template
            print(f'Scene Builder - template of {self._task.name()}/{filename} is undefined -> use default template')
            return template_path

        rev_name = default_file.template_file_revision.get()
        if rev_name == 'Latest': # check template revision
            rev = template.get_head_revision()
        else:
            rev = template.get_revision(rev_name)
        if rev is None or rev.get_sync_status() != 'Available':
            print(f'Scene Builder - template of {self._task.name()}/{filename} is not available -> use default template')
            return template_path

        rev_path = rev.get_path()
        if not os.path.exists(rev_path):
            print(f'Scene Builder - template of {self._task.name()}/{filename} is not available -> use default template')
            return template_path

        print(f'Scene Builder - custom template found: {rev_path}')
        return rev_path
    
    def _ensure_file(self, name, format, to_edit=False, src_path=None, publish_comment=""):
        files = self._task.files
        file_name = "%s_%s" % (name, format)

        if not files.has_mapped_name(file_name):
            files.create_file.file_name.set(name)
            files.create_file.file_format.set(format)
            files.create_file.run(None)
        
        file = files[file_name]

        if not to_edit and not src_path:
            return None
        
        if to_edit:
            revision = file.create_working_copy(source_path=src_path)
        else:
            revision = file.publish(source_path=src_path, comment=publish_comment)

        return revision.get_path()

    def _blender_cmd(self, operator, **kwargs):
        '''
        Returns Blender scene builder operator command as a string.

        Operator must be one of the following: `setup`, `setup_anim`,
                                               `add_asset`, `add_set`, `add_audio`, `add_board`,
                                               `update_audio", "update_storyboard`,
                                               `export_ae`,
                                               `cleanup`, `save`.
        '''

        blender_operators = {
            "setup": {'operator_command': "bpy.ops.pipeline.scene_builder_setup",
                      'args': "frame_start={frame_start}, frame_end={frame_end}, resolution_x={resolution_x}, resolution_y={resolution_y}, fps={fps}, create_camera=False"},
            "setup_anim": {'operator_command': "bpy.ops.pipeline.scene_builder_setup_animation",
                           'args': 'alembic_filepath="{alembic_filepath}", assets={assets}, do_automate={do_automate}'},

            "add_asset": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_asset',
                          'args': 'filepath="{filepath}", asset_name="{asset_name}", target_collection="{asset_type}"'},
            "add_set": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_set',
                        'args': 'directory="{set_dir}", files={set_dicts}'},
            "add_audio": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_audio',
                          'args': 'filepath="{filepath}"'},
            "add_board": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_storyboard',
                          'args': 'filepath="{filepath}", use_corner={use_corner}'},

            "update_audio": {'operator_command': 'bpy.ops.pipeline.scene_builder_update_audio',
                             'args' :''},
            "update_board": {'operator_command': 'bpy.ops.pipeline.scene_builder_update_storyboard',
                             'args' :'filepath="{filepath}"'},

            "export_ae": {'operator_command': 'bpy.ops.pipeline.scene_builder_export_ae',
                          'args' :'filepath="{filepath}"'},

            "setup_render": {'operator_command': "bpy.ops.pipeline.scene_builder_setup_render",
                             'args': 'kitsu_duration={kitsu_duration}'},

            "cleanup": {'operator_command': 'bpy.ops.pipeline.scene_builder_cleanup',
                               'args': ''},
            "save": {'operator_command': 'bpy.ops.wm.save_mainfile',
                     'args': 'filepath="{filepath}", compress=True'},
        }

        op = blender_operators[operator]
        operator_command = op['operator_command']
        args = op['args'].format(**kwargs)
        command = f"if {operator_command}.poll(): {operator_command}({args})\n"
        return command


class BuildLayoutScene(BuildBlenderScene):

    def get_run_label(self):
        return 'Build layout scene'

    def extra_argv(self):
        # Get scene builder arguments
        frame_start = 101
        frame_end = 101 + self._shot_data.get("nb_frames", 0) - 1
        resolution_x = 2048
        resolution_y = 858
        fps = 24

        assets = self._shot_data.get("assets_data", [])
        sets = self._shot_data.get("sets_data", [])
        animatic_path = self._shot_data.get("animatic_path", None)
        layout_path = self._shot_data["layout_path"] # Mandatory
        template_path = self.get_template_path("layout.blend")

        # Build Blender Python expression
        python_expr = "import bpy\n"
        python_expr += self._blender_cmd("setup", frame_start=frame_start, frame_end=frame_end, resolution_x=resolution_x, resolution_y=resolution_y, fps=fps)
        python_expr += self._blender_cmd("save", filepath=layout_path)
        
        for name, path, asset_type, asset_number in assets:
            for i in range(asset_number):
                python_expr += self._blender_cmd("add_asset", filepath=path, asset_name=name, asset_type=asset_type)
        for set_dir, set_dicts in sets:
            python_expr += self._blender_cmd("add_set", set_dir=set_dir, set_dicts=set_dicts)
        if animatic_path:
            python_expr += self._blender_cmd("add_audio", filepath=animatic_path)

        # python_expr += self._blender_cmd("cleanup")
        python_expr += self._blender_cmd("save", filepath=layout_path)

        return [
            "-b", template_path,
            "--addons", "io_import_images_as_planes,camera_plane,lfs_scene_builder,add_camera_rigs",
            "--python-expr", wrap_python_expr(python_expr)
        ]

    def get_buttons(self):
        msg = "<h2>Build layout shot</h2>"

        for dep in self.dependencies.mapped_items():
            if dep.available.get() in ["Downloadable", "NotAvailable"]:
                msg += (
                    "<h3><font color=#D66700>"
                    "Some dependencies are still missing, either because they do not already exists or need to be downloaded on your site.\n"
                    "You can build the scene anyway, but you will have to manually update it when missing dependencies will be available."
                    "</font></h3>"
                )
                break
        
        self.message.set(msg)

        return ["Build and edit", "Build and publish", "Cancel"]
    
    def run(self, button):
        if button == "Cancel":
            return
        
        if button == "Refresh":
            self.dependencies.touch()
            return self.get_result(refresh=True, close=False)

        shot_name = self._shot.name()
        sequence_name = self._sequence.name()

        # Get shot data
        kitsu_api = self.root().project().kitsu_api()
        shot_data = kitsu_api.get_shot_data(shot_name, sequence_name)

        # Store dependencies file paths for Blender script building
        self._shot_data = {}
        self._shot_data["nb_frames"] = shot_data["nb_frames"]
        self._shot_data["assets_data"] = []
        self._shot_data["sets_data"] = []

        for dep in self.dependencies.mapped_items():
            if dep.available.get() != "Available":
                continue

            asset_type = dep.asset_type.get()
            asset_number = dep.asset_number.get()
            path = dep.asset_path.get().replace("\\", "/")
            path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", path) # check drive name
            if asset_type == "sets":
                set_path = re.sub(r"^\\\\\\\\([^/]+)\\\\", r"\\\\\1\\", path) # revert set path to find images
                set_names = list(map(os.path.basename, glob.glob("%s/*.png" % set_path)))
                self._shot_data["sets_data"].append(
                    (path, [{"name": name} for name in set_names])
                )
            elif asset_type == "animatic":
                self._shot_data["animatic_path"] = path
            else: # characters/props/animals
                self._shot_data["assets_data"].append((dep.asset_code.get(), path, asset_type, asset_number))

        # Configure layout file
        layout_path = self._ensure_file(
            name='layout',
            format='blend',
            to_edit=(button == 'Build and edit'),
            src_path=resources.get("file_templates", "template.blend"),
            publish_comment="Created with scene builder"
        )

        self._task.touch()

        # Store layout output path
        layout_path = layout_path.replace("\\", "/")
        layout_path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", layout_path) # check drive name
        self._shot_data["layout_path"] = layout_path

        # Build
        super(BuildLayoutScene, self).run(button)


def build_layout_scene_action(parent):
    if isinstance(parent, Task) and parent.name() == "layout":
        r = flow.Child(BuildLayoutScene)
        r.name = 'build_layout_scene'
        r.index = None
        return r

def install_extensions(session): 
    return {
        "scene_builder": [
            build_layout_scene_action
        ]
    }
