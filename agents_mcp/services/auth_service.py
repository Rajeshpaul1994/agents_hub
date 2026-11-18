import uuid
import hashlib
import secrets
import hmac

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from dotenv import load_dotenv
import os

from database.connection import SessionLocal
from database.models import AgentUser

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

serializer = URLSafeTimedSerializer(SECRET_KEY)


def hash_password(password: str) -> str:

    salt = secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        310000
    ).hex()

    return f"{salt}${hashed}"


def verify_password(password: str, stored_password: str) -> bool:

    salt, original_hash = stored_password.split("$")

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        310000
    ).hex()

    return hmac.compare_digest(
        original_hash,
        new_hash
    )


def signup(username: str, password: str, goal: str):

    db = SessionLocal()

    try:

        existing_user = db.query(AgentUser).filter(
            AgentUser.username == username
        ).first()

        if existing_user:
            return {
                "success": False,
                "message": "Username already exists"
            }

        agent_uuid = str(uuid.uuid4())

        user = AgentUser(
            username=username,
            agent_uuid=agent_uuid,
            password=hash_password(password),
            role="agent",
            goal=goal
        )

        db.add(user)
        db.commit()

        return {
            "success": True,
            "message": "Agent registered successfully",
            "agent_uuid": agent_uuid,
            "username": username
        }

    finally:
        db.close()


def login(username: str, password: str):

    db = SessionLocal()

    try:
        user = db.query(AgentUser).filter(
            AgentUser.username == username
        ).first()

        if not user:
            return {
                "success": False,
                "message": "Invalid username or password"
            }

        if not verify_password(password, user.password):
            return {
                "success": False,
                "message": "Invalid username or password"
            }

        token = serializer.dumps({
            "agent_uuid": user.agent_uuid,
            "role": user.role
        })

        return {
            "success": True,
            "message": "Login successful",
            "access_token": token,
            "agent_uuid": user.agent_uuid,
            "username": user.username,
            "role": user.role
        }

    finally:
        db.close()


def authenticate_agent(access_token: str):

    try:
        payload = serializer.loads(
            access_token,
            max_age=43200
        )

        agent_uuid = payload.get("agent_uuid")

        db = SessionLocal()

        try:

            user = db.query(AgentUser).filter(
                AgentUser.agent_uuid == agent_uuid
            ).first()

            if not user or user.role != "agent":
                return None

            return {
                "agent_uuid": user.agent_uuid,
                "username": user.username,
                "role": user.role,
                "goal": user.goal
            }

        finally:
            db.close()

    except (BadSignature, SignatureExpired):
        return None