/**
 * academiaView.js
 * View: Gestiona la visualización de los consejos (tips) y filtros por categoría.
 */

export class AcademiaView {
  constructor() {
    this.container = document.getElementById('tips-lista');
    this.modal = document.getElementById('modal-tip');
    
    if (this.modal) {
      this.modalIcono = document.getElementById('modal-tip-icono');
      this.modalTitulo = document.getElementById('modal-tip-titulo');
      this.modalCategoria = document.getElementById('modal-tip-categoria');
      this.modalAutor = document.getElementById('modal-tip-autor');
      this.modalContenido = document.getElementById('modal-tip-contenido');
      
      // Hook closing actions
      const btnCerrar = this.modal.querySelector('.modal-cerrar');
      if (btnCerrar) {
        btnCerrar.addEventListener('click', () => this.cerrarModal());
      }
      
      const btnEntendido = this.modal.querySelector('.modal-cerrar-btn');
      if (btnEntendido) {
        btnEntendido.addEventListener('click', () => this.cerrarModal());
      }
      
      const backdrop = this.modal.querySelector('.modal-backdrop');
      if (backdrop) {
        backdrop.addEventListener('click', () => this.cerrarModal());
      }
    }
  }

  abrirModal(tip) {
    if (!this.modal || !tip) return;
    
    this.modalIcono.textContent = tip.icono_emoji || '💡';
    this.modalTitulo.textContent = tip.titulo || '';
    this.modalCategoria.textContent = (tip.categoria || 'Academia').toUpperCase();
    this.modalAutor.textContent = tip.guardian_autor ? `Recomendado por: ${tip.guardian_autor} 💚` : '';
    this.modalContenido.textContent = tip.contenido || '';
    
    this.modal.classList.remove('oculto');
    document.body.style.overflow = 'hidden';
  }

  cerrarModal() {
    if (this.modal) {
      this.modal.classList.add('oculto');
      document.body.style.overflow = '';
    }
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
      card.style.cursor = 'pointer';
      card.innerHTML = `
        <div class="tip-card-icono">${tip.icono_emoji}</div>
        <div class="tip-card-titulo">${tip.titulo}</div>
        <div class="tip-card-contenido">${tip.contenido}</div>
        ${tip.guardian_autor ? `<div class="tip-card-guardian">💚 ${tip.guardian_autor}</div>` : ''}
        <div class="tip-card-expand-btn">Ver consejo 🔍</div>
      `;

      card.addEventListener('click', () => {
        this.abrirModal(tip);
      });

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

    // Configurar clic en la tarjeta del consejo del día
    const card = document.querySelector('.card-tip-dia');
    if (card) {
      const newCard = card.cloneNode(true);
      if (card.parentNode) {
        card.parentNode.replaceChild(newCard, card);
      }
      newCard.style.cursor = 'pointer';
      newCard.addEventListener('click', () => this.abrirModal(tip));
    }
  }
}
