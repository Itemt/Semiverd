"""
seed.py - Datos iniciales para la base de datos de Semiverd
Ejecutar una sola vez: python -m app.seed

Carga:
  - Las 4 misiones de las Semillas Verdes
  - 12 tips de la Academia de Guardianes
  - Recompensas base del sistema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import Base, Mision, Tip, Recompensa


def crear_tablas():
    """Crea todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")


def cargar_misiones(db):
    """Carga las 4 misiones de las Semillas Verdes"""
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
