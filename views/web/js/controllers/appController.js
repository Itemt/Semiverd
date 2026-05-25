/**
 * appController.js
 * Controller: Coopera entre el StateModel (Model) y las diversas Vistas.
 */

export class AppController {
  constructor(model, views) {
    this.model = model;
    this.mainView = views.mainView;
    this.loginView = views.loginView;
    this.homeView = views.homeView;
    this.treeView = views.treeView;
    this.mapView = views.mapView;
    this.missionView = views.missionView;
    this.academiaView = views.academiaView;
    this.rankingView = views.rankingView;
    this.perfilView = views.perfilView;

    this.animFrameArbol = null;
  }

  inicializar() {
    // 1. Cargar tema guardado
    const temaGuardado = localStorage.getItem('semiverd_tema') || 'dark';
    this.mainView.aplicarTema(temaGuardado);

    // 2. Crear partículas flotantes
    this.mainView.crearParticulas('particles-login', 15);

    // 3. Vincular manejadores de eventos
    this.vincularEventos();

    // 4. Iniciar bucle de animación para el árbol
    this.iniciarAnimacionArbol();

    // 5. Verificar sesión existente
    const sesionActiva = this.model.cargarSesionGuardada();
    if (sesionActiva) {
      this.entrarApp();
    } else {
      this.mainView.mostrarPantalla('login');
      this.loginView.mostrarTab('facial');
    }

    // 6. Ocultar y remover el Splash Screen tras 2.5 segundos
    setTimeout(() => {
      const splash = document.getElementById('splash-screen');
      if (splash) {
        splash.classList.add('fadeout');
        setTimeout(() => {
          splash.remove();
        }, 600);
      }
    }, 2500);
  }

