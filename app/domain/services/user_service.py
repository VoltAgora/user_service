from app.adapters.persistence.user_repository import UserRepositorySQL
from app.adapters.http.user_dtos import UpdateProfileRequest, ChangeRoleRequest
from app.infrastructure.response import ResultHandler

class UserService:
    def __init__(self, user_repo: UserRepositorySQL):
        self.user_repo = user_repo

    def get_user(self, user_id: int):
        try:
            u = self.user_repo.get_by_id(user_id)
            if not u:
                return ResultHandler.not_found(message="Usuario no encontrado")
            data = {
                "id": u.id,
                "document": u.document,
                "name": u.name,
                "lastname": u.lastname,
                "phone": u.phone,
                "email": u.email,
                "role": u.role,
                "is_active": u.is_active
            }
            return ResultHandler.success(data=data)
        except Exception as e:
            print("Error get_user:", e)
            return ResultHandler.internal_error(message="Error al obtener usuario")

    def update_profile(self, target_user_id: int, payload: UpdateProfileRequest, current_user_payload: dict):
        # current_user_payload es lo que devuelve get_current_user (el JWT payload)
        try:
            current_user_id = int(current_user_payload.get("sub"))
            current_role = int(current_user_payload.get("role", 1))
        except Exception as e:
            return ResultHandler.unauthorized(message="Token inválido")

        # permiso: propio usuario o admin (role == 0)
        if current_user_id != target_user_id and current_role != 0:
            return ResultHandler.forbidden(message="No autorizado para editar este perfil")

        # Si intenta cambiar email, validar unicidad
        if payload.email:
            existing = self.user_repo.get_by_email(payload.email)
            if existing and existing.id != target_user_id:
                return ResultHandler.bad_request(message="El correo ya está registrado")

        updates = payload.model_dump(exclude_unset=True)
        try:
            updated_entity = self.user_repo.update_profile(target_user_id, updates)
            if not updated_entity:
                return ResultHandler.not_found(message="Usuario no encontrado")
            response = {
                "id": updated_entity.id,
                "document": updated_entity.document,
                "name": updated_entity.name,
                "lastname": updated_entity.lastname,
                "phone": updated_entity.phone,
                "email": updated_entity.email,
                "role": updated_entity.role,
                "is_active": updated_entity.is_active
            }
            return ResultHandler.success(data=response, message="Perfil actualizado")
        except Exception as e:
            print("Error update_profile:", e)
            return ResultHandler.internal_error(message="Error al actualizar perfil")

    def change_role(self, target_user_id: int, body: ChangeRoleRequest, current_user_payload: dict):
        try:
            current_role = int(current_user_payload.get("role", 1))
        except Exception:
            return ResultHandler.unauthorized(message="Token inválido")

        if current_role != 0:
            return ResultHandler.forbidden(message="Solo admin puede cambiar rol")

        target_user = self.user_repo.get_by_id(target_user_id)
        if not target_user:
            return ResultHandler.not_found(message="Usuario no encontrado")

        # HU-09 CA4: Mismo rol actual → no hacer cambios
        if target_user.role == body.role:
            return ResultHandler.success(
                data={"id": target_user.id, "role": target_user.role},
                message="El rol ya está asignado"
            )

        # HU-09 CA3: No dejar sistema sin administradores activos
        if target_user.role == 0 and body.role != 0:
            other_admins = self.user_repo.count_active_admins(exclude_user_id=target_user_id)
            if other_admins < 1:
                return ResultHandler.bad_request(
                    message="Debe existir al menos un administrador activo"
                )

        try:
            updated_entity = self.user_repo.change_role(target_user_id, body.role)
            if not updated_entity:
                return ResultHandler.not_found(message="Usuario no encontrado")
            return ResultHandler.success(
                data={"id": updated_entity.id, "role": updated_entity.role},
                message="Rol actualizado"
            )
        except Exception as e:
            print("Error change_role:", e)
            return ResultHandler.internal_error(message="Error al cambiar rol")