import styles from "./retrieval.module.scss";
import { PlusOutlined, RightOutlined } from "@ant-design/icons";
import {
    getRetrievalList,
    createRetrieval,
    deleteRetrieval,
    updateRetrieval,
} from "../../axios/retrieval.ts";
import { getModelsList } from "../../axios/models.ts";
import RecordPage from "../recordPage/index";
import { useEffect, useState, useRef } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchRetrievalData } from "../../Redux/actions";
import { fetchModelsData } from "../../Redux/actions";
import DeleteIcon from "../../assets/img/deleteIcon.svg?react";
import EditIcon from "../../assets/img/editIcon.svg?react";
import ChunkIcon from "../../assets/img/chunkIcon.svg?react";
import ModalTable from "../modalTable/index";
import ModelModal from "../modelModal/index";
import CommendComponent from "../../contents/index.tsx";
import { ChildRefType } from "../../constant/index.ts";
import ChunkPage from "../chunkPage/index.tsx";
import ModalFooterEnd from "../modalFooterEnd/index";
import { toast } from "react-toastify";
import ApiErrorResponse from "@/constant/index";
import tooltipTitle from "../../contents/tooltipTitle";
import { useNavigate } from "react-router-dom";
import DeleteModal from "../deleteModal/index.tsx";
import RecordIcon from "../../assets/img/recordIcon.svg?react";
import closeIcon from "../../assets/img/x-close.svg";
import { useTranslation } from "react-i18next";

