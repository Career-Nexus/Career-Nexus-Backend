# Career Nexus Backend Documentation

---

## Index<a name='toc'></a>

## {{TOC}}

# User Registeration

This endpoint registers a new user (Learner/Mentor) in the system. If the payload property 'industry' is sent in the payload request, a mentor is registered in the system. If the payload 'industry' is not included in the request, a learner is registered into the system. N.B:Otp is enforced to certify email address ownership. In the first stage, a request without OTP property in the payload is sent, after email validation, an otp is sent to the email for verification. In the second stage, the same request payload is repeated but this time sent with an otp after verification, an account is created for the user, logged in and an access token is returned in the response.

**Endpoint:**`/user/signup/`

**Method:** `POST`

## Payload

``` json
{

email:*****

industry:*****

password1:*****

password2:*****

otp:*****

}

```
## Response body

**status code:201**

``` json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MjEzMTY4MiwiaWF0IjoxNzUyMDQ1MjgyLCJqdGkiOiJlMmNjZmY0NTU5NjY0Njk0YmUzZDJhM2EzYjI5YzI1NyIsInVzZXJfaWQiOjExfQ.A6FBhNeJ3TZAP4vFOETfT1KgPxBh_6Joe2GAHeiYLWM",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyMDY2ODgyLCJpYXQiOjE3NTIwNDUyODIsImp0aSI6IjI2YTRiZWYwZTBhOTQwMmRiM2U1YjExZjMzMzlkZDZmIiwidXNlcl9pZCI6MTF9.oq8ScALElAUkGUoAf3UfLyRSam94IXCjouHKrHd-MC8",
  "user": "opeyemi_cn2@yopmail.com",
  "status": "Success"
}
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

**Endpoint:**`/user/signin/`

**Method:** `POST`

## Payload

``` json
{

email:*****

password:*****

}

```
## Response body

**status code:200**

``` json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MjEzMzY0OSwiaWF0IjoxNzUyMDQ3MjQ5LCJqdGkiOiI3NTYxZDVjY2ZkNjk0YzBhYTRjN2YzYWYyZTc2ODBhNiIsInVzZXJfaWQiOjF9.JTan4KwvZYOy5J696suc_klUvl16ruVzr8mCmHgsh4g",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyMDY4ODQ5LCJpYXQiOjE3NTIwNDcyNDksImp0aSI6IjVlY2E0ZjA4OGRhODRiODRhODRmMzgxM2Y2YjQ1YzdkIiwidXNlcl9pZCI6MX0.xQRfYoFM9tbaz7SOt9jKqro9GcrKk4t-dj3UT_qp4Fk",
  "user": "saliuoazeez@gmail.com",
  "user_type": "learner"
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

# Profile Retrieve

This endpoint retrieve a logged in user or retrieves a third party's profile data if a query parameter of user_id is passed to the url. N.B:The user_type of the request instance determines the structure of the data passed in the response. properties like years_of_experience,timezone,mentorship_styles,technical_skills etc are only available to mentors profile which is automatically retrieved in response. Retrieving learners profile does not contain sthese properties.

