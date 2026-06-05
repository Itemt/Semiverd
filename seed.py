"""
seed.py - Datos iniciales para la base de datos de Semiverd
Ejecutar una sola vez: python seed.py

Carga:
  - Las 4 misiones de las Semillas Verdes
  - 12 tips de la Academia de Guardianes
  - Recompensas base del sistema
"""

import sys
import os

from models.database import SessionLocal, engine
from models.models import Base, Mision, Tip, Recompensa


def crear_tablas():
    """Crea todas las tablas en la base de datos"""
    try:
        from sqlalchemy import MetaData
        meta = MetaData()
        meta.reflect(bind=engine)
        meta.drop_all(bind=engine)
        print("🗑️  Tablas anteriores eliminadas (limpieza completa)")
    except Exception as e:
        print(f"⚠️ Advertencia al eliminar tablas: {e}")
        
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")


def cargar_misiones(db):
    """Carga las 20 misiones de las Semillas Verdes"""
    misiones_existentes = db.query(Mision).count()
    if misiones_existentes > 0:
        print("ℹ️  Las misiones ya existen, omitiendo...")
        return

    misiones = [
        Mision(
            titulo="Río Caudal: Guardianes del Agua",
            descripcion=(
                "Juliana y Giohan descubren que el río que pasa cerca de su barrio "
                "está lleno de microplásticos. Tu misión es aprender a construir un "
                "filtro de bajo costo con materiales reciclados: arena, grava y tela. "
                "Demuestra que el agua limpia es un derecho de todos en Barrancabermeja."
            ),
            descripcion_corta="Construye un filtro casero para limpiar microplásticos del río.",
            nombre_zona="Río Caudal",
            guardianes="Juliana y Giohan",
            categoria="agua",
            puntos_recompensa=150,
            monedas_recompensa=15,
            dificultad=2,
            orden=1,
            icono_emoji="💧",
            color_hex="#1E88E5"
        ),
        Mision(
            titulo="Bosque de Humo: Mapa Verde",
            descripcion=(
                "Sofía y Camila notan que varias zonas de su ciudad han perdido sus "
                "árboles. Junto a ellas, deberás mapear las zonas más afectadas del barrio "
                "y proponer un plan de reforestación. Aprende qué plantas nativas son "
                "ideales para Barrancabermeja y por qué la siembra colectiva salva al planeta."
            ),
            descripcion_corta="Identifica zonas sin árboles y planifica una reforestación.",
            nombre_zona="Bosque de Humo",
            guardianes="Sofía y Camila",
            categoria="bosque",
            puntos_recompensa=200,
            monedas_recompensa=20,
            dificultad=3,
            orden=2,
            icono_emoji="🌳",
            color_hex="#388E3C"
        ),
        Mision(
            titulo="Ciudad Gris: Reciclaje Electrónico",
            descripcion=(
                "¡Misión de equipo! Las Cuatro Semillas Verdes organizan una jornada "
                "de recolección de residuos electrónicos (RAEE): celulares viejos, pilas, "
                "cables. Descubre por qué tirar una pila contamina 600 litros de agua y "
                "cómo el reciclaje tecnológico puede transformar tu ciudad gris en una "
                "ciudad verde."
            ),
            descripcion_corta="Organiza una jornada de reciclaje de residuos electrónicos.",
            nombre_zona="Ciudad Gris",
            guardianes="Juliana, Camila, Sofía y Giohan",
            categoria="ciudad",
            puntos_recompensa=300,
            monedas_recompensa=30,
            dificultad=4,
            orden=3,
            icono_emoji="♻️",
            color_hex="#F57C00"
        ),
        Mision(
            titulo="Valle Energético: Eficiencia Verde",
            descripcion=(
                "Giohan es el experto en tecnología del grupo. Ha descubierto que su "
                "hogar gasta más energía de la necesaria. Ayúdalo a hacer una auditoría "
                "energética: identifica aparatos que más consumen, aprende sobre energías "
                "renovables (solar, eólica) y diseña un plan para reducir la huella de "
                "carbono de tu hogar en un 20%."
            ),
            descripcion_corta="Audita el consumo energético del hogar y optimízalo.",
            nombre_zona="Valle Energético",
            guardianes="Giohan",
            categoria="energia",
            puntos_recompensa=250,
            monedas_recompensa=25,
            dificultad=3,
            orden=4,
            icono_emoji="⚡",
            color_hex="#FDD835"
        ),
        Mision(
            titulo="Humedal San Silvestre: Siembra Limpia",
            descripcion=(
                "Juliana lidera esta misión en el Humedal San Silvestre. Vamos a sembrar "
                "especies vegetales autóctonas (totora, jacinto de agua) que ayudan de "
                "forma natural a filtrar metales y purificar el agua local. ¡Cuida los "
                "humedales de Barrancabermeja!"
            ),
            descripcion_corta="Siembra plantas acuáticas nativas para purificar el humedal.",
            nombre_zona="Humedal San Silvestre",
            guardianes="Juliana",
            categoria="agua",
            puntos_recompensa=150,
            monedas_recompensa=15,
            dificultad=2,
            orden=5,
            icono_emoji="🌱",
            color_hex="#1E88E5"
        ),
        Mision(
            titulo="Llanito Salvaje: Limpieza de Orillas",
            descripcion=(
                "Juliana y Camila organizan una brigada de limpieza rápida en las "
                "playas y orillas de la Ciénaga del Llanito. Las colillas de cigarrillo "
                "y envoltorios plásticos dañan el hábitat de los peces y manatíes locales. "
                "¡Debemos actuar ya!"
            ),
            descripcion_corta="Limpia plásticos y colillas de la Ciénaga del Llanito.",
            nombre_zona="Llanito Salvaje",
            guardianes="Juliana y Camila",
            categoria="agua",
            puntos_recompensa=180,
            monedas_recompensa=18,
            dificultad=2,
            orden=6,
            icono_emoji="🗑️",
            color_hex="#1E88E5"
        ),
        Mision(
            titulo="Paseo de la Iguana: Cuidado Animal",
            descripcion=(
                "Sofía lidera la protección de la fauna en el Paseo de la Iguana. "
                "Construiremos pequeños refugios de anidación y carteles informativos "
                "de sensibilización urbana para concienciar a los ciudadanos y proteger "
                "el hábitat de las iguanas."
            ),
            descripcion_corta="Crea refugios de anidación para las iguanas locales.",
            nombre_zona="Paseo de la Iguana",
            guardianes="Sofía",
            categoria="bosque",
            puntos_recompensa=160,
            monedas_recompensa=16,
            dificultad=2,
            orden=7,
            icono_emoji="🦎",
            color_hex="#388E3C"
        ),
        Mision(
            titulo="Barrio Centenario: Jardines Verticales",
            descripcion=(
                "Camila te enseña a diseñar jardines verticales. Utilizando botellas "
                "plásticas recicladas como macetas, crearemos un pulmón verde con "
                "plantas trepadoras y florales en fachadas urbanas de cemento."
            ),
            descripcion_corta="Crea muros verdes en fachadas de cemento usando botellas.",
            nombre_zona="Barrio Centenario",
            guardianes="Camila",
            categoria="bosque",
            puntos_recompensa=190,
            monedas_recompensa=19,
            dificultad=3,
            orden=8,
            icono_emoji="🌸",
            color_hex="#388E3C"
        ),
        Mision(
            titulo="Avenida del Ferrocarril: Ciclovía Verde",
            descripcion=(
                "Giohan y Sofía te retan a realizar tus trayectos cotidianos cotidianos "
                "en bicicleta a lo largo de la Avenida del Ferrocarril. Registra tus "
                "kilómetros recorridos y calcula cuánto CO2 has ahorrado al planeta."
            ),
            descripcion_corta="Promueve el uso de bicicleta midiendo CO2 ahorrado.",
            nombre_zona="Avenida del Ferrocarril",
            guardianes="Giohan y Sofía",
            categoria="ciudad",
            puntos_recompensa=220,
            monedas_recompensa=22,
            dificultad=3,
            orden=9,
            icono_emoji="🚲",
            color_hex="#F57C00"
        ),
        Mision(
            titulo="Plaza Bolívar: Compostaje Comunitario",
            descripcion=(
                "Camila y Juliana te guían para instalar compostadores colectivos en "
                "la Plaza Bolívar. Convierte los residuos orgánicos de los hogares en "
                "tierra fértil para sembrar plantas."
            ),
            descripcion_corta="Instala un compostador de residuos orgánicos en la plaza.",
            nombre_zona="Plaza Bolívar",
            guardianes="Camila y Juliana",
            categoria="ciudad",
            puntos_recompensa=240,
            monedas_recompensa=24,
            dificultad=3,
            orden=10,
            icono_emoji="🍂",
            color_hex="#F57C00"
        ),
        Mision(
            titulo="Zona Industrial: Filtros de Aire",
            descripcion=(
                "Giohan ha diseñado un medidor de calidad de aire básico. Tu reto es "
                "sembrar plantas purificadoras (lengua de suegra, cuna de moisés) cerca "
                "de zonas con emisiones industriales y medir la reducción de polvo."
            ),
            descripcion_corta="Monitorea partículas suspendidas y cultiva plantas purificadoras.",
            nombre_zona="Zona Industrial",
            guardianes="Giohan",
            categoria="ciudad",
            puntos_recompensa=280,
            monedas_recompensa=28,
            dificultad=4,
            orden=11,
            icono_emoji="🏭",
            color_hex="#F57C00"
        ),
        Mision(
            titulo="Sector Galán: Paneles Solares",
            descripcion=(
                "Giohan y Camila te enseñan los principios de la energía solar fotovoltaica. "
                "Aprenderás a calcular la potencia necesaria y diseñarás el esquema para "
                "alimentar bombillas de bajo consumo en el Sector Galán."
            ),
            descripcion_corta="Aprende a dimensionar un kit solar doméstico.",
            nombre_zona="Sector Galán",
            guardianes="Giohan y Camila",
            categoria="energia",
            puntos_recompensa=300,
            monedas_recompensa=30,
            dificultad=4,
            orden=12,
            icono_emoji="☀️",
            color_hex="#FDD835"
        ),
        Mision(
            titulo="Refinería Sostenible: Auditoría de Huella",
            descripcion=(
                "Giohan te ayuda a auditar tus hábitos de consumo: transporte, alimentación, "
                "plásticos. Recibe propuestas personalizadas para reducir tu huella ecológica "
                "y optimizar el gasto de energía en el hogar."
            ),
            descripcion_corta="Calcula tu huella ecológica personal anual.",
            nombre_zona="Refinería Sostenible",
            guardianes="Giohan",
            categoria="energia",
            puntos_recompensa=320,
            monedas_recompensa=32,
            dificultad=5,
            orden=13,
            icono_emoji="👣",
            color_hex="#FDD835"
        ),
        Mision(
            titulo="Paso del Río: Lancheros Conscientes",
            descripcion=(
                "Juliana impulsa esta iniciativa en los embarcaderos del Río Magdalena. "
                "Diseña folletos y guías sencillas para prevenir derrames accidentales de "
                "hidrocarburos y gasolina de los motores fuera de borda."
            ),
            descripcion_corta="Instruye a operadores de lanchas en manejo de hidrocarburos.",
            nombre_zona="Paso del Río",
            guardianes="Juliana",
            categoria="agua",
            puntos_recompensa=210,
            monedas_recompensa=21,
            dificultad=3,
            orden=14,
            icono_emoji="⛵",
            color_hex="#1E88E5"
        ),
        Mision(
            titulo="Bosque de la Lizama: Vivero Nativo",
            descripcion=(
                "Sofía lidera la creación de un vivero en el Bosque de la Lizama. "
                "Aprende a recolectar semillas de árboles en peligro de extinción e "
                "inicia la germinación controlada para reforestación local."
            ),
            descripcion_corta="Recolecta y germina semillas de árboles locales.",
            nombre_zona="Bosque de la Lizama",
            guardianes="Sofía",
            categoria="bosque",
            puntos_recompensa=230,
            monedas_recompensa=23,
            dificultad=3,
            orden=15,
            icono_emoji="🌲",
            color_hex="#388E3C"
        ),
        Mision(
            titulo="Comuna 7: Guardianes de la Energía",
            descripcion=(
                "Giohan y Sofía organizan patrullas ecológicas en la Comuna 7 para "
                "concientizar sobre el consumo vampiro (dispositivos enchufados sin usar) "
                "y motivar a apagar bombillos innecesarios."
            ),
            descripcion_corta="Diseña una campaña barrial de ahorro eléctrico en horas pico.",
            nombre_zona="Comuna 7",
            guardianes="Giohan y Sofía",
            categoria="energia",
            puntos_recompensa=250,
            monedas_recompensa=25,
            dificultad=3,
            orden=16,
            icono_emoji="💡",
            color_hex="#FDD835"
        ),
        Mision(
            titulo="Mercado de Torcoroma: Cero Plásticos",
            descripcion=(
                "Camila te invita a liderar el cambio en las plazas de mercado. Confecciona "
                "o recolecta bolsas de tela reutilizables y entrégalas a los compradores del "
                "Mercado de Torcoroma para erradicar las bolsas plásticas."
            ),
            descripcion_corta="Reparte bolsas de tela a compradores del mercado.",
            nombre_zona="Mercado de Torcoroma",
            guardianes="Camila",
            categoria="ciudad",
            puntos_recompensa=260,
            monedas_recompensa=26,
            dificultad=3,
            orden=17,
            icono_emoji="🛍️",
            color_hex="#F57C00"
        ),
        Mision(
            titulo="Parque de la Vida: Feria Ambiental",
            descripcion=(
                "¡Las Cuatro Semillas al completo! Ayúdanos a montar stands interactivos "
                "en el Parque de la Vida con dinámicas divertidas para enseñar a niños "
                "y familias a clasificar residuos y reciclar correctamente."
            ),
            descripcion_corta="Diseña stands interactivos con juegos de reciclaje.",
            nombre_zona="Parque de la Vida",
            guardianes="Juliana, Camila, Sofía y Giohan",
            categoria="ciudad",
            puntos_recompensa=350,
            monedas_recompensa=35,
            dificultad=4,
            orden=18,
            icono_emoji="🎈",
            color_hex="#F57C00"
        ),
        Mision(
            titulo="Quebrada las Camelias: Siembra de Agua",
            descripcion=(
                "Juliana y Sofía necesitan tu ayuda en la Quebrada las Camelias. Sembraremos "
                "plantas de sombrío y protectoras de agua en el nacimiento de la quebrada "
                "para restaurar el cauce y su biodiversidad."
            ),
            descripcion_corta="Restaura el nacimiento de agua plantando heliconias.",
            nombre_zona="Quebrada las Camelias",
            guardianes="Juliana y Sofía",
            categoria="agua",
            puntos_recompensa=270,
            monedas_recompensa=27,
            dificultad=4,
            orden=19,
            icono_emoji="⛲",
            color_hex="#1E88E5"
        ),
        Mision(
            titulo="Gran Bosque del Río: Reforestación Leyenda",
            descripcion=(
                "La misión definitiva de las Cuatro Semillas Verdes. Acompaña a todos los "
                "guardianes a reforestar el cinturón verde del Río Magdalena con 10 árboles "
                "nativos. ¡Conviértete en Leyenda de Barrancabermeja!"
            ),
            descripcion_corta="Siembra 10 árboles nativos y conviértete en Leyenda.",
            nombre_zona="Gran Bosque del Río",
            guardianes="Juliana, Camila, Sofía y Giohan",
            categoria="bosque",
            puntos_recompensa=400,
            monedas_recompensa=40,
            dificultad=5,
            orden=20,
            icono_emoji="👑",
            color_hex="#388E3C"
        ),
    ]

    for mision in misiones:
        db.add(mision)

    db.commit()
    print(f"✅ {len(misiones)} misiones cargadas exitosamente")


