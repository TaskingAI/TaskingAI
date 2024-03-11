import { useTranslation } from "react-i18next";
function TooltipTitle() {
    const { t } = useTranslation();
    const tooltipEditTitle = <span style={{ color: '#777' }}>{t('edit')}</span>;
    const tooltipPlaygroundTitle = <span style={{ color: '#777' }}>{t('projectPlaygroundTitle')}</span>;
    const tooltipDeleteTitle = <span style={{ color: '#777' }}>{t('delete')}</span>;
    const tooltipShowTitle = <span style={{ color: '#777' }}>{t('show')}</span>
    const tooltipHideTitle = <span style={{ color: '#777' }}>{t('hide')}</span>
    const tooltipRecordTitle = <span style={{ color: '#777' }}>{t('record')}</span>
    const tooltipChunkTitle = <span style={{ color: '#777' }}>{t('chunk')}</span>
    return {
        tooltipEditTitle,
        tooltipPlaygroundTitle,
        tooltipDeleteTitle,
        tooltipShowTitle,
        tooltipHideTitle,
        tooltipRecordTitle,
        tooltipChunkTitle
    }
}
export default TooltipTitle;