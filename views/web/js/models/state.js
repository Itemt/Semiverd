/**
 * state.js
 * Model: Gestiona el estado de la aplicación, llamadas a la API y persistencia local.
 */

import { API_BASE, DATOS_DEMO } from '../config.js';

export class StateModel {
  constructor() {
    this.token = null;
    this.usuario = null;
    this.misiones = [];
    this.tips = [];
    this.vistaActual = 'inicio';
    this.streamCamara = null;
    this.fotoCapturada = null;
    this.misionesCargadas = false;
  }

  isDemo() {
    return this.token === 'demo-token';
  }

  cargarSesionGuardada() {
    const tokenGuardado = localStorage.getItem('semiverd_token');
    const usuarioGuardado = localStorage.getItem('semiverd_usuario');
    const demoActivo = localStorage.getItem('semiverd_demo');

    if (demoActivo === 'true') {
      this.token = 'demo-token';
      this.usuario = DATOS_DEMO.usuario;
      this.misiones = DATOS_DEMO.misiones;
      this.tips = DATOS_DEMO.tips;
      return true;
    }

    if (tokenGuardado && usuarioGuardado) {
      this.token = tokenGuardado;
      this.usuario = JSON.parse(usuarioGuardado);
      return true;
    }

    return false;
  }

  async verificarToken() {
    if (this.isDemo()) return true;
    try {
      this.usuario = await this.api('GET', '/auth/yo');
      this.guardarSesion();
      return true;
    } catch (err) {
      this.cerrarSesion();
      return false;
    }
  }

  guardarSesion() {
    localStorage.setItem('semiverd_token', this.token);
    localStorage.setItem('semiverd_usuario', JSON.stringify(this.usuario));
    localStorage.removeItem('semiverd_demo');
  }

  activarDemo() {
    this.usuario = { ...DATOS_DEMO.usuario };
    this.token = 'demo-token';
    this.misiones = JSON.parse(JSON.stringify(DATOS_DEMO.misiones)); // Deep copy
    this.tips = [...DATOS_DEMO.tips];
    localStorage.setItem('semiverd_demo', 'true');
    localStorage.removeItem('semiverd_token');
    localStorage.removeItem('semiverd_usuario');
  }

  cerrarSesion() {
    this.token = null;
    this.usuario = null;
    this.misiones = [];
    this.tips = [];
    this.misionesCargadas = false;
    this.fotoCapturada = null;
    
    if (this.streamCamara) {
      this.streamCamara.getTracks().forEach(t => t.stop());
      this.streamCamara = null;
    }

    localStorage.removeItem('semiverd_token');
    localStorage.removeItem('semiverd_usuario');
    localStorage.removeItem('semiverd_demo');
  }

  async api(metodo, ruta, cuerpo = null) {
    const opciones = {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
    };

    if (this.token && this.token !== 'demo-token') {
      opciones.headers['Authorization'] = `Bearer ${this.token}`;
    }

    if (cuerpo) {
      opciones.body = JSON.stringify(cuerpo);
    }

    const respuesta = await fetch(`${API_BASE}${ruta}`, opciones);

    if (respuesta.status === 401) {
      // Si el 401 viene del login, no recargar la página (mostrar error en UI en vez de matar la sesión)
      if (!ruta.includes('/auth/login')) {
        this.cerrarSesion();
        window.location.reload();
        throw new Error("Sesión expirada. Por favor, ingresa de nuevo.");
      }
    }

    if (!respuesta.ok) {
      let mensajeError = `Error ${respuesta.status}`;
      try {
        const error = await respuesta.json();
        const detail = error.detail;

        if (typeof detail === 'string') {
          // Caso común: detail es un string directo
          mensajeError = detail;
        } else if (Array.isArray(detail)) {
          // Caso Pydantic 422: detail es un array de objetos de validación
          // Extraer el primer mensaje legible
          const primerError = detail[0];
          if (primerError?.msg) {
            // Limpiar el prefijo "Value error, " que añade Pydantic
            mensajeError = primerError.msg.replace(/^Value error,\s*/i, '');
          } else if (primerError?.message) {
            mensajeError = primerError.message;
          } else {
            mensajeError = 'Datos inválidos. Revisa los campos e intenta de nuevo.';
          }
        } else if (detail && typeof detail === 'object') {
          mensajeError = detail.message || detail.msg || JSON.stringify(detail);
        } else if (error.message) {
          mensajeError = error.message;
        }
      } catch (_) {
        // respuesta no era JSON — mantener el mensaje genérico
      }
      throw new Error(mensajeError);
    }

    return respuesta.json();
  }

