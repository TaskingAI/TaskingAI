

interface projectHomeType {
    key: string;
    [key: string]: any;
}
interface ApiErrorResponse {
    response: {
      data: {
        error: {
          message: string;
        };
      };
    };
  }
interface RecordType {
    name: string;
    model_id: string;
    model_schema_id: string;
    provider_id: string;
}
interface projectIdType {
    name: string;
    model_schema_id: string;
    properties: any;
    type: string;
}
interface ChildRefType {
    fetchAiModelsList: () => void; 
  }
interface TableProps {
    columns: any[];
  ifAllowNew?: boolean;
  hangleFilterData?: (value) => void;
  ifOnlyId?: boolean;
  defaultSelectedRowKeys?: string[];
  updatePrevButton?: boolean;
  ifHideFooter?: boolean;
  dataSource?: any[]; 
  mode?: string;
  ifSelect?: boolean;
  onChildEvent?: (event: any) => void;
  id?: string;
  hasMore?: boolean;
  onOpenDrawer?: (value) => void;
  name?: string;
  handleRecordsSelected?: (selectedRowKeys: string[], selectedRows: RecordType[]) => void;
}
interface modelModalProps {
    handleSetModelOne: (value: any) => void;
    modelType?: string;
    getOptionsList: (object:object,modelType:string) => void;
    handleSetModelConfirmOne: (value: boolean) => void;
    open: boolean;
}
interface ModelProviderType{
    provider_id: string;
  name: string;
}
interface promptListType {
    model_schema_id: string;
    provider_id:string;
    type: string;
    name: string;
    properties: any;
}
interface formDataType{
    properties:any;
    required:Array<string>;

}
interface settingModalProps {
    contains?:any,
    style?:{
        display:string
    },
}
interface contentRefType {
    scrollTop?:any;
    scrollHeight?:any;
    scrollTo?:any
}
export default ApiErrorResponse;
export type {contentRefType,formDataType,settingModalProps,promptListType, projectIdType,ModelProviderType,projectHomeType,RecordType,ChildRefType,TableProps,modelModalProps}