/**
 * missionView.js
 * View: Gestiona la lista de misiones y la ventana modal con detalles de cada misión.
 */

export class MissionView {
  constructor() {
    this.container = document.getElementById('misiones-lista');
    this.modal = document.getElementById('modal-mision');
    
    // Elementos del modal
    this.modalIcono = document.getElementById('modal-mision-icono');
    this.modalTitulo = document.getElementById('modal-mision-titulo');
    this.modalZona = document.getElementById('modal-mision-zona');
    this.modalGuardianes = document.getElementById('modal-mision-guardianes');
    this.modalPersonajes = document.getElementById('modal-mision-personajes');
    this.modalDescripcion = document.getElementById('modal-mision-descripcion');
    this.modalPuntos = document.getElementById('modal-puntos');
    this.modalMonedas = document.getElementById('modal-monedas');
    
    this.modalProgressBar = document.getElementById('modal-progress-bar');
    this.modalEstadoTexto = document.getElementById('modal-estado-texto');
    this.modalAcciones = document.getElementById('modal-acciones');
  }

  renderMisiones(misiones, onMisionClick) {
    if (!this.container) return;
    this.container.innerHTML = '';

    misiones.forEach(m => {
      const card = document.createElement('div');
      card.className = `mision-card ${m.estado === 'bloqueada' ? 'bloqueada' : ''}`;
      card.style.setProperty('--color-mision', m.color_hex);

      const badgeClase = {
        disponible:   'badge-disponible',
        en_progreso:  'badge-en-progreso',
        completada:   'badge-completada',
        bloqueada:    'badge-bloqueada',
      }[m.estado] || 'badge-bloqueada';

      const badgeTexto = {
        disponible:   '✨ Disponible',
        en_progreso:  '⏳ En Progreso',
        completada:   '✅ Completada',
        bloqueada:    '🔒 Bloqueada',
      }[m.estado] || '🔒 Bloqueada';

      card.innerHTML = `
        <div class="mision-card-header">
          <div class="mision-card-icono" style="border: 2px solid ${m.color_hex}22">${m.icono_emoji}</div>
          <div class="mision-card-info">
            <div class="mision-card-zona">${m.nombre_zona.toUpperCase()}</div>
            <div class="mision-card-titulo">${m.titulo}</div>
            <div class="mision-card-guardianes">Por: ${m.guardianes}</div>
          </div>
        </div>
        <p class="mision-card-desc">${m.descripcion_corta || m.descripcion.substring(0, 100) + '...'}</p>
        ${m.estado === 'en_progreso' ? `
        <div class="mision-progress">
          <div class="progress-bar-container">
            <div class="progress-bar" style="width:${m.porcentaje_completado}%"></div>
          </div>
        </div>` : ''}
        <div class="mision-card-footer">
          <span class="mision-estado-badge ${badgeClase}">${badgeTexto}</span>
          <span class="mision-puntos">⭐ ${m.puntos_recompensa} pts</span>
        </div>
      `;

      if (m.estado !== 'bloqueada') {
        card.addEventListener('click', () => onMisionClick(m.id));
      }

      this.container.appendChild(card);
    });
  }

