/**
 * config.js
 * Configuraciones globales y datos demo para Semiverd MVP
 */

export const API_BASE = window.location.origin;

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
      estado: 'completada', porcentaje_completado: 100, puntos_ganados: 150,
      imagenes_personajes: ['/pictures/juliana/JULIANAHECHO.png', '/pictures/giohan/GIOHANASIGNANDOTAREA.png']
    },
    {
      id: 2, titulo: 'Bosque de Humo: Mapa Verde',
      descripcion_corta: 'Identifica zonas sin árboles y planifica una reforestación.',
      descripcion: 'Sofía y Camila notan que varias zonas de su ciudad han perdido sus árboles. Junto a ellas, deberás mapear las zonas más afectadas del barrio y proponer un plan de reforestación.',
      nombre_zona: 'Bosque de Humo', guardianes: 'Sofía y Camila',
      categoria: 'bosque', puntos_recompensa: 200, monedas_recompensa: 20,
      dificultad: 3, orden: 2, icono_emoji: '🌳', color_hex: '#388E3C',
      estado: 'en_progreso', porcentaje_completado: 40, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/mariasofia/CleanShot_2026-05-25_at_10.53.42_2x-removebg-preview.png', '/pictures/camila/CAMILAINVESTIGANDO.png']
    },
    {
      id: 3, titulo: 'Ciudad Gris: Reciclaje Electrónico',
      descripcion_corta: 'Organiza una jornada de reciclaje de residuos electrónicos.',
      descripcion: '¡Misión de equipo! Las Cuatro Semillas Verdes organizan una jornada de recolección de residuos electrónicos (RAEE): celulares viejos, pilas, cables. Aprende la importancia de no mezclar estos componentes con la basura común.',
      nombre_zona: 'Ciudad Gris', guardianes: 'Juliana, Camila, Sofía y Giohan',
      categoria: 'ciudad', puntos_recompensa: 300, monedas_recompensa: 30,
      dificultad: 4, orden: 3, icono_emoji: '♻️', color_hex: '#F57C00',
      estado: 'disponible', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/juliana/JULIANAPROPONIENDO.png', '/pictures/camila/CAMILACREANDO1.png', '/pictures/mariasofia/SOFIAINCONFORME.png', '/pictures/giohan/GIOHANDECIDIDO.png']
    },
    {
      id: 4, titulo: 'Valle Energético: Eficiencia Verde',
      descripcion_corta: 'Audita el consumo energético del hogar y optimízalo.',
      descripcion: 'Giohan es el experto en tecnología del grupo. Ha descubierto que su hogar gasta más energía de la necesaria. Ayúdalo a hacer una auditoría energética y a apagar consumos fantasma.',
      nombre_zona: 'Valle Energético', guardianes: 'Giohan',
      categoria: 'energia', puntos_recompensa: 250, monedas_recompensa: 25,
      dificultad: 3, orden: 4, icono_emoji: '⚡', color_hex: '#FDD835',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/giohan/GIOHANINVESTIGANDO.png']
    },
    {
      id: 5, titulo: 'Humedal San Silvestre: Siembra Limpia',
      descripcion_corta: 'Siembra plantas acuáticas nativas para purificar el humedal.',
      descripcion: 'Juliana lidera esta misión en el Humedal San Silvestre. Vamos a sembrar especies vegetales que ayudan de forma natural a filtrar metales y purificar el agua local.',
      nombre_zona: 'Humedal San Silvestre', guardianes: 'Juliana',
      categoria: 'agua', puntos_recompensa: 150, monedas_recompensa: 15,
      dificultad: 2, orden: 5, icono_emoji: '🌱', color_hex: '#1E88E5',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/juliana/JULIANAESPERANDO.png']
    },
    {
      id: 6, titulo: 'Llanito Salvaje: Limpieza de Orillas',
      descripcion_corta: 'Limpia plásticos y colillas de la Ciénaga del Llanito.',
      descripcion: 'Juliana y Camila organizan una brigada de limpieza rápida en las playas del Llanito. Las colillas de cigarrillo y envoltorios dañan el hábitat de los peces; debemos actuar ya.',
      nombre_zona: 'Llanito Salvaje', guardianes: 'Juliana y Camila',
      categoria: 'agua', puntos_recompensa: 180, monedas_recompensa: 18,
      dificultad: 2, orden: 6, icono_emoji: '🗑️', color_hex: '#1E88E5',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/juliana/JULIANAESPERANDO.png', '/pictures/camila/CAMILAPENSANDO.png']
    },
    {
      id: 7, titulo: 'Paseo de la Iguana: Cuidado Animal',
      descripcion_corta: 'Crea refugios de anidación para las iguanas locales.',
      descripcion: 'Sofía lidera la protección de las iguanas en el Paseo de la Iguana. Construiremos pequeños refugios y carteles de sensibilización urbana para evitar su caza o maltrato.',
      nombre_zona: 'Paseo de la Iguana', guardianes: 'Sofía',
      categoria: 'bosque', puntos_recompensa: 160, monedas_recompensa: 16,
      dificultad: 2, orden: 7, icono_emoji: '🦎', color_hex: '#388E3C',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/mariasofia/SOFIATRISTE.png']
    },
    {
      id: 8, titulo: 'Barrio Centenario: Jardines Verticales',
      descripcion_corta: 'Crea muros verdes en fachadas de cemento usando botellas.',
      descripcion: 'Camila te enseña a diseñar jardines verticales. Con botellas de plástico recicladas crearemos un pulmón verde en fachadas de ladrillo del Barrio Centenario.',
      nombre_zona: 'Barrio Centenario', guardianes: 'Camila',
      categoria: 'bosque', puntos_recompensa: 190, monedas_recompensa: 19,
      dificultad: 3, orden: 8, icono_emoji: '🌸', color_hex: '#388E3C',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/camila/CAMILAPENSANDO.png']
    },
    {
      id: 9, titulo: 'Avenida del Ferrocarril: Ciclovía Verde',
      descripcion_corta: 'Promueve el uso de bicicleta midiendo CO2 ahorrado.',
      descripcion: 'Giohan y Sofía te retan a realizar tus trayectos cotidianos en bicicleta a lo largo de la Avenida del Ferrocarril. ¡Calcula y registra cuánto CO2 evitas liberar al aire!',
      nombre_zona: 'Avenida del Ferrocarril', guardianes: 'Giohan y Sofía',
      categoria: 'ciudad', puntos_recompensa: 220, monedas_recompensa: 22,
      dificultad: 3, orden: 9, icono_emoji: '🚲', color_hex: '#F57C00',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/giohan/GIOHANINVESTIGANDO.png', '/pictures/mariasofia/SOFIATRISTE.png']
    },
    {
      id: 10, titulo: 'Plaza Bolívar: Compostaje Comunitario',
      descripcion_corta: 'Instala un compostador de residuos orgánicos en la plaza.',
      descripcion: 'Camila y Juliana te guían para instalar compostadores comunitarios en la Plaza de Bolívar. Convierte los residuos orgánicos de los hogares en abono fértil.',
      nombre_zona: 'Plaza Bolívar', guardianes: 'Camila y Juliana',
      categoria: 'ciudad', puntos_recompensa: 240, monedas_recompensa: 24,
      dificultad: 3, orden: 10, icono_emoji: '🍂', color_hex: '#F57C00',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/camila/CAMILAPENSANDO.png', '/pictures/juliana/JULIANAESPERANDO.png']
    },
    {
      id: 11, titulo: 'Zona Industrial: Filtros de Aire',
      descripcion_corta: 'Monitorea partículas suspendidas y cultiva plantas purificadoras.',
      descripcion: 'Giohan ha diseñado un medidor de calidad de aire básico. Tu reto es sembrar plantas purificadoras (lengua de suegra, cuna de moisés) cerca de zonas de alta emisión industrial.',
      nombre_zona: 'Zona Industrial', guardianes: 'Giohan',
      categoria: 'ciudad', puntos_recompensa: 280, monedas_recompensa: 28,
      dificultad: 4, orden: 11, icono_emoji: '🏭', color_hex: '#F57C00',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/giohan/GIOHANINVESTIGANDO.png']
    },
    {
      id: 12, titulo: 'Sector Galán: Paneles Solares',
      descripcion_corta: 'Aprende a dimensionar un kit solar doméstico.',
      descripcion: 'Giohan y Camila te enseñan los principios de la energía solar. Diseña un plano de cargas eléctricas y calcula cuántos paneles fotovoltaicos requiere un hogar del Sector Galán.',
      nombre_zona: 'Sector Galán', guardianes: 'Giohan y Camila',
      categoria: 'energia', puntos_recompensa: 300, monedas_recompensa: 30,
      dificultad: 4, orden: 12, icono_emoji: '☀️', color_hex: '#FDD835',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/giohan/GIOHANINVESTIGANDO.png', '/pictures/camila/CAMILAPENSANDO.png']
    },
    {
      id: 13, titulo: 'Refinería Sostenible: Auditoría de Huella',
      descripcion_corta: 'Calcula tu huella ecológica personal anual.',
      descripcion: 'Giohan te ayuda a auditar tus hábitos de consumo: transporte, alimentación, plásticos. Recibe propuestas personalizadas para reducir tu huella ecológica a la mitad.',
      nombre_zona: 'Refinería Sostenible', guardianes: 'Giohan',
      categoria: 'energia', puntos_recompensa: 320, monedas_recompensa: 32,
      dificultad: 5, orden: 13, icono_emoji: '👣', color_hex: '#FDD835',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/giohan/GIOHANINVESTIGANDO.png']
    },
    {
      id: 14, titulo: 'Paso del Río: Lancheros Conscientes',
      descripcion_corta: 'Instruye a operadores de lanchas en manejo de hidrocarburos.',
      descripcion: 'Juliana impulsa esta iniciativa en los embarcaderos del Río Magdalena. Diseña folletos y guías sencillas para prevenir derrames de gasolina de motores fuera de borda.',
      nombre_zona: 'Paso del Río', guardianes: 'Juliana',
      categoria: 'agua', puntos_recompensa: 210, monedas_recompensa: 21,
      dificultad: 3, orden: 14, icono_emoji: '⛵', color_hex: '#1E88E5',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/juliana/JULIANAESPERANDO.png']
    },
    {
      id: 15, titulo: 'Bosque de la Lizama: Vivero Nativo',
      descripcion_corta: 'Recolecta y germina semillas de árboles locales.',
      descripcion: 'Sofía lidera la creación de un vivero en el Bosque de la Lizama. Aprende a recolectar semillas de árboles en peligro e inicia la germinación controlada.',
      nombre_zona: 'Bosque de la Lizama', guardianes: 'Sofía',
      categoria: 'bosque', puntos_recompensa: 230, monedas_recompensa: 23,
      dificultad: 3, orden: 15, icono_emoji: '🌲', color_hex: '#388E3C',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/mariasofia/SOFIATRISTE.png']
    },
    {
      id: 16, titulo: 'Comuna 7: Guardianes de la Energía',
      descripcion_corta: 'Diseña una campaña barrial de ahorro eléctrico en horas pico.',
      descripcion: 'Giohan y Sofía organizan patrullas ecológicas en la Comuna 7 para concientizar sobre el consumo vampiro y motivar a apagar bombillos innecesarios.',
      nombre_zona: 'Comuna 7', guardianes: 'Giohan y Sofía',
      categoria: 'energia', puntos_recompensa: 250, monedas_recompensa: 25,
      dificultad: 3, orden: 16, icono_emoji: '💡', color_hex: '#FDD835',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/giohan/GIOHANINVESTIGANDO.png', '/pictures/mariasofia/SOFIATRISTE.png']
    },
    {
      id: 17, titulo: 'Mercado de Torcoroma: Cero Plásticos',
      descripcion_corta: 'Reparte bolsas de tela a compradores del mercado.',
      descripcion: 'Camila te invita a liderar el cambio en las plazas de mercado. Confecciona o recolecta bolsas de tela y entrégalas a los compradores para reducir el uso de bolsas plásticas.',
      nombre_zona: 'Mercado de Torcoroma', guardianes: 'Camila',
      categoria: 'ciudad', puntos_recompensa: 260, monedas_recompensa: 26,
      dificultad: 3, orden: 17, icono_emoji: '🛍️', color_hex: '#F57C00',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/camila/CAMILAPENSANDO.png']
    },
    {
      id: 18, titulo: 'Parque de la Vida: Feria Ambiental',
      descripcion_corta: 'Diseña stands interactivos con juegos de reciclaje.',
      descripcion: '¡Las Cuatro Semillas al completo! Ayúdanos a montar stands en el Parque de la Vida con dinámicas divertidas para enseñar a niños y familias a reciclar correctamente.',
      nombre_zona: 'Parque de la Vida', guardianes: 'Juliana, Camila, Sofía y Giohan',
      categoria: 'ciudad', puntos_recompensa: 350, monedas_recompensa: 35,
      dificultad: 4, orden: 18, icono_emoji: '🎈', color_hex: '#F57C00',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/juliana/JULIANAPROPONIENDO.png', '/pictures/camila/CAMILACREANDO1.png', '/pictures/mariasofia/SOFIAINCONFORME.png', '/pictures/giohan/GIOHANDECIDIDO.png']
    },
    {
      id: 19, titulo: 'Quebrada las Camelias: Siembra de Agua',
      descripcion_corta: 'Restaura el nacimiento de agua plantando heliconias.',
      descripcion: 'Juliana y Sofía necesitan tu ayuda en la Quebrada las Camelias. Sembraremos plantas de sombrío y protectoras de agua en el nacimiento de la quebrada.',
      nombre_zona: 'Quebrada las Camelias', guardianes: 'Juliana y Sofía',
      categoria: 'agua', puntos_recompensa: 270, monedas_recompensa: 27,
      dificultad: 4, orden: 19, icono_emoji: '⛲', color_hex: '#1E88E5',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/juliana/JULIANAESPERANDO.png', '/pictures/mariasofia/SOFIATRISTE.png']
    },
    {
      id: 20, titulo: 'Gran Bosque del Río: Reforestación Leyenda',
      descripcion_corta: 'Siembra 10 árboles nativos y conviértete en Leyenda.',
      descripcion: 'La misión definitiva de las Cuatro Semillas Verdes. Acompaña a todos los guardianes a reforestar el cinturón verde del Río Magdalena con 10 árboles nativos. ¡El planeta y Barrancabermeja te lo agradecen!',
      nombre_zona: 'Gran Bosque del Río', guardianes: 'Juliana, Camila, Sofía y Giohan',
      categoria: 'bosque', puntos_recompensa: 400, monedas_recompensa: 40,
      dificultad: 5, orden: 20, icono_emoji: '👑', color_hex: '#388E3C',
      estado: 'bloqueada', porcentaje_completado: 0, puntos_ganados: 0,
      imagenes_personajes: ['/pictures/juliana/JULIANAPROPONIENDO.png', '/pictures/camila/CAMILACREANDO1.png', '/pictures/mariasofia/SOFIAINCONFORME.png', '/pictures/giohan/GIOHANDECIDIDO.png']
    }
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