  vincularEventos() {
    // Manejo de pestañas de login
    document.getElementById('tab-facial').addEventListener('click', () => this.loginView.mostrarTab('facial'));
    document.getElementById('tab-correo').addEventListener('click', () => this.loginView.mostrarTab('correo'));
    document.getElementById('tab-registro').addEventListener('click', () => this.loginView.mostrarTab('registro'));

    // Botones de acción de login
    document.querySelector('#tab-content-correo button').addEventListener('click', () => this.ejecutarLoginCorreo());
    document.querySelector('#tab-content-registro button').addEventListener('click', () => this.ejecutarRegistro());
    document.querySelector('.btn-demo').addEventListener('click', () => this.ejecutarDemo());

    // Cámara y facial login
    this.loginView.btnActivar.addEventListener('click', () => this.activarCamara());
    this.loginView.btnCapturar.addEventListener('click', () => this.capturarFoto());
    this.loginView.btnFacialLogin.addEventListener('click', () => this.ejecutarLoginFacial());

    // Navegación Sidebar y Bottom Nav
    const routes = ['inicio', 'arbol', 'camino', 'misiones', 'academia', 'ranking', 'perfil'];
    routes.forEach(route => {
      const navBtn = document.getElementById(`nav-${route}`);
      if (navBtn) {
        navBtn.addEventListener('click', () => this.irA(route));
      }
      const bnavBtn = document.getElementById(`bnav-${route}`);
      if (bnavBtn) {
        bnavBtn.addEventListener('click', () => this.irA(route));
      }
    });

    // Control del sidebar
    document.querySelector('.topbar-menu-btn').addEventListener('click', () => this.mainView.toggleSidebar());
    this.mainView.overlay.addEventListener('click', () => this.mainView.cerrarSidebar());
    
    // Tema claro/oscuro
    this.mainView.btnToggleTema.addEventListener('click', () => this.toggleTema());

    // Cerrar sesión
    document.querySelector('.sidebar-logout').addEventListener('click', () => this.cerrarSesion());
    document.querySelector('.perfil-card .btn-danger').addEventListener('click', () => this.cerrarSesion());

    // Filtros de la academia
    document.querySelectorAll('.filtros-categoria .filtro-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const cat = e.target.getAttribute('onclick')?.match(/'([^']+)'/)?.[1] || null;
        // Evitamos usar el atributo inline onclick y añadimos lógica nativa
        let filterCat = null;
        if (e.target.textContent.includes('Jardín')) filterCat = 'jardinería';
        else if (e.target.textContent.includes('Agua')) filterCat = 'agua';
        else if (e.target.textContent.includes('Energía')) filterCat = 'energia';
        else if (e.target.textContent.includes('Reciclaje')) filterCat = 'reciclaje';

        this.academiaView.actualizarFiltrosActivos(e.target);
        this.academiaView.renderTips(this.model.tips, filterCat);
      });
    });

    // Modal cerrar y Escape
    document.querySelector('.modal-cerrar').addEventListener('click', () => this.missionView.cerrarModal());
    document.querySelector('.modal-backdrop').addEventListener('click', () => this.missionView.cerrarModal());
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') this.missionView.cerrarModal();
    });
  }

  async ejecutarLoginCorreo() {
    const { correo, password } = this.loginView.getCredentialsLogin();
    if (!correo || !password) {
      this.loginView.mostrarMensaje('Por favor, completa todos los campos 🌱', 'error');
      return;
    }

    this.loginView.mostrarMensaje('Verificando credenciales...', '');
    try {
      await this.model.loginCorreo(correo, password);
      this.entrarApp();
    } catch (err) {
      this.loginView.mostrarMensaje(err.message || 'Error al iniciar sesión. Verifica tus datos.', 'error');
    }
  }

  async ejecutarRegistro() {
    const { nombre, apodo, correo, password } = this.loginView.getCredentialsRegistro();
    if (!nombre || !correo || !password) {
      this.loginView.mostrarMensaje('Por favor, completa nombre, correo y contraseña 🌱', 'error');
      return;
    }

    if (password.length < 6) {
      this.loginView.mostrarMensaje('La contraseña debe tener al menos 6 caracteres', 'error');
      return;
    }

    this.loginView.mostrarMensaje('Creando tu cuenta de guardián...', '');
    try {
      await this.model.registrarUsuario(nombre, apodo, correo, password);
      this.loginView.mostrarMensaje('¡Bienvenido a las Semillas Verdes! 🌱', 'exito');
      setTimeout(() => this.entrarApp(), 1000);
    } catch (err) {
      this.loginView.mostrarMensaje(err.message || 'Error al crear la cuenta. Inténtalo de nuevo.', 'error');
    }
  }

  ejecutarDemo() {
    this.model.activarDemo();
    this.entrarApp();
  }

  async activarCamara() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 640 } },
        audio: false
      });

      this.model.streamCamara = stream;
      this.loginView.iniciarStreamVideo(stream);
      this.loginView.mostrarMensaje('¡Cámara activa! Centra tu cara en el círculo y captura 📷', 'exito');
    } catch (err) {
      this.loginView.mostrarMensaje('No se pudo acceder a la cámara. Verifica los permisos.', 'error');
      console.warn('Error cámara:', err);
    }
  }

  capturarFoto() {
    if (this.loginView.btnCapturar.textContent.includes('Nueva foto')) {
      this.model.fotoCapturada = null;
      this.loginView.resetearCamara();
      this.activarCamara();
    } else {
      const fotoUrl = this.loginView.capturarFotoEnCanvas();
      this.model.fotoCapturada = fotoUrl;

      // Detener stream
      if (this.model.streamCamara) {
        this.model.streamCamara.getTracks().forEach(t => t.stop());
        this.model.streamCamara = null;
      }
      this.loginView.mostrarMensaje('¡Foto capturada! Escribe tu correo y entra como guardián 🌿', 'exito');
    }
  }

  async ejecutarLoginFacial() {
    const correo = this.loginView.getCorreoFacial();
    if (!this.model.fotoCapturada) {
      this.loginView.mostrarMensaje('Primero captura tu foto 📷', 'error');
      return;
    }

    this.loginView.mostrarMensaje('Verificando identidad...', '');
    try {
      await this.model.loginFacial(correo, this.model.fotoCapturada);
      this.mainView.toast('¡Identidad verificada! Bienvenido guardián 🌿', 'exito');
      this.entrarApp();
    } catch (err) {
      this.loginView.mostrarMensaje(err.message || 'Error en el reconocimiento facial. Intenta de nuevo.', 'error');
    }
  }

  cerrarSesion() {
    this.model.cerrarSesion();
    this.loginView.limpiarFormularios();
    this.loginView.resetearCamara();
    this.mainView.mostrarPantalla('login');
    this.loginView.mostrarTab('correo');
    this.mainView.toast('¡Hasta pronto! Sigue cuidando el planeta 🌿', 'exito');
  }

  toggleTema() {
    const actual = document.documentElement.getAttribute('data-theme') || 'dark';
    const nuevo = actual === 'dark' ? 'light' : 'dark';
    this.mainView.aplicarTema(nuevo);
    localStorage.setItem('semiverd_tema', nuevo);
    this.mainView.toast(nuevo === 'light' ? '☀️ Modo claro activado' : '🌙 Modo oscuro activado', 'exito');
  }

  entrarApp() {
    this.mainView.mostrarPantalla('app');
    this.mainView.actualizarTopbar(this.model.usuario);
    this.mainView.actualizarSidebar(this.model.usuario);
    this.irA('inicio');
    
    // Cargar datos
    this.cargarDatosApp();
  }

  async cargarDatosApp() {
    await this.model.fetchMisiones();
    this.homeView.renderRecentMisiones(this.model.misiones, (id) => this.abrirDetalleMision(id));
    
    const tipDia = await this.model.fetchTipDelDia();
    this.academiaView.renderTipDelDia(tipDia);

    await this.model.fetchTips();
  }

  async irA(vista) {
    this.model.vistaActual = vista;
    this.mainView.cambiarVista(vista);
    this.mainView.actualizarMenuNavegacion(vista);
    this.mainView.cerrarSidebar();

    const completadasCount = this.model.misiones.filter(m => m.estado === 'completada').length;

    switch (vista) {
      case 'inicio':
        this.homeView.actualizarBienvenida(this.model.usuario);
        this.homeView.renderRecentMisiones(this.model.misiones, (id) => this.abrirDetalleMision(id));
        break;
      case 'arbol':
        this.treeView.actualizarInfoNivel(this.model.usuario, completadasCount);
        this.treeView.renderMedallas(this.model.misiones);
        this.treeView.dibujarArbol(this.model.usuario.nivel_arbol);
        break;
      case 'camino':
        this.mapView.renderMapa(this.model.misiones, (id) => this.abrirDetalleMision(id));
        break;
      case 'misiones':
        this.missionView.renderMisiones(this.model.misiones, (id) => this.abrirDetalleMision(id));
        break;
      case 'academia':
        this.academiaView.renderTips(this.model.tips);
        // Reset active filter button state
        const allBtn = document.querySelector('.filtros-categoria .filtro-btn');
        this.academiaView.actualizarFiltrosActivos(allBtn);
        break;
      case 'ranking':
        const ranking = await this.model.fetchRanking();
        this.rankingView.renderRanking(ranking);
        break;
      case 'perfil':
        this.perfilView.renderPerfil(this.model.usuario, completadasCount);
        break;
    }
  }

  abrirDetalleMision(misionId) {
    const m = this.model.misiones.find(x => x.id === misionId);
    if (!m) return;

    const callbacks = {
      onIniciar: (id) => this.ejecutarIniciarMision(id),
      onCompletar: (id) => this.ejecutarCompletarMision(id)
    };

    this.missionView.abrir(m, callbacks);
  }

  async ejecutarIniciarMision(misionId) {
    try {
      await this.model.iniciarMision(misionId);
      this.missionView.cerrarModal();
      this.mainView.toast('¡Misión iniciada! ¡A proteger el planeta! 🌿', 'exito');
      
      // Actualizar vista actual
      if (this.model.vistaActual === 'misiones') {
        this.missionView.renderMisiones(this.model.misiones, (id) => this.abrirDetalleMision(id));
      } else if (this.model.vistaActual === 'camino') {
        this.mapView.renderMapa(this.model.misiones, (id) => this.abrirDetalleMision(id));
      } else {
        this.irA(this.model.vistaActual);
      }
    } catch (err) {
      this.mainView.toast(err.message || 'Error al iniciar la misión', 'error');
    }
  }

  async ejecutarCompletarMision(misionId) {
    try {
      const res = await this.model.completarMision(misionId);
      this.missionView.cerrarModal();
      this.mainView.toast(`🎉 ¡+${res.puntos_ganados} puntos! ¡Misión completada!`, 'exito');
      
      // Sincronizar UI
      this.mainView.actualizarTopbar(this.model.usuario);
      this.mainView.actualizarSidebar(this.model.usuario);

      if (this.model.vistaActual === 'misiones') {
        this.missionView.renderMisiones(this.model.misiones, (id) => this.abrirDetalleMision(id));
      } else if (this.model.vistaActual === 'camino') {
        this.mapView.renderMapa(this.model.misiones, (id) => this.abrirDetalleMision(id));
      } else {
        this.irA(this.model.vistaActual);
      }
    } catch (err) {
      this.mainView.toast(err.message || 'Error al completar la misión', 'error');
    }
  }

  iniciarAnimacionArbol() {
    const animar = () => {
      if (this.model.vistaActual === 'arbol') {
        this.treeView.dibujarArbol(this.model.usuario?.nivel_arbol || 1);
      } else if (this.model.vistaActual === 'inicio' && this.model.usuario) {
        this.homeView.dibujarArbolMini(
          this.model.usuario.nivel_arbol || 1, 
          this.treeView.dibujarRama.bind(this.treeView)
        );
      }
      this.animFrameArbol = requestAnimationFrame(animar);
    };
    animar();
  }
}
