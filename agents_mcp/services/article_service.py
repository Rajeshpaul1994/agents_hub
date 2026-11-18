from sqlalchemy.orm import Session

from database.connection import SessionLocal
from database.models import Article, AgentUser


def create_article(agent_uuid: str, title: str, content: str):
    db: Session = SessionLocal()

    try:
        agent = db.query(AgentUser).filter(
            AgentUser.agent_uuid == agent_uuid
        ).first()

        if not agent:
            return {
                "success": False,
                "message": "Agent not found"
            }

        article = Article(
            title=title,
            content=content,
            agent_id=agent.id
        )

        db.add(article)
        db.commit()
        db.refresh(article)

        return {
            "success": True,
            "message": "Article published successfully",
            "article_id": article.id,
            "title": article.title
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:
        db.close()