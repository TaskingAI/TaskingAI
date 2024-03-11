
interface ApiErrorResponse {
  response: {
    data: {
      error: {
        message: string;
      };
    };
  };
}
interface MenuClickEvent {
  key: string;
}
interface ProjectType {
  name: string;
  description: string;
  project_id: string;
}
interface editUserProfileType {
  open: boolean;
  onOk: (input: string, content: string) => void;
  onCancel: () => void;
}
interface projectHomeType {
  key: string;
  [key: string]: any;
}
interface RecordType {
  name: string;
  model_id: string;
  model_schema_id: string;
  provider_id: string;
  type: string;
  properties: any;
}
interface projectIdType {
  name: string;
  model_schema_id: string;
  properties: any;
  type: string;
  description: string;
}
interface ChildRefType {
  fetchAiModelsList: () => void;
}
interface formDataType {
  properties: any;
  required: Array<string>;

}
interface promptListType {
  model_schema_id: string;
  provider_id: string;
  type: string;
  name: string;
  properties: any;
  description: string
}
interface ModelProviderType {
  provider_id: string;
  name: string;
  num_model_schemas:number,
  description: string
}
interface modelModalProps {
  handleSetModelOne: (value: any) => void;
  modelType?: string;
  getOptionsList: (object: any, modelType?: string) => void;
  handleSetModelConfirmOne: (value: boolean) => void;
  open: boolean;
  type?: string;
}
interface TableProps {
  columns: any[];
  ifAllowNew?: boolean;
  hangleFilterData?: (value: any) => void;
  ifOnlyId?: boolean;
  defaultSelectedRowKeys?: string[];
  updatePrevButton?: boolean;
  ifHideFooter?: boolean;
  dataSource?: any[];
  loading?: boolean;
  mode?: string;
  ifSelect?: boolean;
  onChildEvent?: (event: any) => void;
  id?: string;
  hasMore?: boolean;
  onOpenDrawer?: (value: any) => void;
  name?: string;
  handleRecordsSelected?: (selectedRowKeys: string[], selectedRows: RecordType[]) => void;
}
interface deleteProjectType {
  title: string;
  projectName: string;
  open: boolean;
  onDeleteConfirm: () => void;
  onDeleteCancel: () => void;
  describe: string
}
interface ModalFooterEndProps {
  onCancel: () => void;
  handleOk: () => void;
}
interface CreateAssistantProps {}
export type { MenuClickEvent,CreateAssistantProps, ModalFooterEndProps, deleteProjectType, modelModalProps, TableProps, promptListType, ModelProviderType, ProjectType, editUserProfileType, projectHomeType, RecordType, projectIdType, ChildRefType, formDataType }
export default ApiErrorResponse