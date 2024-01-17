
interface CustomErrorResponse {
    data: {
        error: {
            message: string;
        };
    };
}
class CustomError extends Error {
    response: CustomErrorResponse;

    constructor(message: string, response: CustomErrorResponse) {
        super(message);
        this.name = 'CustomError';
        this.response = response;
    }
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
  hangleFilterData?: () => void;
  ifOnlyId?: boolean;
  defaultSelectedRowKeys?: string[];
  updatePrevButton?: boolean;
  ifHideFooter?: boolean;
  dataSource?: any[]; 
  mode?: string;
  ifSelect?: boolean;
  onChildEvent?: (event: Event) => void;
  id?: string;
  hasMore?: boolean;
  onOpenDrawer?: () => void;
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
export type {formDataType,promptListType, projectIdType,ModelProviderType,projectHomeType,RecordType,ChildRefType,TableProps,modelModalProps}
export default CustomError