/**
 * perfilView.js
 * View: Gestiona la visualización del perfil del usuario y sus estadísticas individuales.
 */

export class PerfilView {
  constructor() {
    this.nombreEl = document.getElementById('perfil-nombre');
    this.nivelEl = document.getElementById('perfil-nivel');
    this.correoEl = document.getElementById('perfil-correo');
    this.puntosEl = document.getElementById('perfil-puntos');
    this.nivelArbolEl = document.getElementById('perfil-nivel-arbol');
    this.monedasEl = document.getElementById('perfil-monedas');
    this.misionesCompletadasEl = document.getElementById('perfil-misiones-completadas');
  }

  renderPerfil(usuario, misionesCompletadas) {
    if (!usuario) return;

    if (this.nombreEl) this.nombreEl.textContent = usuario.apodo || usuario.nombre;
    if (this.nivelEl) this.nivelEl.textContent = usuario.nivel;
    if (this.correoEl) this.correoEl.textContent = usuario.correo;
    if (this.puntosEl) this.puntosEl.textContent = usuario.puntos_totales;
    if (this.nivelArbolEl) this.nivelArbolEl.textContent = usuario.nivel_arbol;
    if (this.monedasEl) this.monedasEl.textContent = usuario.monedas_verdes;
    if (this.misionesCompletadasEl) this.misionesCompletadasEl.textContent = misionesCompletadas;
  }
}