**Endpoint:**`/user/retrieve-profile/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
LEARNERS
{
  "first_name": "Opeyemi",
  "last_name": "Saliu",
  "middle_name": "Abdul-Azeez",
  "country_code": "+234",
  "phone_number": "9069102522",
  "cover_photo": "https://careernexus-storage1.s3.amazonaws.com/cover_photos/70114098-5014-4eda-a725-5421792972dadefault_cp.jpeg",
  "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
  "location": "Ogun",
  "position": "Backend Developer at CareerNexus",
  "bio": "Developer|Programmer|Innovation Specialist",
  "qualification": "Bachelor of Engineering (Civil Engineering)",
  "intro_video": "https://careernexus-storage1.s3.amazonaws.com/intro_videos/6e34ee76-ac17-4146-b7e6-f645f46ce886test_video.mp4",
  "summary": "I am an experienced backend developer with over 4 years of experience in building world class standard tools, developing backend supporting systems and managing server side architecture.",
  "experience": [
    {
      "id": 2,
      "title": "Research Methodologist/Programmer",
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
  ],
  "education": [
    {
      "id": 2,
      "course": "Civil Engineering",
      "school": "Federal University of Agriculture Abeokuta",
      "start_date": "2021-04-21",
      "end_date": "2022-06-05",
      "location": "Abeokuta",
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
  ],
  "certification": [
    {
      "id": 1,
      "title": "Django Rest Framework",
      "school": "Coursera",
      "issue_date": "2023-07-04",
      "cert_id": "iJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyMzEzMDI2LCJpYXQiOjE3NDIyOTE0MjYsImp0aSI6ImYwZjVjMzNjYWQzMTRmYjY5NzMzNjRmYzQ2NzFkMjIwIiwidXNlcl9pZCI6NX0.2jYCbFrubaroyRZ",
      "skills": "Python Programming, Web development, Algorithms"
    }
  ],
  "followers": 1,
  "followings": 2,
  "resume": "https://careernexus-storage1.s3.amazonaws.com/resumes/51b434ab-441f-4ab1-ab72-a58c91ac7172Resume_080525.pdf",
  "timezone": "Africa/Lagos"
}
MENTORS
{
  "first_name": "Abdul Azeez",
  "last_name": "Balogun",
  "middle_name": "Abiola",
  "country_code": "+234",
  "phone_number": "9069102522",
  "cover_photo": "https://careernexus-storage1.s3.amazonaws.com/cover_photos/70114098-5014-4eda-a725-5421792972dadefault_cp.jpeg",
  "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
  "location": "Ogun state",
  "position": "",
  "bio": "",
  "qualification": "Bachelor of Engineering",
  "intro_video": "",
  "summary": "",
  "experience": [],
  "education": [],
  "certification": [],
  "years_of_experience": 6,
  "availability": "weekends",
  "current_job": "Backend Developer",
  "areas_of_expertise": [],
  "technical_skills": [
    "Python",
    "Shell Scripting",
    "Backend development",
    "Devops",
    "AI/ML",
    "Database Management System"
  ],
  "mentorship_styles": [],
  "resume": "",
  "timezone": "Canada/Central",
  "linkedin_url": null,
  "followers": 0,
  "followings": 0
}
```

