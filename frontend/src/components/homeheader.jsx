import "../styles/homeheader.css";
import icon from "../assets/Icons/repo.svg";
import globalicon from "../assets/Icons/globe-alt-2.svg";
export default function HomeLayout({ title, username, children }) {
  return (
    <div className="home-header-container">
      <h1 className="tittle-header">{title}</h1>
      <div className="second-container">
        <button className="first-button">
          {username}
          <i className="bx bx-user-circle" />
        </button>
        <div className="second-button">
          <img
            src={globalicon}
            alt=""
            className="language-selector-icon"
            aria-hidden="true"
          />
          <select
            id="language-select"
            className="language-selector-field"
            aria-label="Seleccionar idioma"
          >
            <option value="" disabled selected>
              Change language
            </option>
            <option value="es">Español</option>
            <option value="en">English</option>
            <option value="fr">Français</option>
          </select>
          <span className="chevron-down"></span>
        </div>
        <a
          href="https://github.com/cenixeriadev/ImageProcessing.git"
          className="third-button"
          target="_blank"
          rel="noopener noreferrer"
        >
          <img src={icon} alt="GitHub Repo Icon" width="18" />
        </a>
      </div>
      {children}
    </div>
  );
}
