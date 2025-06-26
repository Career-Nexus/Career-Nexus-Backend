# Career Nexus Backend Documentation

---

## Index<a name='toc'></a>

## {{TOC}}

# User Registeration

This API registers user on the platform. N.B: Email confirmation is enforced using OTP.

**Endpoint:**`user/signup/`

## Payload

```json
email:*****

password1:*****

password2:*****

otp **for confirmation:*****

}
```

**Method:** `POST`

## Response body

**status code:201**

```json
"status":"OTP sent"
  } success without sending OTP payload

{
"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NzI5MTM4MCwiaWF0IjoxNzQ3MjA0OTgwLCJqdGkiOiI5MjRlMWY3NTNjM2I0NzFjYmNjYmM4YTc0MTJhZTQ4ZSIsInVzZXJfaWQiOjF9.3XAZo7Y5ylKUt5pQRFJEgT-pcY7h48XZ17L0WPrLePQ",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MjI2NTgwLCJpYXQiOjE3NDcyMDQ5ODAsImp0aSI6IjkzYWMxZWQ4MjMyMzRjYWFiYzdmM2ZiZmZmMzVkMGRjIiwidXNlcl9pZCI6MX0.ho7_rOofWa_bSyL88Wa1cf7kr-9C_-7uDRtMbkq14GA"
"email":"example@gmail.com"
"status":"Success"
} success with sending OTP payload
```

