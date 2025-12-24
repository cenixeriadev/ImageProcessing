import { Link } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import "../styles/register.css";

export default function Register() {
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Register submit");
  };
  return (
    <AuthLayout
      title="Register"
      description="Please, enter a new password, check that has at least one special character"
    >
      <form className="contenido" onSubmit={handleSubmit}>
        <div className="input-box">
          <input type="text" placeholder="Username" required />
          <i className="bx bxs-user"></i>
        </div>

        <div className="input-box second">
          <input type="email" placeholder="Email" required />
          <i className="bx  bx-envelope"></i>
        </div>

        <div className="input-box third">
          <input type="password" placeholder="Password" required />
          <button
            className="bx bx-low-vision"
            type="button"
            aria-label="Show password"
          ></button>
        </div>

        <button type="submit" className="btn-glass">
          Sign Up
        </button>

        <p className="flex-gap">
          <span>Already have an account?</span>
          <Link to="/" className="sign-up button">
            Login
          </Link>
        </p>
      </form>
    </AuthLayout>
  );
}
