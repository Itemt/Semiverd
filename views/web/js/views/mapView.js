/**
 * mapView.js
 * View: Gestiona la vista del Camino (Eco-Dashboard de Progreso y Hitos del Guardián).
 */

export class MapView {
  constructor() {
    this.container = document.getElementById('mapa-camino');
  }

  renderMapa(misiones, onNodeClick, usuario) {
    if (!this.container || !misiones.length) return;
    this.container.innerHTML = '';

    // Si no se pasa el usuario (o viene vacío), calculamos valores estimados
    const totalPuntos = usuario ? usuario.puntos_totales : misiones.reduce((acc, m) => acc + (m.estado === 'completada' ? m.puntos_recompensa : 0), 0);
    const nivelNombre = usuario ? usuario.nivel : 'Semilla';
    const completadasCount = misiones.filter(m => m.estado === 'completada').length;

    // 1. Estructura principal
    const dashboard = document.createElement('div');
    dashboard.className = 'camino-dashboard';

    // 2. Sección 1: Estado del Guardián y Nivel
    let ptMin = 0;
    let ptMax = 100;
    if (nivelNombre === 'Semilla') { ptMin = 0; ptMax = 100; }
    else if (nivelNombre === 'Brote') { ptMin = 100; ptMax = 350; }
    else if (nivelNombre === 'Árbol') { ptMin = 350; ptMax = 700; }
    else if (nivelNombre === 'Guardián') { ptMin = 700; ptMax = 1200; }
    else { ptMin = 1200; ptMax = 3000; }

    const rangoNivel = ptMax - ptMin;
    const progresoEnNivel = Math.max(0, totalPuntos - ptMin);
    const pctNivel = Math.min(100, Math.round((progresoEnNivel / rangoNivel) * 100));

    const statusHTML = `
      <div class="camino-status-card">
        <div class="camino-status-header">
          <div class="camino-status-icon">🌱</div>
          <div class="camino-status-info">
            <h4>Tu Rango: <span class="rango-nombre">${nivelNombre}</span></h4>
            <p>${totalPuntos} / ${ptMax} puntos acumulados</p>
          </div>
        </div>
        <div class="progress-bar-container" style="height: 12px; margin-top: 12px;">
          <div class="progress-bar" style="width: ${pctNivel}%"></div>
        </div>
        <div class="camino-status-footer">
          <span>${completadasCount} de ${misiones.length} misiones completadas</span>
          <span>${pctNivel}% para el siguiente rango</span>
        </div>
      </div>
    `;

    // 3. Sección 2: Estado de las Zonas de Barrancabermeja
    const zonas = {
      agua: {
        titulo: 'Río & Ciénagas 🌊',
        desc: 'Filtros de microplásticos, limpieza y reforestación de cuencas.',
        misiones: [],
        color: '#1E88E5'
      },
      bosque: {
        titulo: 'Bosques & Humedales 🌳',
        desc: 'Mapeo y reforestación del Humedal San Silvestre.',
        misiones: [],
        color: '#388E3C'
      },
      energia: {
        titulo: 'Energía & Clima ⚡',
        desc: 'Instalación de paneles solares y hornos ecológicos.',
        misiones: [],
        color: '#F9A825'
      },
      ciudad: {
        titulo: 'Reciclaje Urbano ♻️',
        desc: 'Eco-ladrillos, compostaje y jornadas de reciclaje RAEE.',
        misiones: [],
        color: '#E65100'
      }
    };

    misiones.forEach(m => {
      const cat = m.categoria;
      if (zonas[cat]) {
        zonas[cat].misiones.push(m);
      } else {
        zonas['ciudad'].misiones.push(m);
      }
    });

    let zonesHTML = `
      <div class="camino-seccion-titulo">
        <h3>Restauración Ecológica de Barrancabermeja</h3>
        <p>Completa misiones de cada área para restaurar el balance de la ciudad</p>
      </div>
      <div class="camino-zones-grid">
    `;

    Object.keys(zonas).forEach(key => {
      const z = zonas[key];
      const tot = z.misiones.length;
      const comp = z.misiones.filter(m => m.estado === 'completada').length;
      const pct = tot > 0 ? Math.round((comp / tot) * 100) : 0;
      
      zonesHTML += `
        <div class="camino-zone-card" style="border-left: 5px solid ${z.color}">
          <div class="zone-card-header">
            <h5>${z.titulo}</h5>
            <span class="zone-badge" style="background: ${z.color}15; color: ${z.color}">${comp}/${tot}</span>
          </div>
          <p class="zone-card-desc">${z.desc}</p>
          <div class="zone-progress-container">
            <div class="progress-bar-container" style="height: 6px; background: rgba(255,255,255,0.08);">
              <div class="progress-bar" style="width: ${pct}%; background: ${z.color}"></div>
            </div>
            <div class="zone-progress-labels">
              <span>Restauración: ${pct}%</span>
            </div>
          </div>
        </div>
      `;
    });

    zonesHTML += `</div>`;

    // 4. Sección 3: Hitos del Guardián (Camino de Logros)
    const hitos = [
      { id: 1, req: 1, titulo: '🥉 Eco-Iniciado', desc: 'Completa tu primera misión y siembra tu semilla.', medalla: 'Iniciado' },
      { id: 2, req: 2, titulo: '🌊 Protector del Río Magdalena', desc: 'Completa al menos 2 misiones de conservación hídrica.', categoria: 'agua' },
      { id: 3, req: 2, titulo: '🌳 Guardián Silvestre', desc: 'Completa al menos 2 misiones de reforestación o humedales.', categoria: 'bosque' },
      { id: 4, req: 2, titulo: '⚡ Impulsor Solar', desc: 'Completa al menos 2 misiones de energía solar o ahorro eléctrico.', categoria: 'energia' },
      { id: 5, req: 2, titulo: '♻️ Campeón Residuo Cero', desc: 'Completa al menos 2 misiones de reciclaje o compostaje urbano.', categoria: 'ciudad' },
      { id: 6, req: 20, titulo: '🌟 Defensor Legendario', desc: 'Completa las 20 misiones ecológicas de Barrancabermeja.', medalla: 'Semilla Sagrada' }
    ];

    let hitosHTML = `
      <div class="camino-seccion-titulo" style="margin-top: 32px;">
        <h3>🏆 Camino de Hitos & Logros</h3>
        <p>Supera las metas ecológicas para obtener reconocimiento oficial</p>
      </div>
      <div class="camino-hitos-list">
    `;

    hitos.forEach(h => {
      let cumplido = false;
      if (h.id === 1) cumplido = completadasCount >= 1;
      else if (h.id === 2) cumplido = misiones.filter(m => m.categoria === 'agua' && m.estado === 'completada').length >= 2;
      else if (h.id === 3) cumplido = misiones.filter(m => m.categoria === 'bosque' && m.estado === 'completada').length >= 2;
      else if (h.id === 4) cumplido = misiones.filter(m => m.categoria === 'energia' && m.estado === 'completada').length >= 2;
      else if (h.id === 5) cumplido = misiones.filter(m => m.categoria === 'ciudad' && m.estado === 'completada').length >= 2;
      else cumplido = completadasCount >= 20;

      hitosHTML += `
        <div class="camino-hito-item ${cumplido ? 'cumplido' : 'bloqueado'}">
          <div class="hito-check">
            ${cumplido ? '✅' : '🔒'}
          </div>
          <div class="hito-info">
            <h6>${h.titulo}</h6>
            <p>${h.desc}</p>
          </div>
          <div class="hito-badge">
            ${cumplido ? '⭐ Desbloqueado' : 'Pendiente'}
          </div>
        </div>
      `;
    });

    hitosHTML += `</div>`;

    dashboard.innerHTML = statusHTML + zonesHTML + hitosHTML;
    this.container.appendChild(dashboard);
  }
}
