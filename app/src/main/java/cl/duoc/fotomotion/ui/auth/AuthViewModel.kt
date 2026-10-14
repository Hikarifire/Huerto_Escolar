package cl.duoc.fotomotion.ui.auth

import androidx.lifecycle.ViewModel
import cl.duoc.fotomotion.domain.model.Usuario
import kotlinx.coroutines.flow.*

class AuthViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(AuthUiState())
    val uiState: StateFlow<AuthUiState> = _uiState.asStateFlow()

    fun seleccionarUsuario(usuario: Usuario) { _uiState.update { it.copy(usuarioLogueado = usuario) } }
    fun cerrarSesion() { _uiState.update { it.copy(usuarioLogueado = null) } }
}
