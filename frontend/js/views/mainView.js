/**
 * mainView.js
 * View: Gestiona la barra superior, barra inferior, menú lateral, temas y notificaciones.
 */

export class MainView {
  constructor() {
    this.topbar = document.querySelector('.topbar');
    this.sidebar = document.getElementById('sidebar');
    this.overlay = document.getElementById('sidebar-overlay');
    this.toastContainer = document.getElementById('toast-container');
    this.btnToggleTema = document.getElementById('btn-toggle-tema');
    
    // Vistas principales
    this.pantallaLogin = document.getElementById('pantalla-login');
    this.pantallaApp = document.getElementById('pantalla-app');
  }

  mostrarPantalla(pantalla) {
    this.pantallaLogin.classList.add('oculta');
    this.pantallaApp.classList.add('oculta');

    if (pantalla === 'login') {
      this.pantallaLogin.classList.remove('oculta');
    } else if (pantalla === 'app') {
      this.pantallaApp.classList.remove('oculta');
    }
  }

  toggleSidebar() {
    this.sidebar.classList.toggle('abierto');
    this.overlay.classList.toggle('visible');
  }

  cerrarSidebar() {
    this.sidebar.classList.remove('abierto');
    this.overlay.classList.remove('visible');
  }

  aplicarTema(tema) {
    document.documentElement.setAttribute('data-theme', tema);
    if (this.btnToggleTema) {
      this.btnToggleTema.textContent = tema === 'dark' ? '☀️' : '🌙';
    }
  }

  toast(mensaje, tipo = 'exito') {
    const t = document.createElement('div');
    t.className = `toast ${tipo}`;
    t.textContent = mensaje;
    this.toastContainer.appendChild(t);
    setTimeout(() => t.remove(), 4000);
  }

  actualizarTopbar(usuario) {
    if (!usuario) return;
    const headerPuntos = document.getElementById('header-puntos');
    if (headerPuntos) headerPuntos.textContent = usuario.puntos_totales;

    const headerMonedas = document.getElementById('header-monedas');
    if (headerMonedas) headerMonedas.textContent = usuario.monedas_verdes;
  }

  actualizarSidebar(usuario) {
    if (!usuario) return;
    const sidebarNombre = document.getElementById('sidebar-nombre');
    if (sidebarNombre) sidebarNombre.textContent = usuario.apodo || usuario.nombre;

    const sidebarNivel = document.getElementById('sidebar-nivel');
    if (sidebarNivel) sidebarNivel.textContent = usuario.nivel;
  }

  actualizarMenuNavegacion(vistaActiva) {
    // Sidebar
    document.querySelectorAll('.sidebar-item').forEach(b => b.classList.remove('activo'));
    const navBtn = document.getElementById(`nav-${vistaActiva}`);
    if (navBtn) navBtn.classList.add('activo');

    // Bottom Nav
    document.querySelectorAll('.bottom-nav-item').forEach(b => b.classList.remove('activo'));
    const bnavBtn = document.getElementById(`bnav-${vistaActiva}`);
    if (bnavBtn) bnavBtn.classList.add('activo');
  }

  cambiarVista(vistaActiva) {
    document.querySelectorAll('.vista').forEach(v => v.classList.remove('activa'));
    const vistaEl = document.getElementById(`vista-${vistaActiva}`);
    if (vistaEl) {
      vistaEl.classList.add('activa');
    }
  }

  crearParticulas(containerId, cantidad) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = ''; // Limpiar existentes
    const colores = ['#52b788', '#95d5b2', '#2d6a4f', '#d8f3dc', '#f9c74f'];

    for (let i = 0; i < cantidad; i++) {
      const p = document.createElement('div');
      p.className = 'particle';
      const size = Math.random() * 40 + 10;
      p.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        background: ${colores[Math.floor(Math.random() * colores.length)]};
        --dur: ${Math.random() * 6 + 6}s;
        --delay: ${Math.random() * -10}s;
      `;
      container.appendChild(p);
    }
  }
}
