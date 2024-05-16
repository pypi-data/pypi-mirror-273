import os
import subprocess
import kabaret.app.resources as resources
from kabaret import flow
from kabaret.flow_contextual_dict import get_contextual_dict
from libreflow.baseflow.users import PresetSessionValue
from libreflow.baseflow.file import RenderBlenderPlayblast
from libreflow.flows.default.flow.file import TrackedFile
from libreflow.utils.b3d import wrap_python_expr
from libreflow.resources.icons import gui as _

from . import _version
__version__ = _version.get_versions()['version']


class PlayblastQuality(flow.values.ChoiceValue):

    CHOICES = ['Viewport', 'Final']


class ANPORenderBlenderPlayblast(RenderBlenderPlayblast):

    quality = flow.Param('Viewport', PlayblastQuality)
    # resolution_percentage = flow.Param('100', ResolutionChoiceValue).ui(
    #     label='Resolution scale (%)'
    # )

    _files = flow.Parent(2)
    _task = flow.Parent(3)

    with flow.group('Advanced'):
        use_simplify = flow.SessionParam(False, PresetSessionValue).ui(
            tooltip="Use low-definition rigs",
            editor='bool',
            hidden=True
            )

    # with flow.group('Advanced'):
    #     reduce_textures = flow.SessionParam(False, PresetSessionValue).ui(
    #         tooltip="Reduce texture sizes before render, to reduce memory footprint",
    #         editor='bool',
    #     )
    #     target_texture_width = flow.SessionParam(4096, PresetSessionValue).ui(
    #         tooltip="Size to reduce textures to",
    #         editor='int',
    #     )

    def __init__(self, parent, name):
        super(ANPORenderBlenderPlayblast, self).__init__(parent, name)
        self.file_settings = get_contextual_dict(
            self._file, "settings", ["sequence", "shot"]
        )

    def get_run_label(self):
        return 'ANPO Render playblast {seq} {shot}'.format(
            seq=self.file_settings.get("sequence", "undefined"),
            shot=self.file_settings.get("shot", "undefined")
        )
   
    def check_default_values(self):
        self.revision_name.revert_to_default()
        # self.resolution_percentage.apply_preset()
        # self.reduce_textures.apply_preset()
        # self.target_texture_width.apply_preset()
    
    def update_presets(self):
        pass
        # self.resolution_percentage.update_preset()
        # self.reduce_textures.update_preset()
        # self.target_texture_width.update_preset()

    def extra_argv(self):
        project_name = self.root().project().name()
        revision = self._file.get_revision(self.revision_name.get())
        do_render = self.quality.get() == 'Final'
        python_expr = """import bpy
bpy.ops.lfs.playblast(do_render=%s, filepath='%s', studio='%s', project='%s', sequence='%s', scene='%s', quality='%s', version='%s')""" % (
            str(do_render),
            self.output_path,
            self.root().project().get_current_site().name(),
            project_name,
            self.file_settings.get("sequence", "undefined"),
            self.file_settings.get("shot", "undefined"),
            'PREVIEW' if self.quality.get() == 'Viewport' else 'FINAL',
            self.revision_name.get(),
        )

        if not do_render:
            python_expr += "\nbpy.ops.wm.quit_blender()"
        
        args = [
            revision.get_path(),
            "--addons",
            "mark_sequence",
            "--python-expr",
            wrap_python_expr(python_expr),
        ]

        if do_render:
            args.insert(0, '-b')
        
        return args


def render_blender_playblast(parent):
    if type(parent) is TrackedFile and parent.name().endswith('blend'):
        r = flow.Child(ANPORenderBlenderPlayblast).ui(label='Render playblast')
        r.name = 'render_blender_playblast'
        r.index = 29
        return r


def install_extensions(session): 
    return {
        "playblast": [
            render_blender_playblast,
        ],
    }
