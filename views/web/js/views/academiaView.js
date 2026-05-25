/**
 * academiaView.js
 * View: Gestiona la visualización de los consejos (tips) y filtros por categoría.
 */

export class AcademiaView {
  constructor() {
    this.container = document.getElementById('tips-lista');
  }

  renderTips(tips, categoriaSeleccionada = null) {
    if (!this.container) return;

    const filtrados = categoriaSeleccionada
      ? tips.filter(t => t.categoria === categoriaSeleccionada)
      : tips;

    this.container.innerHTML = '';

    filtrados.forEach((tip, i) => {
      const card = document.createElement('div');
      card.className = 'tip-card';
      card.style.animationDelay = `${i * 0.05}s`;
      card.innerHTML = `
        <div class="tip-card-icono">${tip.icono_emoji}</div>
        <div class="tip-card-titulo">${tip.titulo}</div>
        <div class="tip-card-contenido">${tip.contenido}</div>
        ${tip.guardian_autor ? `<div class="tip-card-guardian">💚 ${tip.guardian_autor}</div>` : ''}
      `;
      this.container.appendChild(card);
    });

    if (filtrados.length === 0) {
      this.container.innerHTML = '<p class="empty-state">No hay consejos en esta categoría aún 🌱</p>';
    }
  }

  actualizarFiltrosActivos(botonActivo) {
    document.querySelectorAll('.filtro-btn').forEach(b => b.classList.remove('activo'));
    if (botonActivo) {
      botonActivo.classList.add('activo');
    }
  }

  renderTipDelDia(tip) {
    if (!tip) return;
    const icono = document.getElementById('tip-dia-icono');
    if (icono) icono.textContent = tip.icono_emoji;
    
    const titulo = document.getElementById('tip-dia-titulo');
    if (titulo) titulo.textContent = tip.titulo;
    
    const contenido = document.getElementById('tip-dia-contenido');
    if (contenido) contenido.textContent = tip.contenido;
    
    const guardian = document.getElementById('tip-dia-guardian');
    if (guardian && tip.guardian_autor) guardian.textContent = `💚 ${tip.guardian_autor}`;
  }
}
