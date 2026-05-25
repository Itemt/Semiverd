/**
 * treeView.js
 * View: Gestiona el canvas principal del árbol, estadísticas de progreso y medallas.
 */

import { NIVELES_ARBOL } from '../config.js';

export class TreeView {
  constructor() {
    this.canvas = document.getElementById('arbol-canvas');
    this.badgeEl = document.getElementById('arbol-nivel-badge');
    this.tituloEl = document.getElementById('arbol-titulo-nivel');
    this.descEl = document.getElementById('arbol-descripcion');
    
    // Elementos de estadísticas
    this.statPuntos = document.getElementById('stat-puntos');
    this.statMisiones = document.getElementById('stat-misiones');
    this.statMonedas = document.getElementById('stat-monedas');
    this.statRacha = document.getElementById('stat-racha');
    
    // Contenedor de medallas
    this.medallasContainer = document.getElementById('medallas-container');
  }

  actualizarInfoNivel(usuario, misionesCompletadas) {
    if (!usuario) return;
    
    const infoNivel = NIVELES_ARBOL[Math.min(usuario.nivel_arbol - 1, 9)];
    
    if (this.badgeEl) this.badgeEl.textContent = `Nivel ${usuario.nivel_arbol}`;
    if (this.tituloEl) this.tituloEl.textContent = infoNivel.titulo;
    if (this.descEl) this.descEl.textContent = infoNivel.desc;

    // Stats
    if (this.statPuntos) this.statPuntos.textContent = usuario.puntos_totales;
    if (this.statMisiones) this.statMisiones.textContent = misionesCompletadas;
    if (this.statMonedas) this.statMonedas.textContent = usuario.monedas_verdes;
    if (this.statRacha) this.statRacha.textContent = usuario.racha_dias || 0;
  }

  renderMedallas(misiones) {
    if (!this.medallasContainer) return;
    
    const medallas = [];
    misiones.forEach(m => {
      if (m.estado === 'completada') {
        medallas.push({ nombre: `Guardián de ${m.nombre_zona}`, icono: m.icono_emoji });
      }
    });

    if (medallas.length === 0) {
      this.medallasContainer.innerHTML = '<p class="empty-state">Completa misiones para ganar medallas 🌱</p>';
      return;
    }

    this.medallasContainer.innerHTML = '';
    medallas.forEach(med => {
      const card = document.createElement('div');
      card.className = 'medalla-card';
      card.innerHTML = `
        <span class="medalla-icono">${med.icono}</span>
        <div class="medalla-nombre">${med.nombre}</div>
      `;
      this.medallasContainer.appendChild(card);
    });
  }

