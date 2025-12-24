import { Link } from "react-router-dom";
import PasswordLayout from "../components/PasswordLayout";
import "../styles/forgetpassword.css";

export default function ForgotPassword() {
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Forgot password submit");
  };
  return (
    <PasswordLayout
      title="Forgot Password"
      description="We will send you an email with the steps to change your password"
    >
      <form className="contenido" onSubmit={handleSubmit}>
        <div className="input-box second">
          <input type="email" placeholder="Enter your Email" required />
          <i className="bxr  bx-envelope"></i>
        </div>

        <button type="submit" className="btn-glass">
          Send Link
        </button>
      </form>
    </PasswordLayout>
  );
}
