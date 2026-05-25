/**
 * loginView.js
 * View: Gestiona los formularios de login, registro, login facial y cámara.
 */

export class LoginView {
  constructor() {
    this.mensajeEl = document.getElementById('login-mensaje');
    this.video = document.getElementById('camara-video');
    this.canvas = document.getElementById('camara-canvas');
    this.placeholder = document.getElementById('camera-placeholder');
    this.btnActivar = document.getElementById('btn-activar-camara');
    this.btnCapturar = document.getElementById('btn-capturar');
    this.btnFacialLogin = document.getElementById('btn-login-facial');
  }

  mostrarTab(tabName) {
    // Desactivar todas las pestañas
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('activo'));
    document.querySelectorAll('.tab-content').forEach(c => {
      c.classList.add('oculta');
      c.classList.remove('activo');
    });

    // Activar la seleccionada
    const tabBtn = document.getElementById(`tab-${tabName}`);
    if (tabBtn) tabBtn.classList.add('activo');
    
    const contenido = document.getElementById(`tab-content-${tabName}`);
    if (contenido) {
      contenido.classList.remove('oculta');
      contenido.classList.add('activo');
    }
  }

  getCredentialsLogin() {
    const correo = document.getElementById('login-correo').value.trim();
    const password = document.getElementById('login-password').value.trim();
    return { correo, password };
  }

  getCredentialsRegistro() {
    const nombre = document.getElementById('reg-nombre').value.trim();
    const apodo = document.getElementById('reg-apodo').value.trim();
    const correo = document.getElementById('reg-correo').value.trim();
    const password = document.getElementById('reg-password').value.trim();
    return { nombre, apodo, correo, password };
  }

  getCorreoFacial() {
    return document.getElementById('facial-correo').value.trim();
  }

  mostrarMensaje(texto, tipo) {
    this.mensajeEl.textContent = texto;
    this.mensajeEl.className = `mensaje ${tipo}`;
    this.mensajeEl.classList.remove('oculto');
  }

  ocultarMensaje() {
    this.mensajeEl.classList.add('oculto');
  }

  limpiarFormularios() {
    document.getElementById('login-correo').value = '';
    document.getElementById('login-password').value = '';
    document.getElementById('reg-nombre').value = '';
    document.getElementById('reg-apodo').value = '';
    document.getElementById('reg-correo').value = '';
    document.getElementById('reg-password').value = '';
    document.getElementById('facial-correo').value = '';
  }

  iniciarStreamVideo(stream) {
    this.video.srcObject = stream;
    this.video.style.display = 'block';
    this.canvas.style.display = 'none';
    this.placeholder.style.display = 'none';
    
    this.btnActivar.classList.add('oculto');
    this.btnCapturar.classList.remove('oculto');
    this.btnCapturar.textContent = '📸 Capturar Foto';
  }

  capturarFotoEnCanvas() {
    this.canvas.width = this.video.videoWidth || 320;
    this.canvas.height = this.video.videoHeight || 320;

    const ctx = this.canvas.getContext('2d');
    
    // Voltear horizontalmente para efecto espejo idéntico al de la cámara
    ctx.translate(this.canvas.width, 0);
    ctx.scale(-1, 1);
    
    ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
    
    // Restaurar transformaciones
    ctx.setTransform(1, 0, 0, 1, 0, 0);

    // Guardar como base64
    const fotoUrl = this.canvas.toDataURL('image/jpeg', 0.8);

    // Mostrar foto capturada
    this.video.style.display = 'none';
    this.canvas.style.display = 'block';
    this.canvas.style.width = '100%';
    this.canvas.style.height = '100%';
    this.canvas.style.objectFit = 'cover';

    this.btnFacialLogin.disabled = false;
    this.btnCapturar.textContent = '🔄 Nueva foto';

    return fotoUrl;
  }

  resetearCamara() {
    this.canvas.style.display = 'none';
    this.video.style.display = 'none';
    this.placeholder.style.display = 'flex';
    this.btnActivar.classList.remove('oculto');
    this.btnCapturar.classList.add('oculto');
    this.btnFacialLogin.disabled = true;
  }
}
