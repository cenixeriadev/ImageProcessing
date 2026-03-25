import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/login";
import Register from "./pages/register";
import ForgotPassword from "./pages/forgotpassword";
import ImageInput from "./pages/BeginImage";
import NewPassword from "./pages/newpassword";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/new-password" element={<NewPassword />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/Initialize" element={<ImageInput />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
