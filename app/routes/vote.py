from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Response
from .. import schemas, database, models, oauth2
from sqlmodel import select

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    session: database.SessionDependency,
    current_user: oauth2.OauthDependency
    ) -> dict:
    
    post = session.get(models.Post, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    vote_query = session.exec(
        select(models.Votes).where(
            models.Votes.post_id == vote.post_id,
            models.Votes.user_id == current_user.id
        )
    )
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted on this post")
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        session.delete(found_vote)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)