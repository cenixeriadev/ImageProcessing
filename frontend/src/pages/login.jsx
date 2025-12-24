import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import "../styles/Login.css";

export default function Login() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/home");
  };

  return (
    <AuthLayout
      title="LOGIN"
      description="Hi, Welcome back, fill each gap with your user credentials."
    >
      <form className="contenido" onSubmit={handleSubmit}>
        <div className="input-box">
          <input type="text" placeholder="Username" required />
          <i className="bx bxs-user"></i>
        </div>

        <div className="input-box second">
          <input type="password" placeholder="Password" required />
          <button
            className="bx bx-low-vision"
            type="button"
            aria-label="Show password"
          ></button>
        </div>

        <Link to="/forgot-password" className="forgot-password">
          Forgot password?
        </Link>

        <button type="submit" className="btn-glass">
          Sign In
        </button>

        <p className="flex-gap">
          <span>Don't have an account yet?</span>
          <Link to="/register" className="sign-up button">
            Sign Up
          </Link>
        </p>
      </form>
    </AuthLayout>
  );
}
