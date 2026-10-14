package cl.duoc.fotomotion.data

import cl.duoc.fotomotion.model.*
import kotlinx.coroutines.flow.Flow

class HuertoRepository(
    private val sectorDao: SectorDao,
    private val cultivoDao: CultivoDao,
    private val tareaDao: TareaDao
) {
    fun obtenerSectores(): Flow<List<SectorEntity>> = sectorDao.obtenerSectores()
    suspend fun guardarSector(sector: SectorEntity) = sectorDao.insertar(sector)

    fun obtenerCultivos(): Flow<List<CultivoEntity>> = cultivoDao.obtenerTodosLosCultivos()
    suspend fun guardarCultivo(cultivo: CultivoEntity) = cultivoDao.insertar(cultivo)

    fun obtenerTodasLasTareas(): Flow<List<TareaEntity>> = tareaDao.obtenerTodasLasTareas()
    suspend fun guardarTarea(tarea: TareaEntity) = tareaDao.insertar(tarea)
    suspend fun actualizarTarea(tarea: TareaEntity) = tareaDao.actualizar(tarea)
}
