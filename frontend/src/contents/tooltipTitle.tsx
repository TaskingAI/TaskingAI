import { useTranslation } from "react-i18next";
function TooltipTitle() {
    const { t } = useTranslation('common');
    const tooltipEditTitle = <span style={{ color: '#777' }}>{t('edit')}</span>;
    const tooltipPlaygroundTitle = <span style={{ color: '#777' }}>{t('playground')}</span>;
    const tooltipDeleteTitle = <span style={{ color: '#777' }}>{t('delete')}</span>;
    const tooltipShowTitle = <span style={{ color: '#777' }}>{t('show')}</span>
    const tooltipHideTitle = <span style={{ color: '#777' }}>{t('hide')}</span>
    const tooltipRecordTitle = <span style={{ color: '#777' }}>{t('records')}</span>
    const tooltipChunkTitle = <span style={{ color: '#777' }}>{t('chunk')}</span>
    const tooltipPluginTitle = <span style={{ color: '#777' }}>{t('details')}</span>
    const tooltipCodeTitle = <span style={{ color: '#777' }}>{t('code')}</span>
    const tooltipMoreTitle = <span style={{ color: '#777' }}>{t('more')}</span>
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