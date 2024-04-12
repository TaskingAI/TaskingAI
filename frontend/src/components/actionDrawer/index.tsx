import {
  Input, Radio, RadioChangeEvent
} from 'antd';
import { ChangeEvent } from 'react';
import styles from './actionDrawer.module.scss'
import { useTranslation } from 'react-i18next';
import { useState, forwardRef,useImperativeHandle,useEffect } from 'react';
const ActionDrawer = forwardRef((props: any, ref: any) => {
  const { t } = useTranslation();
  const { actionId, schema, showTipError,open, onhandleTipError, onSchemaChange, onChangeAuthentication, Authentication, onRadioChange, radioValue, onChangeCustom, custom } = props
  const { TextArea } = Input
  const [resetButtonShow, setResetButtonShow] = useState(actionId ? true : false)
  const schemaPlaceholder = `{
  "openapi": "3.1.0",
  "info": {
      "title": "Get weather data",
      "description": "Retrieves current weather data for a location.",
      "version": "v1.0.0"
  },
  "servers": [
      {
          "url": "https://weather.example.com"
      }
  ],
  "paths": {
      "/location": {
          "get": {
              "description": "Get temperature for a specific location",
              "operationId": "GetCurrentWeather",
              "parameters": [
                  {
                      "name": "location",
                      "in": "query",
                      "description": "The city and state to retrieve the weather for",
                      "required": true,
                      "schema": {
                          "type": "string"
                      }
                  }
              ],
              "deprecated": false
          }
      }
  },
  "components": {
      "schemas": {}
  }
}`
  useImperativeHandle(ref, () => ({
    getResetButtonState: () => resetButtonShow
  }));
  useEffect(() => {
    if(actionId){
      setResetButtonShow(true)
    }else {
      setResetButtonShow(false)
    }
  },[open])
  const handleSchemaChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    onSchemaChange(e.target.value)
    if (!e.target.value) {
      onhandleTipError(true)
    } else {
      onhandleTipError(false)
    }
  }
  const handleResetCredentials = () => {
    setResetButtonShow(false)
    onChangeAuthentication('')
    onChangeCustom('')
  }
  const handleRadioChange = (e: RadioChangeEvent) => {
    onRadioChange(e.target.value)
  }
  const handleCustom = (e: ChangeEvent<HTMLInputElement>) => {
    onChangeCustom(e.target.value)
  }
  const titleCase = (str: string) => {
    const newStr = str.slice(0, 1).toUpperCase() + str.slice(1).toLowerCase();
    return newStr;
  }
  const hangleChangeAuthorization = (e: ChangeEvent<HTMLInputElement>) => {
    onChangeAuthentication(e.target.value)
  }
  return (
    <div className={styles['action-drawer']}>
      <div className={styles['top']}>
        <div className={styles['label']} style={{ marginTop: 0 }}>
          <span className={styles['span']}> * </span>
          <span>{t('projectActionSchema')}</span>
        </div>
        {!actionId ?
          <div className={styles['label-description']}>
            {t('projectActionSchemaCompliant')}
            <a href="https://www.openapis.org/what-is-openapi" target="_blank" rel="noopener noreferrer" className={'href'}> {t('projectActionSchemaDescLink')}</a>.
            {t('projectActionSchemaDesc')}
            <a href="https://docs.tasking.ai/docs/guide/tool/action" target="_blank" rel="noopener noreferrer" className={'href'}> {t('projectActionSchemaDescLinkEnd')} </a>
            {t('projectActionToLearnMore')}
          </div> :
          <div className={styles['label-description']}>{t('projectActionEditDesc')}</div>}

        <TextArea value={schema} placeholder={schemaPlaceholder}
          onChange={(e) => handleSchemaChange(e)} showCount maxLength={32768}></TextArea>
        <div className={`${styles['desc-action-error']} ${showTipError ? styles.show : ''}`}>Schema is required</div>

      </div>
      <div className={styles['bottom']}>
        <div className={styles['label']}>
          <span className={styles['span']}> * </span>
          <span>{t('projectActionAuthentication')}</span>
        </div>
        <div className={styles['label-description']}>{t('projectActionAuthenticationType')}</div>
        {resetButtonShow && <div className={styles['formbuttoncancel']} onClick={handleResetCredentials}>
          <div className={styles['text1']}>{t('projectModelResetCredentials')}</div>
        </div>}
        <div className={resetButtonShow ? styles.resetBackground : undefined}>
          <Radio.Group onChange={handleRadioChange} value={radioValue}>
            <Radio value='none'>{t('projectActionNone')}</Radio>
            <Radio value='basic'>{t('projectActionBasic')}</Radio>
            <Radio value='bearer'>{t('projectActionBearer')}</Radio>
            <Radio value='custom'>{t('projectActionCustom')}</Radio>
          </Radio.Group>
          {radioValue !== 'none' && <div style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'center', margin: '15px 0' }}>
            {radioValue !== 'custom' ? <span className={styles['desc-description']}>Authorization </span> : <Input placeholder='X-Custom' onChange={handleCustom} value={custom} style={{ width: '14%' }} />} <span className={styles['desc-description']}>:</span>  <Input prefix={<span style={{ color: '#999' }} >{radioValue !== 'custom' && titleCase(radioValue)}</span>} value={Authentication} placeholder='<Secret>' onChange={hangleChangeAuthorization} style={{ width: '83%' }}></Input>
          </div>
          }
        </div>

      </div>
    </div>
  )
})
export default ActionDrawer