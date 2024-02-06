import { Table, Select, Input, Button, Pagination, Empty } from 'antd';
import { useState, useEffect } from 'react';
import styles from './modalTable.module.scss'
import { PlusOutlined } from '@ant-design/icons';
import NoApikey from '../../assets/img/NO_APIKEY.svg?react'
import NoAssistant from '../../assets/img/NO_ASSISTANT.svg?react'
import NoCollection from '../../assets/img/NO_COLLECTION.svg?react'
import NoModel from '../../assets/img/NO_MODEL.svg?react'
import NoRecord from '../../assets/img/NO_RECORD_2.svg?react'
import NoTool from '../../assets/img/NO_TOOL.svg?react'
import { TableProps } from '../../contant/index'
function ModalTable({ columns, ifAllowNew, hangleFilterData, ifOnlyId, defaultSelectedRowKeys, updatePrevButton, ifHideFooter, dataSource, mode, ifSelect, onChildEvent, id, hasMore, onOpenDrawer, name, handleRecordsSelected }: TableProps) {
    const [selectedValue, setSelectedValue] = useState('name_search')
    const [inputValue, setInputValue] = useState('')
    const [scroll, setScroll] = useState({ x: 0, y: 0 });
    const [ifClickPageSizeLimit, setIfClickPageSizeLimit] = useState(false)
    const [flagPrev, setFlagPrev] = useState(false)
    const [originalDataSource, setOriginalDataSource] = useState([]);
    const [flagNext, setFlagNext] = useState(false)
    const [nextButtonDisabled, setNextButtonDisabled] = useState(false)
    const [previousButtonDisabled, setPrevButtonDisabled] = useState(true)
    const [isFirstRender, setIsFirstRender] = useState(true);
    const [_filterConfig, setFilterConfig] = useState<any>({
        limit: 20,
        sort_field: 'created_timestamp',

    })
    const [enterPlaceHolder, setEnterPlaceHolder] = useState('Enter Name')
    const empty = {
        ['API Key']: <NoApikey />,
        assistant: <NoAssistant />,
        collection: <NoCollection />,
        model: <NoModel />,
        record: <NoRecord />,
        action: <NoTool />,
        chunk: <NoRecord />
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
                if (!tableContainer) {
                    return
                }
                containerWidth = tableContainer.offsetWidth;
                containerHeight = tableContainerH.offsetHeight;
                setScroll({
                    x: containerWidth,
                    y: containerHeight - 61
                });
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
                    containerWidth = tableContainer.offsetWidth;
                    containerHeight = tableContainerH.offsetHeight;
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
        setOriginalDataSource(dataSource)
    }, [])
    useEffect(() => {
        if (defaultSelectedRowKeys && defaultSelectedRowKeys.length) {
            const tag = defaultSelectedRowKeys.map(item => item.split('-').pop())
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
            value: 'name',
            label: 'Name',
        },
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
    const handleSelectFrontChange = (value) => {
        if (value === 'name') {
            setSelectedValue('name_search')
        } else {
            setSelectedValue('id_search')
        }
    }
    const handleSelectEndChange = (value) => {
        if (value === 'Selected Records') {
            const filteredRows = originalDataSource.filter(row => selectedRowKeys.includes(row.key));
            hangleFilterData(filteredRows)
        } else {
            hangleFilterData(originalDataSource)
        }
    }
    const onSelectChange = (newSelectedRowKeys, selectedRows) => {
        handleRecordsSelected(newSelectedRowKeys, selectedRows)
    };
    const onSelectChange1 = (record) => {
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
        getCheckboxProps: (record) => ({
            checked: selectedRowKeys.includes(record.key),
        }),
        type: mode === 'multiple' ? 'checkbox' : 'radio',
        hideDefaultSelections: true,
    };
    const handleSearch = () => {
        setIfClickPageSizeLimit(true)
        setFilterConfig(prevFilterConfig => {
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
            onChildEvent(newFilterConfig);
            return newFilterConfig;
        });
        setPrevButtonDisabled(true)
    }
    const handleInputChange = (e) => {
        setInputValue(e.target.value)
    }
    const handlePrevious = () => {
        setIfClickPageSizeLimit(false)

        setFilterConfig(prevFilterConfig => {

            const newFilterConfig = {
                ...prevFilterConfig,
                before: dataSource[0][id],
            };
            delete newFilterConfig.after
            onChildEvent(newFilterConfig);
            setFlagPrev(true)
            setFlagNext(false)
            return newFilterConfig;
        });

    }
    const handleNext = () => {

        setIfClickPageSizeLimit(false)
        setFilterConfig(prevFilterConfig => {
            const newFilterConfig = {
                ...prevFilterConfig,
                after: dataSource[dataSource.length - 1][id],
            };
            delete newFilterConfig.before
            onChildEvent(newFilterConfig);
            setFlagNext(true)
            setFlagPrev(false)
            return newFilterConfig;
        });

    }
    const handleCreatePrompt = () => {
        onOpenDrawer(true)
    }
    const handleRowClick = (record) => {

        // const checkboxProps = rowSelection.getCheckboxProps(record);
        if (!ifSelect) {
            return
        }
        const key = record.key;

        const isSelected = selectedRowKeys.includes(key);
        let newSelectedRowKeys
        if (mode === 'multiple') {
            newSelectedRowKeys = isSelected
                ? selectedRowKeys.filter((selectedKey) => selectedKey !== key)
                : [...selectedRowKeys, key];
            const data = dataSource.filter(row => newSelectedRowKeys.includes(row.key));
            handleRecordsSelected(newSelectedRowKeys, data)
        } else {
            newSelectedRowKeys = isSelected
                ? []
                : [key]
            handleRecordsSelected(newSelectedRowKeys, [record])

        }
        setSelectedRowKeys(newSelectedRowKeys);
    };

    const handleChangePageLimit = (_value, pageSize) => {
        setIfClickPageSizeLimit(true)
        setPrevButtonDisabled(true)
        setFilterConfig(prevFilterConfig => {
            const newFilterConfig = {
                ...prevFilterConfig,
                limit: pageSize,
            };
            delete newFilterConfig.before
            delete newFilterConfig.after
            onChildEvent(newFilterConfig);
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
            image={empty[name]}
            description={
                <div>
                    <p style={{ color: '#bfbfbf', fontSize: '14px' }}>No {name}</p>
                    {!ifAllowNew && <Button icon={<PlusOutlined />} className={styles['prompt-button']} onClick={handleCreatePrompt}>New {name}</Button>}

                </div>
            }
        />
    );
    return (
        <div className={styles['modal-table']}>
            {!ifHideFooter ? <div className={styles['header-table']}>
                <Select defaultValue={ifOnlyId ? 'ID' : 'name'} onChange={handleSelectFrontChange} options={ifOnlyId ? optionsFront1 : optionsFront} className={styles['select-name']} />
                <Input placeholder={enterPlaceHolder} className={styles['input-name']} onChange={handleInputChange} value={inputValue} />
                <Button className='cancel-button' onClick={handleSearch}>Search</Button>
                {(ifSelect && mode === 'multiple') && <Select defaultValue="All records" onChange={handleSelectEndChange} options={optionsEnd} className={styles['select-data']} />}
                {!ifSelect && <div className={styles['header-new']}>
                    <div className={styles['plusParent']}>
                        <Button icon={<PlusOutlined />} className={styles['prompt-button']} onClick={handleCreatePrompt}>New {name}</Button>
                    </div>
                </div>}
            </div> : <div className={styles['header-news']}>
                <div className={styles['plusParent']}>
                    <Button icon={<PlusOutlined />} className={styles['prompt-button']} onClick={handleCreatePrompt}>New {name}</Button>
                </div>
            </div>}

            <div className={styles['table-border']}>
                <Table scroll={scroll} columns={columns} dataSource={dataSource} pagination={false}
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
                    className={`${dataSource.length === 0 && styles['empty-table']}`}
                />
                {!ifHideFooter && <div className={`${styles.footer} ${ifSelect ? styles['footer-position'] : ''}`}>
                    <Button className={styles['previous-button']} style={{ borderRight: 'none' }} onClick={handlePrevious} disabled={previousButtonDisabled}>Previous</Button>
                    <Button className={styles['next-button-group']} onClick={handleNext} disabled={nextButtonDisabled}>Next</Button>
                    <Pagination defaultPageSize={20} showQuickJumper={false} showSizeChanger={true} onChange={handleChangePageLimit} />
                </div>}
            </div>
        </div>
    )
}
export default ModalTable;