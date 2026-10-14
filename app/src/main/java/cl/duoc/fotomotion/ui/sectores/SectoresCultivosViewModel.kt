package cl.duoc.fotomotion.ui.sectores

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import cl.duoc.fotomotion.data.*
import cl.duoc.fotomotion.model.*
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class SectoresCultivosViewModel(application: Application) : AndroidViewModel(application) {
    private val db = AppDatabase.getInstance(application)
    private val repo = HuertoRepository(db.sectorDao(), db.cultivoDao(), db.tareaDao())

    private val _uiState = MutableStateFlow(SectoresCultivosUiState())
    val uiState: StateFlow<SectoresCultivosUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch { repo.obtenerSectores().collect { s -> _uiState.update { it.copy(sectores = s) } } }
        viewModelScope.launch { repo.obtenerCultivos().collect { c -> _uiState.update { it.copy(cultivos = c) } } }
    }

    fun cambiarNombreSector(v: String) { _uiState.update { it.copy(nuevoNombreSector = v) } }
    fun cambiarUbicacionSector(v: String) { _uiState.update { it.copy(nuevaUbicacionSector = v) } }

    fun guardarSector() {
        val st = _uiState.value
        if (st.nuevoNombreSector.isBlank()) return
        viewModelScope.launch {
            repo.guardarSector(SectorEntity(nombre = st.nuevoNombreSector, descripcion = "", ubicacion = st.nuevaUbicacionSector, estado = "EN_USO", responsableId = "DOC-001", fechaCreacion = "2026-10-14", fechaActualizacion = "2026-10-14"))
            _uiState.update { it.copy(nuevoNombreSector = "", nuevaUbicacionSector = "") }
        }
    }

    fun cambiarNombreCultivo(v: String) { _uiState.update { it.copy(nuevoNombreCultivo = v) } }
    fun cambiarSectorSeleccionado(id: Int) { _uiState.update { it.copy(sectorSeleccionadoId = id) } }

    fun guardarCultivo() {
        val st = _uiState.value
        if (st.nuevoNombreCultivo.isBlank() || st.sectorSeleccionadoId == null) return
        viewModelScope.launch {
            repo.guardarCultivo(CultivoEntity(nombreComun = st.nuevoNombreCultivo, descripcion = "", sectorId = st.sectorSeleccionadoId!!, fechaSiembra = "2026-10-14", fechaTrasplante = null, fechaEstimadaCosecha = "2026-12-01", frecuenciaRiegoDias = 1, estado = "SEMBRADO", observaciones = "", fotografiaReferencialFicticia = null))
            _uiState.update { it.copy(nuevoNombreCultivo = "", sectorSeleccionadoId = null) }
        }
    }
}
