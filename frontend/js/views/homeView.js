/**
 * homeView.js
 * View: Gestiona el panel de bienvenida y el dibujo del árbol miniatura (Canvas).
 */

import { PUNTOS_NIVEL } from '../config.js';

export class HomeView {
  constructor() {
    this.canvas = document.getElementById('arbol-mini-canvas');
    this.bienvenidaEl = document.getElementById('bienvenida-nombre');
    this.arbolTextoEl = document.getElementById('arbol-nivel-texto');
    this.progressBarEl = document.getElementById('arbol-progress-bar');
    this.progressLabelEl = document.getElementById('arbol-progress-label');
    this.misionesContainer = document.getElementById('misiones-inicio');
  }

  actualizarBienvenida(usuario) {
    if (!usuario) return;
    if (this.bienvenidaEl) {
      this.bienvenidaEl.textContent = usuario.apodo || usuario.nombre;
    }
    if (this.arbolTextoEl) {
      this.arbolTextoEl.textContent = `Nivel ${usuario.nivel_arbol} - ${usuario.nivel}`;
    }

    const puntosNivel = PUNTOS_NIVEL[usuario.nivel] || 100;
    const porcentaje = Math.min(100, (usuario.puntos_totales / puntosNivel) * 100);

    if (this.progressBarEl) {
      this.progressBarEl.style.width = `${porcentaje}%`;
    }
    if (this.progressLabelEl) {
      this.progressLabelEl.textContent = `${usuario.puntos_totales} / ${puntosNivel} puntos`;
    }
  }

  renderRecentMisiones(misiones, onMisionClick) {
    if (!this.misionesContainer) return;
    this.misionesContainer.innerHTML = '';
    
    const recientes = misiones.slice(0, 4);
    recientes.forEach(m => {
      const card = document.createElement('div');
      card.className = `mision-mini-card ${m.estado === 'bloqueada' ? 'bloqueada' : ''}`;
      
      if (m.estado !== 'bloqueada') {
        card.addEventListener('click', () => onMisionClick(m.id));
      }
      
      card.innerHTML = `
        <div class="mision-mini-icono">${m.icono_emoji}</div>
        <div class="mision-mini-zona">${m.nombre_zona.toUpperCase()}</div>
        <div class="mision-mini-titulo">${m.titulo.split(':')[1]?.trim() || m.titulo}</div>
        <div class="mision-mini-pts">${m.estado === 'completada' ? '✅ Completada' : '⭐ ' + m.puntos_recompensa + ' pts'}</div>
      `;
      this.misionesContainer.appendChild(card);
    });
  }

  dibujarArbolMini(nivelArbol, dibujarRamaFn) {
    if (!this.canvas) return;
    const ctx = this.canvas.getContext('2d');
    const W = this.canvas.width;
    const H = this.canvas.height;

    ctx.clearRect(0, 0, W, H);

    // Fondo degradado cielo nocturno/selva
    const bg = ctx.createLinearGradient(0, 0, 0, H);
    bg.addColorStop(0, '#071a10');
    bg.addColorStop(1, '#1a4a2a');
    ctx.fillStyle = bg;
    ctx.roundRect(0, 0, W, H, 12);
    ctx.fill();

    // Suelo
    ctx.fillStyle = '#2d6a4f';
    ctx.roundRect(0, H - 14, W, 14, [0, 0, 12, 12]);
    ctx.fill();

    const alturaBase = H * 0.35 + (nivelArbol / 10) * H * 0.25;
    
    // Llamar a la función recursiva de dibujo compartida
    dibujarRamaFn(ctx, W / 2, H - 14, -Math.PI / 2, alturaBase, 5 + nivelArbol, nivelArbol, 0);
  }
}
