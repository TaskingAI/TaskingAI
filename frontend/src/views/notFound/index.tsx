import { useNavigate } from "react-router-dom";
import illustration from '../../assets/img/Illustration.png'
import styles from  "./notFound.module.scss";

const NotFound = () => {
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
          <b className={styles["title"]}>Page Not Found</b>
          <div className={styles["subtitle"]}>
            The page you are looking for doesn’t exist or has been moved
          </div>
        </div>
        <div className={styles["home-button"]} onClick={handlerBackHome}>
          <div className={styles["text"]}>Back Home</div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
