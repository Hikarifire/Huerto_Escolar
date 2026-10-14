package cl.duoc.fotomotion.ui.auth

import cl.duoc.fotomotion.domain.model.PerfilUsuario
import cl.duoc.fotomotion.domain.model.Usuario

data class AuthUiState(
    val usuarioLogueado: Usuario? = null,
    val usuariosFicticiosPrueba: List<Usuario> = listOf(
        Usuario("USR-001", "Profesor Carlos Silva", PerfilUsuario.ADMINISTRADOR, "Taller de Ecología", listOf("TODAS"), true),
        Usuario("USR-002", "Estudiante Mateo Rojas", PerfilUsuario.ESTUDIANTE, "Taller de Ecología", listOf("CONSULTAR"), true)
    )
)
