from etiket_client.python_api.dataset_model.dataset import dataset_model
from etiket_client.python_api.dataset import dataset_read_raw, dataset_create_raw, DatasetCreate
from etiket_client.python_api.scopes import get_scopes
from etiket_client.python_api.dataset_model.files import FileStatusLocal

from etiket_client.settings.user_settings import user_settings

from qdrive.dataset.file_manager import file_manager
from qdrive.dataset.files.file_mgr_single import file_mgr_single

import uuid, datetime, typing


class dataset(dataset_model):
    def __init__(self, ds_uuid : 'uuid.UUID | str'):
        l_ds, r_ds = dataset_read_raw(ds_uuid)
        super().__init__(l_ds, r_ds, user_settings.verbose)
        self.__files = file_manager(self, self.files)
        
    @classmethod
    def create(cls, name, description = None, scope_name = None):
        if scope_name is None:
            try:
                scope_uuid=uuid.UUID(user_settings.current_scope)
            except Exception as exc:
                raise ValueError("No scope provided and no default scope set. Please provide a scope.") from exc
        else:
            scope_uuid = None
            scopes = get_scopes()
            for scope in scopes:
                if scope.name == scope_name:
                    scope_uuid = scope.uuid
        
            if scope_uuid == None:
                raise ValueError(f"Scope '{scope_name}' does not exist ): .")
        
        datasetCreate = DatasetCreate(uuid=uuid.uuid4(), collected=datetime.datetime.now(),
                                      name=name, creator=user_settings.user_name,
                                      description=description, keywords=[],
                                      ranking= 0, synchronized=False,
                                      scope_uuid=scope_uuid)
        l_ds = dataset_create_raw(datasetCreate)
        ds = cls.__new__(cls)
        super(type(ds), ds).__init__(l_ds, None, user_settings.verbose)
        ds.__files = file_manager(ds, ds.files)
        return ds
    
    def __iter__(self):
        return iter(self.__files)
        
    def __getitem__(self, item) -> typing.Type[file_mgr_single]:
        return self.__files[item]
    
    def __setitem__(self, item, value):
        self.__files[item] = value
    
    def add_new_file(self,name, destination, file_type, generator, status = FileStatusLocal.complete):
        self.__files._add_new_file(name, destination, file_type, generator, status)
    
    
