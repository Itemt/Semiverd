/**
 * mapView.js
 * View: Gestiona la vista del Camino (mapa de niveles/misiones).
 */

export class MapView {
  constructor() {
    this.container = document.getElementById('mapa-camino');
  }

  renderMapa(misiones, onNodeClick) {
    if (!this.container || !misiones.length) return;
    this.container.innerHTML = '';

    misiones.forEach((m, i) => {
      // Mapear estados a clases de estilo
      const estadoNodo = {
        completada:  'completado',
        en_progreso: 'disponible',
        disponible:  'disponible',
        bloqueada:   'bloqueado',
      }[m.estado] || 'bloqueado';

      const parada = document.createElement('div');
      parada.className = `mapa-parada ${i % 2 === 1 ? 'parada-par' : ''}`;
      
      if (m.estado !== 'bloqueada') {
        parada.addEventListener('click', () => onNodeClick(m.id));
        parada.style.cursor = 'pointer';
      }

      parada.innerHTML = `
        <div class="mapa-nodo ${estadoNodo}" style="border-color:${m.color_hex}">
          ${m.estado === 'completada' ? '✅' : m.estado === 'bloqueada' ? '🔒' : m.icono_emoji}
        </div>
        <div class="mapa-parada-info">
          <div class="mapa-parada-zona">${m.nombre_zona.toUpperCase()}</div>
          <div class="mapa-parada-titulo">${m.titulo}</div>
          <div class="mapa-parada-pts">⭐ ${m.puntos_recompensa} pts • ${m.guardianes}</div>
        </div>
      `;

      this.container.appendChild(parada);
    });
  }
}
