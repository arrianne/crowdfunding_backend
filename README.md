# Crowdfunding Back End

Arrianne O'Shea

## Project Overview

This Django REST API enables users to create fundraisers and pledge contributions. With custom permissions, users can only modify their own fundraisers and pledges, while viewing is open to all.
It uses:
Django
Django REST Framework
Custom object-level permissions
Custom validation for money vs. skill pledges

## Planning:

### Concept/Name

🧠 Planning

This backend powers a community-driven crowdfunding system for body corporates or strata buildings who perhaps don't have enough money in their sinking funds to complete works in the common areas of the building.
Owners/committee members can create fundraisers for issues such as:

Fixing roof leaks
Painting stairwells
Repairing shared gardens
Upgrading lighting

Other residents/friends/family/tradespeople can support fundraisers in two ways:

Money pledges — contributing funds
Skill pledges — contributing trade skills or labour

The backend handles authentication, permissions, validation, and the relationships between users, fundraisers, and pledges.

### Intended Audience

Owners
Residents
Committee members
Tradespeople
Contractors

### User Stories

As a resident, I can view all fundraisers happening in the building.
As a resident, I can create a new fundraiser.
As a neighbour, I can pledge money to help fund a project.
As a tradesperson, I can pledge skills (e.g., electrical, carpentry).
As a user, I can update my own pledge if needed.
As a fundraiser creator, I can edit my fundraiser, but not others.
As any visitor, I can browse all fundraisers and pledges without logging in.
As an authenticated user, I can support fundraisers by pledging.

### Front End Pages/Functionality

- **Homepage (Fundraisers List)**

  - Displays all fundraisers retrieved from `/fundraisers/`
  - Shows basic details: title, image, goal, progress
  - Allows users to click into fundraiser details
  - Publicly accessible (no login required)

- **Fundraiser Detail Page**

  - Shows full fundraiser information
  - Displays a list of all pledges associated with the fundraiser
  - Allows logged-in users to create a pledge
  - Allows the owner to edit the fundraiser

- **Create Fundraiser Page**

  - Form for entering title, description, goal, and image
  - Submits data to `/fundraisers/` via POST
  - Only available to authenticated users

- **Create Pledge Page**

  - Allows a user to choose between “Money” or “Skill” pledge
  - Money pledge requires `amount`
  - Skill pledge requires `skill_description`
  - Automatically links pledge to logged-in supporter
  - POSTs to `/pledges/`

- **User Dashboard (future enhancement)**
  - Shows fundraisers they’ve created
  - Shows pledges they’ve made

### API Spec

| URL                  | HTTP Method | Purpose                              | Request Body                                                                 | Success Response Code | Authentication / Authorisation |
| -------------------- | ----------- | ------------------------------------ | ---------------------------------------------------------------------------- | --------------------- | ------------------------------ |
| `/fundraisers/`      | GET         | List all fundraisers                 | None                                                                         | 200                   | Public                         |
| `/fundraisers/`      | POST        | Create a new fundraiser              | `{ "title", "description", "goal", "image", "is_open" }`                     | 201                   | Authenticated users only       |
| `/fundraisers/<id>/` | GET         | Retrieve a fundraiser (with pledges) | None                                                                         | 200                   | Public                         |
| `/fundraisers/<id>/` | PUT         | Update a fundraiser                  | Any fundraiser fields                                                        | 200                   | Only the owner                 |
| `/pledges/`          | GET         | List all pledges                     | None                                                                         | 200                   | Public                         |
| `/pledges/`          | POST        | Create a pledge (money or skill)     | `{ "pledge_type", "amount?", "skill_description?", "hours?", "fundraiser" }` | 201                   | Authenticated users only       |
| `/pledges/<id>/`     | GET         | Retrieve a single pledge             | None                                                                         | 200                   | Public                         |
| `/pledges/<id>/`     | PUT         | Update a pledge                      | Money/skill pledge fields                                                    | 200                   | Only the supporter             |

### DB Schema

![]( {{ ./relative/path/to/your/schema/image.png }} )
