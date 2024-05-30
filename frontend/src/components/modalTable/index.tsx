import { Table, Select, Input, Button, Pagination, Empty, ConfigProvider } from 'antd';
import { useState, useEffect, ChangeEvent } from 'react';
import styles from './modalTable.module.scss'
import { PlusOutlined } from '@ant-design/icons';
import NoApikey from '../../assets/img/NO_APIKEY.svg?react'
import NoAssistant from '../../assets/img/NO_ASSISTANT.svg?react'
import NoCollection from '../../assets/img/NO_COLLECTION.svg?react'
import NoModel from '../../assets/img/NO_MODEL.svg?react'
import NoRecord from '../../assets/img/NO_RECORD_2.svg?react'
import NoTool from '../../assets/img/NO_TOOL.svg?react'
import NoProject from '../../assets/img/NO_PROJECT.svg?react'
import { TableProps } from '../../constant/index'
function ModalTable({ columns, ifAllowNew,title, hangleFilterData,isShowNewCreateButton=true, ifOnlyId, defaultSelectedRowKeys, updatePrevButton,ifHideLeftHeader, ifHideFooter=false, dataSource, mode, ifSelect, onChildEvent, id, hasMore, onOpenDrawer, name, handleRecordsSelected }: TableProps) {
    const [selectedValue, setSelectedValue] = useState('id_search')
    const [inputValue, setInputValue] = useState('')
    const [scroll, setScroll] = useState({ x: 0, y: 0 });
    const [ifClickPageSizeLimit, setIfClickPageSizeLimit] = useState(false)
    const [flagPrev, setFlagPrev] = useState(false)
    const [originalDataSource, setOriginalDataSource] = useState<any[]>([]);
    const [flagNext, setFlagNext] = useState(false)
    const [nextButtonDisabled, setNextButtonDisabled] = useState(false)
    const [previousButtonDisabled, setPrevButtonDisabled] = useState(true)
    const [isFirstRender, setIsFirstRender] = useState(true);
    const [_filterConfig, setFilterConfig] = useState<any>({
        limit: 20,
        sort_field: 'created_timestamp',
    })
    const [enterPlaceHolder, setEnterPlaceHolder] = useState('Enter Name')
    const empty: Record<string, any> = {
        ['API Key']: <NoApikey style={{ width: '158px', height: '100px' }} />,
        assistant: <NoAssistant style={{ width: '158px', height: '100px' }} />,
        collection: <NoCollection style={{ width: '158px', height: '100px' }} />,
        model: <NoModel style={{ width: '158px', height: '100px' }} />,
        record: <NoRecord style={{ width: '158px', height: '100px' }} />,
        action: <NoTool style={{ width: '158px', height: '100px' }} />,
        plugin: <NoTool style={{ width: '158px', height: '100px' }} />,
        Invoice: <NoRecord style={{ width: '158px', height: '100px' }} />,
        project: <NoProject style={{ width: '158px', height: '100px' }} />,
    }
    const [selectedRowKeys, setSelectedRowKeys] = useState((defaultSelectedRowKeys && defaultSelectedRowKeys.length) ? defaultSelectedRowKeys : []);
    useEffect(() => {
        const updateScroll = () => {
            let tableContainer: HTMLElement | null = document.querySelector('.ant-table-container .ant-table-body table');
            let tableContainerH: HTMLElement | null = document.querySelector('.ant-table-container');
            let modalInnerTable: HTMLElement | null = document.querySelector('.modal-inner-table');
            let modalOpen = true;
            if (modalInnerTable) {
                modalOpen = getComputedStyle(modalInnerTable).display === 'none'
            }
            let elementsWithPrefix: any = document.querySelectorAll('[class*="_drawer-inner-table"]');
            let elementsWithPrefix1: any = document.querySelectorAll('[class*="_drawer-inner-chunk"]');
            let containerWidth = 0;
            let containerHeight = 0;
            if (!modalInnerTable && elementsWithPrefix.length === 0 && elementsWithPrefix1.length === 0) {
                setTimeout(() => {
                    if (!tableContainer) {
                        return
                    }
                    containerWidth = tableContainer.offsetWidth;

                    containerHeight = tableContainerH?.offsetHeight as any;
                    setScroll({
                        x: containerWidth,
                        y: containerHeight - 61
                    });
                }, 0)
            } else if (elementsWithPrefix.length !== 0 && elementsWithPrefix1.length === 0 && modalOpen) {

                setTimeout(() => {
                    let firstElement = elementsWithPrefix[0];
                    let antDrawerBodyClassName = firstElement.querySelector('.ant-drawer-body');
                    let tableClassName = firstElement.querySelector('.ant-drawer-body table')
                    containerWidth = tableClassName.offsetWidth;
                    containerHeight = antDrawerBodyClassName.offsetHeight;
                    setScroll({
                        x: containerWidth,
                        y: containerHeight - 202,
                    });

                }, 0)
            } else if (elementsWithPrefix1.length !== 0 && elementsWithPrefix.length === 0 && modalOpen) {
                setTimeout(() => {
                    let firstElement = elementsWithPrefix1[0];
                    let antDrawerBodyClassName = firstElement.querySelector('.ant-drawer-body');
                    let tableClassName = firstElement.querySelector('.ant-drawer-body table')
                    containerWidth = tableClassName.offsetWidth;
                    containerHeight = antDrawerBodyClassName.offsetHeight;
                    setScroll({
                        x: containerWidth,
                        y: containerHeight - 202,
                    });
                })
            } else if (modalInnerTable) {
                setTimeout(() => {
                    const tableContainer: HTMLElement | null = document.querySelector('.modal-inner-table .ant-table-container table');
                    const tableContainerH: HTMLElement | null = document.querySelector('.modal-inner-table .ant-table-container');
                    containerWidth = tableContainer?.offsetWidth as any;
                    containerHeight = tableContainerH?.offsetHeight as any;
                    setScroll({
                        x: containerWidth,
                        y: 400,
                    });
                }, 0)
            }
        };
        updateScroll();
    }, []);
    useEffect(() => {
        setOriginalDataSource(dataSource as any[])
    }, [])
    useEffect(() => {
        if (defaultSelectedRowKeys && defaultSelectedRowKeys.length) {
            const tag = defaultSelectedRowKeys.map(item => item.split('-').pop()) as any[]
            setSelectedRowKeys(tag)
        } else {
            setSelectedRowKeys([])
        }
    }, [defaultSelectedRowKeys])
    useEffect(() => {
        if (flagNext) {
            setPrevButtonDisabled(false)
            if (!hasMore) {
                setNextButtonDisabled(true)
            } else {
                setNextButtonDisabled(false)
            }
        }
    }, [flagNext])
    useEffect(() => {
        if (flagPrev) {
            setNextButtonDisabled(false)
            if (!hasMore) {
                setPrevButtonDisabled(true)
            } else {
                setPrevButtonDisabled(false)
            }
        }
    }, [flagPrev])
    useEffect(() => {
        if (selectedValue === 'name_search') {
            setEnterPlaceHolder('Enter Name')
        } else {
            setEnterPlaceHolder('Enter ID')
        }
        if (ifOnlyId) {
            setEnterPlaceHolder('Enter ID')
        }
    }, [selectedValue, ifOnlyId, enterPlaceHolder])
    useEffect(() => {
        if (isFirstRender) {
            setIsFirstRender(false)
            if (!hasMore) {
                setNextButtonDisabled(true)
                setPrevButtonDisabled(true)
            }
            return
        }
        if (!hasMore && !flagPrev && !flagNext) {
            setNextButtonDisabled(true)
            setPrevButtonDisabled(true)
        }
        if (hasMore && !flagPrev && !flagNext) {
            setNextButtonDisabled(false)
            setPrevButtonDisabled(true)
        }
        if (hasMore && flagPrev && !flagNext) {
            setNextButtonDisabled(false)
            setPrevButtonDisabled(false)
        }
        if (hasMore && !flagPrev && flagNext) {
            setNextButtonDisabled(false)
            setPrevButtonDisabled(false)
        }
        if (!hasMore && flagPrev && !flagNext) {
            setNextButtonDisabled(false)
            setPrevButtonDisabled(true)
            if (ifClickPageSizeLimit || updatePrevButton) {
                setNextButtonDisabled(true)
            }
        }
        if (!hasMore && !flagPrev && flagNext) {
            setNextButtonDisabled(true)
            setPrevButtonDisabled(false)
        }
        if (ifClickPageSizeLimit || updatePrevButton) {
            setPrevButtonDisabled(true)
        }

    }, [onChildEvent, hasMore])
    const optionsFront = [
        {
            value: 'id',
            label: 'ID',
        }
    ]
    const optionsFront1 = [
        {
            value: 'id',
            label: 'ID',
        }
    ]
    const handleSelectFrontChange = (value: string) => {
        if (value === 'name') {
            setSelectedValue('name_search')
        } else {
            setSelectedValue('id_search')
        }
    }
    const handleSelectEndChange = (value: string) => {
        const filteredRows = value === 'Selected Records'
            ? originalDataSource.filter(row => selectedRowKeys.includes(row.key))
            : originalDataSource;
        if (hangleFilterData) {
            hangleFilterData(filteredRows);
        }
    };
    const onSelectChange = (newSelectedRowKeys: any, selectedRows: any) => {
        if (handleRecordsSelected) {
            handleRecordsSelected(newSelectedRowKeys, selectedRows)

        }
    };
    const onSelectChange1 = (record: any) => {
        const key = record.key;
        const isSelected = selectedRowKeys.includes(key);
        let newSelectedRowKeys
        if (mode === 'multiple') {
            newSelectedRowKeys = isSelected
                ? selectedRowKeys.filter((selectedKey) => selectedKey !== key)
                : [...selectedRowKeys, key];
        } else {
            newSelectedRowKeys = isSelected
                ? []
                : [key]
        }
        setSelectedRowKeys(newSelectedRowKeys);
    }
    const rowSelection: any = {
        selectedRowKeys,
        width: 45,
        onChange: onSelectChange,
        onSelect: onSelectChange1,
        columnTitle: ' ',
        getCheckboxProps: (record: any) => ({
            checked: selectedRowKeys.includes(record.key),
        }),
        type: mode === 'multiple' ? 'checkbox' : 'radio',
        hideDefaultSelections: true,
    };
    const handleSearch = () => {
        setIfClickPageSizeLimit(true)
        setFilterConfig((prevFilterConfig: any) => {
            const newFilterConfig = {
                ...prevFilterConfig,
                [selectedValue]: inputValue
            };
            delete newFilterConfig.after
            delete newFilterConfig.before
            if (inputValue === '') {
                delete newFilterConfig[selectedValue]
            }
            if (selectedValue === 'name_search') {
                delete newFilterConfig.id_search
            } else {
                delete newFilterConfig.name_search
            }
            if (ifOnlyId) {
                delete newFilterConfig.name_search
                newFilterConfig.id_search = inputValue
                if (inputValue === '') {
                    delete newFilterConfig.id_search
                }
            }
            if (onChildEvent) {
                onChildEvent(newFilterConfig);
            }
            return newFilterConfig;
        });
        setPrevButtonDisabled(true)
    }
    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setInputValue(e.target.value)
    }
    const handlePrevious = () => {
        setIfClickPageSizeLimit(false)

        setFilterConfig((prevFilterConfig: any) => {

            const newFilterConfig = {
                ...prevFilterConfig,
                before: dataSource && dataSource[0][id as string],
            };
            delete newFilterConfig.after
            if (onChildEvent) {
                onChildEvent(newFilterConfig);
            }
            setFlagPrev(true)
            setFlagNext(false)
            return newFilterConfig;
        });

    }
    const handleNext = () => {

        setIfClickPageSizeLimit(false)
        setFilterConfig((prevFilterConfig: any) => {
            const newFilterConfig = {
                ...prevFilterConfig,
                after: dataSource && dataSource[dataSource.length - 1][id as string],
            };
            delete newFilterConfig.before
            if (onChildEvent) {
                onChildEvent(newFilterConfig);
            }
            setFlagNext(true)
            setFlagPrev(false)
            return newFilterConfig;
        });

    }
    const handleCreatePrompt = () => {
        if (onOpenDrawer) {
            onOpenDrawer(true)
        }
    }
    const handleRowClick = (record: any) => {
        if (!ifSelect) {
            return
        }
        const key = record.key;

        const isSelected = selectedRowKeys.includes(key);
        let newSelectedRowKeys: any
        if (mode === 'multiple') {
            newSelectedRowKeys = isSelected
                ? selectedRowKeys.filter((selectedKey) => selectedKey !== key)
                : [...selectedRowKeys, key];
            const data = dataSource?.filter(row => newSelectedRowKeys.includes(row.key)) as any[];
            if (handleRecordsSelected) {
                handleRecordsSelected(newSelectedRowKeys, data)

            }
        } else {
            newSelectedRowKeys = isSelected
                ? []
                : [key]
            if (handleRecordsSelected) {
                handleRecordsSelected(newSelectedRowKeys, [record])
            }
        }
        setSelectedRowKeys(newSelectedRowKeys);
    };

    const handleChangePageLimit = (_value: number, pageSize: number) => {
        setIfClickPageSizeLimit(true)
        setPrevButtonDisabled(true)
        setFilterConfig((prevFilterConfig: any) => {
            const newFilterConfig = {
                ...prevFilterConfig,
                limit: pageSize,
            };
            delete newFilterConfig.before
            delete newFilterConfig.after
            if (onChildEvent) {
                onChildEvent(newFilterConfig);

            }
            return newFilterConfig;
        });
    };

    const optionsEnd = [

        {
            value: 'All Records',
            label: 'All Records',
        },
        {
            value: 'Selected Records',
            label: 'Selected Records',
        }
    ]
    const customEmptyText = (
        <Empty
            image={empty[name as string]}
            description={
                <>
                    <p style={{ color: '#bfbfbf', fontSize: '14px' }}>No {name}</p>
                    {!ifAllowNew && <Button icon={<PlusOutlined />} className={styles['prompt-button']} onClick={handleCreatePrompt}>{title}</Button>}
                </>
            }
        />
    );
    return (

        <div className={styles['modal-table']} key={name}>
            {!ifHideLeftHeader ? (
                <div className={styles['header-table']}>
                    <Select defaultValue={'ID' } onChange={handleSelectFrontChange} options={ifOnlyId ? optionsFront1 : optionsFront} className={styles['select-name']} />
                    <Input placeholder={enterPlaceHolder} className={styles['input-name']} onChange={handleInputChange} value={inputValue} />
                    <Button className='cancel-button' onClick={handleSearch}>Search</Button>
                    {(ifSelect && mode === 'multiple') && <Select defaultValue="All Records" onChange={handleSelectEndChange} options={optionsEnd} className={styles['select-data']} />}
                    {!ifSelect && (
                        <div className={styles['header-new']}>
                            <div className={styles['plusParent']}>
                                <Button icon={<PlusOutlined />} className={styles['prompt-button']} onClick={handleCreatePrompt}>{title}</Button>
                            </div>
                        </div>
                    )}
                </div>
            ) : (
                isShowNewCreateButton && <div className={styles['header-news']}>
                    <div className={styles['plusParent']}>
                        <Button icon={<PlusOutlined />} className={styles['prompt-button']} onClick={handleCreatePrompt}>{title}</Button>
                    </div>
                </div>
            )}
            <div className={styles['table-border']}>
                <ConfigProvider theme={{
                    components: {
                        Table: {
                            headerBg: 'white',
                            headerColor: '#2b2b2b'
                        }
                    }
                }}>
                    <Table
                        scroll={scroll}
                        columns={columns}
                        dataSource={dataSource}
                        pagination={false}
                        {...(ifSelect ? { rowSelection: rowSelection } : null)}
                        onRow={(record) => {
                            return {
                                onClick: () => {
                                    handleRowClick(record)
                                }
                            }
                        }}
                        locale={{
                            emptyText: customEmptyText
                        }}
                        className={`${dataSource?.length === 0 && styles['empty-table']}`}
                    />
                </ConfigProvider>
                {!ifHideFooter && (
                    <div className={`${styles.footer} ${ifSelect ? styles['footer-position'] : ''}`}>
                        <Button className={`${styles['previous-button']} ${!previousButtonDisabled && styles['able-click-button']}`} style={{ borderRight: 'none' }} onClick={handlePrevious} disabled={previousButtonDisabled}>Previous</Button>
                        <Button className={`${styles['next-button-group']} ${!nextButtonDisabled && styles['able-click-button']}`} onClick={handleNext} disabled={nextButtonDisabled}>Next</Button>
                        <Pagination defaultPageSize={20} showQuickJumper={false} showSizeChanger={true} onChange={handleChangePageLimit} />
                    </div>
                )}
            </div>
        </div>
    );
}
export default ModalTable;