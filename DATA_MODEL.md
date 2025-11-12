# Modelo de datos - API UADE Academy

## Entidades Principales
- **Estudiante**: id(pk),nombre (str),apellido(str),email(str)
- **Curso**: id(pk),titulo(str),descripcion(str),duracion(int)
- **Inscripcion**:id(pk),estudiante(fk),curso(fk),fecha_inscripcion(date)
- **Asistencia**: id(pk),inscripcion(fk),fecha(date),presente(bool)
