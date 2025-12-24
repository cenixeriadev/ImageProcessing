import { Link } from "react-router-dom";
import PasswordLayout from "../components/PasswordLayout";
import "../styles/newpassword.css";

export default function Register() {
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Register submit");
  };
  return (
    <PasswordLayout
      title="New Password"
      description="Hi, Welcome to the Image Processing please complete each gap with your personal data"
    >
      <form className="contenido" onSubmit={handleSubmit}>
        <div className="input-box second">
          <input type="email" placeholder="Email" required />
          <i className="bx  bx-envelope"></i>
        </div>

        <button type="submit" className="btn-glass">
          Submit
        </button>
      </form>
    </PasswordLayout>
  );
}
