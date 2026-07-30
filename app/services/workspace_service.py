from app.models.user import User
from app.models.workspace import Workspace
from app.models.associations import WorkspaceMember
from app.models.enums import WorkspaceRole, SystemRole
from app.core.exceptions import ErrorMessages
from app.repositories.workspace_repo import WorkspaceRepository
from app.schemas.workspace import AddMemberRequest, WorkspaceCreateRequest, WorkspaceUpdateRequest
from fastapi import HTTPException, status


class WorkspaceService:

    def __init__(self, workspace_repo: WorkspaceRepository):
        self.workspace_repo = workspace_repo

    def create_workspace(
        self, current_user: User, dto: WorkspaceCreateRequest
    ) -> Workspace:
        workspace = Workspace(
            name=dto.name,
            description=dto.description,
            owner_id=current_user.id,
        )
        created_ws = self.workspace_repo.create(workspace)

        # Người tạo tự động trở thành OWNER
        self.workspace_repo.add_member(
            created_ws.id, current_user.id, WorkspaceRole.OWNER
        )
        self.workspace_repo.db.refresh(created_ws) # refresh lại session
        return self.workspace_repo.get_by_id(created_ws.id)

    def get_workspace_detail(
        self, workspace_id: str, current_user: User
    ) -> Workspace:
        workspace = self.workspace_repo.get_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found",
            )

        member = self.workspace_repo.get_member(workspace_id, current_user.id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this workspace",
            )

        return workspace

    def add_member(
        self, workspace_id: str, current_user: User, dto: AddMemberRequest
    ) -> WorkspaceMember:
        workspace = self.workspace_repo.get_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found",
            )

        # Chỉ OWNER hoặc EDITOR mới được phép thêm member
        requester = self.workspace_repo.get_member(
            workspace_id, current_user.id
        )
        if not requester or requester.role not in [
            WorkspaceRole.OWNER,
            WorkspaceRole.EDITOR,
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Owner or Editor can add members",
            )

        existing_member = self.workspace_repo.get_member(
            workspace_id, dto.user_id
        )
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of this workspace",
            )

        return self.workspace_repo.add_member(
            workspace_id, dto.user_id, dto.role
        )

    def remove_member(
        self, workspace_id: str, current_user: User, user_id_to_remove: str
    ) -> None:
        workspace = self.workspace_repo.get_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found",
            )

        requester = self.workspace_repo.get_member(
            workspace_id, current_user.id
        )
        if not requester:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

        member_to_remove = self.workspace_repo.get_member(
            workspace_id, user_id_to_remove
        )
        if not member_to_remove:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found in workspace",
            )

        # Không thể xóa Owner của Workspace
        if member_to_remove.role == WorkspaceRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove the workspace Owner",
            )

        # User tự rời khỏi nhóm HOẶC Owner/Editor thực hiện xóa
        is_self_removal = current_user.id == user_id_to_remove
        is_owner_or_editor = requester.role in [
            WorkspaceRole.OWNER,
            WorkspaceRole.EDITOR,
        ]

        if not (is_self_removal or is_owner_or_editor):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to remove this member",
            )

        self.workspace_repo.remove_member(member_to_remove)
        is_self_removal = (current_user.id == user_id_to_remove)
        is_admin_or_owner = requester.role in [WorkspaceRole.OWNER, SystemRole.ADMIN]

        if not (is_self_removal or is_admin_or_owner):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to remove this member")

        self.workspace_repo.remove_member(member_to_remove)

    def update_workspace(
        self, workspace_id: str, current_user: User, dto: WorkspaceUpdateRequest
    ) -> Workspace:
        workspace = self.workspace_repo.get_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessages.NOTFOUND_WORKSPACE
            )

        # Kiểm tra quyền: Chỉ OWNER hoặc EDITOR mới được sửa thông tin
        requester = self.workspace_repo.get_member(workspace_id, current_user.id)
        if not requester or requester.role not in [WorkspaceRole.OWNER, WorkspaceRole.EDITOR]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorMessages.UPDATE_PERMISSION_WORKSPACE,
            )

        # Trích xuất dữ liệu thực sự gửi lên (bỏ qua None)
        update_data = dto.model_dump(exclude_unset=True)
        if not update_data:
            return workspace

        return self.workspace_repo.update(workspace, update_data)

    def delete_workspace(self, workspace_id: str, current_user: User) -> None:
        workspace = self.workspace_repo.get_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessages.NOTFOUND_WORKSPACE,
            )

        # Kiểm tra quyền: Chỉ duy nhất OWNER mới được quyền xóa Workspace
        requester = self.workspace_repo.get_member(workspace_id, current_user.id)
        if not requester or requester.role != WorkspaceRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorMessages.DELETE_PERMISSION_WORKSPACE,
            )

        self.workspace_repo.delete(workspace)