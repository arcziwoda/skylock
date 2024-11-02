from fastapi import HTTPException, Path


def validate_path(path: str = Path(...)):
    if not path.strip():
        raise HTTPException(status_code=400, detail="Path cannot be an empty string")
    return path
