import React from 'react';
import styles from './parameter.module.scss';
import MessageSuccess from '../../assets/img/messageSuccess.svg?react'
import { useTranslation } from 'react-i18next';

const ParameterTable = ({ parameters }) => {
  const { t } = useTranslation(['components/parameterTable/index'])
  return (
    <div className={styles.table}>
      <div className={`${styles.cell} ${styles.header} ${styles.headerName}`}>{t('parameterName')}</div>
      <div className={`${styles.cell} ${styles.header} ${styles.headerType}`}>{t('type')}</div>
      <div className={`${styles.cell} ${styles.header} ${styles.headerRequired}`}>{t('required')}</div>
      <div className={`${styles.cell} ${styles.header} ${styles.headerDescription}`}>{t('description')}</div>
      {parameters.map((param, index) => (
        <React.Fragment key={index}>
          <div className={styles.cell}>{param.name}</div>
          <div className={styles.cell}>{param.type}</div>
          <div className={`${styles.cell} ${styles.required}`}>{param.required ? <MessageSuccess/> : ''}</div>
          <div className={styles.cell}>{param.description}</div>
        </React.Fragment>
      ))}
    </div>
  );
};

export default ParameterTable;