  async loginCorreo(correo, password) {
    const respuesta = await this.api('POST', '/auth/login', { correo, password });
    this.token = respuesta.access_token;
    this.usuario = respuesta.usuario;
    this.guardarSesion();
    return respuesta;
  }

  async registrarUsuario(nombre, apodo, correo, password) {
    await this.api('POST', '/auth/registrar', { nombre, apodo, correo, password });
    // Auto login
    return this.loginCorreo(correo, password);
  }

  async loginFacial(correo, fotoBase64) {
    const respuesta = await this.api('POST', '/auth/login-facial', {
      imagen_base64: fotoBase64,
      correo: correo || null
    });
    this.token = respuesta.access_token;
    this.usuario = respuesta.usuario;
    this.guardarSesion();
    return respuesta;
  }

  async loginFacialConNombre(correo, nombre, password, fotoBase64) {
    const respuesta = await this.api('POST', '/auth/login-facial', {
      imagen_base64: fotoBase64,
      correo: correo || null,
      nombre: nombre || null,
      password: password || null
    });
    this.token = respuesta.access_token;
    this.usuario = respuesta.usuario;
    this.guardarSesion();
    return respuesta;
  }

  async actualizarPerfil({ nombre, apodo, foto_perfil }) {
    if (this.isDemo()) {
      if (nombre !== undefined && nombre !== null) {
        this.usuario.nombre = nombre;
        this.usuario.apodo = apodo || nombre;
      }
      if (foto_perfil !== undefined && foto_perfil !== null) {
        this.usuario.foto_perfil = foto_perfil;
      }
      this.guardarSesion();
      return this.usuario;
    }
    const respuesta = await this.api('PUT', '/usuarios/perfil', {
      nombre: nombre || null,
      apodo: apodo || null,
      foto_perfil: foto_perfil || null
    });
    this.usuario = respuesta;
    this.guardarSesion();
    return respuesta;
  }

  async fetchMisiones() {
    if (this.isDemo()) {
      return this.misiones;
    }

    try {
      const misiones = await this.api('GET', '/misiones/');
      this.misiones = misiones;
      this.misionesCargadas = true;
    } catch (err) {
      console.warn('Error cargando misiones desde API, usando demo:', err);
      if (!this.misiones.length) {
        this.misiones = JSON.parse(JSON.stringify(DATOS_DEMO.misiones));
      }
    }
    return this.misiones;
  }

  async fetchTips() {
    if (this.isDemo()) {
      this.tips = DATOS_DEMO.tips;
      return this.tips;
    }

    try {
      const todos = await this.api('GET', '/tips/');
      this.tips = todos;
    } catch {
      if (!this.tips.length) {
        this.tips = DATOS_DEMO.tips;
      }
    }
    return this.tips;
  }

  async fetchTipDelDia() {
    if (this.isDemo()) {
      const hoy = new Date().getDay();
      return this.tips[hoy % this.tips.length] || DATOS_DEMO.tips[0];
    }

    try {
      return await this.api('GET', '/tips/diario');
    } catch (err) {
      return this.tips[0] || DATOS_DEMO.tips[0];
    }
  }

  async iniciarMision(misionId) {
    if (this.isDemo()) {
      const m = this.misiones.find(x => x.id === misionId);
      if (m) m.estado = 'en_progreso';
      return m;
    }

    await this.api('POST', `/misiones/${misionId}/iniciar`);
    const m = this.misiones.find(x => x.id === misionId);
    if (m) m.estado = 'en_progreso';
    return m;
  }

