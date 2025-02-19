from sqlalchemy.orm import Session
import app.repository.environment as repo
import app.schemas.environment as schemas

def assign_environment(user_id: int, db: Session):
    """
    Creates a new user record in the database.

    Args:
        user (UserBase): The data for the new user.
        db (Session): Database session dependency.

    Returns:
        Tuple: UserResponse object and error message (if any).
    """
    new_user, is_error = repo.create_user(user, db)
    if is_error:
        return None, "Failed to create user"

    user_response = schemas.UserResponse(
        user_id=new_user.user_id,
        username=new_user.username,
    )

    return user_response, None