[Table of contents](#toc) 

# Profile Update

This endpoint updates the profile data of a user. N.B:Some field updates such as years_of_experience, areas_of_expertise,availability,current_job,technical_skills,mentorship_styles and linkedin_url are only available to mentors and can only be updated by this user type. Also fields like areas_of_expertise,mentorship_styles and technical_skills properties must be a list of strings as their request format.

**Endpoint:**`/user/profile-update/`

**Method:** `PUT`

## Payload

``` json
{

first_name:*****

last_name:*****

middle_name:*****

country_code:*****

phone_number:*****

availability:*****

qualification:*****

location:*****

resume:*****

areas_of_expertise:*****

years_of_experience:*****

current_job:*****

technical_skills:*****

mentorship_styles:*****

profile_photo:*****

cover_photo:*****

summary:*****

position:*****

bio:*****

intro_video:*****

timezone:*****

linkedin_url:*****

}

```
## Response body

**status code:200**

``` json
MENTORS
{
  "first_name": "Opeyemi",
  "last_name": "Saliu",
  "middle_name": "Abdul-Azeez",
  "country_code": "+234",
  "phone_number": "9069102522",
  "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
  "cover_photo": "https://careernexus-storage1.s3.amazonaws.com/cover_photos/70114098-5014-4eda-a725-5421792972dadefault_cp.jpeg",
  "qualification": "Bachelor of Engineering",
  "intro_video": "",
  "location": "Ogun state",
  "bio": "",
  "position": "",
  "summary": "",
  "years_of_experience": 6,
  "availability": "weekends",
  "current_job": "Backend Developer",
  "areas_of_expertise": [],
  "technical_skills": [
    "Python",
    "Shell Scripting",
    "Backend development",
    "Devops",
    "AI/ML",
    "Database Management System"
  ],
  "mentorship_styles": [],
  "timezone": "UTC",
  "linkedin_url": null
}
LEARNERS
{
  "first_name": "Opeyemi",
  "last_name": "Saliu",
  "middle_name": "Abdul-Azeez",
  "country_code": "+234",
  "phone_number": "9069102522",
  "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
  "cover_photo": "https://careernexus-storage1.s3.amazonaws.com/cover_photos/70114098-5014-4eda-a725-5421792972dadefault_cp.jpeg",
  "qualification": "Bachelor of Engineering (Civil Engineering)",
  "intro_video": "https://careernexus-storage1.s3.amazonaws.com/intro_videos/6e34ee76-ac17-4146-b7e6-f645f46ce886test_video.mp4",
  "location": "Ogun",
  "bio": "Developer|Programmer|Innovation Specialist",
  "position": "Backend Developer at CareerNexus",
  "summary": "I am an experienced backend developer with over 4 years of experience in building world class standard tools, developing backend supporting systems and managing server side architecture.",
    "timezone": "UTC"
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

# Get Posts

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
  "count": 7,
  "next": "http://127.0.0.1:8000/post/?page=2",
  "previous": null,
  "results": [
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)"
      },
      "body": "From a friend.",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-07-11T11:44:28.647331Z",
      "comment_count": 1,
      "like_count": 0,
      "share_count": 0,
      "parent": {
        "profile": {
          "id": 2,
          "first_name": "N/A",
          "last_name": "N/A",
          "middle_name": "N/A",
          "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png",
          "qualification": "Bachelor of Science"
        },
        "body": "Precision agriculture is transforming farming through data, GPS, and automation. The future of agri-tech is smart, efficient, and sustainable. #AgriTech #SmartFarming",
        "pic1": "N/A",
        "pic2": "N/A",
        "pic3": "N/A",
        "video": "N/A",
        "article": "N/A",
        "time_stamp": "2025-04-17T14:31:33.731704Z"
      },
      "can_like": true,
      "can_follow": false,
      "is_self": true,
      "is_saved": false,
      "post_id": 18
    },
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)"
      },
      "body": "Lately, I’ve been trying to spend less time glued to my screen and more time outside. There’s something incredibly calming about early morning walks — the way the air feels cooler and the birds sound louder when your phone’s on silent.

At the same time, I’ve been exploring some new AI tools for work, and I’m both amazed and slightly overwhelmed at how fast things are changing in tech. Balancing curiosity with intentional living is becoming its own kind of discipline.

Also started journaling again — not every day, but whenever something weighs on my mind. I find that writing, even just a few lines, helps me reset.

Anyone else feeling that urge to slow down while everything else speeds up?",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-06-18T21:46:34.030565Z",
      "comment_count": 3,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": false,
      "is_self": true,
      "is_saved": false,
      "post_id": 13
    },
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)"
      },
      "body": "🌾 Tech in the Fields 📲🌍

Agriculture isn’t just about soil and sun anymore — it’s about sensors, satellites, and software. Farmers today use data analytics, autonomous tractors, and climate-smart tools to grow more with less. With technology in their hands, they’re not just feeding communities — they’re feeding the future.

#AgriInnovation #FarmTech #DigitalFarming #FutureOfFood",
      "pic1": "https://careernexus-storage1.s3.amazonaws.com/posts/media/0149c8fd-1055-4d23-9a2c-ac78ee61abc2branch.jpeg",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "#AgriTech #AgriInnovation",
      "time_stamp": "2025-05-15T13:44:08.197325Z",
      "comment_count": 0,
      "like_count": 1,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": false,
      "is_self": true,
      "is_saved": false,
      "post_id": 11
    }
  ],
  "last_page": "http://127.0.0.1:8000/post/?page=3"
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

This endpoint creates a comment to a post. N.B:The media field is optional meaning a comment can be made with or without a media attached but however, a comment MUST have a body text

**Endpoint:**`/post/comment/`

**Method:** `POST`

## Payload

``` json
{

post:*****

body:*****

media:*****

}

```
## Response body

**status code:201**

``` json
{
  "user": {
    "id": 1,
    "first_name": "Opeyemi",
    "last_name": "Saliu",
    "middle_name": "Abdul-Azeez",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
    "qualification": "Bachelor of Engineering (Civil Engineering)"
  },
  "body": "This is how i spend my time now.",
  "media": "https://careernexus-storage1.s3.amazonaws.com/comments/media/48214744-ac6a-410a-8116-e33492a1fd3dScreenshot_from_2025-04-30_23-26-06.png",
  "time_stamp": "2025-07-11T10:33:59.533796Z"
}
```

[Table of contents](#toc) 

# Get comment

This endpoint retrieves all the comments and sub-comments (replies) relating to a post.

**Endpoint:**`/post/comment/?post_id=13`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "post": 13,
    "commenter": {
      "first_name": "N/A",
      "last_name": "N/A",
      "middle_name": "N/A",
      "profile_picture": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png"
    },
    "body": "That's a very interesting piece",
    "media": "N/A",
    "parent": null,
    "replies": [
      {
        "post": 13,
        "commenter": {
          "first_name": "Opeyemi",
          "last_name": "Saliu",
          "middle_name": "Abdul-Azeez",
          "profile_picture": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg"
        },
        "body": "I can't believe I did comment this.",
        "media": "N/A",
        "parent": 12,
        "replies": [],
        "likes": 0,
        "time_stamp": "2025-07-11T11:13:31.478023Z",
        "can_like": true,
        "comment_id": 15
      }
    ],
    "likes": 0,
    "time_stamp": "2025-06-18T21:54:43.242430Z",
    "can_like": true,
    "comment_id": 12
  },
  {
    "post": 13,
    "commenter": {
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_picture": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg"
    },
    "body": "This is how i spend my time now.",
    "media": "https://careernexus-storage1.s3.amazonaws.com/comments/media/c036ce59-229f-4143-bc5b-49c63060c1d1Screenshot_from_2025-04-30_23-26-06.png",
    "parent": null,
    "replies": [],
    "likes": 1,
    "time_stamp": "2025-07-11T10:29:20.820639Z",
    "can_like": false,
    "comment_id": 13
  },
  {
    "post": 13,
    "commenter": {
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_picture": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg"
    },
    "body": "This is how i spend my time now.",
    "media": "https://careernexus-storage1.s3.amazonaws.com/comments/media/48214744-ac6a-410a-8116-e33492a1fd3dScreenshot_from_2025-04-30_23-26-06.png",
    "parent": null,
    "replies": [],
    "likes": 0,
    "time_stamp": "2025-07-11T10:33:59.533796Z",
    "can_like": true,
    "comment_id": 14
  }
]
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

This endpoint retrieves all the saved posts by the logged in user

**Endpoint:**`/post/save/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "post": {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)"
      },
      "body": "Driving the Future: How Technology is Transforming Transportation
