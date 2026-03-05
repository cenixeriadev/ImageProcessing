import { Link } from "react-router-dom";
import "../styles/forgetpassword.css";
import AuthLayout from "../components/AuthLayout";

export default function ForgotPassword() {
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Forgot password submit");
  };
  return (
    <AuthLayout
      title="Forgot Password"
      description="We will send you an email with the steps to change your password"
    >
      <form className="contenido" onSubmit={handleSubmit}>
        <div className="input-box second">
          <input type="email" placeholder="Enter your Email" required />
          <i class="bx bx-envelope" />
        </div>

        <button type="submit" className="btn-glass">
          Send Link
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