def cargar_tips(db):
    """Carga los consejos de la Academia de Guardianes"""
    tips_existentes = db.query(Tip).count()
    if tips_existentes > 0:
        print("ℹ️  Los tips ya existen, omitiendo...")
        return

    tips = [
        # Tips de jardinería
        Tip(
            titulo="Riega en las horas frescas",
            contenido="Riega tus plantas temprano en la mañana o al atardecer. El agua se evapora menos y tus plantas absorben mejor los nutrientes.",
            categoria="jardinería",
            icono_emoji="🌅",
            guardian_autor="Sofía"
        ),
        Tip(
            titulo="El compostaje es magia verde",
            contenido="Los restos de comida (cáscaras, hojas) se pueden convertir en abono rico para tus plantas. ¡Es gratis y elimina basura!",
            categoria="jardinería",
            icono_emoji="🍂",
            guardian_autor="Camila"
        ),
        Tip(
            titulo="Plantas nativas, menos esfuerzo",
            contenido="Las plantas nativas de tu región necesitan menos agua y cuidado porque están adaptadas al clima local. Pregunta cuáles son las de Barrancabermeja.",
            categoria="jardinería",
            icono_emoji="🌿",
            guardian_autor="Sofía"
        ),
        Tip(
            titulo="Un jardín vertical en tu balcón",
            contenido="¿Poco espacio? Usa botellas plásticas colgantes para hacer un jardín vertical. Reciclas y cultivas al mismo tiempo.",
            categoria="jardinería",
            icono_emoji="🏡",
            guardian_autor="Juliana"
        ),
        # Tips de agua
        Tip(
            titulo="Captura el agua de lluvia",
            contenido="Coloca un balde bajo las goteras durante la lluvia. Usa esa agua para regar tus plantas. ¡El cielo te da agua gratis!",
            categoria="agua",
            icono_emoji="🌧️",
            guardian_autor="Juliana"
        ),
        Tip(
            titulo="No tires aceite por el drenaje",
            contenido="Un litro de aceite usado puede contaminar hasta 1,000 litros de agua. Guárdalo en un recipiente y llévalo a un punto de reciclaje.",
            categoria="agua",
            icono_emoji="🚫",
            guardian_autor="Giohan"
        ),
        Tip(
            titulo="Cierra el grifo al cepillarte",
            contenido="Dejar el grifo abierto mientras te cepillas los dientes desperdicia hasta 12 litros de agua por minuto. ¡Ciérralo!",
            categoria="agua",
            icono_emoji="🦷",
            guardian_autor="Camila"
        ),
        # Tips de energía
        Tip(
            titulo="Desconecta el cargador vacío",
            contenido="Los cargadores conectados sin teléfono siguen consumiendo energía. Desconéctalo y ahorra en tu factura.",
            categoria="energia",
            icono_emoji="🔌",
            guardian_autor="Giohan"
        ),
        Tip(
            titulo="Usa bombillas LED",
            contenido="Las bombillas LED consumen hasta 80% menos energía que las tradicionales y duran mucho más. ¡Un pequeño cambio, gran impacto!",
            categoria="energia",
            icono_emoji="💡",
            guardian_autor="Giohan"
        ),
        # Tips de reciclaje
        Tip(
            titulo="Los 3 colores del reciclaje",
            contenido="Verde para vidrio, azul para papel y cartón, amarillo para plástico y metal. Separa tus residuos y facilita el reciclaje.",
            categoria="reciclaje",
            icono_emoji="🗑️",
            guardian_autor="Camila"
        ),
        Tip(
            titulo="Las pilas no van a la basura",
            contenido="Una sola pila puede contaminar 600,000 litros de agua subterránea. Guárdalas y llévalas a puntos de recolección especiales.",
            categoria="reciclaje",
            icono_emoji="🔋",
            guardian_autor="Juliana"
        ),
        Tip(
            titulo="Ropa de segunda mano: moda consciente",
            contenido="La industria textil es una de las más contaminantes. Comprar ropa de segunda mano reduce el desperdicio y tu huella ambiental.",
            categoria="reciclaje",
            icono_emoji="👕",
            guardian_autor="Sofía"
        ),
        Tip(
            titulo="No más pitillos de plástico",
            contenido="Los pitillos de plástico tardan hasta 500 años en descomponerse. Pide tus bebidas sin pitillo o usa uno de metal reutilizable.",
            categoria="reciclaje",
            icono_emoji="🥤",
            guardian_autor="Camila"
        ),
        Tip(
            titulo="Aprovecha la luz natural",
            contenido="Abre tus ventanas y cortinas durante el día en lugar de encender la luz. Ahorrarás energía y la luz solar es mejor para tu salud.",
            categoria="energia",
            icono_emoji="☀️",
            guardian_autor="Giohan"
        ),
        Tip(
            titulo="Ducha rápida, planeta feliz",
            contenido="Tomar duchas de 5 minutos en lugar de 10 puede ahorrar hasta 50 litros de agua cada día. Pon tu canción favorita de 5 minutos y úsala como reloj.",
            categoria="agua",
            icono_emoji="🚿",
            guardian_autor="Juliana"
        ),
        Tip(
            titulo="Crea un hotel para insectos",
            contenido="Apila troncos, hojas secas y ladrillos con huecos en una esquina de tu jardín. Esto atraerá abejas solitarias y mariquitas que polinizarán tus plantas.",
            categoria="jardinería",
            icono_emoji="🐞",
            guardian_autor="Sofía"
        ),
        Tip(
            titulo="Apaga la pantalla de tu computadora",
            contenido="Si vas a alejarte de tu computadora por más de 10 minutos, apaga el monitor. Ahorra energía y prolonga la vida útil de tu equipo.",
            categoria="energia",
            icono_emoji="🖥️",
            guardian_autor="Giohan"
        ),
    ]

    for tip in tips:
        db.add(tip)

    db.commit()
    print(f"✅ {len(tips)} tips cargados exitosamente")