  async completarMision(misionId) {
    if (this.isDemo()) {
      const m = this.misiones.find(x => x.id === misionId);
      if (m) {
        const puntosGanados = m.puntos_recompensa;
        m.estado = 'completada';
        m.porcentaje_completado = 100;
        m.puntos_ganados = puntosGanados;
        this.usuario.puntos_totales += puntosGanados;
        this.usuario.monedas_verdes += m.monedas_recompensa;
        this.usuario.nivel_arbol = this.calcularNivelArbol(this.usuario.puntos_totales);

        // Recalcular nivel del usuario
        let n = 'Semilla';
        if (this.usuario.puntos_totales >= 1200) n = 'Maestro del Bosque';
        else if (this.usuario.puntos_totales >= 700) n = 'Guardián';
        else if (this.usuario.puntos_totales >= 350) n = 'Árbol';
        else if (this.usuario.puntos_totales >= 100) n = 'Brote';
        this.usuario.nivel = n;

        // Desbloquear la siguiente misión
        const siguiente = this.misiones.find(x => x.orden === m.orden + 1);
        if (siguiente && siguiente.estado === 'bloqueada') {
          siguiente.estado = 'disponible';
        }
      }
      return {
        puntos_ganados: m?.puntos_recompensa || 0,
        puntos_totales: this.usuario.puntos_totales,
        nivel: this.usuario.nivel,
        nivel_arbol: this.usuario.nivel_arbol
      };
    }

    const resultado = await this.api('POST', `/misiones/${misionId}/completar`);
    const m = this.misiones.find(x => x.id === misionId);
    if (m) {
      m.estado = 'completada';
      m.porcentaje_completado = 100;
      
      // Desbloquear la siguiente misión localmente para actualizar la UI
      const siguiente = this.misiones.find(x => x.orden === m.orden + 1);
      if (siguiente && siguiente.estado === 'bloqueada') {
        siguiente.estado = 'disponible';
      }
    }
    this.usuario.puntos_totales = resultado.puntos_totales;
    this.usuario.nivel          = resultado.nivel;
    this.usuario.nivel_arbol    = resultado.nivel_arbol;

    return resultado;
  }

  calcularNivelArbol(puntos) {
    if (puntos < 100)  return 1;
    if (puntos < 250)  return 2;
    if (puntos < 450)  return 3;
    if (puntos < 700)  return 4;
    if (puntos < 1000) return 5;
    if (puntos < 1350) return 6;
    if (puntos < 1750) return 7;
    if (puntos < 2200) return 8;
    if (puntos < 2700) return 9;
    return 10;
  }

  async fetchRanking() {
    const rankingDemo = [
      { posicion: 1, nombre: 'Juliana G.', apodo: 'Guardiana del Río',     puntos_totales: 1200, nivel: 'Guardián', nivel_arbol: 8 },
      { posicion: 2, nombre: 'Sofía M.',   apodo: 'Reforestadora Mayor',   puntos_totales: 950,  nivel: 'Árbol',    nivel_arbol: 6 },
      { posicion: 3, nombre: 'Camila P.',  apodo: 'Maestra del Reciclaje', puntos_totales: 700,  nivel: 'Árbol',    nivel_arbol: 5 },
      { posicion: 4, nombre: 'Giohan R.', apodo: 'Ingeniero Verde',        puntos_totales: 450,  nivel: 'Brote',    nivel_arbol: 3 },
      { posicion: 5, nombre: this.usuario?.nombre || 'Tú', apodo: this.usuario?.apodo || 'Nuevo Guardián', puntos_totales: this.usuario?.puntos_totales || 0, nivel: this.usuario?.nivel || 'Semilla', nivel_arbol: this.usuario?.nivel_arbol || 1 },
    ];

    if (this.isDemo()) {
      return rankingDemo;
    }

    try {
      return await this.api('GET', '/usuarios/ranking');
    } catch {
      return rankingDemo;
    }
  }
}