  dibujarArbol(nivelArbol) {
    if (!this.canvas) return;
    const ctx = this.canvas.getContext('2d');
    const W = this.canvas.width;
    const H = this.canvas.height;

    ctx.clearRect(0, 0, W, H);

    // Fondo degradado cielo nocturno
    const bgGrad = ctx.createLinearGradient(0, 0, 0, H);
    bgGrad.addColorStop(0, '#0a1f14');
    bgGrad.addColorStop(1, '#1a4a2a');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // Dibujar estrellas aleatorias
    ctx.fillStyle = 'rgba(255,255,255,0.4)';
    for (let i = 0; i < 20; i++) {
      const x = (Math.sin(i * 45.3) * 0.5 + 0.5) * W;
      const y = (Math.cos(i * 12.7) * 0.5 + 0.5) * H * 0.45;
      ctx.beginPath();
      ctx.arc(x, y, 1, 0, Math.PI * 2);
      ctx.fill();
    }

    const factorCrecimiento = nivelArbol / 10;
    const alturaBase = H * 0.35 + factorCrecimiento * H * 0.25;
    const grosorBase = 8 + nivelArbol * 2;
    const baseX = W / 2;
    const baseY = H - 20;

    // Suelo / pasto
    const sueloGrad = ctx.createLinearGradient(0, H - 20, 0, H);
    sueloGrad.addColorStop(0, '#2d6a4f');
    sueloGrad.addColorStop(1, '#1a3a2a');
    ctx.fillStyle = sueloGrad;
    ctx.fillRect(0, H - 20, W, 20);

    // Raíces (visibles desde nivel 3)
    if (nivelArbol >= 3) {
      ctx.strokeStyle = '#5c3d2e';
      ctx.lineWidth = 2;
      const raices = [[-30, 15], [30, 12], [-15, 20], [15, 18]];
      raices.forEach(([dx, dy]) => {
        ctx.beginPath();
        ctx.moveTo(baseX, baseY - 10);
        ctx.quadraticCurveTo(baseX + dx * 0.5, baseY, baseX + dx, baseY + dy);
        ctx.stroke();
      });
    }

    // Dibujar rama principal
    this.dibujarRama(ctx, baseX, baseY, -Math.PI / 2, alturaBase, grosorBase, nivelArbol, 0);

    // Animación de brillo radial
    ctx.save();
    ctx.globalAlpha = 0.05 + Math.sin(Date.now() / 1000) * 0.03;
    const brilloGrad = ctx.createRadialGradient(baseX, baseY - alturaBase * 0.6, 20, baseX, baseY - alturaBase * 0.6, 80);
    brilloGrad.addColorStop(0, 'rgba(149,213,178,1)');
    brilloGrad.addColorStop(1, 'rgba(149,213,178,0)');
    ctx.fillStyle = brilloGrad;
    ctx.beginPath();
    ctx.arc(baseX, baseY - alturaBase * 0.6, 80, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  dibujarRama(ctx, x, y, angulo, largo, grosor, nivel, profundidad) {
    if (profundidad > 4 || grosor < 0.8) return;

    const xFin = x + Math.cos(angulo) * largo;
    const yFin = y + Math.sin(angulo) * largo;

    // Color del tronco (marrón)
    const r = Math.floor(92 + profundidad * 10);
    ctx.strokeStyle = `rgb(${r}, 61, 46)`;
    ctx.lineWidth = grosor;
    ctx.lineCap = 'round';

    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(xFin, yFin);
    ctx.stroke();

    // Hojas en los extremos
    if (profundidad >= 2 || nivel >= 5) {
      const radioHoja = 8 + nivel * 3 - profundidad * 2;
      const alpha = 0.7 + Math.sin(Date.now() / 1200 + profundidad) * 0.15;
      const hojaColor = `rgba(45,106,79,${alpha})`;

      ctx.fillStyle = hojaColor;
      ctx.beginPath();
      ctx.arc(xFin, yFin, radioHoja, 0, Math.PI * 2);
      ctx.fill();

      // Capa de hojas más claras para dar volumen
      ctx.fillStyle = `rgba(82,183,136,${alpha * 0.6})`;
      ctx.beginPath();
      ctx.arc(xFin - radioHoja * 0.3, yFin - radioHoja * 0.3, radioHoja * 0.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Frutos (nivel 4+)
    if (nivel >= 4 && profundidad >= 2 && (Math.sin(xFin * yFin) > 0.2)) {
      const coloresFrutos = ['#f4845f', '#f9c74f', '#e63946', '#48cae4'];
      const colorFruto = coloresFrutos[nivel % coloresFrutos.length];
      ctx.fillStyle = colorFruto;
      ctx.beginPath();
      ctx.arc(xFin + Math.sin(xFin) * 8, yFin + Math.cos(yFin) * 8, 4 + nivel * 0.5, 0, Math.PI * 2);
      ctx.fill();
    }

    const maxProf = Math.min(4, Math.ceil(nivel / 2));
    if (profundidad < maxProf) {
      const numRamas = profundidad === 0 ? 2 : (nivel >= 7 ? 3 : 2);
      const anguloDif = (0.4 + nivel * 0.03) * (1 - profundidad * 0.1);

      for (let i = 0; i < numRamas; i++) {
        const dirAngulo = i === 0 ? anguloDif : -anguloDif;
        const altDelta = numRamas === 3 && i === 1 ? 0 : 0;
        this.dibujarRama(
          ctx,
          xFin,
          yFin,
          angulo + dirAngulo + altDelta,
          largo * (0.6 + nivel * 0.02),
          grosor * 0.65,
          nivel,
          profundidad + 1
        );
      }
    }
  }
}