def cargar_recompensas(db):
    """Carga el catálogo de medallas y recompensas"""
    recompensas_existentes = db.query(Recompensa).count()
    if recompensas_existentes > 0:
        print("ℹ️  Las recompensas ya existen, omitiendo...")
        return

    recompensas = [
        Recompensa(
            nombre="Primera Semilla",
            descripcion="Completa tu primera misión en Semiverd",
            icono_emoji="🌱",
            tipo="medalla",
            condicion="Completar 1 misión",
            puntos_necesarios=0
        ),
        Recompensa(
            nombre="Guardián del Río",
            descripcion="Completaste la misión del Río Caudal",
            icono_emoji="💧",
            tipo="medalla",
            condicion="Completar misión Río Caudal",
            puntos_necesarios=150
        ),
        Recompensa(
            nombre="Reforestador Urbano",
            descripcion="Completaste la misión del Bosque de Humo",
            icono_emoji="🌳",
            tipo="medalla",
            condicion="Completar misión Bosque de Humo",
            puntos_necesarios=200
        ),
        Recompensa(
            nombre="Tecnología Verde",
            descripcion="Completaste la misión del Valle Energético",
            icono_emoji="⚡",
            tipo="medalla",
            condicion="Completar misión Valle Energético",
            puntos_necesarios=250
        ),
        Recompensa(
            nombre="Semilla Verde Total",
            descripcion="¡Completaste todas las misiones! Eres un verdadero Guardián de Barrancabermeja",
            icono_emoji="🏆",
            tipo="titulo",
            condicion="Completar las 4 misiones",
            puntos_necesarios=900
        ),
        Recompensa(
            nombre="Árbol Centenario",
            descripcion="Tu árbol Semiverd ha alcanzado el nivel máximo de crecimiento",
            icono_emoji="🌲",
            tipo="titulo",
            condicion="Alcanzar nivel de árbol 10",
            puntos_necesarios=1000
        ),
    ]

    for recompensa in recompensas:
        db.add(recompensa)

    db.commit()
    print(f"✅ {len(recompensas)} recompensas cargadas exitosamente")


def main():
    """Función principal del seed"""
    print("🌱 Iniciando carga de datos de Semiverd...")
    print("=" * 50)

    # 1. Crear tablas
    crear_tablas()

    # 2. Abrir sesión y cargar datos
    db = SessionLocal()
    try:
        cargar_misiones(db)
        cargar_tips(db)
        cargar_recompensas(db)
        print("=" * 50)
        print("✅ ¡Base de datos de Semiverd lista! 🌿")
    except Exception as e:
        print(f"❌ Error durante el seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