  abrirModal(m, callbacks) {
    if (!m) return;

    // Rellenar contenido del modal
    this.modalIcono.textContent = m.icono_emoji;
    this.modalTitulo.textContent = m.titulo;
    this.modalZona.textContent = m.nombre_zona;
    this.modalGuardianes.textContent = `Guardianes: ${m.guardianes}`;
    
    // Renderizar imágenes de los personajes
    if (this.modalPersonajes) {
      this.modalPersonajes.innerHTML = '';
      const dialogoLayout = document.getElementById('modal-personaje-dialogo');
      const spriteImg = document.getElementById('modal-personaje-sprite');
      const dialogoTexto = document.getElementById('modal-personaje-dialogo-texto');
      
      if (dialogoLayout) {
        dialogoLayout.classList.add('oculto');
      }

      if (m.imagenes_personajes && m.imagenes_personajes.length > 0) {
        m.imagenes_personajes.forEach((imgUrl, idx) => {
          const img = document.createElement('img');
          img.src = imgUrl;
          img.alt = 'Personaje';
          img.className = 'modal-personaje-img';
          
          // Obtener nombre del personaje para el tooltip
          let nombre = 'Guardián';
          const lower = imgUrl.toLowerCase();
          if (lower.includes('juliana')) nombre = 'Juliana';
          else if (lower.includes('giohan')) nombre = 'Giohan';
          else if (lower.includes('camila')) nombre = 'Camila';
          else if (lower.includes('mariasofia') || lower.includes('maria sofia') || lower.includes('sofia')) nombre = 'Sofía';
          
          img.title = nombre;
          
          // Al hacer clic, mostrar mensaje y sprite grande sin corte
          img.addEventListener('click', () => {
            // Quitar clase activa
            this.modalPersonajes.querySelectorAll('.modal-personaje-img').forEach(el => el.classList.remove('activo'));
            img.classList.add('activo');
            
            // Mostrar diálogo
            if (dialogoLayout && dialogoTexto && spriteImg) {
              const msg = this.getMensajePersonaje(nombre, imgUrl);
              spriteImg.src = imgUrl;
              spriteImg.alt = nombre;
              dialogoTexto.innerHTML = `<strong>${nombre}:</strong> "${msg}"`;
              dialogoLayout.classList.remove('oculto');
            }
          });

          this.modalPersonajes.appendChild(img);

          // Activar el primero por defecto
          if (idx === 0) {
            setTimeout(() => {
              img.click();
            }, 50);
          }
        });
        this.modalPersonajes.style.display = 'flex';
      } else {
        this.modalPersonajes.style.display = 'none';
      }
    }

    this.modalDescripcion.textContent = m.descripcion;
    this.modalPuntos.textContent = m.puntos_recompensa;
    this.modalMonedas.textContent = m.monedas_recompensa;

    // Progreso
    this.modalProgressBar.style.width = `${m.porcentaje_completado}%`;
    this.modalEstadoTexto.textContent = `${m.porcentaje_completado}% completado`;

    // Acciones dinámicas según el estado
    this.modalAcciones.innerHTML = '';

    if (m.estado === 'bloqueada') {
      this.modalAcciones.innerHTML = '<p style="text-align:center;color:rgba(255,255,255,0.4);font-size:0.9rem;">🔒 Completa la misión anterior para desbloquear</p>';
    } else if (m.estado === 'completada') {
      this.modalAcciones.innerHTML = '<p style="text-align:center;color:var(--azul-agua);font-size:1rem;font-weight:800;">✅ ¡Misión completada! Eres un verdadero guardián.</p>';
    } else if (m.estado === 'disponible') {
      const btn = document.createElement('button');
      btn.className = 'btn-iniciar';
      btn.textContent = '🌱 Iniciar Misión';
      btn.addEventListener('click', () => callbacks.onIniciar(m.id));
      this.modalAcciones.appendChild(btn);
    } else if (m.estado === 'en_progreso') {
      const btnCompletar = document.createElement('button');
      btnCompletar.className = 'btn-completar';
      btnCompletar.textContent = '🏆 Marcar como Completada';
      btnCompletar.addEventListener('click', () => callbacks.onCompletar(m.id));
      this.modalAcciones.appendChild(btnCompletar);
    }

    this.modal.classList.remove('oculto');
    document.body.style.overflow = 'hidden';
  }

  getMensajePersonaje(nombre, imgUrl) {
    const name = nombre.toLowerCase();
    const url = imgUrl.toLowerCase();
    
    if (name.includes('juliana')) {
      if (url.includes('hecho') || url.includes('proponiendo')) {
        return "¡Hagamos que el Río Magdalena vuelva a brillar! Cada acción cuenta para descontaminar nuestras aguas. 💧✨";
      } else if (url.includes('esperando')) {
        return "El agua no espera, ¡los cambios deben iniciar hoy! ¿Listo para proteger el humedal? 🌊";
      } else if (url.includes('creando')) {
        return "¡Ideemos soluciones creativas para proteger la ciénaga y el río! 🌿🔬";
      }
      return "¡El agua limpia es vida y dignidad para Barrancabermeja! Cuidémosla juntos. 💚";
    }
    
    if (name.includes('giohan')) {
      if (url.includes('hecho') || url.includes('decidido')) {
        return "¡Eso es! Logramos reducir residuos y limpiar espacios. ¡Jugamos limpio por el planeta! ⚽♻️";
      } else if (url.includes('asignandotarea') || url.includes('investigando')) {
        return "Tenemos una nueva tarea ecológica. ¡Trabajemos en equipo para ganar este partido ambiental! 🤝";
      }
      return "¡La basura de unos es el tesoro de otros! A reutilizar y reciclar con toda la energía. 🗑️⚡";
    }
    
    if (name.includes('camila')) {
      if (url.includes('hecho') || url.includes('creando')) {
        return "¡Qué alegría ver brotar nuevas hojas! Cada árbol plantado limpia nuestro aire en Barranca. 🌳🌸";
      } else if (url.includes('pensando') || url.includes('investigando')) {
        return "Me pregunto... ¿cómo podemos mejorar la siembra de árboles hoy? ¡Las plantas aman los cuidados! 🍂";
      }
      return "¡Cuidar de la tierra es sembrar nuestro propio futuro! Seamos amigos de los árboles. 🌿";
    }
    
    if (name.includes('sofía') || name.includes('sofia')) {
      if (url.includes('hecho') || url.includes('decidido')) {
        return "¡Meta cumplida! Ahorrar energía es clave para mitigar el cambio climático. ⚡☀️";
      } else if (url.includes('inconforme') || url.includes('triste') || url.includes('cleanshot')) {
        return "Me preocupa el desperdicio de recursos... ¡Pero no nos rindamos! Podemos optimizar nuestro consumo. 📉💚";
      }
      return "¡El sol de Barrancabermeja es nuestra mayor fuente de energía limpia! Aprovechémosla con inteligencia. ☀️🔌";
    }
    
    return "¡Juntos podemos transformar a Barrancabermeja en una ecociudad ejemplar! 🌳✨";
  }

  cerrarModal() {
    this.modal.classList.add('oculto');
    document.body.style.overflow = '';
  }
}
