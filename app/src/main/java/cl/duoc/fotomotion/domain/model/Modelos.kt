package cl.duoc.fotomotion.domain.model

enum class PerfilUsuario { ADMINISTRADOR, ESTUDIANTE }
enum class EstadoLectura { NORMAL, ALTO, BAJO }

data class Usuario(
    val id: String,
    val nombreFicticio: String,
    val perfil: PerfilUsuario,
    val tallerAsignado: String,
    val funcionesAutorizadas: List<String>,
    val estadoCuenta: Boolean
)

data class LecturaSensor(
    val id: String,
    val sectorId: String,
    val fechaHoraLectura: String,
    val humedadSueloSimulada: Double,
    val temperaturaAmbientalSimulada: Double,
    val humedadAmbientalSimulada: Double,
    val origenDato: String = "simulación académica",
    val estadoLectura: EstadoLectura
)
