/**
 * config.js
 * Configuraciones globales y datos demo para Semiverd MVP
 */

export const API_BASE = 'http://localhost:8000';

export const PUNTOS_NIVEL = {
  'Semilla': 100,
  'Brote': 350,
  'Árbol': 700,
  'Guardián': 1200,
  'Maestro del Bosque': 9999
};

export const DATOS_DEMO = {
  usuario: {
    id: 1,
    nombre: 'Demo Guardián',
    apodo: 'El Guardián Verde',
    correo: 'demo@semiverd.com',
    puntos_totales: 350,
    nivel: 'Brote',
    nivel_arbol: 3,
    racha_dias: 5,
    monedas_verdes: 35,
  },
  misiones: [
    {
      id: 1, titulo: 'Río Caudal: Guardianes del Agua',
      descripcion_corta: 'Construye un filtro casero para limpiar microplásticos del río.',
      descripcion: 'Juliana y Giohan descubren que el río que pasa cerca de su barrio está lleno de microplásticos. Tu misión es aprender a construir un filtro de bajo costo con materiales reciclados: arena, grava y tela. Demuestra que el agua limpia es un derecho de todos en Barrancabermeja.',
      nombre_zona: 'Río Caudal', guardianes: 'Juliana y Giohan',
      categoria: 'agua', puntos_recompensa: 150, monedas_recompensa: 15,
      dificultad: 2, orden: 1, icono_emoji: '💧', color_hex: '#1E88E5',
      estado: 'completada', porcentaje_completado: 100, puntos_ganados: 150
    },
    {
      id: 2, titulo: 'Bosque de Humo: Mapa Verde',
      descripcion_corta: 'Identifica zonas sin árboles y planifica una reforestación.',
      descripcion: 'Sofía y Camila notan que varias zonas de su ciudad han perdido sus árboles. Junto a ellas, deberás mapear las zonas más afectadas del barrio y proponer un plan de reforestación.',
      nombre_zona: 'Bosque de Humo', guardianes: 'Sofía y Camila',
      categoria: 'bosque', puntos_recompensa: 200, monedas_recompensa: 20,
      dificultad: 3, orden: 2, icono_emoji: '🌳', color_hex: '#388E3C',
      estado: 'en_progreso', porcentaje_completado: 40, puntos_ganados: 0
    },
    {
      id: 3, titulo: 'Ciudad Gris: Reciclaje Electrónico',
      descripcion_corta: 'Organiza una jornada de reciclaje de residuos electrónicos.',
      descripcion: '¡Misión de equipo! Las Cuatro Semillas Verdes organizan una jornada de recolección de residuos electrónicos (RAEE): celulares viejos, pilas, cables.',
      nombre_zona: 'Ciudad Gris', guardianes: 'Juliana, Camila, Sofía y Giohan',
      categoria: 'ciudad', puntos_recompensa: 300, monedas_recompensa: 30,
      dificultad: 4, orden: 3, icono_emoji: '♻️', color_hex: '#F57C00',
      estado: 'disponible', porcentaje_completado: 0, puntos_ganados: 0
    },
    {
      id: 4, titulo: 'Valle Energético: Eficiencia Verde',
      descripcion_corta: 'Audita el consumo energético del hogar y optimízalo.',
      descripcion: 'Giohan es el experto en tecnología del grupo. Ha descubierto que su hogar gasta más energía de la necesaria. Ayúdalo a hacer una auditoría energética.',
      nombre_zona: 'Valle Energético', guardianes: 'Giohan',
      categoria: 'energia', puntos_recompensa: 250, monedas_recompensa: 25,
      dificultad: 3, orden: 4, icono_emoji: '⚡', color_hex: '#FDD835',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0
    },
  ],
  tips: [
    { id:1, titulo:'Riega en las horas frescas', contenido:'Riega tus plantas temprano en la mañana o al atardecer. El agua se evapora menos y tus plantas absorben mejor los nutrientes.', categoria:'jardinería', icono_emoji:'🌅', guardian_autor:'Sofía' },
    { id:2, titulo:'El compostaje es magia verde', contenido:'Los restos de comida se pueden convertir en abono rico para tus plantas. ¡Es gratis y elimina basura!', categoria:'jardinería', icono_emoji:'🍂', guardian_autor:'Camila' },
    { id:3, titulo:'Captura el agua de lluvia', contenido:'Coloca un balde bajo las goteras durante la lluvia. Usa esa agua para regar tus plantas. ¡El cielo te da agua gratis!', categoria:'agua', icono_emoji:'🌧️', guardian_autor:'Juliana' },
    { id:4, titulo:'Desconecta el cargador vacío', contenido:'Los cargadores conectados sin teléfono siguen consumiendo energía. Desconéctalo y ahorra en tu factura.', categoria:'energia', icono_emoji:'🔌', guardian_autor:'Giohan' },
    { id:5, titulo:'Los 3 colores del reciclaje', contenido:'Verde para vidrio, azul para papel y cartón, amarillo para plástico y metal. Separa tus residuos.', categoria:'reciclaje', icono_emoji:'🗑️', guardian_autor:'Camila' },
    { id:6, titulo:'Usa bombillas LED', contenido:'Las bombillas LED consumen hasta 80% menos energía y duran mucho más. ¡Un pequeño cambio, gran impacto!', categoria:'energia', icono_emoji:'💡', guardian_autor:'Giohan' },
    { id:7, titulo:'No tires aceite por el drenaje', contenido:'Un litro de aceite usado puede contaminar hasta 1,000 litros de agua. Guárdalo y llévalo a un punto de reciclaje.', categoria:'agua', icono_emoji:'🚫', guardian_autor:'Giohan' },
    { id:8, titulo:'Plantas nativas, menos esfuerzo', contenido:'Las plantas nativas necesitan menos agua y cuidado porque están adaptadas al clima local.', categoria:'jardinería', icono_emoji:'🌿', guardian_autor:'Sofía' },
    { id:9, titulo:'Cierra el grifo al cepillarte', contenido:'Dejar el grifo abierto desperdicia hasta 12 litros de agua por minuto. ¡Ciérralo!', categoria:'agua', icono_emoji:'🦷', guardian_autor:'Camila' },
    { id:10, titulo:'Las pilas no van a la basura', contenido:'Una sola pila puede contaminar 600,000 litros de agua subterránea. Llévalas a puntos de recolección especiales.', categoria:'reciclaje', icono_emoji:'🔋', guardian_autor:'Juliana' },
    { id:11, titulo:'Jardín vertical en tu balcón', contenido:'¿Poco espacio? Usa botellas plásticas colgantes para hacer un jardín vertical. Reciclas y cultivas.', categoria:'jardinería', icono_emoji:'🏡', guardian_autor:'Juliana' },
    { id:12, titulo:'Ropa de segunda mano: moda consciente', contenido:'La industria textil es muy contaminante. Comprar ropa de segunda mano reduce el desperdicio.', categoria:'reciclaje', icono_emoji:'👕', guardian_autor:'Sofía' },
  ]
};

