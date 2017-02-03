from invisibleroads_posts.models import DummyBase, FolderMixin
from os.path import join


class Tool(FolderMixin, DummyBase):

    id = 1

    @classmethod
    def get_from(Class, request, record_id=None):
        return Class(id=record_id)


class Result(FolderMixin, DummyBase):

    tool_id = Tool.id

    @classmethod
    def get_from(Class, request, record_id=None):
        instance = super(Result, Class).get_from(request, record_id)
        instance.tool = Tool(id=instance.tool_id)
        return instance

    def get_source_folder(self, data_folder):
        return join(self.get_folder(data_folder), 'x')

    def get_target_folder(self, data_folder):
        return join(self.get_folder(data_folder), 'y')