Transportation has always been the engine of progress—moving people, goods, and ideas across cities, countries, and continents. But in the 21st century, it’s not just about getting from point A to point B. It’s about how we get there: faster, safer, cleaner, and smarter. And at the heart of this transformation? Technology.

1. Autonomous Vehicles: From Sci-Fi to Street Legal
What was once a futuristic dream is now cruising through city streets. Autonomous vehicles (AVs) use AI, sensors, and real-time data to navigate without human input. Companies like Waymo, Tesla, and Cruise are already testing and deploying self-driving cars, while autonomous trucks promise to revolutionize logistics and supply chains. The potential benefits are huge: fewer accidents, reduced congestion, and more accessible transportation for the elderly and disabled.

2. Electrification: Powering a Sustainable Tomorrow
The shift from fossil fuels to electric power is reshaping the automotive industry. Electric vehicles (EVs) are no longer niche—they're mainstream. Governments are offering incentives, automakers are committing to electric-only futures, and battery tech is advancing rapidly. Beyond cars, electric buses, bikes, and even airplanes are emerging, helping reduce emissions and create a cleaner planet.

3. Smart Infrastructure: Cities That Talk Back
Roads, traffic lights, and parking lots are getting an upgrade. Smart infrastructure uses IoT (Internet of Things) sensors and connectivity to manage traffic flow, detect maintenance needs, and even communicate with autonomous vehicles. Imagine a traffic signal that adapts in real time to reduce congestion or a parking lot that directs you to an open spot. These innovations aren't just cool—they improve safety, reduce fuel use, and enhance urban life.

