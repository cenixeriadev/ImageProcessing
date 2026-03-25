import icon from "../assets/Icons/repo.svg";
import "../styles/Authlayout.css";

export default function AuthLayout({ title, description, children }) {
  return (
    //Esto es un componente que se reutiliza en varios lugares
    <div className="auth-container">
      <div className="auth-left">
        <h1>Image Processing</h1>
        <p>Apply powerful filters and transformations to your images.</p>
      </div>
      <div className="auth-right">
        <div className="form-box">
          <a
            href="https://github.com/cenixeriadev/ImageProcessing.git"
            className="btn-github-repository"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img src={icon} alt="GitHub Repo Icon" width="16" />
          </a>
          <h1 className="title">{title}</h1>
          <p className="descripcion">{description}</p>
          {children}
          <div className="separador">
            <span></span>
            <p>Or</p>
            <span></span>
          </div>
          <a
            href="https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fcenixeriadev%2FImageProcessing"
            className="btn-github-login"
            target="_blank"
            rel="noopener noreferrer"
          >
            <i className="bx bxl-github"></i>
            Sign In with GitHub
          </a>
        </div>
      </div>
    </div>
  );
}