[Table of contents](#toc)

## 

# Verify Otp Hash

This endpoint verifies the validity of a hash used in alternate verification me  
thod during user registration.  

**Endpoint:**`user/hash/verify/`  

**Method:** `POST`  

## Payload

```json
{  

hash:*****  

}  
```

## Response body

**status code:201**  

```json
{  
"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaC  
IsImV4cCI6MTc0NzI5MTM4MCwiaWF0IjoxNzQ3MjA0OTgwLCJqdGkiOiI5MjRlMWY3NTNjM2I0NzFjY  
mNjYmM4YTc0MTJhZTQ4ZSIsInVzZXJfaWQiOjF9.3XAZo7Y5ylKUt5pQRFJEgT-pcY7h48XZ17L0WPr  
LePQ",  
 "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzI  
iwiZXhwIjoxNzQ3MjI2NTgwLCJpYXQiOjE3NDcyMDQ5ODAsImp0aSI6IjkzYWMxZWQ4MjMyMzRjYWFi  
YzdmM2ZiZmZmMzVkMGRjIiwidXNlcl9pZCI6MX0.ho7_rOofWa_bSyL88Wa1cf7kr-9C_-7uDRtMbkq  
14GA"  
"email":"example@gmail.com"  
"status":"Success"  
}   
```

[Table of contents](#toc) 

# Login API

This endpoint authenticates a user using email and password.

**Method:** `POST`  
**Endpoint:** `/user/signin`

## Request Body

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

## Response

 **status code:200**

```json
{
 "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjA5MDgxNCwiaWF0IjoxNzQ2MDA0NDE0LCJqdGkiOiI3NjkyOGY4OTZhYmY0ZmEwODJmYTc3NmUzYWZkZmRiMyIsInVzZXJfaWQiOjF9.BWuP8ogqd8DngeZQTgdzrEPW8c3dKi9_tYdTHLyEmhw",
 "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDI2MDE0LCJpYXQiOjE3NDYwMDQ0MTQsImp0aSI6IjJkNzRlNDI1N2E1YzQ1ZTQ5NGQ1OTQ2MTU3Njc5NzNhIiwidXNlcl9pZCI6MX0.TkC5-SF7KQI993gQFMme9juUVzlF4IJqN4GmLAx8o8I",
 "user": "saliuoazeez@gmail.com"
}
```

[Table of contents](#toc) 

# LogOut

Logsout the user and blacklists the access token.

**Endpoint:**`/user/signout/`

## Payload

```json
refresh:*****

}
```

**Method:** `POST`

## Response body

**status code:202**

```json
    "status":"Logged out"
}
```

[Table of contents](#toc)

# Profile Retrieve API

This endpoint retrieve a logged in user or retrieves a third party's profile data if a query parameter of user_id is passed to the url.

**NB:user must be authenticated via Bearer token**

**Method:** `GET`  
**Endpoint:** `user/retrieve-profile/`

## Response Body

**status code:200**

```json
{
  "first_name": "Opeyemi",
  "last_name": "Saliu",
  "middle_name": "Abdul-Azeez",
  "cover_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png",
  "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png",
  "location": "Alabama, USA",
  "position": "Aquaculturist and Graduate assistant",
  "bio": "Aquaculturist | UI/UX | Graduate Assistant",
  "qualification": "Bachelor of Science",
  "intro_video": "",
  "summary": "An aquaculturist with over 5 years of working expeience.",
  "experience": [
    {
      "id": 4,
      "title": "Extension Officer",
      "organization": "Aller Aqua",
      "start_date": "2022-12-21",
      "end_date": "2024-12-20",
      "location": "Lagos",
      "employment_type": "Onsite",
      "detail": "Managed the sales department of the company."
    },
    {
      "id": 3,
      "title": "Aquaculturist",
      "organization": "Atlantic shrimpers",
      "start_date": "2020-01-19",
      "end_date": "2022-11-29",
      "location": "Lagos",
      "employment_type": "Onsite",
      "detail": "Managed the culturing of shrimps and prawns."
    }
  ],
  "education": [
    {
      "id": 6,
      "course": "Aquaculture (MsC)",
      "school": "Auburn University Alabama,",
      "start_date": "2025-01-03",
      "end_date": "Present",
      "location": "USA",
      "detail": "Began studying for a masters degree in Aquaculture."
    },
    {
      "id": 5,
      "course": "Aquaculture and Fisheries Management",
      "school": "Federal University of Agriculture Abeokuta",
      "start_date": "2011-02-12",
      "end_date": "2016-07-23",
      "location": "Abeokuta",
      "detail": "Graduated with a Second class upper honors"
    }
  ],
  "certification": [
    {
      "id": 3,
      "title": "Introduction to frontend development",
      "school": "Coursera",
      "issue_date": "2023-07-04",
      "cert_id": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1MzIzMTE1LCJpYXQiOjE3NDUzMDE1MTUsImp0aSI6IjU2ZGY1YTVhMGQ2NTRjMGI4MDMwMTcxY2MwZjUxMzE1IiwidXNlcl9pZCI6Mn0.y-c-FZ9U-130hlP0B4cIK8Vl21c72xnJHJWGZBWiiaU",
      "skills": "Html,CSS"
    }
  ],
  "followers": 1,
  "followings": 0
}
```

[Table of contents](#toc) 

# Update Profile

Updates profile data.

**Endpoint:**`/user/profile-update/`

## Payload

```json
qualification:*****

summary:*****

location:*****

position:*****

bio:*****

profile_photo:*****

cover_photo:*****

intro_video:*****

first_name:*****

last_name:*****

middle_name:*****

country_code:****

phone_number:****
}
```

**Method:** `PUT`

## Response body

**status code:201**

```json
  "first_name": "Opeyemi",
  "last_name": "Saliu",
  "middle_name": "Abdul Azeez",
  "country_code": "+234",
  "phone_number": "9069102522",
  "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/e740aee1-0716-4d16-aebc-924d43c3843dMy_Torso_Picture.jpg",
  "cover_photo": "https://careernexus-storage1.s3.amazonaws.com/cover_photos/6a687725-56b1-4f1e-ad55-ae814dce20febg_image1.jpeg",
  "qualification": "Bachelor of Engineering (Civil Engineering)",
  "intro_video": "https://careernexus-storage1.s3.amazonaws.com/intro_videos/6e34ee76-ac17-4146-b7e6-f645f46ce886test_video.mp4",
  "location": "Ogun",
  "bio": "Developer|Programmer|Innovation Specialist",
  "position": "Backend Developer at CareerNexus",
  "summary": "I am an experienced backend developer with over 4 years of experience in building world class standard tools, developing backend supporting systems and managing server side architecture."
}
```

[Table of contents](#toc) 

# User-industry Update

Updates the user type and industry of the user

**Endpoint:**`/user/profile-update/`

## Payload

```json
industry:*****

}
```

**Method:** `PATCH`

## Response body

**status code:206**

```json
  "industry": "technology",
  "email": "saliuoazeez@gmail.com"
}
```

[Table of contents](#toc)

# View Experience

Retrieves all the experience profile of the user

**Endpoint:**`user/experience/`

## Payload

```

```

**Method:** `GET`

## Response body

**status code:200**

```
[
  {
    "id": 2,
    "title": "Research Methodologist",
    "organization": "Delta Logistics",
    "start_date": "2022-10-29",
    "end_date": "2024-11-29",
    "location": "Lagos",
    "employment_type": "Remote",
    "detail": "Worked as a Research Methodologist, Innovation specialist and Python developer."
  },
  {
    "id": 1,
    "title": "Branch Service Associate",
    "organization": "Wema Bank PLC",
    "start_date": "2021-02-15",
    "end_date": "2022-10-18",
    "location": "Ogun",
    "employment_type": "Onsite",
    "detail": "Managed the cashpoint in various branches within the location."
  }
]
```

[Table of contents](#toc) 

# Add Experience

Adds a user experience data to user's profile

**Endpoint:**`/user/experience/`

## Payload

```{
title:*****

organization:*****

start_date:*****

end_date:*****

location:*****

employment_type:*****

detail:*****

}
```

**Method:** `POST`

## Response body

**status code:201**

```{
  "title": "Extension Officer",
  "organization": "Aller Aqua",
  "start_date": "2022-12-21",
  "end_date": "2024-12-20",
  "location": "Lagos",
  "employment_type": "Onsite",
  "detail": "Managed the sales department of the company."
}
```

```

```

[Table of contents](#toc) 

# Delete Experience

Deletes an experience data associated with the user

**Endpoint:**`user/experience/?experience_id=5`

## Payload

```

```

**Method:** `DELETE`

## Response body

**status code:204**

```{"status":"Deleted"}

```

[Table of contents](#toc) 

# Updating User Eperience

This endpoints updates data of a user's experience. It takes any of the allowed parameter as a payload and updates it accordingly.

**Endpoint:**`user/update-experience/`

## Payload

```json
{

id:*****

title:*****

organization:*****

start_date:*****

end_date:*****

location:*****

employment_type:*****

detail:*****

}
```

**Method:** `PUT`

## Response body

**status code:201**

```json
{
  "id": 2,
  "title": "Research Methodologist/Programmer",
  "organization": "Delta Logistics",
  "start_date": "2022-10-29",
  "end_date": "2024-11-29",
  "location": "Lagos",
  "employment_type": "Remote",
  "detail": "Worked as a Research Methodologist, Innovation specialist and Python developer."
}
```

[Table of contents](#toc)

# Retrieve Education API

Retrieves all education data of the user profile

**Endpoint:**`user/education/`

## Payload

```

```

**Method:** `GET`

## Response body

**status code:200**

```[
  {
    "id": 4,
    "course": "Backend Development",
    "school": "Meta through Coursera",
    "start_date": "2023-04-21",
    "end_date": "2023-05-18",
    "location": "Online",
    "detail": "Completed Online course"
  },
  {
    "id": 2,
    "course": "Civil Engineering",
    "school": "Federal University of Agriculture Abeokuta",
    "start_date": "2021-04-21",
    "end_date": "2022-06-05",
    "location": "Online",
    "detail": "Completed the online course"
  },
  {
    "id": 3,
    "course": "Civil Engineering",
    "school": "Federal University of Agriculture Abeokuta",
    "start_date": "2013-01-13",
    "end_date": "2018-11-15",
    "location": "Abeokuta",
    "detail": "Awarded Bachelor of Engineering honours Graduated with a Second Class Upper honors."
  }
]
```

[Table of contents](#toc) 

# Add Education API

Add education data to the user profile.

**Endpoint:**`user/education/`

## Payload

```{
course:*****

school:*****

start_date:*****

end_date:*****

location:*****

detail:*****

}
```

**Method:** `POST`

## Response body

**status code:201**

```{
    "id": 4,
    "course": "Backend Development",
    "school": "Meta through Coursera",
    "start_date": "2023-04-21",
    "end_date": "2023-05-18",
    "location": "Online",
    "detail": "Completed Online course"
  },
```

[Table of contents](#toc) 

# Delete Education

Deletes a profile education data.

**Endpoint:**`user/education/?education_id=7`

## Payload

```

```

**Method:** `DELETE`

## Response body

**status code:204**

[Table of contents](#toc) 

# View Certification

Views all certifications added to the user profile

**Endpoint:**`user/certification/`

**Method:** `GET`

## Response body

**status code:200**

```[
  {
    "id": 3,
    "title": "Introduction to frontend development",
    "school": "Coursera",
    "issue_date": "2023-07-04",
    "cert_id": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1MzIzMTE1LCJpYXQiOjE3NDUzMDE1MTUsImp0aSI6IjU2ZGY1YTVhMGQ2NTRjMGI4MDMwMTcxY2MwZjUxMzE1IiwidXNlcl9pZCI6Mn0.y-c-FZ9U-130hlP0B4cIK8Vl21c72xnJHJWGZBWiiaU",
    "skills": "Html,CSS"
  }
]
```

[Table of contents](#toc) 

# Add Certification

Adds certification data to user profile

**Endpoint:**`user/certification/`

```{
title:*****

school:*****

issue_date:*****

cert_id:*****

skills:*****

}
```

**Method:** `POST`

## Response body

**status code:201**

```{
    "id": 3,
    "title": "Introduction to frontend development",
    "school": "Coursera",
    "issue_date": "2023-07-04",
    "cert_id": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1MzIzMTE1LCJpYXQiOjE3NDUzMDE1MTUsImp0aSI6IjU2ZGY1YTVhMGQ2NTRjMGI4MDMwMTcxY2MwZjUxMzE1IiwidXNlcl9pZCI6Mn0.y-c-FZ9U-130hlP0B4cIK8Vl21c72xnJHJWGZBWiiaU",
    "skills": "Html,CSS"
  }
```

[Table of contents](#toc) 

# Delete Certification

Endpoint deletes a profile certification data.

**Endpoint:**`user/certification/?certification_id=4`

## Payload

```

```

**Method:** `DELETE`

## Response body

**status code:204**

```

```

[Table of contents](#toc) 

# User Analytics

This endpoint retrieves all the analytic data of the users's profile like number of connections, number of times the profile was viewed, etc...

**Endpoint:**`/user/analytics/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "total_posts": 3,
  "total_views": 12,
  "total_connections": 1
}
```

[Table of contents](#toc) 

# Profile Completion

This endpoint retrieves the percentage completion of a user's profile along with the completed and incomplete items.

**Endpoint:**`/user/completion/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "completion": 100,
  "incomplete_items": [],
  "complete_items": [
    "profile_photo",
    "intro_video",
    "experience",
    "certification",
    "bio",
    "education"
  ]
}
```

[Table of contents](#toc) 

# Post Get

This endpoints retrieves posts associated with the user's selected industry and also posts by mentors on the platform.

**Endpoint:**`/post/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
        "qualification": "Bachelor of Engineering (Civil Engineering)"
      },
      "body": "Fadman Montessori. School building leaders and table shakers.",
      "pic1": "https://careernexus-storage1.s3.amazonaws.com/posts/pic/d0642e69-2ff3-4179-9b6b-b745ec637088fadman_thumbnail.png",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-06-18T19:25:29.242254Z",
      "comment_count": 0,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "post_id": 12
    }
  ],
  "last_page": "http://127.0.0.1:8000/post/?page=1"
}
```

[Table of contents](#toc) 

# Post Retrieve

This endpoint retrieves a particular post through a post_id query parameter passed in the url.

**Endpoint:**`/post/?post_id=12`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "profile": {
    "id": 1,
    "first_name": "Opeyemi",
    "last_name": "Saliu",
    "middle_name": "Abdul-Azeez",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
    "qualification": "Bachelor of Engineering (Civil Engineering)"
  },
  "body": "Fadman Montessori. School building leaders and table shakers.",
  "pic1": "https://careernexus-storage1.s3.amazonaws.com/posts/pic/d0642e69-2ff3-4179-9b6b-b745ec637088fadman_thumbnail.png",
  "pic2": "N/A",
  "pic3": "N/A",
  "video": "N/A",
  "article": "N/A",
  "time_stamp": "2025-06-18T19:25:29.242254Z",
  "comment_count": 0,
  "like_count": 0,
  "share_count": 0,
  "parent": null,
  "post_id": 12
}
```

[Table of contents](#toc) 

# Post Create

This endpoint publishes a post by the logged in user.

**Endpoint:**`/post/`

**Method:** `POST`

## Payload

``` json
{

body:*****

pic1:*****

pic2:*****

pic3:*****

video:*****

article:*****

}

```
## Response body

**status code:201**

``` json
{
  "body": "Lately, I’ve been trying to spend less time glued to my screen and more time outside. There’s something incredibly calming about early morning walks — the way the air feels cooler and the birds sound louder when your phone’s on silent.

At the same time, I’ve been exploring some new AI tools for work, and I’m both amazed and slightly overwhelmed at how fast things are changing in tech. Balancing curiosity with intentional living is becoming its own kind of discipline.

Also started journaling again — not every day, but whenever something weighs on my mind. I find that writing, even just a few lines, helps me reset.

Anyone else feeling that urge to slow down while everything else speeds up?",
  "pic1": "N/A",
  "pic2": "N/A",
  "pic3": "N/A",
  "video": "N/A",
  "article": "N/A",
  "time_stamp": "2025-06-18T21:46:34.030565Z"
}
```

[Table of contents](#toc) 

# Create comment

This endpoint creates a comment to a post.

**Endpoint:**`/post/comment/`

**Method:** `POST`

## Payload

```json
{

post:*****

body:*****

}
```

## Response body

**status code:201**

```json
{
  "user": {
    "id": 1,
    "first_name": "Opeyemi",
    "last_name": "Saliu",
    "middle_name": "Abdul-Azeez",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/e740aee1-0716-4d16-aebc-924d43c3843dMy_Torso_Picture.jpg",
    "qualification": "Bachelor of Engineering (Civil Engineering)"
  },
  "body": "Lol, I think it has become somewhat like a custom.",
  "time_stamp": "2025-05-14T11:46:12.094543Z"
}
```

[Table of contents](#toc) 

# Get comment

This endpoint retrieves all the comments and sub-comment/replies relating to a post.

**Endpoint:**`/post/comment/?post_id=7`

**Method:** `GET`

## Payload

```json

```

## Response body

**status code:200**

```json
  [
  {
    "post": 7,
    "commenter": {
      "first_name": "N/A",
      "last_name": "N/A",
      "middle_name": "N/A",
      "profile_picture": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png"
    },
    "body": "Great content and really worth reading. Thank you Saliu.",
    "parent": null,
    "replies": [],
    "time_stamp": "2025-04-24T14:30:29.567863Z",
    "comment_id": 6
  },
  {
    "post": 7,
    "commenter": {
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_picture": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/e740aee1-0716-4d16-aebc-924d43c3843dMy_Torso_Picture.jpg"
    },
    "body": "You really need to see this guys!! Don't forget to leave a comment.",
    "parent": null,
    "replies": [],
    "time_stamp": "2025-05-13T16:35:39.864129Z",
    "comment_id": 7
  },
  {
    "post": 7,
    "commenter": {
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_picture": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/e740aee1-0716-4d16-aebc-924d43c3843dMy_Torso_Picture.jpg"
    },
    "body": "You really need to see this guys!! Don't forget to leave a comment.",
    "parent": null,
    "replies": [
      {
        "post": 7,
        "commenter": {
          "first_name": "Opeyemi",
          "last_name": "Saliu",
          "middle_name": "Abdul-Azeez",
          "profile_picture": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/e740aee1-0716-4d16-aebc-924d43c3843dMy_Torso_Picture.jpg"
        },
        "body": "Don't forget to leave a comment guys.",
        "parent": 8,
        "replies": [],
        "time_stamp": "2025-05-13T16:45:58.617940Z",
        "comment_id": 9
      }
    ],
    "time_stamp": "2025-05-13T16:36:28.468871Z",
    "comment_id": 8
  }
]
```

## Failure

**status code:400**

```{
  "error": "Inexistent post"
}
```

[Table of contents](#toc)

# Reply Comment

This endpoint creates a reply to the comment of a post. These replies are also retrieved through the get comment API.

**Endpoint:**`/post/reply/`

**Method:** `POST`

## Payload

```json
{

parent:*****

body:*****

}
```

## Response body

**status code:201**

```json
{
  "user": {
    "id": 1,
    "first_name": "Opeyemi",
    "last_name": "Saliu",
    "middle_name": "Abdul-Azeez",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/e740aee1-0716-4d16-aebc-924d43c3843dMy_Torso_Picture.jpg",
    "qualification": "Bachelor of Engineering (Civil Engineering)"
  },
  "body": "Thank you for your time"
}
```

[Table of contents](#toc) 

# Post Like

This endpoint likes a post.

**Endpoint:**`/post/like/`

**Method:** `POST`

## Payload

```json
{

post:*****

}
```

## Response body

**status code:201**

```json
{
  "post": 6
}
```

[Table of contents](#toc) 

# Reposting

This endpoint reposts an already existing post along with an optional body of text. This is also treated as apost of it's own and is suggested and retrieved along with the get post API" 

**Endpoint:**`/post/repost/`

**Method:** `POST`

## Payload

```json
{

parent:*****

body:*****

}
```

## Response body

**status code:201**

```json
{
  "profile": {
    "id": 1,
    "first_name": "Opeyemi",
    "last_name": "Saliu",
    "middle_name": "Abdul-Azeez",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/e740aee1-0716-4d16-aebc-924d43c3843dMy_Torso_Picture.jpg",
    "qualification": "Bachelor of Engineering (Civil Engineering)"
  },
  "body": "Great content",
  "media": "N/A",
  "article": "N/A",
  "time_stamp": "2025-05-14T12:01:50.373904Z"
}
```

[Table of contents](#toc) 

# Post Save

This endpoint archives a post which could be retrieved by the logged in user.

**Endpoint:**`/post/save/`

**Method:** `POST`

## Payload

```json
{

post:*****

}
```

## Response body

**status code:201**

```json
{
  "post_id": 7
}
```

[Table of contents](#toc) 

# Get Saved Post

This endpoint retrieves all the saved posts by the logged in user.

**Endpoint:**`/post/save/`

**Method:** `GET`

## Payload

```json

```

## Response body

**status code:200**

```json
[
  {
    "post": {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/e740aee1-0716-4d16-aebc-924d43c3843dMy_Torso_Picture.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)"
      },
      "body": "Driving the Future: How Technology is Transforming Transportation\nTransportation has always been the engine of progress—moving people, goods, and ideas across cities, countries, and continents. But in the 21st century, it’s not just about getting from point A to point B. It’s about how we get there: faster, safer, cleaner, and smarter. And at the heart of this transformation? Technology.\n\n1. Autonomous Vehicles: From Sci-Fi to Street Legal\nWhat was once a futuristic dream is now cruising through city streets. Autonomous vehicles (AVs) use AI, sensors, and real-time data to navigate without human input. Companies like Waymo, Tesla, and Cruise are already testing and deploying self-driving cars, while autonomous trucks promise to revolutionize logistics and supply chains. The potential benefits are huge: fewer accidents, reduced congestion, and more accessible transportation for the elderly and disabled.\n\n2. Electrification: Powering a Sustainable Tomorrow\nThe shift from fossil fuels to electric power is reshaping the automotive industry. Electric vehicles (EVs) are no longer niche—they're mainstream. Governments are offering incentives, automakers are committing to electric-only futures, and battery tech is advancing rapidly. Beyond cars, electric buses, bikes, and even airplanes are emerging, helping reduce emissions and create a cleaner planet.\n\n3. Smart Infrastructure: Cities That Talk Back\nRoads, traffic lights, and parking lots are getting an upgrade. Smart infrastructure uses IoT (Internet of Things) sensors and connectivity to manage traffic flow, detect maintenance needs, and even communicate with autonomous vehicles. Imagine a traffic signal that adapts in real time to reduce congestion or a parking lot that directs you to an open spot. These innovations aren't just cool—they improve safety, reduce fuel use, and enhance urban life.\n\n4. Mobility-as-a-Service (MaaS): The End of Car Ownership?\nWith apps like Uber, Lyft, Bird, and Lime, personal car ownership is becoming less necessary in urban environments. MaaS platforms integrate various transport options—bikes, scooters, rideshares, public transit—into a single, seamless service. Add in AI-powered route planning, and getting around becomes effortless, personalized, and more eco-friendly.\n\n5. Hyperloop & High-Speed Rail: Redefining Long-Distance Travel\nWhile still in early stages, hyperloop technology—propelling pods through low-pressure tubes at airplane speeds—could dramatically shorten travel times between major cities. Meanwhile, countries like Japan and France continue to lead the way with efficient high-speed rail, showing the world what’s possible with investment in advanced public transport.\n\n6. Data-Driven Decisions: Analytics Behind the Wheel\nEvery vehicle on the road today is a rolling data center. From GPS tracking to engine diagnostics, real-time data helps optimize routes, predict maintenance issues, and improve safety. Municipalities and logistics companies alike are leveraging this data to make smarter transportation decisions, reduce emissions, and cut costs.\n\nThe Road Ahead\nTechnology isn’t just changing how we move—it’s changing what’s possible. The intersection of AI, data, automation, and sustainability is creating a transportation revolution. But as we accelerate toward the future, we must ensure equity, safety, and accessibility for all. The journey has just begun.",
      "media": "N/A",
      "article": "N/A",
      "time_stamp": "2025-04-24T14:06:45.666911Z"
    }
  }
]
```

[Table of contents](#toc) 

# Post Share

This endpoint is designed to create a link particular to a post which could be called to retrieve the details of the post from external sources. Currently, it saves the post and associates it with the user and adds to the share count data which can be retrieved from the get posts API.

**Endpoint:**`/post/share/`

**Method:** `POST`

## Payload

```json
{

post:*****

}
```

## Response body

**status code:201**

```json
{
  "post_id": 7
}
```

[Table of contents](#toc) 

# Followings Posts

This endpoint retrieves the posts of users the logged in user is currently following.

**Endpoint:**`/post/following/`

**Method:** `GET`

## Payload

```json

```

## Response body

**status code:200**

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "profile": {
        "id": 2,
        "first_name": "N/A",
        "last_name": "N/A",
        "middle_name": "N/A",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png",
        "qualification": "Bachelor of Science"
      },
      "body": "Did you know? Conservation agriculture can increase crop yields by up to 30% while preserving soil health. Time to rethink how we farm sustainably. #AgriFacts #SustainableFarming",
      "media": "https://careernexus-storage1.s3.amazonaws.com/posts/media/98c7a008-4433-4f13-ae73-0e4640a758b4branch.jpeg",
      "article": "N/A",
      "time_stamp": "2025-04-17T14:30:11.005024Z",
      "comment_count": 1,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "post_id": 1
    },
    {
      "profile": {
        "id": 2,
        "first_name": "N/A",
        "last_name": "N/A",
        "middle_name": "N/A",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png",
        "qualification": "Bachelor of Science"
      },
      "body": "Farmers are the backbone of our food system. Supporting local agriculture means supporting healthier food and stronger communities. Let’s buy local. #SupportFarmers #AgroLife",
      "media": "N/A",
      "article": "N/A",
      "time_stamp": "2025-04-17T14:30:44.280807Z",
      "comment_count": 0,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "post_id": 2
    },
    {
      "profile": {
        "id": 2,
        "first_name": "N/A",
        "last_name": "N/A",
        "middle_name": "N/A",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png",
        "qualification": "Bachelor of Science"
      },
      "body": "Precision agriculture is transforming farming through data, GPS, and automation. The future of agri-tech is smart, efficient, and sustainable. #AgriTech #SmartFarming",
      "media": "N/A",
      "article": "N/A",
      "time_stamp": "2025-04-17T14:31:33.731704Z",
      "comment_count": 0,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "post_id": 3
    }
  ]
}
```

[Table of contents](#toc)

# 

# 


# Forget Password

This endpoint is a state API that manages password change by users. It manages the three stages of password change which it infers based on payload. Three stages are 1. OTP generation and sending 2. OTP/Hash verification 3. Password Change. Sending only email as payload discards any existing OTP and generates a new one which it sends to the email data. Sending only Hash or OTP verifies the hash and marks the user eligible for a password change. N.B: This eligibility is time constrained. 3. Sending email,password1 and password2 checks the eligibilty of the user and if eligible, changes the password accoridingly. Also note that there is only a single eligibility per password request and any immediate change must again be routed through the entire flow.

**Endpoint:**`/user/forget-password/`

**Method:** `POST`

## Payload

``` json
{

email:*****

password1:*****

password2:*****

otp:*****

hash:*****

}

```
## Response body

**status code:200**

``` json
{
	"status":"Password Changes"
	"email":"saliuoazeez@gmail.com"
}
```

[Table of contents](#toc)


# Get Country Phone Codes

This API retrieves countries and their phone codes. It optionally uses a query flag status to filter based on the countries current permissions on the platform. status could be either enable/disable and if status is exempted, it pulls the entire country lists on the platform irrespective of their status

**Endpoint:**`/info/country-permit/?status=disable`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 155,
    "country": "Nigeria ",
    "code": "+234"
  }
]
```

[Table of contents](#toc)


# Alter Country Permissions

This endpoint permits or unpermits country phone number codes from being allowed on the platform. N.B:status can either be enable or disable

**Endpoint:**`info/country-permit/`

**Method:** `PUT`

## Payload

``` json
{

country:*****

status:*****

}

```
## Response body

**status code:200**

``` json
{
  "country": "Nigeria ",
  "permitted": true
}
```

[Table of contents](#toc)


# Content Management

This endpoint retrieves contents and meta data based on the query string title.

**Endpoint:**`/info/?title=tos`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "status": "Success",
  "content": {
    "title": "tos",
    "content": "By accessing or using Career Nexus, you agree to be bound by these Terms and Conditions. Please read them carefully.\n1. Use of Platform You agree to use Career Nexus only for lawful purposes and in a way that does not infringe the rights of others.\n2. Account Responsibility You are responsible for maintaining the confidentiality of your account and password, and for all activities under your account.\n3. Data & Privacy Your data is handled in accordance with our Privacy Policy. We do not share your information without consent.\n4. Changes to Terms We reserve the right to update these terms at any time. Continued use of the platform means you accept any changes.\n5. Contact For questions or support, contact us at: support@career-nexus.com",
    "items": null,
    "updated": "2025-05-23"
  },
  "Available_titles": [
    "tos"
  ]
}
```

[Table of contents](#toc)


# Get Chat Sessions

This endpoint gets all chat sessions that had been initiated by or with the user.

**Endpoint:**`/chats/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "initiator": {
      "id": 3,
      "first_name": "N/A",
      "last_name": "N/A",
      "middle_name": "N/A",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png",
      "qualification": "Bachelor of Education (English)"
    },
    "contributor": {
      "id": 1,
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "qualification": "Bachelor of Engineering (Civil Engineering)"
    },
    "chat_id": 2
  },
  {
    "initiator": {
      "id": 1,
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "qualification": "Bachelor of Engineering (Civil Engineering)"
    },
    "contributor": {
      "id": 2,
      "first_name": "N/A",
      "last_name": "N/A",
      "middle_name": "N/A",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png",
      "qualification": "Bachelor of Science"
    },
    "chat_id": 1
  }
]
```

[Table of contents](#toc)


# Chat History

This endpoint gets all the previous chat messages of a particular chat session.

**Endpoint:**`/chats/messages/?chat_id=2`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "person": {
      "id": 3,
      "first_name": "N/A",
      "last_name": "N/A",
      "middle_name": "N/A",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png",
      "qualification": "Bachelor of Education (English)"
    },
    "message": "What's good",
    "timestamp": "2025-06-03T14:40:27.272781Z"
  },
  {
    "person": {
      "id": 1,
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "qualification": "Bachelor of Engineering (Civil Engineering)"
    },
    "message": "Hello friend",
    "timestamp": "2025-06-03T14:40:21.375709Z"
  }
]
```

[Table of contents](#toc)


# job Create

This endpoint creates a new job post. N.B: PAYLOAD OPTIONS include employment_type(full_time,part_time,internship,freelance,contract), work_type(remote,onsite,hybrid).

**Endpoint:**`/job/`

**Method:** `POST`

## Payload

``` json
{

title:*****

organization:*****

employment_type:*****

work_type:*****

country:*****

salary:*****

overview:*****

description:*****

experience_level:*****

}

```
## Response body

**status code:201**

``` json
{
  "title": "Backend Developer",
  "organization": "Mitiget Assurance Limited",
  "employment_type": "full_time",
  "work_type": "hybrid",
  "country": "Nigeria",
  "salary": "350,000NGN",
  "overview": "We are seeking a skilled and motivated Backend Developer to join our development team. You will be responsible for building and maintaining the server-side logic, database interactions, and API integrations that power our applications. The ideal candidate is experienced in backend technologies, database design, and scalable system architecture.",
  "description": "As a Backend Developer, you will play a crucial role in designing, implementing, and optimizing the backbone of our digital services. You'll work closely with frontend developers, DevOps engineers, and product teams to deliver robust and high-performance applications. Responsibilities include developing RESTful APIs, ensuring data integrity and security, managing database schemas, and optimizing application performance. A strong understanding of backend frameworks, data structures, and software engineering principles is essential.",
  "industry": "technology",
  "experience_level": "senior"
}
```

[Table of contents](#toc)


# Get Job Posts

This endpoint retrieves all the jobs posted by a user.

**Endpoint:**`/job/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "title": "Backend Developer",
      "organization": "Career Nexus Ltd",
      "employment_type": "full_time",
      "work_type": "hybrid",
      "country": "Nigeria",
      "salary": "350,000NGN",
      "overview": "We are looking",
      "description": "You'll be responsible for turning user needs into elegant, intuitive interfaces for both web and mobile applications."
    },
    {
      "title": "Backend Developer",
      "organization": "Career Nexus Ltd",
      "employment_type": "full_time",
      "work_type": "hybrid",
      "country": "Nigeria",
      "salary": "350,000NGN",
      "overview": "We are looking",
      "description": "You'll be responsible for turning user needs into elegant, intuitive interfaces for both web and mobile applications."
    }
  ]
}
```

[Table of contents](#toc)


# Recommended Job Posts.

This endpoint retrieves job posts related to the user based on their selected industry.

**Endpoint:**`/job/recommend/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "title": "Backend Developer",
      "organization": "Career Nexus Ltd",
      "employment_type": "full_time",
      "work_type": "hybrid",
      "country": "Nigeria",
      "salary": "350,000NGN",
      "overview": "We are looking",
      "description": "You'll be responsible for turning user needs into elegant, intuitive interfaces for both web and mobile applications."
    },
    {
      "title": "Backend Developer",
      "organization": "Career Nexus Ltd",
      "employment_type": "full_time",
      "work_type": "hybrid",
      "country": "Nigeria",
      "salary": "350,000NGN",
      "overview": "We are looking",
      "description": "You'll be responsible for turning user needs into elegant, intuitive interfaces for both web and mobile applications."
    }
  ]
}
```

[Table of contents](#toc)


# Job Preference

This endpoint sets a job preference for the user to let them get notifications when a job matching their set preferences has been posted. VALID PAYLOAD OPTIONS:employment_type(full_time,part_time,internship,contract,freelance), work_type(remote,onsite,hybrid), industry(agriculture,banking,business,commerce,construction,education,entertainment,government,health,manufacturing,media,others,sports,technology,transportation), experience_level(entry,mid,senior,executive).

**Endpoint:**`/job/preference/`

**Method:** `PUT`

## Payload

``` json
{

title:*****

employment_type:*****

work_type:*****

industry:*****

experience_level:*****

}

```
## Response body

**status code:200**

``` json
{
  "title": "Backend Developer",
  "employment_type": "full_time",
  "work_type": "hybrid",
  "industry": "technology",
  "experience_level": "senior"
}
```

[Table of contents](#toc)


# Job Notifications

This endpoint enables a logged in user to connect to a Job post notification websocket. N.B: A valid token must be attached as a query string to the endpoint url.

**Endpoint:**`/ws/notification/jobs/?token=******`

**Method:** `NONE`

## Payload

``` json


```
## Response body

**status code:NONE**

``` json
NONE
```

[Table of contents](#toc)


# Get Job Preference

This endpoint retrieves the job preferences set by the user or N/A if no preference has been set. It also includes a preference_set key in response which is True if the user has set his job preference or false if he has not.

**Endpoint:**`/job/preference/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "title": "Backend Developer",
  "employment_type": "full_time",
  "work_type": "remote",
  "industry": "technology",
  "experience_level": "senior",
  "preference_set": true
}
```

[Table of contents](#toc)


# Valid Choice

This endpoint retrieves valid request parameters for API fields. Running this endpoint without a request parameter retrieves all choice field names required in some request payloadss. Running this endpoint with a query parameter field_name=**** retrieves all the valid options for that choice field.

**Endpoint:**`/info/choice-data/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "field_names": [
    "industry",
    "employment_type",
    "user",
    "employment_category",
    "experience_level",
    "work_type"
  ]
}

OR

{
  "field_name": "experience_level",
  "Valid options": [
    "entry",
    "mid",
    "senior",
    "executive"
  ]
}
```

[Table of contents](#toc)


# Connection Retrieve

This endpoint retrieves all the connections that the user has established over the platform and the status whether they have or have not been confirmed by the recipient.

**Endpoint:**`/connection/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 3,
    "connection": {
      "first_name": "N/A",
      "last_name": "N/A",
      "middle_name": "N/A",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png",
      "qualification": "Bachelor of Science",
      "status": "CONFIRMED",
      "user_id": 2
    }
  },
  {
    "id": 4,
    "connection": {
      "first_name": "N/A",
      "last_name": "N/A",
      "middle_name": "N/A",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png",
      "qualification": "Bachelor of Education (English)",
      "status": "CONFIRMED",
      "user_id": 3
    }
  }
]
```

[Table of contents](#toc)


# Connection Create

This endpoint initiates a connection request to another user. The status of the connection is PENDING and is not regarded as a connection yet until the other User Accepts the reque connection to a user can only be initiated once while the status is PENDING/CONFIRMED>

**Endpoint:**`/connection/`

**Method:** `POST`

## Payload

``` json
{

connection:*****

}

```
## Response body

**status code:201**

``` json
{
  "user": 4,
  "connection": 3,
  "status": "PENDING"
}
```

[Table of contents](#toc)


# Connection Pending Retrieve

This endpoint retrieves all the pending connection requests that was initiated by other users of the platform. N.B: These connection requests are those involving the logged in user and not any requests between other users of the platform.

**Endpoint:**`/connection/pending/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 6,
    "connection": {
      "first_name": "Adeniji",
      "last_name": "Adekogbe",
      "middle_name": "Michael",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png",
      "qualification": "Bachelor of Science (Education)",
      "status": "PENDING",
      "user_id": 4
    }
  }
]
```

[Table of contents](#toc)


# Connection Accept/Reject

This endpoint accepts or rejects a pending connection request initiated by another user on the platform. N.B:Valid status payload is either Accept or Reject.

**Endpoint:**`/connection/status/`

**Method:** `POST`

## Payload

``` json
{

connection_id:*****

status:*****

}

```
## Response body

**status code:200**

``` json
{
  "status": "Rejected"
}
```

[Table of contents](#toc)


# Connection Recommendation

This endpoint recommends connections for the logged in user based on any of the criteria location/industry. This must be explicitly specified in the request URL as a query parameter.

**Endpoint:**`/connection/recommendation/?criteria=location`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 4,
      "name": "Adeniji Adekogbe",
      "qualification": "Bachelor of Science (Education)"
    }
  ],
  "last_page": "http://127.0.0.1:8000/connection/recommendation/?page=1"
}
```

[Table of contents](#toc)