import icon from "../assets/Icons/repo.svg";
import LOY from "../assets/images/StarLoy.jpeg";
import { Link } from "react-router-dom";

export default function PasswordLayout({ title, description, children }) {
  return (
    //Esto es un componente que se reutiliza en varios lugares
    <div className="container">
      <div className="container1">
        <div className="form-box">
          <a
            href="https://github.com/cenixeriadev/ImageProcessing.git"
            className="btn-github-repository"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img src={icon} alt="GitHub Repo Icon" width="16" />
          </a>

          <h1 className="login">{title}</h1>
          <p className="descripcion">{description}</p>

          {children}

          <p className="flex-gap">
            <span>Don't have an account yet?</span>
            <Link to="/register" className="sign-up button">
              Sign Up
            </Link>
          </p>
        </div>
        <img src={LOY} alt="StarLoy Logo" className="logo-img" />
      </div>
    </div>
  );
}
