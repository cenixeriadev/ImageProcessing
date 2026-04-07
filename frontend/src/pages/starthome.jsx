import React, { useState, useRef } from "react";
import repoIcon from "../assets/Icons/folder.svg";
import "../styles/starthome.css";
import HomeLayout from "../components/homeheader";

export default function Home() {
  // NUEVO ESTADO: Guarda la información de la imagen seleccionada
  const [selectedImage, setSelectedImage] = useState(null);

  // Estado para saber si hay una imagen flotando sobre el cuadro
  const [isDragging, setIsDragging] = useState(false);

  // 1. Cuando la imagen entra al cuadro
  const handleDragOver = (e) => {
    e.preventDefault(); // CRUCIAL: Evita que el navegador abra la imagen en otra pestaña
    if (!selectedImage) setIsDragging(true); // Solo animar si no hay imagen
  };

  // 2. Cuando la imagen sale del cuadro sin soltarla
  const handleDragLeave = () => {
    setIsDragging(false);
  };

  // 3. Cuando el usuario SUELTA la imagen
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    if (selectedImage) return; // Si ya hay imagen, no aceptar más

    // Capturamos los archivos soltados
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      console.log("Imagen recibida con éxito:", files[0].name);
      // Aquí podrías llamar a una función para procesar la imagen
    }
  };

  // Función para procesar el archivo (clic o drop)
  const handleProcessFile = (file) => {
    // Validamos que sea una imagen
    if (!file.type.startsWith("image/")) {
      alert("Por favor, selecciona un archivo de imagen válido.");
      return;
    }

    // Creamos un objeto con la info y la URL temporal para el <img />
    const imageData = {
      name: file.name,
      size: (file.size / 1024 / 1024).toFixed(2) + " MB", // Convertimos bytes a MB
      url: URL.createObjectURL(file), // Genera un enlace local temporal
    };

    setSelectedImage(imageData);
    console.log("Imagen lista para procesar:", file);
  };

  const fileInputRef = useRef(null);
  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  // Manejar selección por clic
  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleProcessFile(file);
    }
  };

  // Función para quitar la imagen y volver al estado inicial
  const removeImage = () => {
    // Es buena práctica "revocar" la URL temporal para liberar memoria
    if (selectedImage) URL.revokeObjectURL(selectedImage.url);
    setSelectedImage(null);
    if (fileInputRef.current) fileInputRef.current.value = ""; // Resetea el input
  };

  return (
    <>
      <HomeLayout username="LOY" />{" "}
      <h1 className="tittlehome">Welcome to Image Processing</h1>
      {/* Agregamos los eventos al contenedor */}
      <div
        className={`square-upload ${isDragging ? "dragging" : ""} ${selectedImage ? "has-image" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {/* ESTADO 1: No hay imagen seleccionada (Muestra la zona de carga) */}
        {!selectedImage && (
          <>
            <p className="title-square">
              {isDragging
                ? "Drop it here!"
                : "Please try to insert or drag an image to start"}
            </p>

            <button className="custom-upload-btn" onClick={handleButtonClick}>
              <span>Seleccionar un archivo desde el dispositivo</span>
              <img src={repoIcon} alt="" aria-hidden="true" width="18" />
            </button>
          </>
        )}

        {/* ESTADO 2: Imagen seleccionada (Muestra la previsualización "Apple-style") */}
        {selectedImage && (
          <div className="image-preview-panel">
            {/* La imagen en miniatura */}
            <div className="preview-thumbnail">
              <img
                src={selectedImage.url}
                alt="Previsualización"
                className="img-fit"
              />
            </div>

            {/* Detalles del archivo */}
            <div className="file-details">
              <p className="file-name">{selectedImage.name}</p>
              <p className="file-size">{selectedImage.size}</p>
            </div>

            {/* Botón para quitar la imagen */}
            <button
              className="remove-image-btn"
              onClick={removeImage}
              aria-label="Quitar imagen"
            >
              <img src={trashIcon} alt="" aria-hidden="true" width="18" />
            </button>
          </div>
        )}

        {/* Este es el input real que el usuario NO VE */}
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: "none" }}
          accept=".jpg, .jpeg, .png, .webp"
          onChange={(e) =>
            console.log("Archivo seleccionado:", e.target.files[0])
          }
        />
      </div>
    </>
  );
}