4. Mobility-as-a-Service (MaaS): The End of Car Ownership?
With apps like Uber, Lyft, Bird, and Lime, personal car ownership is becoming less necessary in urban environments. MaaS platforms integrate various transport options—bikes, scooters, rideshares, public transit—into a single, seamless service. Add in AI-powered route planning, and getting around becomes effortless, personalized, and more eco-friendly.

5. Hyperloop & High-Speed Rail: Redefining Long-Distance Travel
While still in early stages, hyperloop technology—propelling pods through low-pressure tubes at airplane speeds—could dramatically shorten travel times between major cities. Meanwhile, countries like Japan and France continue to lead the way with efficient high-speed rail, showing the world what’s possible with investment in advanced public transport.

6. Data-Driven Decisions: Analytics Behind the Wheel
Every vehicle on the road today is a rolling data center. From GPS tracking to engine diagnostics, real-time data helps optimize routes, predict maintenance issues, and improve safety. Municipalities and logistics companies alike are leveraging this data to make smarter transportation decisions, reduce emissions, and cut costs.

The Road Ahead
Technology isn’t just changing how we move—it’s changing what’s possible. The intersection of AI, data, automation, and sustainability is creating a transportation revolution. But as we accelerate toward the future, we must ensure equity, safety, and accessibility for all. The journey has just begun.",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-04-24T14:06:45.666911Z",
      "comment_count": 3,
      "like_count": 2,
      "share_count": 1,
      "parent": null,
      "can_like": false,
      "can_follow": false,
      "is_self": true,
      "is_saved": true,
      "post_id": 7
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

# Get Followings Post

This endpoint retrieves the posts of users the logged in user is currently following

**Endpoint:**`/post/following/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
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
      "body": "Precision agriculture is transforming farming through data, GPS, and automation. The future of agri-tech is smart, efficient, and sustainable. #AgriTech #SmartFarming",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-04-17T14:31:33.731704Z",
      "comment_count": 0,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": false,
      "is_self": false,
      "is_saved": false,
      "post_id": 3
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
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-04-17T14:30:44.280807Z",
      "comment_count": 0,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": false,
      "is_self": false,
      "is_saved": false,
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
      "body": "Did you know? Conservation agriculture can increase crop yields by up to 30% while preserving soil health. Time to rethink how we farm sustainably. #AgriFacts #SustainableFarming",
      "pic1": "https://careernexus-storage1.s3.amazonaws.com/posts/media/98c7a008-4433-4f13-ae73-0e4640a758b4branch.jpeg",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-04-17T14:30:11.005024Z",
      "comment_count": 1,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": false,
      "is_self": false,
      "is_saved": false,
      "post_id": 1
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

This endpoint retrieves all the pending connection requests that was initiated by other users of the platform. N.B: These connection requests are those involving the logged in user and not any requests between other users of the platform. This API also retrieves the total number of these items.

**Endpoint:**`/connection/pending/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "pending_requests": [
    {
      "id": 7,
      "connection": {
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)",
        "status": "PENDING",
        "user_id": 1
      }
    }
  ],
  "count": 1
}
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
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 4,
      "name": "Adeniji Adekogbe",
      "qualification": "Bachelor of Science (Education)",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png",
      "followers": 0
    },
    {
      "id": 11,
      "name": "Opeyemi Saliu",
      "qualification": "Bachelor of Engineering",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "followers": 0
    }
  ],
  "last_page": "http://127.0.0.1:8000/connection/recommendation/?page=1"
}
```

[Table of contents](#toc)


# Follow User

This endpoint creates a one-way follow from one user (follower) and another (following). N.B:It is not possible to follow self or the same user multiple times.

**Endpoint:**`/follow/`

**Method:** `POST`

## Payload

``` json
{

user_following:*****

}

