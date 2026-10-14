package cl.duoc.fotomotion.ui.tareas

import android.net.Uri
import cl.duoc.fotomotion.model.TareaEntity

data class TareasUiState(
    val tareas: List<TareaEntity> = emptyList(),
    val tareaEnEjecucion: TareaEntity? = null,
    val imagenEvidenciaUri: Uri? = null,
    val comentarioEstudiante: String = ""
)
