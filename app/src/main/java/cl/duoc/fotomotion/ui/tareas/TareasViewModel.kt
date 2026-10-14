package cl.duoc.fotomotion.ui.tareas

import android.app.Application
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import cl.duoc.fotomotion.data.*
import cl.duoc.fotomotion.model.TareaEntity
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class TareasViewModel(application: Application) : AndroidViewModel(application) {
    private val db = AppDatabase.getInstance(application)
    private val repo = HuertoRepository(db.sectorDao(), db.cultivoDao(), db.tareaDao())

    private val _uiState = MutableStateFlow(TareasUiState())
    val uiState: StateFlow<TareasUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch { repo.obtenerTodasLasTareas().collect { t -> _uiState.update { it.copy(tareas = t) } } }
    }

    fun seleccionarTarea(t: TareaEntity) { _uiState.update { it.copy(tareaEnEjecucion = t) } }
    fun setUri(uri: Uri?) { _uiState.update { it.copy(imagenEvidenciaUri = uri) } }

    fun enviarTarea() {
        val t = _uiState.value.tareaEnEjecucion ?: return
        viewModelScope.launch {
            repo.actualizarTarea(t.copy(estado = "PENDIENTE_DE_VALIDACION", fechaHoraRealizacion = "2026-10-14 14:00", fotografiaAdjunta = _uiState.value.imagenEvidenciaUri?.toString()))
            _uiState.update { it.copy(tareaEnEjecucion = null, imagenEvidenciaUri = null) }
        }
    }

    fun validar(t: TareaEntity, aprobada: Boolean) {
        viewModelScope.launch {
            repo.actualizarTarea(t.copy(estado = if (aprobada) "VALIDADA" else "RECHAZADA", fechaHoraValidacion = "2026-10-14 14:30"))
        }
    }
}
