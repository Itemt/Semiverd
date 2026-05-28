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
    this.btnToggleTemas = document.querySelectorAll('.btn-toggle-tema');
    this.btnHamburguesa = document.getElementById('btn-hamburguesa');
    this.avatarWrapper = document.getElementById('avatar-wrapper');
    this.avatarDropdown = document.getElementById('avatar-dropdown');

    // Vistas principales
    this.pantallaLogin = document.getElementById('pantalla-login');
    this.pantallaApp = document.getElementById('pantalla-app');

    // Cerrar sidebar al redimensionar la pantalla (ej. al reducir el ancho)
    let lastWidth = window.innerWidth;
    window.addEventListener('resize', () => {
      const currentWidth = window.innerWidth;
      if (currentWidth !== lastWidth) {
        if (this.sidebar && this.sidebar.classList.contains('abierto')) {
          this.sidebar.classList.remove('abierto');
          if (this.pantallaApp) this.pantallaApp.classList.remove('sidebar-abierto');
          if (this.overlay) this.overlay.classList.remove('visible');
          if (this.btnHamburguesa) this.btnHamburguesa.classList.remove('hamburguesa-activo');
        }
        lastWidth = currentWidth;
      }
    });
  }

  mostrarPantalla(pantalla) {
    this.pantallaLogin.classList.add('oculta');
    this.pantallaApp.classList.add('oculta');

    if (pantalla === 'login') {
      this.pantallaLogin.classList.remove('oculta');
      // Limpiar estados de sidebar al ir al login
      this.sidebar.classList.remove('abierto');
      this.pantallaApp.classList.remove('sidebar-abierto');
      this.overlay.classList.remove('visible');
    } else if (pantalla === 'app') {
      this.pantallaApp.classList.remove('oculta');
    }
  }

  toggleSidebar() {
    const abierto = this.sidebar.classList.toggle('abierto');
    this.pantallaApp.classList.toggle('sidebar-abierto', abierto);
    
    // El overlay solo aplica en pantallas pequeñas (móvil/tablet < 1024px)
    if (window.innerWidth < 1024) {
      this.overlay.classList.toggle('visible', abierto);
    } else {
      this.overlay.classList.remove('visible');
    }

    // Animar hamburguesa
    if (this.btnHamburguesa) {
      this.btnHamburguesa.classList.toggle('hamburguesa-activo', abierto);
    }
  }

  cerrarSidebar() {
    // En desktop (>= 1024px) no colapsamos el sidebar al navegar.
    // Solo lo cerramos en pantallas móviles/tabletas.
    if (window.innerWidth < 1024) {
      this.sidebar.classList.remove('abierto');
      this.pantallaApp.classList.remove('sidebar-abierto');
      this.overlay.classList.remove('visible');
      if (this.btnHamburguesa) {
        this.btnHamburguesa.classList.remove('hamburguesa-activo');
      }
    }
  }

  toggleAvatarDropdown() {
    if (this.avatarDropdown) {
      this.avatarDropdown.classList.toggle('abierto');
    }
  }

  cerrarAvatarDropdown() {
    if (this.avatarDropdown) {
      this.avatarDropdown.classList.remove('abierto');
    }
  }

  aplicarTema(tema) {
    document.documentElement.setAttribute('data-theme', tema);
    this.btnToggleTemas.forEach(btn => {
      btn.textContent = tema === 'dark' ? '☀️' : '🌙';
    });
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

    // Actualizar avatar con foto si existe
    this._actualizarAvatar(usuario);
  }

  _actualizarAvatar(usuario) {
    const foto = usuario?.foto_perfil;
    const nombre = usuario?.apodo || usuario?.nombre || 'Guardián';
    const correo = usuario?.correo || '';

    // Topbar avatar
    const headerAvatar = document.getElementById('header-avatar');
    if (headerAvatar && foto) {
      headerAvatar.innerHTML = `<img src="${foto}" alt="Avatar" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" />`;
    }

    // Dropdown nombre y correo
    const ddNombre = document.getElementById('avatar-dd-nombre');
    if (ddNombre) ddNombre.textContent = nombre;

    const ddCorreo = document.getElementById('avatar-dd-correo');
    if (ddCorreo) ddCorreo.textContent = correo;

    const ddIcon = document.getElementById('avatar-dd-icon');
    if (ddIcon && foto) {
      ddIcon.innerHTML = `<img src="${foto}" alt="Avatar" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" />`;
    }
  }

  actualizarSidebar(usuario) {
    if (!usuario) return;
    const sidebarNombre = document.getElementById('sidebar-nombre');
    if (sidebarNombre) sidebarNombre.textContent = usuario.apodo || usuario.nombre;

    const sidebarNivel = document.getElementById('sidebar-nivel');
    if (sidebarNivel) sidebarNivel.textContent = usuario.nivel;

    // Avatar sidebar
    const sidebarAvatar = document.getElementById('sidebar-avatar-img');
    if (sidebarAvatar && usuario?.foto_perfil) {
      sidebarAvatar.innerHTML = `<img src="${usuario.foto_perfil}" alt="Avatar" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" />`;
    }
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
