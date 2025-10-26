import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/login";
import Register from "./components/register";
import Home from "./pages/home";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/Home" element={<Home />} />
        <Route path="/Register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
