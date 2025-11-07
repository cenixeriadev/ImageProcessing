import React from "react";
import "../styles/Login.css";
import icon from "../assets/Icons/repo.svg";
import LOY from "../assets/images/StarLoy.jpeg";

export default function Login() {
  return (
    <div className="container">
      <div className="container1">
        <div className="form-box">
          <a
            href="https://github.com/cenixeriadev/ImageProcessing.git"
            className="btn-github-repository"
            aria-label="View GitHub repository"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img src={icon} alt="GitHub Repo Icon" width="16" />
          </a>
          <h1 className="login">LOGIN</h1>
          <p className="descripcion">
            Hi, Welcome back, fill each gap with your user credentials. (Esto es
            el avance richard jijij)
          </p>
          <form className="contenido">
            <div className="input-box">
              <input
                id="login-user"
                type="text"
                placeholder="Username"
                required
              />
              <i className="bx bxs-user"></i>
            </div>

            <div className="input-box second">
              <input
                id="confirm-password"
                type="password"
                placeholder="Password"
                required
              />
              <button
                className="bx bx-low-vision"
                type="button"
                aria-label="Show password"
              ></button>
            </div>

            <a href="#" className="forgot-password">
              Forgot password?
            </a>

            <button type="submit" className="btn-glass">
              Sign In
            </button>

            <p className="flex-gap">
              <span>Don't have an account yet?</span>
              <a href="#" className="sign-up button" type="button">
                Sign Up
              </a>
            </p>

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
          </form>
        </div>
        <img src={LOY} alt="StarLoy Logo" className="logo-img" />
      </div>
    </div>
  );
}
