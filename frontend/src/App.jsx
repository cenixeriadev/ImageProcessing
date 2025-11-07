import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/login"; // 👈 te falta esta línea
import Home from "./pages/home";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
