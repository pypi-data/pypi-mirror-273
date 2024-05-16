from kabaret import flow
from kabaret.flow_contextual_dict import get_contextual_dict
from libreflow.baseflow.file import GenericRunAction
from libreflow.flows.default.flow.file import TrackedFile
from libreflow.flows.default.flow.shot import Shot, Sequence

from . import _version
__version__ = _version.get_versions()['version']


class PlaySequenceActionFromFile(flow.Action):

    ICON = ('icons.gui', 'chevron-sign-to-right')

    _file = flow.Parent()
    _sequence = flow.Parent(7)

    @classmethod
    def supported_extensions(cls):
        return ["mp4","mov", "mxf"]

    def allow_context(self, context):
        return (
            context 
            and self._file.format.get() in self.supported_extensions()
        )
    
    def needs_dialog(self):
        self._sequence.play_sequence.priority_files.revert_to_default()
        if self._sequence.play_sequence.priority_files.get() is None:
            self._sequence.play_sequence.status == 'Not Configured'
            return True

        self._sequence.play_sequence.status = self._sequence.play_sequence.get_files()

        if self._sequence.play_sequence.status == 'Nothing':
            return True
        
        return False

    def get_buttons(self):
        if self._sequence.play_sequence.status == 'Not Configured':
            self.message.set('<h2>Action is not configured.</h2>\nSet priority files in Action Value Store.')
        elif self._sequence.play_sequence.status == 'Nothing':
            self.message.set('<h2>No files has been found.</h2>')

        return ['Close']
    
    def run(self, button):
        if button == 'Close' or self._sequence.play_sequence.status == 'Nothing':
            return None
        
        return self.get_result(goto_target=self._sequence.play_sequence.run('Open'))


class PlaySequenceSessionValue(flow.values.SessionValue):

    _action = flow.Parent()
   
    def revert_to_default(self):
        value = self.root().project().get_action_value_store().get_action_value(
            self._action.name(),
            self.name(),
        )
        if value is None:
            default_values = {}
            default_values[self.name()] = self.get()

            self.root().project().get_action_value_store().ensure_default_values(
                self._action.name(),
                default_values
            )
            return self.revert_to_default()

        self.set(value)


class MRVPlaySequenceAction(GenericRunAction):

    ICON = ('icons.gui', 'chevron-sign-to-right')

    _sequence = flow.Parent()

    # Exemple value : ['compositing/compositing_movie.mov', 'compositing/animatic.mov']
    priority_files   = flow.SessionParam([], PlaySequenceSessionValue).ui(hidden=True)
   
    def __init__(self, parent, name):
        super(MRVPlaySequenceAction, self).__init__(parent, name)
        self._paths = []
        self.status = None

    def needs_dialog(self):
        self.priority_files.revert_to_default()
        if self.priority_files.get() is None:
            self.status == 'Not Configured'
            return True

        self.status = self.get_files()

        if self.status == 'Nothing':
            return True
        
        return False

    def get_buttons(self):
        if self.status == 'Not Configured':
            self.message.set('<h2>Action is not configured.</h2>\nSet priority files in Action Value Store.')
        elif self.status == 'Nothing':
            self.message.set('<h2>No files has been found.</h2>')

        return ['Close']
    
    def runner_name_and_tags(self):
        return 'Mrviewer', []
    
    def get_version(self, button):
        return None
          
    def extra_argv(self):
        return self._paths + ['-e']
    
    def run(self, button):
        if button == 'Close' or self.status == 'Nothing':
            return
      
        super(MRVPlaySequenceAction, self).run(button)
        return self.get_result(close=True)
    
    def get_files(self):
        self._paths = []
       
        for shot in self._sequence.shots.mapped_items():
            path = None
            
            for priority_file in self.priority_files.get():
                task, file_name = priority_file.rsplit('/', 1)
                name, ext = file_name.rsplit('.', 1)

                if shot.tasks[task].files.has_file(name, ext):
                    revision = shot.tasks[task].files[f'{name}_{ext}'].get_head_revision(sync_status='Available')

                    if revision is not None:
                        path = revision.get_path()
                        break
            
            if path is None:
                continue
            
            self._paths += [path]
        
        if self._paths == []:
            return 'Nothing'


class MRVPlaySequenceActionFromShot(MRVPlaySequenceAction):

    _sequence = flow.Parent(3)


def play_sequence(parent):
    if type(parent) is Sequence:
        r = flow.Child(MRVPlaySequenceAction).ui(label='Play Sequence', hidden=True)
        r.name = 'play_sequence'
        r.index = 4
        return r

    if type(parent) is Shot:
        r = flow.Child(MRVPlaySequenceActionFromShot).ui(label='Play Sequence', hidden=True)
        r.name = 'play_sequence'
        r.index = 3
        return r

    if type(parent) is TrackedFile and parent.name().endswith(('mov' or 'mp4' or 'mxf')):
        r = flow.Child(PlaySequenceActionFromFile).ui(label='Play Sequence')
        r.name = 'play_sequence'
        r.index = 34
        return r


def install_extensions(session): 
    return {
        "playback": [
            play_sequence,
        ],
    }