```
## Response body

**status code:201**

``` json
{
  "follower": 1,
  "following": 12
}
```

[Table of contents](#toc)


# Get Followings

This endpoint curates a list of all the users the logged in user is currently following.

**Endpoint:**`/followings/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 2,
    "first_name": "N/A",
    "last_name": "N/A",
    "middle_name": "N/A",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png",
    "qualification": "Bachelor of Science"
  }
]
```

[Table of contents](#toc)


# User Followers

This endpoint retrieves all the users currently following the logged in user.

**Endpoint:**`/followers/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 2,
    "first_name": "N/A",
    "last_name": "N/A",
    "middle_name": "N/A",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png",
    "qualification": "Bachelor of Science"
  }
]
```

[Table of contents](#toc)


# Followings Count

This endpoint retrieves the total numbers of users that the current logged in user is following.

**Endpoint:**`/followings/count/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "following_count": 1
}
```

[Table of contents](#toc)


# Followers Count

This endpoint retrieves the sum total of the number of Users the current logged in user is following.

**Endpoint:**`/followers/count/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "followers count": 1
}
```

[Table of contents](#toc)


# Get Own Posts

This endpoint retrieves a paginated result of all the posts made by the logged in user.

**Endpoint:**`/post/posted/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "count": 13,
  "next": "http://127.0.0.1:8000/post/posted/?page=2",
  "previous": null,
  "results": [
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)"
      },
      "body": "From a friend.",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-07-11T11:44:28.647331Z",
      "comment_count": 1,
      "like_count": 0,
      "share_count": 0,
      "parent": {
        "profile": {
          "id": 2,
          "first_name": "N/A",
          "last_name": "N/A",
          "middle_name": "N/A",
          "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/7c565a1b-bbdf-4140-831f-8b3086eaafd0default_avatar.png",
          "qualification": "Bachelor of Science"
        },
        "body": "Precision agriculture is transforming farming through data, GPS, and automation. The future of agri-tech is smart, efficient, and sustainable. #AgriTech #SmartFarming",
        "pic1": "N/A",
        "pic2": "N/A",
        "pic3": "N/A",
        "video": "N/A",
        "article": "N/A",
        "time_stamp": "2025-04-17T14:31:33.731704Z"
      },
      "can_like": true,
      "can_follow": false,
      "is_self": true,
      "is_saved": false,
      "post_id": 18
    },
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)"
      },
      "body": "Success rarely comes from doing one big thing right — it comes from doing the small things right, over and over again. Whether you're writing code, learning a language, or building a business, consistency beats intensity. Show up every day. Improve a little. The results will follow.",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-06-18T22:36:11.257113Z",
      "comment_count": 0,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": false,
      "is_self": true,
      "is_saved": false,
      "post_id": 15
    },
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)"
      },
      "body": "Success rarely comes from doing one big thing right — it comes from doing the small things right, over and over again. Whether you're writing code, learning a language, or building a business, consistency beats intensity. Show up every day. Improve a little. The results will follow.",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-06-18T22:34:36.796671Z",
      "comment_count": 0,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": false,
      "is_self": true,
      "is_saved": false,
      "post_id": 14
    }
  ],
  "last_page": "http://127.0.0.1:8000/post/posted/?page=5"
}
```

[Table of contents](#toc)


# Unlike Post

This endpoint unlikes a Post that has been previously liked. N.B: To unlike a post, the post should have been liked previously.

**Endpoint:**`/post/unlike/`

**Method:** `POST`

## Payload

``` json
{

post:*****

}

