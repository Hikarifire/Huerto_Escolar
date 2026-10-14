package cl.duoc.fotomotion.ui.alertas

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import cl.duoc.fotomotion.data.*
import cl.duoc.fotomotion.domain.model.EstadoLectura
import cl.duoc.fotomotion.domain.model.LecturaSensor
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class AlertasSensoresViewModel(application: Application) : AndroidViewModel(application) {
    private val db = AppDatabase.getInstance(application)
    private val repo = HuertoRepository(db.sectorDao(), db.cultivoDao(), db.tareaDao())

    private val _uiState = MutableStateFlow(AlertasSensoresUiState())
    val uiState: StateFlow<AlertasSensoresUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            repo.obtenerTodasLasTareas().collect { t -> _uiState.update { it.copy(historial = t) } }
        }
        _uiState.update {
            it.copy(
                lecturasSensores = listOf(
                    LecturaSensor("SENS-01", "Sector A1 (Invernadero)", "2026-10-14 10:00", 22.0, 25.5, 50.0, "simulación académica", EstadoLectura.BAJO),
                    LecturaSensor("SENS-02", "Sector B2 (Exterior)", "2026-10-14 10:00", 65.0, 22.0, 62.0, "simulación académica", EstadoLectura.NORMAL)
                )
            )
        }
    }
}
