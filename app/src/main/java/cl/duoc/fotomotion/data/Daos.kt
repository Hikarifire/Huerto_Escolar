package cl.duoc.fotomotion.data

import androidx.room.*
import cl.duoc.fotomotion.model.*
import kotlinx.coroutines.flow.Flow

@Dao
interface SectorDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertar(sector: SectorEntity)
    @Query("SELECT * FROM sectores ORDER BY id DESC") fun obtenerSectores(): Flow<List<SectorEntity>>
}

@Dao
interface CultivoDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertar(cultivo: CultivoEntity)
    @Query("SELECT * FROM cultivos ORDER BY id DESC") fun obtenerTodosLosCultivos(): Flow<List<CultivoEntity>>
}

@Dao
interface TareaDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertar(tarea: TareaEntity)
    @Update suspend fun actualizar(tarea: TareaEntity)
    @Query("SELECT * FROM tareas ORDER BY id DESC") fun obtenerTodasLasTareas(): Flow<List<TareaEntity>>
}
