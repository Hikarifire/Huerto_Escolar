package cl.duoc.fotomotion.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "sectores")
data class SectorEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val nombre: String,
    val descripcion: String,
    val ubicacion: String,
    val estado: String,
    val responsableId: String,
    val fechaCreacion: String,
    val fechaActualizacion: String
)

@Entity(tableName = "cultivos")
data class CultivoEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val nombreComun: String,
    val descripcion: String,
    val sectorId: Int,
    val fechaSiembra: String?,
    val fechaTrasplante: String?,
    val fechaEstimadaCosecha: String?,
    val frecuenciaRiegoDias: Int,
    val estado: String,
    val observaciones: String,
    val fotografiaReferencialFicticia: String?
)

@Entity(tableName = "tareas")
data class TareaEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val tipo: String,
    val descripcion: String,
    val sectorId: Int,
    val cultivoId: Int?,
    val fechaCreacion: String,
    val fechaProgramada: String,
    val responsableId: String,
    val creadorId: String,
    val estado: String,
    val fechaHoraRealizacion: String?,
    val fotografiaAdjunta: String?,
    val comentarioEstudiante: String?,
    val comentarioDocente: String?,
    val validadorId: String?,
    val fechaHoraValidacion: String?
)