```
## Response body

**status code:200**

``` json
{
  "status": "Unliked post"
}
```

[Table of contents](#toc)


# Unfollow User

This endpoint unfollows an already followeduser. N.B:The user must have been previously followed in order to be eligible to be unfollowed.

**Endpoint:**`/unfollow/`

**Method:** `POST`

## Payload

``` json
{

user_following:*****

}

```
## Response body

**status code:200**

``` json
{
  "status": "Unfollowed user"
}
```

[Table of contents](#toc)






# Like Comment/Reply

This endpoint likes a comment or reply. N.B: The comment or reply can only be liked once and must not have been previously liked by the user.

**Endpoint:**`/post/like/comment/`

**Method:** `POST`

## Payload

``` json
{

comment:*****

}

```
## Response body

**status code:200**

``` json
{
  "comment_id": 13,
  "user_id": 1,
  "status": "Liked Comment"
}
```

[Table of contents](#toc)


# Unlike Comment/Reply

This endpoint unlikes a comment or reply. N.B: The comment/reply must have been previously liked in order to be available for unlike.

**Endpoint:**`/post/unlike/comment/`

**Method:** `POST`

## Payload

``` json
{

comment:*****

}

```
## Response body

**status code:200**

``` json
{
  "status": "Unliked Comment"
}
```

[Table of contents](#toc)


# Mentor Search/Filter

This API searches for mentors based on query parameters. The query parameters allowed include text,experience_level(entry,mid,senior,executive),skills and availability(weekdays,weekends).

**Endpoint:**`/mentor/search/?text=yemi&availability=weekends`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 11,
    "name": "Opeyemi Abdul-Azeez Saliu",
    "qualification": "Bachelor of Engineering",
    "position": "",
    "years_of_experience": 6,
    "technical_skills": [
      "Python",
      "Shell Scripting",
      "Backend development",
      "Devops",
      "AI/ML",
      "Database Management System"
    ]
  }
]
```

