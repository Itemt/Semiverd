/**
 * rankingView.js
 * View: Gestiona la visualización de la tabla de posiciones de los guardianes.
 */

export class RankingView {
  constructor() {
    this.container = document.getElementById('ranking-lista');
  }

  renderRanking(ranking) {
    if (!this.container) return;
    this.container.innerHTML = '';

    ranking.forEach(g => {
      const posClase = g.posicion <= 3 ? `ranking-pos-${g.posicion}` : '';
      const medallaPos = g.posicion === 1 ? '🥇' : g.posicion === 2 ? '🥈' : g.posicion === 3 ? '🥉' : `#${g.posicion}`;
      
      const item = document.createElement('div');
      item.className = 'ranking-item';
      item.innerHTML = `
        <div class="ranking-pos ${posClase}">${medallaPos}</div>
        <div class="ranking-info">
          <div class="ranking-nombre">${g.nombre}</div>
          <div class="ranking-apodo">${g.apodo || ''}</div>
          <div class="ranking-nivel">${g.nivel} • Árbol Nv.${g.nivel_arbol}</div>
        </div>
        <div class="ranking-puntos">⭐ ${g.puntos_totales}</div>
      `;
      this.container.appendChild(item);
    });
  }
}
