import { useNavigate } from "react-router-dom";
import illustration from '../../assets/img/Illustration.png'
import styles from  "./notFound.module.scss";
import { useTranslation } from 'react-i18next';

const NotFound = () => {
  const { t } = useTranslation('views/notFound/index');
    const navigate = useNavigate();
    const handlerBackHome = ()=>{
        const token=localStorage.getItem('token')
        if(token) {
          navigate(-1)
        }else{
            navigate('/auth/signin')
        }
    }
  return (
    <div className={styles["div"]}>
      <div className={styles["frame"]}>
        <img className={styles["illustration-icon"]} src={illustration} />
        <div className={styles["title-section"]}>
          <b className={styles["title"]}>{t('pageNotFound')}</b>
          <div className={styles["subtitle"]}>
            {t('pageDoesNotExistOrMoved')}
          </div>
        </div>
        <div className={styles["home-button"]} onClick={handlerBackHome}>
          <div className={styles["text"]}>{t('backHome')}</div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