import {
    Space,
    Drawer,
    Input,
    Tooltip,
    Spin,
    Select,
    Modal,
    Button,
} from "antd";
function Retrieval() {
    const { t } = useTranslation();
    const { retrievalLists } = useSelector((state: any) => state.retrieval);
    const dispatch = useDispatch();
    const { modelsTableColumn, collectionTableColumn } = CommendComponent();
    const {
        tooltipEditTitle,
        tooltipDeleteTitle,
        tooltipChunkTitle,
        tooltipRecordTitle,
    } = tooltipTitle();
    const columns = [...collectionTableColumn];
    columns.push({
        title: `${t("projectColumnActions")}`,
        key: "action",
        fixed: "right",
        width: 200,
        render: (_: string, record: object) => (
            <Space size="middle">
                <div
                    className="table-edit-icon"
                    onClick={() => handleRecord(record, "Records")}
                >
                    <Tooltip
                        placement="bottom"
                        color="#fff"
                        arrow={false}
                        overlayClassName="table-tooltip"
                        title={tooltipRecordTitle}
                    >
                        <RecordIcon />
                    </Tooltip>
                </div>
                <div
                    className="table-edit-icon"
                    onClick={() => handleRecord(record, "Chunks")}
                >
                    <Tooltip
                        placement="bottom"
                        color="#fff"
                        arrow={false}
                        overlayClassName="table-tooltip"
                        title={tooltipChunkTitle}
                    >
                        <ChunkIcon />
                    </Tooltip>
                </div>
                <div onClick={() => handleEdit(record)} className="table-edit-icon">
                    <Tooltip
                        placement="bottom"
                        title={tooltipEditTitle}
                        color="#fff"
                        arrow={false}
                        overlayClassName="table-tooltip"
                    >
                        <EditIcon />
                    </Tooltip>
                </div>
                <div onClick={() => handleDelete(record)} className="table-edit-icon">
                    <Tooltip
                        placement="bottom"
                        title={tooltipDeleteTitle}
                        color="#fff"
                        arrow={false}
                        overlayClassName="table-tooltip"
                    >
                        <DeleteIcon />
                    </Tooltip>
                </div>
            </Space>
        ),
    });
    const [promptList, setPromptList] = useState([]);
    const [hasMore, setHasMore] = useState(false);
    const [modelHasMore, setModelHasMore] = useState(false);
    const [OpenDrawer, setOpenDrawer] = useState(false);
    const [loading, setLoading] = useState(false);
    const [limit, setLimit] = useState(20);
    const [updatePrevButton, setUpdatePrevButton] = useState(false);
    const [updateRetrievalPrevButton, setUpdateRetrievalPrevButton] =
        useState(false);
    const [defaultSelectedRowKeys, setDefaultSelectedRowKeys] = useState([]);
    const [modalTableOpen, setModalTableOpen] = useState(false);
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false);
    const [recordOpen, setRecordOpen] = useState(false);
    const [drawerTitle, setDrawerTitle] = useState("Create Collection");
    const [drawerName, setDrawerName] = useState("");
    const [embeddingSize, setEmbeddingSize] = useState(0);
    const [deleteValue, setDeleteValue] = useState("");
    const [recordsSelected, setRecordsSelected] = useState([]);
    const [selectedRows, setSelectedRows] = useState<string[]>([]);
    const [options, setOptions] = useState([]);
    const childRef = useRef<ChildRefType | null>(null);
    const [selectValue, setSelectValue] = useState(1000);
    const [modelOne, setModelOne] = useState(false);
    const [descriptionText, setDescriptionText] = useState("");
    const [editDisabled, setEditDisabled] = useState(false);
    const [collectionId, setCollectionId] = useState("");
    const [collectionRecordId, setCollectionRecordId] = useState("");
    const [recordOrChunk, setRecordOrChunk] = useState("Records");
    const navigate = useNavigate();
    useEffect(() => {
        const params = {
            limit: 20,
        };
        fetchModelsList(params);
    }, []);
    useEffect(() => {
        if (retrievalLists.data.length > 0) {
            const data = retrievalLists.data.map((item: any) => {
                return {
                    ...item,
                    capacity1: item.num_chunks + "/" + item.capacity,
                    key: item.collection_id,
                };
            });
            setPromptList(data);
            setHasMore(retrievalLists.has_more);
        } else {
            setPromptList([]);
        }
    }, [retrievalLists]);
    const handleRecordsSelected = (value: any, selectedRows: Array<any>) => {
        setRecordsSelected(value);
        const tag = selectedRows.map((item) => item.name + "-" + item.model_id);
        if (value.length === 0) {
            setSelectedRows([]);
        } else {
            setSelectedRows(tag);
        }
    };
    const handleModalClose = () => {
        setModalTableOpen(false);
    };
    const fetchData = async (params: Record<string, string | number>) => {
        setLoading(true);
        try {
            const res: any = await getRetrievalList(params);
            const data = res.data.map((item: any) => {
                return {
                    ...item,
                    capacity1: item.num_chunks + "/" + item.capacity,
                    key: item.collection_id,
                };
            });
            setPromptList(data);
            setHasMore(res.has_more);
        } catch (error) {
            console.log(error);
        }
        setLoading(false);
    };
    const fetchModelsList = async (
        params: Record<string, any>,
        type?: string,
    ) => {
        if (type) {
            dispatch(fetchModelsData(20) as any);
        }
        try {
            const res: any = await getModelsList(params, "text_embedding");
            const data = res.data.map((item: any) => {
                return {
                    ...item,
                    key: item.model_id,
                };
            });
            setModelHasMore(res.has_more);
            setOptions(data);
        } catch (error) {
            console.log(error);
        }
    };
    const handleCreatePrompt = () => {
        setDrawerTitle("Create Collection");
        setDrawerName("");
        setCollectionId("");
        setRecordsSelected([]);
        setDefaultSelectedRowKeys([]);
        setDescriptionText("");
        setSelectedRows([]);
        setSelectValue(1000);
        setEmbeddingSize(0);
        setOpenDrawer(true);
        setEditDisabled(false);
    };
    const handleRecord = (val: any, recordOrChunk: string) => {
        setCollectionRecordId(val.collection_id);
        const routeData = recordOrChunk.toLowerCase();
        navigate(`/project/collections/${val.collection_id}/${routeData}`);
        setDrawerName(val.name || "Untitled Collection");
        setRecordOrChunk(recordOrChunk);
        setRecordOpen(true);
    };
    const handleEdit = (val: any) => {
        setDrawerTitle("Edit Collection");
        setDrawerName(val.name);
        setEditDisabled(true);
        setSelectedRows(
            val.name
                ? [val.name + "-" + val.embedding_model_id]
                : [val.embedding_model_id],
        );
        setDescriptionText(val.description);
        setCollectionId(val.collection_id);
        setEmbeddingSize(val.embedding_size);
        setSelectValue(val.capacity);
        setOpenDrawer(true);
    };

    const handleDelete = (val: any) => {
        setOpenDeleteModal(true);
        setDeleteValue(val.name);
        setCollectionId(val.collection_id);
    };
    const onDeleteCancel = () => {
        setOpenDeleteModal(false);
    };
    const handleRecordCancel = () => {
        setRecordOpen(false);
        navigate(`/project/collections`);
    };
    const onDeleteConfirm = async () => {
        try {
            const limit1: number = limit || 20;

            await deleteRetrieval(collectionId);
            dispatch(fetchRetrievalData(limit1) as any);
            setOpenDeleteModal(false);
            setUpdateRetrievalPrevButton(true);
        } catch (error) {
            const apiError = error as ApiErrorResponse;
            const errorMessage: string = apiError.response.data.error.message;
            toast.error(errorMessage);
        }
    };

    const handleRequest = async () => {
        if (selectedRows.length === 0 || !selectValue) {
            return toast.error(`${t("missingRequiredParameters")}`);
        }
        try {
            if (collectionId) {
                const params = {
                    name: drawerName || "",
                    description: descriptionText || "",
                };
                await updateRetrieval(collectionId, params);
            } else {
                const params = {
                    capacity: Number(selectValue),
                    embedding_model_id: selectedRows[0].slice(-8),

                    name: drawerName || "",
                    description: descriptionText || "",
                    embedding_size: embeddingSize || undefined,
                };
                await createRetrieval(params);
            }
            setOpenDrawer(false);

            const limit1 = limit || 20;
            dispatch(fetchRetrievalData(limit1) as any);
            setUpdateRetrievalPrevButton(true);
        } catch (error) {
            const apiError = error as ApiErrorResponse;
            const errorMessage: string = apiError.response.data.error.message;
            toast.error(errorMessage);
        }
    };
    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setDrawerName(e.target.value);
    };
    const handleCancel = () => {
        setOpenDrawer(false);
    };
    const handleModalCancel = () => {
        setModelOne(false);
    };
    const handleSetModelConfirmOne = () => {
        setModelOne(false);
        setUpdatePrevButton(true);
    };
    const handleCreateModelId = async () => {
        await setModelOne(true);
        childRef.current?.fetchAiModelsList();
    };
    const handleChildModelEvent = async (value: Record<string, any>) => {
        setUpdatePrevButton(false);
        await fetchModelsList(value);
    };
    const handleSelectValue = (value: number) => {
        setSelectValue(value);
    };
    const handleSelectModelId = () => {
        if (editDisabled) {
            return;
        }
        setModalTableOpen(true);
    };

    const handleChildEvent = async (value: any) => {
        setLimit(value.limit);
        setUpdateRetrievalPrevButton(false);
        await fetchData(value);
    };
    return (
        <div className={styles["retrieval"]}>
            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable
                    loading={loading}
                    updatePrevButton={updateRetrievalPrevButton}
                    onChildEvent={handleChildEvent}
                    name="collection"
                    hasMore={hasMore}
                    id="collection_id"
                    columns={columns}
                    ifSelect={false}
                    onOpenDrawer={handleCreatePrompt}
                    dataSource={promptList}
                />
            </Spin>
            <Drawer
                className={styles["drawer-retrievals"]}
                closeIcon={
                    <img
                        src={closeIcon}
                        alt="closeIcon"
                        className={styles["img-icon-close"]}
                    />
                }
                onClose={handleCancel}
                title={drawerTitle}
                placement="right"
                open={OpenDrawer}
                size="large"
                footer={
                    <ModalFooterEnd
                        handleOk={() => handleRequest()}
                        onCancel={handleCancel}
                    />
                }
            >
                <div className={styles["drawer-retrieval"]}>
                    <div className={styles["name-prompt"]}>
                        {t("projectModelColumnName")}
                    </div>
                    <Input
                        className={styles["input"]}
                        value={drawerName}
                        onChange={handleNameChange}
                    ></Input>
                    <div className={styles["desc-prompt"]}>
                        {t("projectAssistantsColumnDescription")}
                    </div>
                    <div className={styles["label-desc"]}>
                        {t("projectRetrievalCreateDesc")}
                    </div>
                    <Input.TextArea
                        autoSize={{ minRows: 3, maxRows: 10 }}
                        showCount
                        placeholder={t("projectRecordEnterDescription")}
                        value={descriptionText}
                        className={styles["input"]}
                        onChange={(e) => setDescriptionText(e.target.value)}
                        maxLength={200}
                    />
                    <div className={styles["hr"]}></div>
                    <div className={styles["label"]}>
                        <span className={styles["span"]}>*</span>
                        <span>{t("projectRetrievalEmbeddingModel")}</span>
                    </div>
                    <div className={styles["label-desc"]}>
                        {t("projectRetrievalEmbeddingModelDesc")}
                    </div>
                    <Select
                        placeholder={t("projectSelectModel")}
                        open={false}
                        className={styles["input"]}
                        mode="multiple"
                        disabled={editDisabled}
                        suffixIcon={<RightOutlined />}
                        maxTagCount={2}
                        removeIcon={null}
                        value={selectedRows}
                        onClick={handleSelectModelId}
                    ></Select>
                    <div className={styles["hr"]}></div>
                    <div className={styles["label"]}>
                        <span className={styles["span"]}>*</span>
                        <span>{t("projectRetrievalColumnCapacity")}</span>
                    </div>
                    <div className={styles["label-desc"]}>
                        {t("projectRetrievalCapacityDesc")}
                    </div>
                    <Select
                        placeholder={t("projectRetrievalCapacityPlaceholder")}
                        onChange={handleSelectValue}
                        value={selectValue}
                        className={styles["input"]}
                        disabled={editDisabled}
                        options={[
                            {
                                value: "1000",
                                label: "1000 chunks",
                            },
                        ]}
                    />
                </div>
            </Drawer>
            <ModelModal
                type="text_embedding"
                ref={childRef}
                open={modelOne}
                handleSetModelOne={handleModalCancel}
                getOptionsList={fetchModelsList}
                modelType="text_embedding"
                handleSetModelConfirmOne={handleSetModelConfirmOne}
            ></ModelModal>
            <Modal
                closeIcon={
                    <img
                        src={closeIcon}
                        alt="closeIcon"
                        className={styles["img-icon-close"]}
                    />
                }
                onCancel={handleModalClose}
                centered
                footer={[
                    <div className="footer-group" key="footer">
                        <Button
                            key="model"
                            icon={<PlusOutlined />}
                            onClick={handleCreateModelId}
                            className="cancel-button"
                        >
                            {t("projectNewModel")}
                        </Button>
                        <div>
                            <span className="select-record">
                                {recordsSelected.length}{" "}
                                {recordsSelected.length > 1
                                    ? `${t("projectItemsSelected")}`
                                    : `${t("projectItemSelected")}`}
                            </span>
                            <Button
                                key="cancel"
                                onClick={handleModalClose}
                                className={`cancel-button ${styles.cancelButton}`}
                            >
                                {t("cancel")}
                            </Button>
                            <Button
                                key="submit"
                                onClick={handleModalClose}
                                className="next-button"
                            >
                                {t("confirm")}
                            </Button>
                        </div>
                    </div>,
                ]}
                title={t("projectSelectModel")}
                open={modalTableOpen}
                width={1000}
                className={`modal-inner-table ${styles["retrieval-model"]}`}
            >
                <ModalTable
                    name="model"
                    loading={false}
                    onOpenDrawer={handleCreateModelId}
                    updatePrevButton={updatePrevButton}
                    defaultSelectedRowKeys={defaultSelectedRowKeys}
                    handleRecordsSelected={handleRecordsSelected}
                    ifSelect={true}
                    columns={modelsTableColumn}
                    hasMore={modelHasMore}
                    id="model_id"
                    dataSource={options}
                    onChildEvent={handleChildModelEvent}
                ></ModalTable>
            </Modal>
            <DeleteModal
                describe={`${t("deleteItem")} ${deleteValue || "Untitled Collection"
                    }? ${t("projectRetrievalDeleteDesc")}`}
                open={OpenDeleteModal}
                title={t("projectRetrievalDelete")}
                projectName={deleteValue || "Untitled Collection"}
                onDeleteCancel={onDeleteCancel}
                onDeleteConfirm={onDeleteConfirm}
            />
            <Drawer
                className={
                    recordOrChunk !== "Chunks"
                        ? styles["drawer-inner-table"]
                        : styles["drawer-inner-chunk"]
                }
                closeIcon={
                    <img
                        src={closeIcon}
                        alt="closeIcon"
                        className={styles["img-icon-close"]}
                    />
                }
                onClose={handleRecordCancel}
                placement="right"
                size="large"
                open={recordOpen}
                width={1000}
                title={`${drawerName} / ${recordOrChunk === "Chunks"
                        ? t("projectChunks")
                        : t("projectRetrievalColumnRecords")
                    }`}
            >
                {recordOrChunk === "Chunks" ? (
                    <ChunkPage collectionId={collectionRecordId} />
                ) : (
                    <RecordPage collectionId={collectionRecordId}></RecordPage>
                )}
            </Drawer>
        </div>
    );
}
export default Retrieval;
