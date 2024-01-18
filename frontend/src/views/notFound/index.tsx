import { useNavigate } from "react-router-dom";
import illustration from '../../assets/img/Illustration.png'
import "./notFound.scss";

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
    <div className="div">
      <div className="frame">
        <img className="illustration-icon" src={illustration} />
        <div className="title-section">
          <b className="title">Page Not Found</b>
          <div className="subtitle">
            The page you are looking for doesn’t exist or has been moved
          </div>
        </div>
        <div className="home-button" onClick={handlerBackHome}>
          <div className="text">Back Home</div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