export const NIVELES_ARBOL = [
  { min: 1,  titulo: '🌱 Semilla',           desc: 'Tu árbol da sus primeros pasos. ¡Completa misiones para hacerlo crecer!' },
  { min: 2,  titulo: '🌿 Brote Joven',        desc: 'Pequeñas hojas comienzan a aparecer. El árbol se despierta.' },
  { min: 3,  titulo: '🌳 Árbol Pequeño',      desc: 'Las raíces se asientan y las ramas se extienden hacia el cielo.' },
  { min: 4,  titulo: '🍃 Árbol en Flor',      desc: '¡Floreciendo! Las primeras flores y frutos aparecen en el árbol.' },
  { min: 5,  titulo: '🌲 Árbol Robusto',      desc: 'Tu árbol es fuerte y majestuoso. El barrio lo nota.' },
  { min: 6,  titulo: '🌴 Árbol Tropical',     desc: 'El árbol prospera en el clima de Barrancabermeja. ¡Hermoso!' },
  { min: 7,  titulo: '🏕️ Árbol Guardián',    desc: 'Los pájaros ya anidan en él. Es refugio de vida.' },
  { min: 8,  titulo: '🌿 Árbol Ancestral',    desc: 'El árbol ya tiene historia. Las generaciones vienen a verlo.' },
  { min: 9,  titulo: '🌳 Gran Árbol Verde',   desc: 'Casi centenario. Un monumento ecológico del barrio.' },
  { min: 10, titulo: '🌲 Árbol Centenario',   desc: '¡FELICIDADES! Tu árbol es leyenda. Las Cuatro Semillas Verdes triunfaron.' },
];
