import React from "react";
import "../styles/Login.css";

export default function Login() {
  return (
    <div className="container">
      <div className="container1">
        <div className="form-box">
          <a
            href="#"
            className="btn-github-repository"
            aria-label="View GitHub repository"
          >
            <i className="bx bxl-github"></i>
            <i className="bx bxs-folder"></i>
          </a>
          <form>
            <h1>Log in</h1>
            <p>Hi, Welcome back, fill each gap with your user credentials.</p>
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
                id="Confirm-password"
                type="password"
                placeholder="Password"
                required
              />
              <button className="bx bx-low-vision" type="button"></button>
            </div>
            <a href="" className="forgot-password">
              forgot password?
            </a>
            <button type="submit" className="btn-glass">
              Sign In
            </button>
            <p>
              Don't have an account yet?
              <a href="" className="Sign-up button" type="button">
                Sign Up
              </a>
            </p>
            <div className="separador">
              <span></span>
              <p>Or</p>
              <span></span>
            </div>
            <a href="" className="btn-Github-login">
              <i className="bx bxl-github"></i>
              Sign In with Git Hub
            </a>
          </form>
        </div>
      </div>
      <div className="cuadrado">
        <h1>Welcome to the image processing</h1>
        <p>Here is a little introduction of this project</p>
      </div>
    </div>
  );
}
