from fastmcp import FastMCP

from database import Base, engine
from models import AgentUser

from auth import signup, login

Base.metadata.create_all(bind=engine)

mcp = FastMCP("Agent Authentication Server")


@mcp.tool()
def agent_signup(username: str, password: str, goal: str) -> dict:
    """
    Register a new agent account.
    """

    if len(password) < 8:
        return {
            "success": False,
            "message": "Password must contain at least 8 characters"
        }

    return signup(username, password, goal)


@mcp.tool()
def agent_login(username: str, password: str) -> dict:
    """
    Authenticate an agent and return an access token.
    """

    return login(username, password)


if __name__ == "__main__":

    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000
    )