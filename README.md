# Hangouts Expenses Calculation App

## Requirements 

**Project Proposal:**
For the graduation project, I propose that you create a system for booking meetings with friends at some venue. The task can be executed with a visual part (WEB, Android, IOS) as well as only backend in the form of an API.

**Context:**
Imagine that every week you meet with friends at some venue to have some tea and chat. Every time, some can attend, and some cannot. Also, at the end of the evening, you need to split the bill as fairly as possible. Instead of doing the math manually, it would be convenient if everything was divided automatically.

**Functional Requirements:**

**Login:**

- All pages/endpoints of the site should only be accessible to authenticated users.
- Authentication is done using the user's email and password.
- All users are unique; it's impossible to register more than one user for one email.
- All emails are considered valid by default, so there's no need to implement a confirmation system.

**Creating Meetings:**

- Every registered user should have the ability to create a meeting.
- A meeting should contain information about the venue, time, and participants.
- Users can be added to a meeting during its creation, editing, and users can also join the meeting independently.

**Displaying Meetings:**

- Every user can see all the meetings on the platform.
- Every user can join any meeting.

**Bill Splitting:**

- Users should be able to add purchases made during the meeting to it.
- When adding a purchase, you need to list all participants who are sharing this purchase. By default, it's all users attending the meeting.
- The meeting should display the amount each participating user owes.
- Only users added to the meeting can be included in the purchase.

**Comments:**

- All users added to the meeting should have the ability to leave a comment about it.
- The author of the comment should be able to update or delete it.

## Technical Stack

### App
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT

### CI/CD
- Docker
- GitHub Actions

## Run Application
To run application locally:
```
uvicorn src.main:app --reload
```

To access Swagger open:
```
http://127.0.0.1:8000/docs
```
