import React from 'react';
import styles from './parameter.module.scss';
import MessageSuccess from '../../assets/img/messageSuccess.svg?react'

const ParameterTable = ({ parameters }) => {
  return (
    <div className={styles.table}>
      <div className={`${styles.cell} ${styles.header} ${styles.headerName}`}>Parameter name</div>
      <div className={`${styles.cell} ${styles.header} ${styles.headerType}`}>Type</div>
      <div className={`${styles.cell} ${styles.header} ${styles.headerRequired}`}>Required</div>
      <div className={`${styles.cell} ${styles.header} ${styles.headerDescription}`}>Description</div>
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