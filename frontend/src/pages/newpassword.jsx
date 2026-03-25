import { Link } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import "../styles/newpassword.css";

export default function NewPassword() {
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Register submit");
  };
  return (
    <AuthLayout
      title="New Password"
      description="Please, enter a new password, check that has at least one special character"
    >
      <form className="contenido" onSubmit={handleSubmit}>
        <div className="input-box">
          <input
            type="password"
            name="password"
            placeholder="Enter your new Password"
            required
          />
          <button
            className="bx bx-low-vision"
            type="button"
            aria-label="Show password"
          ></button>
        </div>

        <div className="input-box second">
          <input
            type="password"
            name="ConfirmPassword"
            placeholder="Reconfirm your password"
            required
          />
          <button
            className="bx bx-low-vision"
            type="button"
            aria-label="Show password"
          ></button>
        </div>

        <button type="submit" className="btn-glass">
          Submit
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
