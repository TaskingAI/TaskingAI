import { useState, useEffect } from 'react';
import styles from './pagination.module.scss'
import { Button, Pagination } from 'antd';
function Paginations(props:any) {
    const { onFetchData, hasMore, } = props
    const [previousButtonDisabled, setPreviousButtonDisabled] = useState(true)
    const [nextButtonDisabled, setNextButtonDisabled] = useState(true)
    const [previousFlag, setPreviousFlag] = useState(false)
    const [nextFlag, setNextFlag] = useState(false)
    const [pageSize, setPageSize] = useState(10)
    const [offset, setOffset] = useState(0)
    const [isFirstRender, setIsFirstRender] = useState(true)
    useEffect(() => {
        if (isFirstRender && hasMore) {
            setNextButtonDisabled(false)
            setIsFirstRender(false)
            return
        }
        if (previousFlag && offset !== 0) {
            setPreviousButtonDisabled(false)
            setNextButtonDisabled(false)
        }
        if (nextFlag && hasMore) {
            setNextButtonDisabled(false)
            setPreviousButtonDisabled(false)
        }
        if (previousFlag && offset === 0) {
            setPreviousButtonDisabled(true)
            setNextButtonDisabled(false)
        }
        if (nextFlag && !hasMore) {
            setNextButtonDisabled(true)
            setPreviousButtonDisabled(false)
        }
    }, [previousFlag, nextFlag, hasMore,offset])
    const handlePrevious = () => {
        setPreviousFlag(true)
        setNextFlag(false)
        const params = {
            limit: pageSize,
            offset: offset - pageSize,
            lang: 'en'
        }
        setOffset(offset - pageSize)
        onFetchData(params)
    }
    const handleChangePageLimit = (page:number, pageSize:number) => {
        setPageSize(pageSize)
        setOffset(pageSize * (page - 1))
        const params = {
            limit: pageSize,
            offset: pageSize * (page - 1),
            lang: 'en'
        }
        onFetchData(params)
    }
    const handleNext = () => {
        setNextFlag(true)
        setPreviousFlag(false)
        setOffset(offset + pageSize)

        const params = {
            limit: pageSize,
            offset: offset + pageSize,
            lang: 'en'
        }
        onFetchData(params)
    }
    return (
        <div className={styles.footer}>
            <Button className={styles['previous-button']} style={{ borderRight: 'none' }} onClick={handlePrevious} disabled={previousButtonDisabled}>Previous</Button>
            <Button className={styles['next-button-group']} onClick={handleNext} disabled={nextButtonDisabled}>Next</Button>
            <Pagination defaultPageSize={10} showQuickJumper={false} showSizeChanger={true} onChange={handleChangePageLimit} />
        </div>
    );
}
export default Paginations;