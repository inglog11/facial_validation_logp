import React, { useState, useRef, useEffect } from 'react';
import { checkInAPI } from '../api';

function CheckIn() {
  const [employeeCode, setEmployeeCode] = useState('');
  const [stream, setStream] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    // Actualizar el video cuando cambie el stream
    if (videoRef.current && stream) {
      videoRef.current.srcObject = stream;
      videoRef.current.play().catch(err => {
        console.error('Error al reproducir video:', err);
      });
    }
    
    return () => {
      // Limpiar stream al desmontar
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      if (videoRef.current) {
        videoRef.current.srcObject = null;
      }
    };
  }, [stream]);

  const startCamera = async () => {
    try {
      setError(null);
      console.log('Solicitando acceso a la cámara...');
      
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { 
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        }
      });
      
      console.log('Stream obtenido:', mediaStream);
      console.log('Tracks:', mediaStream.getVideoTracks());
      
      setStream(mediaStream);
      
      // El useEffect se encargará de asignar el stream al video
    } catch (err) {
      console.error('Error al acceder a la cámara:', err);
      if (err.name === 'NotAllowedError') {
        setError('Permiso de cámara denegado. Por favor, permite el acceso a la cámara en la configuración del navegador.');
      } else if (err.name === 'NotFoundError') {
        setError('No se encontró ninguna cámara disponible.');
      } else {
        setError('Error al acceder a la cámara: ' + err.message);
      }
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
      if (videoRef.current) {
        videoRef.current.srcObject = null;
      }
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) {
      setError('Video no disponible para capturar');
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    // Verificar que el video tenga dimensiones válidas
    if (video.videoWidth === 0 || video.videoHeight === 0) {
      setError('El video aún no está listo. Espera un momento e intenta de nuevo.');
      return;
    }

    const context = canvas.getContext('2d');
    
    // Establecer dimensiones del canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Dibujar el frame del video en el canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convertir a base64
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    
    // Validar que la imagen no esté vacía
    if (!imageData || imageData === 'data:,' || imageData.length < 100) {
      setError('Error al capturar la imagen. Intenta de nuevo.');
      return;
    }
    
    console.log('Imagen capturada, tamaño:', imageData.length, 'primeros chars:', imageData.substring(0, 50));
    setCapturedImage(imageData);
    stopCamera();
  };

  const handleCheckIn = async () => {
    if (!employeeCode.trim()) {
      setError('Por favor ingrese el código de empleado');
      return;
    }

    if (!capturedImage) {
      setError('Por favor capture una foto primero');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await checkInAPI.checkIn(employeeCode, capturedImage);
      setResult(response.data);
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.response?.data?.details || err.message;
      setError('Error en check-in: ' + (typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage)));
      console.error('Error completo:', err.response?.data || err);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setCapturedImage(null);
    setResult(null);
    setError(null);
    stopCamera();
  };

  return (
    <div className="card">
      <h2>Registro de Entrada (Check-in)</h2>
      
      <div className="form-group">
        <label>Código de Empleado *</label>
        <input
          type="text"
          value={employeeCode}
          onChange={(e) => setEmployeeCode(e.target.value)}
          placeholder="Ej: EMP001"
          disabled={loading}
        />
      </div>

      <div className="camera-container">
        {!stream && !capturedImage && (
          <button onClick={startCamera} className="btn btn-primary">
            Iniciar Cámara
          </button>
        )}

        {stream && (
          <>
            <div style={{ position: 'relative', width: '100%', maxWidth: '640px', backgroundColor: '#000', borderRadius: '4px', overflow: 'hidden' }}>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="video-preview"
                onLoadedMetadata={() => {
                  console.log('Video metadata cargado:', {
                    width: videoRef.current?.videoWidth,
                    height: videoRef.current?.videoHeight,
                    readyState: videoRef.current?.readyState
                  });
                  if (videoRef.current) {
                    videoRef.current.play().catch(err => {
                      console.error('Error al reproducir:', err);
                    });
                  }
                }}
                onPlay={() => {
                  console.log('Video reproduciéndose');
                }}
                onError={(e) => {
                  console.error('Error en video:', e);
                  setError('Error en el video');
                }}
                style={{ 
                  width: '100%', 
                  height: 'auto',
                  minHeight: '360px',
                  display: 'block',
                  objectFit: 'cover'
                }}
              />
            </div>
            <div style={{ marginTop: '10px' }}>
              <button onClick={capturePhoto} className="btn btn-success">
                Capturar Foto
              </button>
              <button onClick={stopCamera} className="btn btn-secondary">
                Cancelar
              </button>
            </div>
          </>
        )}

        {capturedImage && (
          <>
            <img 
              src={capturedImage} 
              alt="Capturada"
              className="captured-image"
            />
            <div>
              <button 
                onClick={handleCheckIn} 
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Verificando...' : 'Verificar y Registrar'}
              </button>
              <button onClick={reset} className="btn btn-secondary">
                Capturar Otra Vez
              </button>
            </div>
          </>
        )}
      </div>

      <canvas ref={canvasRef} style={{ display: 'none' }} />

      {error && <div className="error">{error}</div>}

      {result && (
        <div className={`result-card ${result.decision ? 'result-success' : 'result-failure'}`}>
          <h3>{result.decision ? '✓ Check-in Exitoso' : '✗ Check-in Rechazado'}</h3>
          <div className="result-info">
            <p><strong>Score:</strong> {result.score.toFixed(4)}</p>
            <p><strong>Umbral:</strong> {result.threshold_used}</p>
            <p><strong>Empleado:</strong> {result.employee_code}</p>
            <p><strong>Timestamp:</strong> {new Date(result.timestamp).toLocaleString()}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default CheckIn;
