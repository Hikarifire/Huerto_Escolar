package cl.duoc.fotomotion.ui.sectores

import cl.duoc.fotomotion.model.CultivoEntity
import cl.duoc.fotomotion.model.SectorEntity

data class SectoresCultivosUiState(
    val sectores: List<SectorEntity> = emptyList(),
    val cultivos: List<CultivoEntity> = emptyList(),
    val nuevoNombreSector: String = "",
    val nuevaUbicacionSector: String = "",
    val nuevoNombreCultivo: String = "",
    val sectorSeleccionadoId: Int? = null
)