[Table of contents](#toc)



# Book Mentorship Session

This API enables mentees to book a mentorship session with a mentor. N.B: session_type can either be group/individual.

**Endpoint:**`/mentor/sessions/book/`

**Method:** `POST`

## Payload

``` json
{

mentor:*****

session_type:*****

date:*****

time:*****

discourse:*****

}

```
## Response body

**status code:201**

``` json
{
  "mentor": {
    "id": 11,
    "first_name": "Opeyemi",
    "last_name": "Saliu",
    "middle_name": "Abdul-Azeez",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
    "qualification": "Bachelor of Engineering"
  },
  "mentee": {
    "id": 1,
    "first_name": "Opeyemi",
    "last_name": "Saliu",
    "middle_name": "Abdul-Azeez",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
    "qualification": "Bachelor of Engineering (Civil Engineering)"
  },
  "session_type": "individual",
  "session_at": {
    "date": "2025-07-21",
    "time": "00:00:00"
  },
  "discourse": "Career Building",
  "status": "PENDING"
}
```

[Table of contents](#toc)


# Retrieve Mentorship Sessions

This API retrieves mentorship session information. N.B:This API is strictly dependent on query parameter status. (?status=requested:This retrieves all the mentorship sessions that was requested by the user but has not been accepted/rejected yet. ?status=accepted:This retrieves all the mentorship sessions that was requested by the user and has been accepted by the mentor. ?status=scheduled:This query parameter is only available if the user is a mentor. It retrieves all the mentorship sessions that are still pending and those that have been accepted by the user who must be a mentor.

**Endpoint:**`/mentor/sessions/?status=requested`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 11,
    "mentor": {
      "id": 11,
      "first_name": "Abdul Azeez",
      "last_name": "Balogun",
      "middle_name": "Abiola",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "qualification": "Bachelor of Engineering"
    },
    "mentee": {
      "id": 1,
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
      "qualification": "Bachelor of Engineering (Civil Engineering)"
    },
    "join": true,
    "session_type": "individual",
    "session_at": {
      "date": "2025-07-20",
      "time": "18:00:00"
    },
    "discourse": "Career Building",
    "status": "ACCEPTED"
  },
  {
    "id": 12,
    "mentor": {
      "id": 11,
      "first_name": "Abdul Azeez",
      "last_name": "Balogun",
      "middle_name": "Abiola",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "qualification": "Bachelor of Engineering"
    },
    "mentee": {
      "id": 1,
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
      "qualification": "Bachelor of Engineering (Civil Engineering)"
    },
    "join": false,
    "session_type": "individual",
    "session_at": {
      "date": "2025-07-20",
      "time": "18:00:00"
    },
    "discourse": "Career Building",
    "status": "PENDING"
  },
  {
    "id": 13,
    "mentor": {
      "id": 11,
      "first_name": "Abdul Azeez",
      "last_name": "Balogun",
      "middle_name": "Abiola",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "qualification": "Bachelor of Engineering"
    },
    "mentee": {
      "id": 1,
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
      "qualification": "Bachelor of Engineering (Civil Engineering)"
    },
    "join": true,
    "session_type": "individual",
    "session_at": {
      "date": "2025-07-31",
      "time": "01:36:00"
    },
    "discourse": "Career Building",
    "status": "ACCEPTED"
  }
]
```

[Table of contents](#toc)


# Accept/Reject Mentorship Session Request

This endpoint enables a mentor to accept/reject a mentorship session request. N.B:A session can only be accepted/rejected once. Also a Rejected session is not available for viewing again and would be subsequently deleted from the system. The action property can either be Accept or Reject.

**Endpoint:**`/mentor/sessions/accept-reject/`

**Method:** `POST`

## Payload

``` json
{

session:*****

action:*****

}

```
## Response body

**status code:200**

``` json
{
  "session_id": 11,
  "action": "Accepted"
}
```

[Table of contents](#toc)


# Following Recommendation

This API suggests to the login user other users that can be followed. It considers the logged in user's location and industry. (Most applicable in columns such as Who To Follow,etc)

**Endpoint:**`/follow/recommendation/`

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
      "id": 4,
      "name": "Adeniji Adekogbe",
      "qualification": "Bachelor of Science (Education)",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png",
      "followers": 0
    },
    {
      "id": 11,
      "name": "Abdul Azeez Balogun",
      "qualification": "Bachelor of Engineering",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "followers": 0
    }
  ]
}
```

[Table of contents](#toc)


# Connections Count

This API retrieves the count of all established connections. N.B:Connection requests that are still pending are not counted.

**Endpoint:**`/connection/count/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "connections_count": 2
}
```

[Table of contents](#toc)


# Connection Requests Sent

This API retrieves all the connections that was initiated by the logged in user and are yet to be Confirmed or Rejected.

**Endpoint:**`/connection/requests/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "connection_requests": [
    {
      "id": 7,
      "connection": {
        "first_name": "Abdul Azeez",
        "last_name": "Balogun",
        "middle_name": "Abiola",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
        "qualification": "Bachelor of Engineering",
        "status": "PENDING",
        "user_id": 11
      }
    },
    {
      "id": 8,
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
  ],
  "count": 2
}
```

[Table of contents](#toc)


# Mentors Recommendation

This endpoint recommends mentors to the logged in user.

**Endpoint:**`/mentor/recommendation/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 11,
    "first_name": "Abdul Azeez",
    "last_name": "Balogun",
    "middle_name": "Abiola",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
    "current_job": "Backend Developer",
    "experience_level": "Senior"
  }
]
```

[Table of contents](#toc)