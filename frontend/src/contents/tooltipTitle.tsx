import { useTranslation } from "react-i18next";
function TooltipTitle() {
    const { t } = useTranslation();
    const tooltipEditTitle = <span style={{ color: '#777' }}>{t('edit')}</span>;
    const tooltipPlaygroundTitle = <span style={{ color: '#777' }}>{t('projectPlaygroundTitle')}</span>;
    const tooltipDeleteTitle = <span style={{ color: '#777' }}>{t('delete')}</span>;
    const tooltipShowTitle = <span style={{ color: '#777' }}>{t('show')}</span>
    const tooltipHideTitle = <span style={{ color: '#777' }}>{t('hide')}</span>
    const tooltipRecordTitle = <span style={{ color: '#777' }}>Records</span>
    const tooltipChunkTitle = <span style={{ color: '#777' }}>{t('chunk')}</span>
    const tooltipPluginTitle = <span style={{ color: '#777' }}>Details</span>
    const tooltipCodeTitle = <span style={{ color: '#777' }}>Code</span>
    const tooltipMoreTitle = <span style={{ color: '#777' }}>More</span>
    return {
        tooltipEditTitle,
        tooltipPlaygroundTitle,
        tooltipDeleteTitle,
        tooltipShowTitle,
        tooltipHideTitle,
        tooltipRecordTitle,
        tooltipChunkTitle,
        tooltipPluginTitle,
        tooltipCodeTitle,
        tooltipMoreTitle
    }
}
export default TooltipTitle;