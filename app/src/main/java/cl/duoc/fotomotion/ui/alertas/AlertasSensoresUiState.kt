package cl.duoc.fotomotion.ui.alertas

import cl.duoc.fotomotion.domain.model.LecturaSensor
import cl.duoc.fotomotion.model.TareaEntity

data class AlertasSensoresUiState(
    val lecturasSensores: List<LecturaSensor> = emptyList(),
    val historial: List<TareaEntity> = emptyList()
)
