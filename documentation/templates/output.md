# Career Nexus Backend Documentation<a name='career_nexus_backend_documentation'></a>

---

## Index<a name='toc'></a>

## 
1. [](#)  
2. [accept/reject mentorship session request](#accept/reject_mentorship_session_request)  
3. [add certification](#add_certification)  
4. [add education api](#add_education_api)  
5. [add experience](#add_experience)  
6. [add organization members](#add_organization_members)  
7. [admin retrieve dispute tickets](#admin_retrieve_dispute_tickets)  
8. [alter country permissions](#alter_country_permissions)  
9. [apply for job](#apply_for_job)  
10. [book mentorship session](#book_mentorship_session)  
11. [cancel mentorship session](#cancel_mentorship_session)  
12. [career nexus backend documentation](#career_nexus_backend_documentation)  
13. [chat history](#chat_history)  
14. [chat websockets](#chat_websockets)  
15. [clear notifications](#clear_notifications)  
16. [connection accept/reject](#connection_accept/reject)  
17. [connection create](#connection_create)  
18. [connection pending retrieve](#connection_pending_retrieve)  
19. [connection recommendation](#connection_recommendation)  
20. [connection requests sent](#connection_requests_sent)  
21. [connection retrieve](#connection_retrieve)  
22. [connections count](#connections_count)  
23. [content management](#content_management)  
24. [create a newsletter](#create_a_newsletter)  
25. [create comment](#create_comment)  
26. [create corporate account](#create_corporate_account)  
27. [create project catalogue](#create_project_catalogue)  
28. [creating library content](#creating_library_content)  
29. [delete certification](#delete_certification)  
30. [delete education](#delete_education)  
31. [delete experience](#delete_experience)  
32. [delete library content](#delete_library_content)  
33. [delete post](#delete_post)  
34. [delete project catalogue](#delete_project_catalogue)  
35. [delete user](#delete_user)  
36. [dispute creation](#dispute_creation)  
37. [dispute summary](#dispute_summary)  
38. [dispute ticket resolution](#dispute_ticket_resolution)  
39. [edit job](#edit_job)  
40. [follow user](#follow_user)  
41. [followers count](#followers_count)  
42. [following recommendation](#following_recommendation)  
43. [followings count](#followings_count)  
44. [forget password](#forget_password)  
45. [general notifications](#general_notifications)  
46. [get all notifications](#get_all_notifications)  
47. [get chat sessions](#get_chat_sessions)  
48. [get comment](#get_comment)  
49. [get country phone codes](#get_country_phone_codes)  
50. [get followings](#get_followings)  
51. [get followings post](#get_followings_post)  
52. [get job preference](#get_job_preference)  
53. [get newsletter](#get_newsletter)  
54. [get other user post](#get_other_user_post)  
55. [get saved post](#get_saved_post)  
56. [google signin](#google_signin)  
57. [initiate chat session](#initiate_chat_session)  
58. [job create](#job_create)  
59. [job notifications](#job_notifications)  
60. [job preference](#job_preference)  
61. [join mentorship session](#join_mentorship_session)  
62. [lead register](#lead_register)  
63. [like comment/reply](#like_comment/reply)  
64. [login api](#login_api)  
65. [logout](#logout)  
66. [mentor search/filter](#mentor_search/filter)  
67. [mentors recommendation](#mentors_recommendation)  
68. [mentorship session annotation.](#mentorship_session_annotation.)  
69. [post create](#post_create)  
70. [post like](#post_like)  
71. [post retrieve](#post_retrieve)  
72. [post save](#post_save)  
73. [post share](#post_share)  
74. [profile completion](#profile_completion)  
75. [profile retrieve](#profile_retrieve)  
76. [profile update](#profile_update)  
77. [recommended job posts.](#recommended_job_posts.)  
78. [remove organization member](#remove_organization_member)  
79. [reply comment](#reply_comment)  
80. [reposting](#reposting)  
81. [retrieve applied jobs](#retrieve_applied_jobs)  
82. [retrieve corporate leads](#retrieve_corporate_leads)  
83. [retrieve education api](#retrieve_education_api)  
84. [retrieve invited sessions](#retrieve_invited_sessions)  
85. [retrieve job applications](#retrieve_job_applications)  
86. [retrieve job posts](#retrieve_job_posts)  
87. [retrieve library contents](#retrieve_library_contents)  
88. [retrieve linked accounts](#retrieve_linked_accounts)  
89. [retrieve mentor vault data](#retrieve_mentor_vault_data)  
90. [retrieve mentors posts](#retrieve_mentors_posts)  
91. [retrieve mentorship sessions](#retrieve_mentorship_sessions)  
92. [retrieve own posts](#retrieve_own_posts)  
93. [retrieve portfolio projects](#retrieve_portfolio_projects)  
94. [retrieve posts](#retrieve_posts)  
95. [retrieve recent applicants](#retrieve_recent_applicants)  
96. [retrieve saved jobs](#retrieve_saved_jobs)  
97. [retrieve saved mentors](#retrieve_saved_mentors)  
98. [retrieve shared post](#retrieve_shared_post)  
99. [retrieve user settings](#retrieve_user_settings)  
100. [retrieve vault transactions](#retrieve_vault_transactions)  
101. [save a job](#save_a_job)  
102. [save a mentor](#save_a_mentor)  
103. [session payment with flutterwave](#session_payment_with_flutterwave)  
104. [session payment with stripe](#session_payment_with_stripe)  
105. [signup with google](#signup_with_google)  
106. [subscribe to newsletter](#subscribe_to_newsletter)  
107. [switch account](#switch_account)  
108. [unfollow user](#unfollow_user)  
109. [unlike comment/reply](#unlike_comment/reply)  
110. [unlike post](#unlike_post)  
111. [unregistered users subscribe to newsletter](#unregistered_users_subscribe_to_newsletter)  
112. [unsave job](#unsave_job)  
113. [unsave mentor](#unsave_mentor)  
114. [unsubscribe from newsletter](#unsubscribe_from_newsletter)  
115. [update job status](#update_job_status)  
116. [update user account settings](#update_user_account_settings)  
117. [updating user eperience](#updating_user_eperience)  
118. [user analytics](#user_analytics)  
119. [user followers](#user_followers)  
120. [user registeration](#user_registeration)  
121. [user retrieve dispute](#user_retrieve_dispute)  
122. [user search](#user_search)  
123. [user-industry update](#user-industry_update)  
124. [valid choice](#valid_choice)  
125. [verify otp hash](#verify_otp_hash)  
126. [view certification](#view_certification)  
127. [view experience](#view_experience)  

# User Registeration<a name='user_registeration'></a>

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

# Verify Otp Hash<a name='verify_otp_hash'></a>

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

# Login API<a name='login_api'></a>

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

# LogOut<a name='logout'></a>

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

# Profile Retrieve<a name='profile_retrieve'></a>

This endpoint retrieve a logged in user or retrieves a third party's profile data if a query parameter of user_id is passed to the url. N.B:The user_type of the request instance determines the structure of the data passed in the response. properties like years_of_experience,timezone,mentorship_styles,technical_skills etc are only available to mentors profile which is automatically retrieved in response. Retrieving learners profile does not contain these properties.

**Endpoint:**`/user/retrieve-profile/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
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
  "followings": 0,
  "session_rate": "3000NGN",
  "rating": 0,
  "user_type": "mentor",
  "industry": "technology",
  "can_message": false,
  "can_follow": true
}

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
  "timezone": "Africa/Lagos",
  "user_type": "learner",
  "industry": "technology",
  "can_message": false,
  "can_follow": true
}

CORPORATE
{
  "id": 21,
  "company_name": "Bojvent LTD",
  "company_type": "private",
  "industry": "technology",
  "company_size": "1-10",
  "country_code": "+000",
  "phone_number": "00000000000",
  "location": "Lagos",
  "website": "www.bojventltd.com",
  "tagline": "Dealers in recycled wastes and compositions.",
  "logo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/b86858f7-c77e-4c5f-9796-14f27c855f7cDefault_company_image.png",
  "cover_photo": "https://careernexus-storage1.s3.amazonaws.com/cover_photos/70114098-5014-4eda-a725-5421792972dadefault_cp.jpeg",
  "members": [
    {
      "member": {
        "id": 1,
        "name": "Opeyemi Abdul-Azeez Saliu",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "extras": "Bachelor of Engineering (Civil Engineering)"
      }
    }
  ],
  "user_type": "employer",
  "can_message": false,
  "can_follow": false
}
```

[["/user/retrieve-profile/","GET"]][Table of contents](#toc) 

# Profile Update<a name='profile_update'></a>

This endpoint updates the profile data of a user. N.B:Some field updates such as years_of_experience, areas_of_expertise,availability,current_job,technical_skills,mentorship_styles and linkedin_url are only available to mentors and can only be updated by this user type. Also fields like areas_of_expertise,mentorship_styles and technical_skills properties must be a list of strings as their request format. company_size options include ("1-10","11-50","51-200","201-500","501-1000","1001-5000","+5000").

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

session_rate:*****

company_name:*****

company_type:*****

company_size:*****

industry:*****

website:*****

logo:*****

tagline:*****

}

```
## Response body

**status code:201**

``` json
Similar Response for Learners and Mentors
{
  "first_name": "Abdul Azeez",
  "last_name": "Balogun",
  "middle_name": "Abiola",
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
  "resume": "",
  "mentorship_styles": [],
  "timezone": "Canada/Central",
  "linkedin_url": null,
  "session_rate": 2
}

Response for corporate
{
  "id": 21,
  "company_name": "Bojvent LTD",
  "company_type": "private",
  "company_size": "1-10",
  "country_code": "+000",
  "phone_number": "00000000000",
  "location": "Lagos",
  "website": "www.bojventltd.com",
  "tagline": "Dealers in recycled wastes and compositions.",
  "logo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/b86858f7-c77e-4c5f-9796-14f27c855f7cDefault_company_image.png",
  "cover_photo": "https://careernexus-storage1.s3.amazonaws.com/cover_photos/70114098-5014-4eda-a725-5421792972dadefault_cp.jpeg"
}
```

[["/user/profile-update/","PUT"]][Table of contents](#toc) 

# User-industry Update<a name='user-industry_update'></a>

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

# View Experience<a name='view_experience'></a>

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

# Add Experience<a name='add_experience'></a>

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

# Delete Experience<a name='delete_experience'></a>

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

# Updating User Eperience<a name='updating_user_eperience'></a>

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

# Retrieve Education API<a name='retrieve_education_api'></a>

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

# Add Education API<a name='add_education_api'></a>

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

# Delete Education<a name='delete_education'></a>

Deletes a profile education data.

**Endpoint:**`user/education/?education_id=7`

## Payload

```

```

**Method:** `DELETE`

## Response body

**status code:204**

[Table of contents](#toc) 

# View Certification<a name='view_certification'></a>

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

# Add Certification<a name='add_certification'></a>

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

# Delete Certification<a name='delete_certification'></a>

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

# User Analytics<a name='user_analytics'></a>

This endpoint retrieves all the analytic data of the users's profile like number of connections, number of times the profile was viewed, etc... N.B:If a query parameter user_id is past into the url endpoint, analytics of another user can be retrieved (If the user enables show_analytics in their settings).

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
  "total_views": 18,
  "total_connections": 1
}
```

[Table of contents](#toc) 

# Profile Completion<a name='profile_completion'></a>

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

# Retrieve Posts<a name='retrieve_posts'></a>

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
        "id": 21,
        "first_name": "Bojvent LTD",
        "last_name": "",
        "middle_name": "",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/b86858f7-c77e-4c5f-9796-14f27c855f7cDefault_company_image.png",
        "qualification": "Dealers in recycled wastes and compositions.",
        "user_type": "employer"
      },
      "body": "Technology isn’t just about gadgets and apps — it’s the invisible force shaping how we live, work, and connect. From cloud systems powering businesses to AI assisting in everyday tasks, it keeps pushing boundaries of speed, scale, and creativity.

But here’s the thing: technology is only as impactful as the minds behind it. The real breakthrough happens when curiosity meets code, when ideas turn into solutions.

In a world moving faster than ever, the question is no longer “What can technology do?” but “What will we choose to build with it?” 🚀",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-09-18T03:44:39.929867Z",
      "comment_count": 0,
      "like_count": 0,
      "share_count": 2,
      "parent": null,
      "can_like": true,
      "can_follow": true,
      "is_self": false,
      "is_saved": false,
      "post_id": 25
    },
    {
      "profile": {
        "id": 11,
        "first_name": "Abdul Azeez",
        "last_name": "Balogun",
        "middle_name": "Abiola",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
        "qualification": "Bachelor of Engineering",
        "user_type": "mentor"
      },
      "body": "Success rarely comes from doing one big thing right — it comes from doing the small things right, over and over again. Whether you're writing code, learning a language, or building a business, consistency beats intensity. Show up every day. Improve a little. The results will follow.",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-08-09T10:18:07.879587Z",
      "comment_count": 0,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": true,
      "is_self": false,
      "is_saved": false,
      "post_id": 21
    },
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)",
        "user_type": "learner"
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
      "comment_count": 2,
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
        "qualification": "Bachelor of Engineering (Civil Engineering)",
        "user_type": "learner"
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
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": false,
      "is_self": true,
      "is_saved": false,
      "post_id": 11
    },
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)",
        "user_type": "learner"
      },
      "body": "Farming Meets the Future 🚜💡

From drones mapping crop health to AI-driven irrigation systems, agriculture is being transformed by technology. Precision farming is reducing waste, boosting yields, and helping farmers make smarter, faster decisions. As the world faces growing food demands and climate challenges, agri-tech is planting the seeds of a sustainable future.

#AgriTech #SmartFarming #SustainableAgriculture #InnovationInFarming",
      "pic1": "https://careernexus-storage1.s3.amazonaws.com/posts/media/37653a4e-4370-40c5-8f8a-c5c296e27108branch.jpeg",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-05-15T13:42:20.543966Z",
      "comment_count": 1,
      "like_count": 1,
      "share_count": 0,
      "parent": null,
      "can_like": false,
      "can_follow": false,
      "is_self": true,
      "is_saved": false,
      "post_id": 10
    }
  ],
  "last_page": "http://127.0.0.1:8000/post/?page=2"
}
```

[["/post/","GET"]][Table of contents](#toc) 

# Post Retrieve<a name='post_retrieve'></a>

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

# Post Create<a name='post_create'></a>

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

# Create comment<a name='create_comment'></a>

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

# Get comment<a name='get_comment'></a>

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

# Reply Comment<a name='reply_comment'></a>

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

# Post Like<a name='post_like'></a>

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

# Reposting<a name='reposting'></a>

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

# Post Save<a name='post_save'></a>

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

# Get Saved Post<a name='get_saved_post'></a>

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

# Post Share<a name='post_share'></a>

This endpoint is designed to create a link particular to a post which could be called to retrieve the details of the post from external sources.

**Endpoint:**`/post/share/`

**Method:** `POST`

## Payload

``` json
{

"post":"*****"

}

```
## Response body

**status code:200**

``` json
{
  "post_hash": "8ca6d40e-aa6d-4188-b079-fa8a7aacce57"
}
```

[["/post/share/","POST"]][Table of contents](#toc) 

# Get Followings Post<a name='get_followings_post'></a>

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

# <a name=''></a>

# <a name=''></a>


# Forget Password<a name='forget_password'></a>

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


# Get Country Phone Codes<a name='get_country_phone_codes'></a>

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


# Alter Country Permissions<a name='alter_country_permissions'></a>

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


# Content Management<a name='content_management'></a>

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


# Get Chat Sessions<a name='get_chat_sessions'></a>

This endpoint gets all chat sessions that had been initiated by or with the user.

**Endpoint:**`/notification-chat/chats/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "contributor": {
      "id": 3,
      "first_name": "N/A",
      "last_name": "N/A",
      "middle_name": "N/A",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png",
      "qualification": "Bachelor of Education (English)"
    },
    "chat_id": 2
  },
  {
    "contributor": {
      "id": 2,
      "first_name": null,
      "last_name": "",
      "middle_name": "",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/b86858f7-c77e-4c5f-9796-14f27c855f7cDefault_company_image.png",
      "qualification": null
    },
    "chat_id": 1
  }
]
```

[["/notification-chat/chats/","GET"]][Table of contents](#toc)


# Chat History<a name='chat_history'></a>

This endpoint gets all the previous chat messages of a particular chat session.

**Endpoint:**`/notification-chat/chat/messages/?chat_id=2`

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
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
      "qualification": "Bachelor of Engineering (Civil Engineering)"
    },
    "message": "Hello friend",
    "timestamp": "2025-06-03T14:40:21.375709Z"
  }
]
```

[Table of contents](#toc)


# Job Create<a name='job_create'></a>

This endpoint creates a new job post. N.B: PAYLOAD OPTIONS include employment_type(full_time,part_time,internship,freelance,contract), work_type(remote,onsite,hybrid). Also, an optional status can be provided in the payload to specify the status of the job being created. N.B:status can either be active,draft or closed. If no status payload is provided, the job post defaults to active status.

**Endpoint:**`/job/`

**Method:** `POST`

## Payload

``` json
{

'title':'*****',

'organization':'*****',

'employment_type':'*****',

'work_type':'*****',

'country':'*****',

'salary':'*****',

'overview':'*****',

'description':'*****',

'experience_level':'*****',

'status (**optional)':'*****',

'application_deadline':'*****',

}

```
## Response body

**status code:201**

``` json
{
  "title": "Backend Developer",
  "organization": "Sterling Technologies",
  "employment_type": "full_time",
  "work_type": "remote",
  "country": "Nigeria",
  "salary": "200,000NGN",
  "overview": "A skilled backend developer aith at least 
5 years of experience",
  "description": "As a Backend Developer, you will play a crucial role in designing, implementing, and optimizing the backbone of our digital services. You'll work closely with frontend developers, DevOps engineers, and product teams to deliver robust and high-performance applications. Responsibilities include developing RESTful APIs, ensuring data integrity and security, managing database schemas, and optimizing application performance. A strong understanding of backend frameworks, data structures, and software engineering principles is essential.",
  "industry": "technology",
  "experience_level": "senior",
  "application_deadline": "2025-12-31"
}
```

[["/job/","POST"]][Table of contents](#toc)


# Retrieve Job Posts<a name='retrieve_job_posts'></a>

This API retrieves all the job posts of the logged in user. N.B:Also, a query parameter status can be passed in the url to retrieve jobs by status. Valid options for status include active, draft and closed.

**Endpoint:**`/job/`

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
      "id": 12,
      "title": "Backend Developer",
      "organization": "Sterling Technologies",
      "employment_type": "full_time",
      "work_type": "remote",
      "country": "Nigeria",
      "salary": "200,000NGN",
      "overview": "A skilled backend developer aith at least 
5 years of experience",
      "description": "As a Backend Developer, you will play a crucial role in designing, implementing, and optimizing the backbone of our digital services. You'll work closely with frontend developers, DevOps engineers, and product teams to deliver robust and high-performance applications. Responsibilities include developing RESTful APIs, ensuring data integrity and security, managing database schemas, and optimizing application performance. A strong understanding of backend frameworks, data structures, and software engineering principles is essential.",
      "experience_level": "senior",
      "time_stamp": "2025-12-11",
      "application_deadline": "2025-12-31",
      "is_saved": false
    },
    {
      "id": 10,
      "title": "Frontend Developer",
      "organization": "TechExperts",
      "employment_type": "full_time",
      "work_type": "remote",
      "country": "Nigeria",
      "salary": "150,000NGN",
      "overview": "A skilled frontend developer aith at least 
5 years of experience",
      "description": "As a Frontend Developer, you will play a crucial role in designing, implementing, and optimizing the backbone of our digital services. You'll work closely with frontend developers, DevOps engineers, and product teams to deliver robust and high-performance applications. Responsibilities include developing RESTful APIs, ensuring data integrity and security, managing database schemas, and optimizing application performance. A strong understanding of backend frameworks, data structures, and software engineering principles is essential.",
      "experience_level": "senior",
      "time_stamp": "2025-10-30",
      "application_deadline": "2025-12-11",
      "is_saved": false
    },
    {
      "id": 11,
      "title": "Backend Developer",
      "organization": "Sterling Technologies",
      "employment_type": "full_time",
      "work_type": "hybrid",
      "country": "Nigeria",
      "salary": "350,000NGN",
      "overview": "A skilled backend developer aith at least 
5 years of experience",
      "description": "As a Backend Developer, you will play a crucial role in designing, implementing, and optimizing the backbone of our digital services. You'll work closely with frontend developers, DevOps engineers, and product teams to deliver robust and high-performance applications. Responsibilities include developing RESTful APIs, ensuring data integrity and security, managing database schemas, and optimizing application performance. A strong understanding of backend frameworks, data structures, and software engineering principles is essential.",
      "experience_level": "senior",
      "time_stamp": "2025-10-30",
      "application_deadline": "2025-12-11",
      "is_saved": false
    }
  ]
}
```

[["/job/","GET"]][Table of contents](#toc)


# Recommended Job Posts.<a name='recommended_job_posts.'></a>

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
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "title": "Backend Developer",
      "organization": "Career Nexus Ltd",
      "employment_type": "full_time",
      "work_type": "hybrid",
      "country": "Nigeria",
      "salary": "350,000NGN",
      "overview": "We are looking",
      "description": "You'll be responsible for turning user needs into elegant, intuitive interfaces for both web and mobile applications.",
      "experience_level": "entry",
      "time_stamp": "2025-06-11",
      "is_saved": false
    },
    {
      "id": 3,
      "title": "Backend Developer",
      "organization": "Career Nexus Ltd",
      "employment_type": "full_time",
      "work_type": "hybrid",
      "country": "Nigeria",
      "salary": "350,000NGN",
      "overview": "We are looking",
      "description": "You'll be responsible for turning user needs into elegant, intuitive interfaces for both web and mobile applications.",
      "experience_level": "entry",
      "time_stamp": "2025-06-11",
      "is_saved": false
    },
    {
      "id": 6,
      "title": "Backend Developer",
      "organization": "Mitiget Assurance Limited",
      "employment_type": "full_time",
      "work_type": "hybrid",
      "country": "Nigeria",
      "salary": "350,000NGN",
      "overview": "We are seeking a skilled and motivated Backend Developer to join our development team. You will be responsible for building and maintaining the server-side logic, database interactions, and API integrations that power our applications. The ideal candidate is experienced in backend technologies, database design, and scalable system architecture.",
      "description": "As a Backend Developer, you will play a crucial role in designing, implementing, and optimizing the backbone of our digital services. You'll work closely with frontend developers, DevOps engineers, and product teams to deliver robust and high-performance applications. Responsibilities include developing RESTful APIs, ensuring data integrity and security, managing database schemas, and optimizing application performance. A strong understanding of backend frameworks, data structures, and software engineering principles is essential.",
      "experience_level": "senior",
      "time_stamp": "2025-06-19",
      "is_saved": false
    },
    {
      "id": 7,
      "title": "Backend Developer",
      "organization": "Mitiget Assurance Limited",
      "employment_type": "full_time",
      "work_type": "remote",
      "country": "Nigeria",
      "salary": "350,000NGN",
      "overview": "We are seeking a skilled and motivated Backend Developer to join our development team. You will be responsible for building and maintaining the server-side logic, database interactions, and API integrations that power our applications. The ideal candidate is experienced in backend technologies, database design, and scalable system architecture.",
      "description": "As a Backend Developer, you will play a crucial role in designing, implementing, and optimizing the backbone of our digital services. You'll work closely with frontend developers, DevOps engineers, and product teams to deliver robust and high-performance applications. Responsibilities include developing RESTful APIs, ensuring data integrity and security, managing database schemas, and optimizing application performance. A strong understanding of backend frameworks, data structures, and software engineering principles is essential.",
      "experience_level": "senior",
      "time_stamp": "2025-06-19",
      "is_saved": false
    },
    {
      "id": 8,
      "title": "Backend Developer",
      "organization": "TechExperts",
      "employment_type": "full_time",
      "work_type": "remote",
      "country": "Nigeria",
      "salary": "150,000NGN",
      "overview": "We are seeking a skilled and motivated Backend Developer to join our development team. You will be responsible for building and maintaining the server-side logic, database interactions, and API integrations that power our applications. The ideal candidate is experienced in backend technologies, database design, and scalable system architecture.",
      "description": "As a Backend Developer, you will play a crucial role in designing, implementing, and optimizing the backbone of our digital services. You'll work closely with frontend developers, DevOps engineers, and product teams to deliver robust and high-performance applications. Responsibilities include developing RESTful APIs, ensuring data integrity and security, managing database schemas, and optimizing application performance. A strong understanding of backend frameworks, data structures, and software engineering principles is essential.",
      "experience_level": "senior",
      "time_stamp": "2025-06-19",
      "is_saved": false
    }
  ]
}
```

[Table of contents](#toc)


# Job Preference<a name='job_preference'></a>

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


# Job Notifications<a name='job_notifications'></a>

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


# Get Job Preference<a name='get_job_preference'></a>

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


# Valid Choice<a name='valid_choice'></a>

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


# Connection Retrieve<a name='connection_retrieve'></a>

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


# Connection Create<a name='connection_create'></a>

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


# Connection Pending Retrieve<a name='connection_pending_retrieve'></a>

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


# Connection Accept/Reject<a name='connection_accept/reject'></a>

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


# Connection Recommendation<a name='connection_recommendation'></a>

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


# Follow User<a name='follow_user'></a>

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


# Get Followings<a name='get_followings'></a>

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


# User Followers<a name='user_followers'></a>

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


# Followings Count<a name='followings_count'></a>

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


# Followers Count<a name='followers_count'></a>

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


# Retrieve Own Posts<a name='retrieve_own_posts'></a>

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
  "count": 11,
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
        "qualification": "Bachelor of Engineering (Civil Engineering)",
        "user_type": "learner"
      },
      "body": "Success rarely comes from doing one big thing right — it comes from doing the small things right, over and over again. Whether you're writing code, learning a language, or building a business, consistency beats intensity. Show up every day. Improve a little. The results will follow.",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-06-18T22:36:11.257113Z",
      "comment_count": 0,
      "like_count": 1,
      "share_count": 0,
      "parent": null,
      "can_like": false,
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
        "qualification": "Bachelor of Engineering (Civil Engineering)",
        "user_type": "learner"
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
    },
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)",
        "user_type": "learner"
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
      "comment_count": 2,
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
        "qualification": "Bachelor of Engineering (Civil Engineering)",
        "user_type": "learner"
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
      "can_like": true,
      "can_follow": false,
      "is_self": true,
      "is_saved": false,
      "post_id": 12
    },
    {
      "profile": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)",
        "user_type": "learner"
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
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": false,
      "is_self": true,
      "is_saved": false,
      "post_id": 11
    }
  ],
  "last_page": "http://127.0.0.1:8000/post/posted/?page=3"
}
```

[["/post/posted/","GET"]][Table of contents](#toc)


# Unlike Post<a name='unlike_post'></a>

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


# Unfollow User<a name='unfollow_user'></a>

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






# Like Comment/Reply<a name='like_comment/reply'></a>

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


# Unlike Comment/Reply<a name='unlike_comment/reply'></a>

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


# Mentor Search/Filter<a name='mentor_search/filter'></a>

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



# Book Mentorship Session<a name='book_mentorship_session'></a>

This API enables mentees to book a mentorship session with a mentor. N.B: session_type can either be group/individual. If the sesion_type selected is group, an invitees payload containing a list of all user invitees ids. Also, Invitees cannot be more than 10. Any extras would not be invited.

**Endpoint:**`/mentor/sessions/book/`

**Method:** `POST`

## Payload

``` json
{

"mentor":"*****"

"session_type":"*****"

"invitees (**optional)":"*****"

"date":"*****"

"time":"*****"

"discourse":"*****"

}

```
## Response body

**status code:201**

``` json
{
  "id": 26,
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
  "session_type": "group",
  "session_at": {
    "date": "2025-11-11",
    "time": "16:35:00"
  },
  "discourse": "Career Coaching",
  "amount": "1500NGN",
  "rating": 0,
  "status": "PENDING",
  "is_paid": false
}
```

[["/mentor/sessions/book/","POST"]][Table of contents](#toc)


# Retrieve Mentorship Sessions<a name='retrieve_mentorship_sessions'></a>

This API retrieves mentorship session information. N.B:This API is strictly dependent on query parameter status. (?status=requested:If this API is called by a learner, it retrieves all the sessions that has been requested by the user which are yet to be accepted by the mentor. However, if this API is called by a mentor, it retrieves all the mentorship booking requests made by other users towards himself. ?status=accepted:This retrieves all the mentorship sessions that was requested by the user and has been accepted by the mentor. ?status=scheduled:This query parameter is only available if the user is a mentor. It retrieves all the mentorship sessions that are still pending and those that have been accepted by the user who must be a mentor. ?status=completed:This retrieves all the completed sessions that the user (mentor or learner) participated in.

**Endpoint:**`/mentor/sessions/?status=completed`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 23,
    "mentor": {
      "id": 11,
      "first_name": "Abdul Azeez",
      "last_name": "Balogun",
      "middle_name": "Abiola",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "qualification": "Bachelor of Engineering",
      "user_type": "mentor"
    },
    "mentee": {
      "id": 1,
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
      "qualification": "Bachelor of Engineering (Civil Engineering)",
      "user_type": "learner"
    },
    "invitees": [],
    "join": true,
    "session_type": "individual",
    "session_at": {
      "date": "2025-10-15",
      "time": "08:35:00"
    },
    "discourse": "Career Coaching",
    "amount": "0NGN",
    "rating": 0,
    "status": "ACCEPTED",
    "is_paid": true
  },
  {
    "id": 29,
    "mentor": {
      "id": 11,
      "first_name": "Abdul Azeez",
      "last_name": "Balogun",
      "middle_name": "Abiola",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "qualification": "Bachelor of Engineering",
      "user_type": "mentor"
    },
    "mentee": {
      "id": 1,
      "first_name": "Opeyemi",
      "last_name": "Saliu",
      "middle_name": "Abdul-Azeez",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
      "qualification": "Bachelor of Engineering (Civil Engineering)",
      "user_type": "learner"
    },
    "invitees": [
      {
        "invitee": {
          "id": 3,
          "first_name": "N/A",
          "last_name": "N/A",
          "middle_name": "N/A",
          "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png",
          "qualification": "Bachelor of Education (English)",
          "user_type": "learner"
        }
      }
    ],
    "join": true,
    "session_type": "group",
    "session_at": {
      "date": "2025-11-11",
      "time": "16:21:00"
    },
    "discourse": "Career Coaching",
    "amount": "0NGN",
    "rating": 0,
    "status": "ACCEPTED",
    "is_paid": true
  }
]
```

[["/mentor/sessions/?status=completed","GET"]][Table of contents](#toc)


# Accept/Reject Mentorship Session Request<a name='accept/reject_mentorship_session_request'></a>

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


# Following Recommendation<a name='following_recommendation'></a>

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


# Connections Count<a name='connections_count'></a>

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


# Connection Requests Sent<a name='connection_requests_sent'></a>

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


# Mentors Recommendation<a name='mentors_recommendation'></a>

This API recommends mentors for the logged in user which is based on their selected industry.

**Endpoint:**`/mentor/recommendation/`

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
      "id": 11,
      "first_name": "Abdul Azeez",
      "last_name": "Balogun",
      "middle_name": "Abiola",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
      "current_job": "Backend Developer",
      "years_of_experience": 6,
      "technical_skills": [
        "Python",
        "Shell Scripting",
        "Backend development",
        "Devops",
        "AI/ML",
        "Database Management System"
      ],
      "session_rate": "3000NGN",
      "rating": 0,
      "is_saved": true
    }
  ]
}
```

[Table of contents](#toc)


# Subscribe to Newsletter<a name='subscribe_to_newsletter'></a>

This API subscribes a user to the platforms Newsletter updates. 

**Endpoint:**`/newsletter/subscribe/`

**Method:** `POST`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "subscriber": {
    "id": 1,
    "first_name": "Opeyemi",
    "last_name": "Saliu",
    "middle_name": "Abdul-Azeez",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
    "qualification": "Bachelor of Engineering (Civil Engineering)"
  },
  "subscribed_at": "2025-08-03T08:18:10.419778Z"
}
```

[Table of contents](#toc)


# Unsubscribe from NewsLetter<a name='unsubscribe_from_newsletter'></a>

This API Unsubscribes a user from the Newsletter Updates. N.B:The User must have been previously subscribed.

**Endpoint:**`/newsletter/unsubscribe/`

**Method:** `POST`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "status": "Unsubscribed from Newsletter"
}
```

[Table of contents](#toc)


# Create a NewsLetter<a name='create_a_newsletter'></a>

This API allows the creation of a NewsLetter. N.B:This API is designed for admin use.

**Endpoint:**`/newsletter/create/`

**Method:** `POST`

## Payload

``` json
{

title:*****

content:*****

image (.png,.jpg,.jpeg):*****

}

```
## Response body

**status code:201**

``` json
{
  "title": "\"Build & Beyond – Your Weekly Dive into Tech, Tools, and Tactics\"",
  "content": "Hey Builders,\n\nWelcome back to Build & Beyond, your space to explore the latest in modern tech, smarter workflows, and the people reimagining what’s possible.\n\nThis week, we're diving into innovation that isn’t just loud — it’s smart.\n\n🧠 This Week’s Highlights\n⚙️ Productivity Stack: What’s Hot in 2025\nOur curated list of top tools to speed up your workflows — from browser extensions to AI assistants. Whether you're coding, designing, or organizing your life, this stack is a game-changer.\n\n🔥 Side Project Spotlight: “RecurTrack”\nBuilt by a solo founder in Lagos, RecurTrack is a lightweight tool that helps freelancers track recurring clients without needing a full CRM. Simple, elegant, and now open-source.\n\n🔍 Framework Deep Dive: Django 5.1\nThe new Django update introduces native async views, stricter typing, and performance boosts. Our guide shows how to upgrade and what to watch for if you’re building APIs.\n\n📚 Learn Something New:\n\n“How SQLite is secretly powering the world”\n\n“The psychology of clean code”\n\n“Why battery tech matters to cloud computing”\n\n🎯 Quick Tip of the Week\nUse htop instead of top in your Linux terminal. It’s interactive, colorful, and gives you real-time control over process priorities.\n\n🧭 What We’re Exploring Next Week\nA deep look at Postgres tuning\n\nHow indie developers are funding projects without VCs\n\nBuilding a minimalist dev environment (yes, even on 4GB RAM)\n\nKeep tinkering, keep shipping — and remember: the best tools are the ones you actually use.\n\nSee you next week,\n— The Build & Beyond Crew",
  "image": "https://careernexus-storage1.s3.amazonaws.com/Newsletter/Images/0ca08693-14c4-4fff-8954-2bdb337ba28d/techtacticsmay2025.jpg",
  "timestamp": "2025-08-03T11:05:28.134040Z"
}
```

[Table of contents](#toc)


# Get NewsLetter<a name='get_newsletter'></a>

This API retrieves the latest newsletter article and also includes a list of newsletter archives.

**Endpoint:**`/newsletter/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "recent": {
    "title": "\"Focus Frame – Clarity in a Noisy World\"",
    "content": "Hello Thinker,\n\nWelcome to this week's edition of Focus Frame, where we distill powerful ideas, simple systems, and grounded insight to help you work better and live smarter.\n\n🧭 This Week's Frame\n📌 1. One Goal, One Week\nWhat’s the one thing you need to ship, solve, or start this week? Clarity comes when we give one goal full attention. Write it down. Make it real.\n\n🛠️ 2. System > Hustle\nWe often chase motivation, but it’s fleeting. What works long term? Quiet, boring systems. The checklist. The morning reset. The Friday review. Build systems — not streaks.\n\n📖 3. Reading Corner: “The Psychology of Attention”\nThis week’s pick is a short read on how to protect your focus in high-noise environments. Key takeaway: the more inputs you silence, the deeper your clarity grows.\n\n🔧 4. Tool in Focus: Obsidian (Your Second Brain)\nObsidian is more than just a note app. It’s a quiet place to think, connect ideas, and build your own knowledge base. Markdown-powered. Offline-friendly. Highly recommended for focused minds.\n\n🌱 Practice This Week\nPause before switching tasks.\nEven 10 seconds of breathing between contexts improves focus, energy, and intentionality.\n\nThanks for reading. Stay clear, stay steady, and stay in your frame.\n\nTill next time,\n— The Focus Frame Team",
    "image": "",
    "timestamp": "2025-08-03T15:15:04.097683Z"
  },
  "archive": {
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
      {
        "title": "\"Creative Current – Flowing Ideas for Modern Makers\"",
        "content": "Hey Creator,\n\nWelcome to this week’s issue of Creative Current, your go-to burst of fresh ideas, tools, and trends designed to keep you in motion and ahead of the curve.\n\n⚡ What’s Flowing This Week\n🎨 1. Design Is Solving Real Problems Again\nWe’re seeing a shift from over-stylized UIs to interfaces that do more with less. Utility-driven design is back — and users love it. Clean, purposeful, minimal. It’s not boring — it’s smart.\n\n📣 2. Product Launch Tip: Talk to 5 People Before You Build\nStill thinking of your next MVP? Before writing a single line of code, talk to 5 real users. A 30-minute conversation can save you 3 weeks of feature bloat.\n\n🧰 3. Tool Spotlight: Penpot (Free Design & Prototyping)\nAn open-source Figma alternative that respects your data, works in teams, and integrates beautifully into dev workflows. Free forever, community-powered, and quickly maturing.\n\n🔎 4. Quick Peek: What’s Working on Landing Pages in 2025\n\n1 headline\n\n1 image or demo\n\n1 call to action\nEverything else? Distraction.\n\n🚀 Challenge of the Week\nCreate a “one-screen” version of your project — just the essence. No menus, no subpages. Then ask: does the value still shine through?\n\nThanks for riding the current with us. Stay bold, stay curious — and build with joy.\n\nSee you next wave,\n— The Creative Current Team",
        "image": "",
        "timestamp": "2025-08-03T13:06:18.976427Z"
      },
      {
        "title": "\"Insight Loop – Your Weekly Edge in Tech & Innovation\"",
        "content": "Hi Innovator,\n\nWelcome to this week’s edition of Insight Loop, where we connect you with ideas, tools, and developments shaping the tech ecosystem — all in under 5 minutes.\n\n🌟 This Week's Briefing\n⚡ Feature Focus: Smarter Automation, Simpler Workflows\nNo-code automation tools like Make and Pipedream are changing how teams link APIs and manage workflows. We walk through how one team saved 9 hours a week using 3 automations — no engineers involved.\n\n📊 Industry Insight: AI Isn’t Just the Future — It’s the New Baseline\nFrom customer service to backend optimization, AI is now table stakes. We share 3 quick ways to plug affordable AI into your stack — even if you're not “building AI.”\n\n🧠 Thought Piece: The Silent Value of Internal Documentation\nClear internal docs aren’t a nice-to-have. They’re competitive leverage. This week, we break down how good docs reduce onboarding time by 40% and improve system resilience.\n\n🔧 Team Pick: Cronicle (Lightweight Job Scheduler)\nLooking for an alternative to bulky cron dashboards? Cronicle is an open-source task runner with a beautiful UI and REST API support. Super handy for DevOps or small backend teams.\n\n🎯 Pro Tip of the Week\nUse watch -n 2 \"df -h\" to monitor disk space in real time — great for managing logs or backup-heavy environments.\n\nKeep learning. Keep refining. Keep building with purpose.\n\nSee you next week,\n— The Insight Loop Team",
        "image": "https://careernexus-storage1.s3.amazonaws.com/Newsletter/Images/760bdaaf-03d1-4e5e-8a0d-67d120314f08/Innovator.png",
        "timestamp": "2025-08-03T13:04:59.094410Z"
      },
      {
        "title": "\"The Forward Byte – Small Ideas, Big Impact\"",
        "content": "Hey there, Trailblazer,\n\nWelcome to this week’s edition of The Forward Byte, where we break down powerful trends, clever tools, and the kind of ideas that quietly change the game.\n\n🚀 This Week’s Highlights\n🧠 1. Micro Productivity is the New Superpower\nForget 4-hour work marathons. Studies now show that consistent, focused 20-minute sessions produce better results, especially in deep work. Try the \"3x20 rule\" this week — and track the difference.\n\n🛠️ 2. Tool of the Week: \"Raycast\" for Devs & Creators\nImagine Spotlight Search on steroids. Raycast brings code snippets, GitHub issues, Slack commands, and custom scripts all under your keyboard. And it’s free.\n\n📈 3. Quietly Exploding: Voice Interfaces in SaaS\nVoice commands aren’t just for Alexa anymore. Startups are embedding whisper-quiet voice input into CRMs, dashboards, and analytics tools — making SaaS more accessible and hands-free.\n\n💬 4. Quote Worth Sharing:\n\n\"Don’t aim for a million users. Aim to help 10 people so well they can’t live without it.\"\n— Paul Graham\n\n🧭 Your Weekly Action Step:\n✅ Choose one tool, habit, or workflow tweak this week and stick with it for 3 days straight.\nSmall change = massive momentum.\n\nThanks for reading — keep building, stay curious, and never underestimate a small shift.\n\nUntil next week,\n— The Forward Byte Team",
        "image": "",
        "timestamp": "2025-08-03T12:59:42.577694Z"
      },
      {
        "title": "\"TechPulse Weekly – Staying Ahead in a Rapidly Changing World\"",
        "content": "Hello Innovators,\n\nWelcome to this week’s edition of TechPulse Weekly, where we bring you the latest insights, tools, and trends shaping the future of technology, business, and beyond.\n\n🔍 What’s Inside This Week:\n1. 🚀 AI Adoption Surges in Small Businesses\nA new study reveals that over 60% of small businesses have integrated AI tools into their daily operations, with automation and content generation leading the way. Experts predict this trend will only accelerate as tools become more affordable and accessible.\n\n2. 🔐 Cybersecurity Breaches on the Rise\nA string of high-profile cyberattacks has put data privacy back in the spotlight. We explore best practices for safeguarding your systems — and why zero-trust architecture is more than just a buzzword.\n\n3. 💡 Dev Spotlight: Open-Source Tools to Watch\nFrom low-code platforms to innovative data visualizers, we highlight three rising open-source projects making waves in the dev community.\n\n4. 📱 App of the Week: Arc Browser\nIt’s not just another Chrome alternative. Arc’s unique sidebar, tab containers, and personal spaces are redefining how we interact with the web. Our tech writer breaks down the pros and cons.\n\n5. 🌍 Global Tech Events Coming Up\n\nDEFCON 33 (Aug 8–11) – Las Vegas\n\nFOSDEM Africa (Sep) – Nairobi\n\nAI Expo Europe (Oct) – Amsterdam\n\n💬 From the Editor\nTechnology moves fast, but thoughtful adoption and community learning can help us move smarter. Whether you’re a developer, entrepreneur, or lifelong learner, keep experimenting, keep sharing, and most of all — stay curious.\n\nTill next time,\n— The TechPulse Team",
        "image": "https://careernexus-storage1.s3.amazonaws.com/Newsletter/Images/53782840-1409-4aca-b5b7-e6612d0b1bab/pngtree-business-technology-digital-high-tech-world-background-image_15631454.jpg",
        "timestamp": "2025-08-03T11:21:59.707107Z"
      },
      {
        "title": "\"Build & Beyond – Your Weekly Dive into Tech, Tools, and Tactics\"",
        "content": "Hey Builders,\n\nWelcome back to Build & Beyond, your space to explore the latest in modern tech, smarter workflows, and the people reimagining what’s possible.\n\nThis week, we're diving into innovation that isn’t just loud — it’s smart.\n\n🧠 This Week’s Highlights\n⚙️ Productivity Stack: What’s Hot in 2025\nOur curated list of top tools to speed up your workflows — from browser extensions to AI assistants. Whether you're coding, designing, or organizing your life, this stack is a game-changer.\n\n🔥 Side Project Spotlight: “RecurTrack”\nBuilt by a solo founder in Lagos, RecurTrack is a lightweight tool that helps freelancers track recurring clients without needing a full CRM. Simple, elegant, and now open-source.\n\n🔍 Framework Deep Dive: Django 5.1\nThe new Django update introduces native async views, stricter typing, and performance boosts. Our guide shows how to upgrade and what to watch for if you’re building APIs.\n\n📚 Learn Something New:\n\n“How SQLite is secretly powering the world”\n\n“The psychology of clean code”\n\n“Why battery tech matters to cloud computing”\n\n🎯 Quick Tip of the Week\nUse htop instead of top in your Linux terminal. It’s interactive, colorful, and gives you real-time control over process priorities.\n\n🧭 What We’re Exploring Next Week\nA deep look at Postgres tuning\n\nHow indie developers are funding projects without VCs\n\nBuilding a minimalist dev environment (yes, even on 4GB RAM)\n\nKeep tinkering, keep shipping — and remember: the best tools are the ones you actually use.\n\nSee you next week,\n— The Build & Beyond Crew",
        "image": "https://careernexus-storage1.s3.amazonaws.com/Newsletter/Images/0ca08693-14c4-4fff-8954-2bdb337ba28d/techtacticsmay2025.jpg",
        "timestamp": "2025-08-03T11:05:28.134040Z"
      }
    ]
  }
}
```

[Table of contents](#toc)


# Get Other User Post<a name='get_other_user_post'></a>

This API retrieves the posts of another userby specifying the user_id query parameter in the url endpoint.

**Endpoint:**`/post/by-user/?user_id=2`

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


# Retrieve User Settings<a name='retrieve_user_settings'></a>

This API retrieves user settings parameters.

**Endpoint:**`/user/settings/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "email_notify": false,
  "push_notify": false,
  "message_notify": false,
  "weekly_summary": false,
  "job_alerts": false,
  "marketing": false,
  "show_email": false,
  "show_activity": false,
  "show_location": false,
  "timezone": "Africa/Tunis"
}
```

[["/user/settings/","GET"]][Table of contents](#toc)


# Update User Account Settings<a name='update_user_account_settings'></a>

This API updates user account settings parameters. N.B:All fields (except timezone) are Boolean.(True/False).

**Endpoint:**`/user/settings/`

**Method:** `PUT`

## Payload

``` json
{

email_notify:*****

push_notify:*****

message_notify:*****

weekly_summary:*****

job_alerts:*****

marketing:*****

show_email:*****

show_activity:*****

show_location:*****

timezone:*****

}

```
## Response body

**status code:200**

``` json
{
  "email_notify": true,
  "push_notify": false,
  "message_notify": false,
  "weekly_summary": false,
  "job_alerts": false,
  "marketing": false,
  "show_email": false,
  "show_activity": false,
  "show_location": false,
  "timezone": "Africa/Lagos"
}
```

[["/user/settings/","PUT"]][Table of contents](#toc)


# User Search<a name='user_search'></a>

This API searches for users based on a keyword query.

**Endpoint:**`/user/search/?keyword=backend developer`

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
      "id": 1,
      "name": "Opeyemi Saliu",
      "qualification": "Bachelor of Engineering (Civil Engineering)",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
      "user_type": "learner"
    }
  ]
}
```

[["/user/search/?keyword=backend developer","GET"]][Table of contents](#toc)


# Create Project Catalogue<a name='create_project_catalogue'></a>

This API creates a project catalogue for the logged in user. N.B:The image and downloadable_material fields are optional. Image(max_size=1mb), Download_material(max_size=5mb)

**Endpoint:**`/project/`

**Method:** `POST`

## Payload

``` json
{

title:*****

description:*****

image:*****

download_material:*****

}

```
## Response body

**status code:201**

``` json
{
  "id": 1,
  "title": "Backend architecture",
  "description": "A complete backend code base to support small, medium and large social media startups and webapps.",
  "image": "https://careernexus-storage1.s3.amazonaws.com/portfolio/image/6229255a-7c60-4f15-b932-39c525350c86default_portfolio.png",
  "download_material": null
}
```

[Table of contents](#toc)


# Retrieve Portfolio Projects<a name='retrieve_portfolio_projects'></a>

This API retrieves all the project portfolio uploaded by the user. N.B:By passing a portfolio_id in the url, data of a particular portfolio could be retrieved. Also, portfolios of other users can be retrieved by adding a user_id query parameter to the url endpoint.

**Endpoint:**`/project/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 1,
    "title": "Backend architecture",
    "description": "A complete backend code base to support small, medium and large social media startups and webapps.",
    "image": "https://careernexus-storage1.s3.amazonaws.com/portfolio/image/6229255a-7c60-4f15-b932-39c525350c86default_portfolio.png",
    "download_material": null
  },
  {
    "id": 2,
    "title": "Graphics Design",
    "description": "A beautiful graphic design by myself",
    "image": "https://careernexus-storage1.s3.amazonaws.com/portfolio/image/21909625-6545-415c-b047-88535407590eKSK_IV.jpg",
    "download_material": null
  },
  {
    "id": 3,
    "title": "Graphics and Art Design",
    "description": "An Invitation IV by myself.",
    "image": "https://careernexus-storage1.s3.amazonaws.com/portfolio/image/ae1ebba5-8f28-4252-8fe6-483d91468be8KSK_IV.jpg",
    "download_material": "https://careernexus-storage1.s3.amazonaws.com/portfolio/material/2f985276-5a60-4d6d-bf57-4a239ebc140fChatGPT%20Image%20Jun%2013%2C%202025%2C%2010_31_26%20PM.png"
  }
]
```

[Table of contents](#toc)


# Delete Project Catalogue<a name='delete_project_catalogue'></a>

This API deletes a project catalogue belonging to the loged in user. N.B:A portfolio_id must be provided in the endpoint url.

**Endpoint:**`/project/?portfolio_id=4`

**Method:** `DELETE`

## Payload

``` json


```
## Response body

**status code:204**

``` json
 
```

[Table of contents](#toc)


# Retrieve Mentors Posts<a name='retrieve_mentors_posts'></a>

This API retrieves Posts made by mentors on the platform.

**Endpoint:**`/post/by-mentors/`

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
        "id": 11,
        "first_name": "Abdul Azeez",
        "last_name": "Balogun",
        "middle_name": "Abiola",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg",
        "qualification": "Bachelor of Engineering"
      },
      "body": "Success rarely comes from doing one big thing right — it comes from doing the small things right, over and over again. Whether you're writing code, learning a language, or building a business, consistency beats intensity. Show up every day. Improve a little. The results will follow.",
      "pic1": "N/A",
      "pic2": "N/A",
      "pic3": "N/A",
      "video": "N/A",
      "article": "N/A",
      "time_stamp": "2025-08-09T10:18:07.879587Z",
      "comment_count": 0,
      "like_count": 0,
      "share_count": 0,
      "parent": null,
      "can_like": true,
      "can_follow": true,
      "is_self": false,
      "is_saved": false,
      "post_id": 21
    }
  ]
}
```

[Table of contents](#toc)


# Save a Mentor<a name='save_a_mentor'></a>

This API saves a Mentor for future reference. N.B:The user to be saved must be a mentor and must not have been previously saved.

**Endpoint:**`/mentor/save/`

**Method:** `POST`

## Payload

``` json
{

mentor:*****

}

```
## Response body

**status code:201**

``` json
{
  "saved": {
    "id": 11,
    "first_name": "Abdul Azeez",
    "last_name": "Balogun",
    "middle_name": "Abiola",
    "years_of_experience": 6,
    "technical_skills": [
      "Python",
      "Shell Scripting",
      "Backend development",
      "Devops",
      "AI/ML",
      "Database Management System"
    ],
    "current_job": "Backend Developer",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg"
  }
}
```

[Table of contents](#toc)


# Retrieve Saved Mentors<a name='retrieve_saved_mentors'></a>

This API retrieves all the Mentors that have been saved by the logged in user.

**Endpoint:**`/mentor/save/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "saved": {
      "id": 11,
      "first_name": "Abdul Azeez",
      "last_name": "Balogun",
      "middle_name": "Abiola",
      "years_of_experience": 6,
      "technical_skills": [
        "Python",
        "Shell Scripting",
        "Backend development",
        "Devops",
        "AI/ML",
        "Database Management System"
      ],
      "current_job": "Backend Developer",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg"
    }
  }
]
```

[Table of contents](#toc)


# Unsave Mentor<a name='unsave_mentor'></a>

This API removes a mentor from the saved list. N.B:This user must have been previously saved by the loggedin user.

**Endpoint:**`/mentor/save/?mentor=11`

**Method:** `DELETE`

## Payload

``` json


```
## Response body

**status code:204**

[Table of contents](#toc)


# Creating Library Content<a name='creating_library_content'></a>

This API creates contents on the platform's library section. N.B:titles cannot be duplicated.

**Endpoint:**`/info/library/`

**Method:** `POST`

## Payload

``` json
{

title:*****

description:*****

tags (list of strings):*****

file (downloadable file):*****

}

```
## Response body

**status code:201**

``` json
{
  "id": 1,
  "title": "Creating Udemy Courses",
  "description": "This document is a template for creating courses \nover the Udemy LMS platform. Their requirements \nand standards.",
  "tags": [
    "courses",
    "template"
  ],
  "file": "https://careernexus-storage1.s3.amazonaws.com/Library/uploads/df6e30bb-a6ef-486c-a323-fa54d111a6e5_CREATING_COURSES_ON%20UDEMY.docx"
}
```

[Table of contents](#toc)


# Retrieve Library Contents<a name='retrieve_library_contents'></a>

This API retrieves all the contents within the library. Also, by passing a content_id query parameter, information pertaining to a particular content could also be retrieved.

**Endpoint:**`/info/library/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 1,
    "title": "Creating Udemy Courses",
    "description": "This document is a template for creating courses \nover the Udemy LMS platform. Their requirements \nand standards.",
    "tags": [
      "courses",
      "template"
    ],
    "file": "https://careernexus-storage1.s3.amazonaws.com/Library/uploads/df6e30bb-a6ef-486c-a323-fa54d111a6e5_CREATING_COURSES_ON%20UDEMY.docx"
  }
]
```

[Table of contents](#toc)


# Delete Library Content<a name='delete_library_content'></a>

Tis API deletes a content from the platform's library section. N>B: A content_id query parameter is required for this request.

**Endpoint:**`/info/library/?content_id=2`

**Method:** `DELETE`

## Payload

``` json


```
## Response body

**status code:204**

[Table of contents](#toc)


# Save a Job<a name='save_a_job'></a>

This API saves a Job to be referenced and retrieved later.

**Endpoint:**`/job/save/`

**Method:** `POST`

## Payload

``` json
{

job:*****

}

```
## Response body

**status code:201**

``` json
{
  "job": {
    "title": "Backend Developer",
    "organization": "Career Nexus Ltd",
    "employment_type": "full_time",
    "work_type": "hybrid",
    "country": "Nigeria",
    "salary": "350,000NGN",
    "overview": "We are looking",
    "description": "You'll be responsible for turning user needs into elegant, intuitive interfaces for both web and mobile applications.",
    "experience_level": "entry"
  }
}
```

[Table of contents](#toc)


# Retrieve Saved Jobs<a name='retrieve_saved_jobs'></a>

This API retrieves all the jobs saved by the logged in user.

**Endpoint:**`/job/save/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "job": {
      "id": 2,
      "title": "Backend Developer",
      "organization": "Career Nexus Ltd",
      "employment_type": "full_time",
      "work_type": "hybrid",
      "country": "Nigeria",
      "salary": "350,000NGN",
      "overview": "We are looking",
      "description": "You'll be responsible for turning user needs into elegant, intuitive interfaces for both web and mobile applications.",
      "experience_level": "entry"
    }
  }
]
```

[Table of contents](#toc)


# Unsave Job<a name='unsave_job'></a>

This API removes a job from the users list of saved jobs. N.B:The job must have been previously saved.

**Endpoint:**`/job/unsave/?job=3`

**Method:** `DELETE`

## Payload

``` json


```
## Response body

**status code:204**

[Table of contents](#toc)


# General Notifications<a name='general_notifications'></a>

This API enables connecting to a general notification websocket. N.B:Notification is connected via ws/wss protocol. Also a valid token must be attached to the url string.

**Endpoint:**`/ws/notification/?token=****************`

**Method:** `NONE`

## Payload

``` json


```
[Table of contents](#toc)


# Get All Notifications<a name='get_all_notifications'></a>

This API retrieves all the notifications that have been recieved.

**Endpoint:**`/notification-chat/notifications/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "count": 22,
  "next": "http://127.0.0.1:8000/notification-chat/notifications/?page=2",
  "previous": null,
  "results": [
    {
      "id": 43,
      "text": "Someone just liked your post.",
      "page": "Post",
      "route": "post/?post_id=15",
      "obj_id": "15",
      "timestamp": "2025-11-19T08:21:47.314149Z"
    },
    {
      "id": 42,
      "text": "N/A N/A just replied to your comment.",
      "page": "Post",
      "route": "post/?post_id=13",
      "obj_id": null,
      "timestamp": "2025-11-18T14:40:57.985623Z"
    },
    {
      "id": 41,
      "text": "Mentor Abdul Azeez Balogun accepted your mentorship request.",
      "page": null,
      "route": null,
      "obj_id": null,
      "timestamp": "2025-11-11T16:21:06.756745Z"
    },
    {
      "id": 39,
      "text": "Mentor Abdul Azeez Balogun accepted your mentorship request.",
      "page": null,
      "route": null,
      "obj_id": null,
      "timestamp": "2025-11-11T16:16:40.721125Z"
    },
    {
      "id": 38,
      "text": "Mentor Abdul Azeez Balogun rejected your mentorship request.",
      "page": null,
      "route": null,
      "obj_id": null,
      "timestamp": "2025-11-11T16:16:16.247567Z"
    }
  ]
}
```

[["/notification-chat/notifications/","GET"]][Table of contents](#toc)


# Clear Notifications<a name='clear_notifications'></a>

This API clears all the notifications for a user.

**Endpoint:**`/notification-chat/notifications/`

**Method:** `DELETE`

## Payload

``` json


```
## Response body

**status code:204**

[Table of contents](#toc)


# Mentorship Session Annotation.<a name='mentorship_session_annotation.'></a>

This API marks a mentorship session as completed and allows the learner to rate the mentor. N.B:A session would be assumed to have been completed if it has been paid for and the set time for the mentorship session is not in the future. Also, a session can only be annotated by the learner that sent the booking request in the first place. Also, the mark_completed payload must be True for the request to be valid and also, the rating can only be from 1 to 5.

**Endpoint:**`/mentor/annotate/`

**Method:** `POST`

## Payload

``` json
{

"session":"*****"

"mark_completed":"*****"

"rating":"*****"

}

```
## Response body

**status code:200**

``` json
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
    "date": "2025-07-21",
    "time": "00:00:00"
  },
  "discourse": "Career Building",
  "amount": "2USD",
  "status": "COMPLETED",
  "is_paid": true
}
```

[Table of contents](#toc)


# Session Payment with Flutterwave<a name='session_payment_with_flutterwave'></a>

This API allows a learner to pay for a session with flutterwave. N.B:The learner must be the one that initiated the session request and the session must have been accepted by the mentor inorder to be available for payment. NGN currency is enforced in use by this API.

**Endpoint:**`/payments/flutterwave/initiate/`

**Method:** `POST`

## Payload

``` json
{

"session":"*****"

}

```
## Response body

**status code:200**

``` json
{
  "payment link": "https://checkout-v2.dev-flutterwave.com/v3/hosted/pay/9f95437309518f386e80"
}
```

[Table of contents](#toc)


# Session Payment with Stripe<a name='session_payment_with_stripe'></a>

This API allows learners to pay for mentorship sessions using Stripe. N.B::The learner must be the one that initiated the session request and the session must have been accepted by the mentor inorder to be available for payment. The USD currency is enforced for this payment option.

**Endpoint:**`/payments/stripe/initiate/`

**Method:** `POST`

## Payload

``` json
{

"session":"*****"

}

```
## Response body

**status code:200**

``` json
{
  "session_id": "cs_test_a1dI9QEtjX8x4MlZYjh0R3AT74XL1EbflEE0osclkyDUucfGOSDhptF1mS",
  "url": "https://checkout.stripe.com/c/pay/cs_test_a1dI9QEtjX8x4MlZYjh0R3AT74XL1EbflEE0osclkyDUucfGOSDhptF1mS#fidkdWxOYHwnPyd1blpxYHZxWjA0VjVLS1FGSkBURkp8YXRkTz1zdlBNaHBiUkowSDZ9YDRIZnxJRk9XTTNDaW5GfG53Y0pnQDZANGdOZ2Rqc2hXdF9fUl1Cc0ZpYUkwNH1LdF1DZF1%2FVk40NTV3NlNNNkZKQycpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"
}
```

[Table of contents](#toc)


# Cancel Mentorship Session<a name='cancel_mentorship_session'></a>

This API cancels a mentorship sessions. N.B:Only the session initiator (mentee) can cancel a mentorship session. Also, a session can only be canceled if it is yet to be paid for.

**Endpoint:**`/mentor/session/cancel/`

**Method:** `POST`

## Payload

``` json
{

"session":"*****"

}

```
## Response body

**status code:200**

``` json
{
  "status": "Success",
  "message": "Cancelled Mentorship session"
}
```

[Table of contents](#toc)


# Join Mentorship Session<a name='join_mentorship_session'></a>

This API retrieves the session id and the jwt token to authenticate Jitsi as a Service. N.B:The user must either be a learner(mentee) or the sessions mentor. Also, only paid sessions can be joined and also, the time set for the session must not be in the future.

**Endpoint:**`/mentor/session/join/?session=13`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "session_id": 21,
  "room_name": "Room_1_11_a2eb040d-b005-49fc-8fa6-6b9e028fc825",
  "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6InZwYWFzLW1hZ2ljLWNvb2tpZS01NjQwNmY0ODFkODU0NmI2OTE1OGU1MjQyZmEzZTk3Mi8xMzljNTkiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJqaXRzaSIsImNvbnRleHQiOnsidXNlciI6eyJpZCI6IlVzZXJfMSIsIm5hbWUiOiJPcGV5ZW1pIFNhbGl1IiwiYXZhdGFyIjoiaHR0cHM6Ly9jYXJlZXJuZXh1cy1zdG9yYWdlMS5zMy5hbWF6b25hd3MuY29tL3Byb2ZpbGVfcGljdHVyZXMvODI4YmZlNGMtNDhkYy00N2Q3LTgyZjktNDZlYWJiNzAxOTdkTGFwdG9wMS5qcGciLCJlbWFpbCI6InNhbGl1b2F6ZWV6QGdtYWlsLmNvbSIsIm1vZGVyYXRvciI6ZmFsc2V9LCJmZWF0dXJlcyI6eyJsaXZlc3RyZWFtaW5nIjpmYWxzZSwib3V0Ym91bmQtY2FsbCI6ZmFsc2UsInRyYW5zY3JpcHRpb24iOmZhbHNlLCJyZWNvcmRpbmciOmZhbHNlfSwicm9vbSI6eyJyZWdleCI6ZmFsc2V9fSwiZXhwIjoxNzU5MzUzODM1LCJpc3MiOiJjaGF0IiwibmJmIjoxNzU5MzUwMjM1LCJyb29tIjoiKiIsInN1YiI6InZwYWFzLW1hZ2ljLWNvb2tpZS01NjQwNmY0ODFkODU0NmI2OTE1OGU1MjQyZmEzZTk3MiJ9.I0PqCprAYvRPWtJ6G9NtFszbDku96nzL2x9AnzFdqurVujFq8PuBaaetou3Apk096QazOYLK5AZzF1R78uq00CVSA42C6J3ASWsQO9F2CJSn57B_AbIYezdpa1cAgse8fRRQd5muG29Wy0wFHxxtYzEOddVBgf3qcqaFhImm1gRu_DE-Tytov6UqMPud_si6lOz6Lthm2dm-uxHr_wpXCuijymQJCtYxxHo7lds6VFocnJluN39tNNZJE40WgAL6FWNyKeoV5PHFH5x0UiNcgUAgjmC7A0FzqkQcNFGBn1jqgtQIqrYj39UfhanlGH7bCTqy4iCMmIY-vEmIB6YOUvUTwmK_EcnEUGCJNg2MIcQ07WeEyoL2Ac0oHvb-t5r5NQqDRdQP1aKR0vENjYTE9tgOTUVUARFQGh7iJF4bpA76cMmR6mQruf9HPvp947DKOzZOXP4fFMMS0TOwJYOF1rlI76hOM1gzDf6DsIe2sJkveHx7v0g0RRIicwVou6jdaemR2lby4V_J0B3tGBFRzhL0wBNM_RB3FNKOKxiv2CEcvDbUXsdp76OEVW5GB1m5A9u_ZVDIkvL0_Q1CtygecxUe_a4_ER_63LxTnOq3WQ2Urf53l0Gpi9-H5dotaVzcu1B5dv8Af-JpYiTdDvymkL8VArOG87_7NnW1ke0b7D0"
}
```

[["/mentor/session/join/?session=13","GET"]][Table of contents](#toc)


# Google Signin<a name='google_signin'></a>

This API exchanges a google code for authentication details. N.B:A call to google's oauth2 API should have been previously made to obtain a valid code to be used for this request.

**Endpoint:**`/user/google/signin/`

**Method:** `POST`

## Payload

``` json
{

"code":"*****"

}

```
## Response body

**status code:200**

``` json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1Njk5MDI4NSwiaWF0IjoxNzU2OTAzODg1LCJqdGkiOiI3M2ZmNGQxMmQ1NmM0ZTY3YWU2ODM4ZDk1NDE5NGUwYiIsInVzZXJfaWQiOjF9.YjOJm8AYgT0h39mdH27FF9goXOgvIIbvIEbsFjQGsMM",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2OTI1NDg1LCJpYXQiOjE3NTY5MDM4ODUsImp0aSI6IjQxZjhkZDhkY2RhNTQ2M2RhNGViNWRlMWViMzlmYzM0IiwidXNlcl9pZCI6MX0.MQwDkQZGzeP6h_3mTOeOMJYR5sbm39RzzuXbKzk51cE",
  "email": "saliuoazeez@gmail.com",
  "user_type": "learner",
  "id": 1
}
```

[Table of contents](#toc)


# Signup with Google<a name='signup_with_google'></a>

This API allows a google user to signup with their account. N.B:Request to goole's oauth2 should have been previously made to obtain a valid code. Also, Someone that registers via google account is setup to be passwordless. (They can only login via google or login normally after changing their password). Also, If a user_type extra payload is passed with a value of mentor, A mentor use is signed up.

**Endpoint:**`/user/google/signup/`

**Method:** `POST`

## Payload

``` json
{

"code":"*****"

"user_type(optional)":"*****"

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

[["/user/google/signup/","POST"]][Table of contents](#toc)


# Delete Post<a name='delete_post'></a>

This API deletes a post. N.B:A user can only delete their own post.

**Endpoint:**`/post/delete/?post_id=23`

**Method:** `DELETE`

## Payload

``` json


```
## Response body

**status code:204**

[Table of contents](#toc)


# Dispute Creation<a name='dispute_creation'></a>

This API allows a user to create a dispute/request for the admin. N.B:The options of categories are (technical,payment,account,request,others). The options for priority are (low,medium,high,urgent).

**Endpoint:**`/user/disputes/`

**Method:** `POST`

## Payload

``` json
{

"category":"*****"

"priority":"*****"

"message":"*****"

}

```
## Response body

**status code:201**

``` json
{
  "id": 1,
  "category": "request",
  "priority": "low",
  "message": "I just want to request for \na feature that would allow \nearning as a learner.",
  "status": "pending",
  "admin_response": null,
  "timestamp": "2025-09-11T13:44:08.574258Z"
}
```

[Table of contents](#toc)


# User Retrieve Dispute<a name='user_retrieve_dispute'></a>

This API allows users to retrieve disputes that has been created by them. N.B:Also by adding a status query parameter to the url, disputes could be filtered by status. (status is either pending,in_progress,resolved or closed).

**Endpoint:**`/user/disputes/`

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
      "id": 2,
      "category": "account",
      "priority": "high",
      "message": "I can't log into my account.",
      "status": "pending",
      "admin_response": null,
      "timestamp": "2025-09-11T13:55:26.575118Z"
    },
    {
      "id": 1,
      "category": "request",
      "priority": "low",
      "message": "I just want to request for \na feature that would allow \nearning as a learner.",
      "status": "pending",
      "admin_response": null,
      "timestamp": "2025-09-11T13:44:08.574258Z"
    }
  ]
}
```

[Table of contents](#toc)


# Dispute Ticket Resolution<a name='dispute_ticket_resolution'></a>

This API allows an admin to annotate a user dispute. This annotation can be either changing the status of the dispute and/or attaching an admin response to the dispute. N.B:Only an Admin is permitted for this operation.

**Endpoint:**`/user/admin/disputes/`

**Method:** `PUT`

## Payload

``` json
{

"dispute":"*****"

"status":"*****"

"response":"*****"

}

```
## Response body

**status code:200**

``` json
{
  "id": 1,
  "category": "request",
  "priority": "low",
  "message": "I just want to request for \na feature that would allow \nearning as a learner.",
  "status": "pending",
  "admin_response": "We are working on it",
  "timestamp": "2025-09-11T13:44:08.574258Z"
}
```

[Table of contents](#toc)


# Admin Retrieve Dispute Tickets<a name='admin_retrieve_dispute_tickets'></a>

This API allows admins to retrieve dispute tickets created by users accross the system. N.B:By adding query parameters priority and/or category, ticket entries could be filtered.

**Endpoint:**`/user/admin/disputes/`

**Method:** `GEt`

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
      "id": 2,
      "category": "account",
      "priority": "high",
      "message": "I can't log into my account.",
      "status": "pending",
      "admin_response": null,
      "timestamp": "2025-09-11T13:55:26.575118Z"
    }
  ]
}
```

[Table of contents](#toc)


# Dispute Summary<a name='dispute_summary'></a>

This API retrieves and counts all disputes by categories.

**Endpoint:**`/user/admin/disputes/summary/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "technical": 0,
  "payment": 0,
  "account": 1,
  "request": 1,
  "others": 0
}
```

[Table of contents](#toc)


# Delete User<a name='delete_user'></a>

This is a temporary API that allows deletion of a user.

**Endpoint:**`/user/delete/`

**Method:** `DELETE`

## Payload

``` json
{

"email":"*****"

}

```
## Response body

**status code:204**

[["/user/delete/","DELETE"]][Table of contents](#toc)


# Create Corporate Account<a name='create_corporate_account'></a>

This API creates a corporate user account for a previously registered user and links it to the user's account. N.B:The main user must be logged in to create a corporate profile. Also, the logo field upload is optional.

**Endpoint:**`/user/corporate/signup/`

**Method:** `POST`

## Payload

``` json
{

"company_name":"*****"

"company_email":"*****"

"company_type":"*****"

"company_size":"*****"

"industry":"*****"

"website":"*****"

"location":"*****"

"tagline":"*****"

"logo":"*****"

}

```
## Response body

**status code:201**

``` json
{
  "id": 20,
  "company_name": "Bojowa Ventures Limited",
  "company_type": "private",
  "company_size": "1-10",
  "country_code": "+000",
  "phone_number": "00000000000",
  "location": "Lagos",
  "website": "www.bojventltd.com",
  "tagline": "Dealers in recycled wastes and compositions.",
  "logo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/b86858f7-c77e-4c5f-9796-14f27c855f7cDefault_company_image.png",
  "cover_photo": "https://careernexus-storage1.s3.amazonaws.com/cover_photos/70114098-5014-4eda-a725-5421792972dadefault_cp.jpeg"
}
```

[["/user/corporate/signup/","POST"]][Table of contents](#toc)


# Retrieve Linked Accounts<a name='retrieve_linked_accounts'></a>

This API retrieves all the accounts linked to currently logged in account.

**Endpoint:**`/user/linked-accounts/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "account": {
      "id": 21,
      "name": "Bojowa Ventures Limited",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/b86858f7-c77e-4c5f-9796-14f27c855f7cDefault_company_image.png",
      "extras": "Dealers in recycled wastes and compositions."
    }
  }
]
```

[["/user/linked-accounts/","GET"]][Table of contents](#toc)


# Switch Account<a name='switch_account'></a>

This API enables a user to switch between accounts. N.B:Both accounts must be previously linked to enable account switching.

**Endpoint:**`/user/switch-account/`

**Method:** `POST`

## Payload

``` json
{

"account":"*****"

}

```
## Response body

**status code:200**

``` json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODI1MTUwMiwiaWF0IjoxNzU4MTY1MTAyLCJqdGkiOiI0YjY2ZTkxN2I0Nzc0YjRjYThjMWNiOTE2OWRmN2M4OSIsInVzZXJfaWQiOjIxfQ.ccoUF4tiNdayPvo9pLN9YpUiJJXNIVbrMLSxhsiR9OU",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4MTg2NzAyLCJpYXQiOjE3NTgxNjUxMDIsImp0aSI6Ijg1NTc2MTI4YWJmNzQwYWFhZDRiMjVjOGIwNmNmOTRjIiwidXNlcl9pZCI6MjF9.BTJcI2rPMO39UlQ5KvuCYSuYO9Klypf_BEGqKgqUqEo",
  "user_id": 21,
  "email": "bojvent@yahoo.com",
  "user_type": "employer"
}
```

[["/user/switch-account/","POST"]][Table of contents](#toc)


# Chat Websockets<a name='chat_websockets'></a>

This API connects a user to a chatroom shared with another user. N.B:The user id of the second user should be provided in the url along with a valid token.

**Endpoint:**`/ws/chat/<user_id>/?token=**********`

**Method:** `NONE`

## Payload

``` json


```
## Response body

**status code:NONE**

[["/ws/chat/<user_id>/?token=**********","NONE"]][Table of contents](#toc)


# Retrieve Mentor Vault Data<a name='retrieve_mentor_vault_data'></a>

This API retrieves the current vault balance of a mentor and also the 10 most recent transactions made within the vault. N.B:Transaction action is either EARN (+) or WITHDRAW (-).

**Endpoint:**`/mentor/vault/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "amount": {
    "amount": 3000,
    "currency": "NGN"
  },
  "recent_transaction_history": [
    {
      "id": 1,
      "action": "EARN",
      "amount": {
        "value": 3000,
        "currency": "NGN"
      },
      "extra_data": {
        "session_id": 13,
        "session_type": "individual"
      },
      "timestamp": "2025-09-25T06:33:04.576684Z"
    }
  ]
}
```

[["/mentor/vault/","GET"]][Table of contents](#toc)


# Retrieve Vault Transactions<a name='retrieve_vault_transactions'></a>

This API retrieves all the Vault transactions (earnings and withdrawals) of a mentor.

**Endpoint:**`/mentor/vault/transactions/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 1,
    "action": "EARN",
    "amount": {
      "value": 3000,
      "currency": "NGN"
    },
    "extra_data": {
      "session_id": 13,
      "session_type": "individual"
    },
    "timestamp": "2025-09-25T06:33:04.576684Z"
  }
]
```

[["/mentor/vault/transactions/","GET"]][Table of contents](#toc)


# Initiate Chat Session<a name='initiate_chat_session'></a>

This API initiates a chatsession with another user or retrieves it if a session already exists. N.B:You cannot initiate a chat session with yourself.

**Endpoint:**`/notification-chat/chats/initiate/`

**Method:** `POST`

## Payload

``` json
{

"user":"*****"

}

```
## Response body

**status code:200**

``` json
{
  "contributor": {
    "id": 3,
    "first_name": "N/A",
    "last_name": "N/A",
    "middle_name": "N/A",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png",
    "qualification": "Bachelor of Education (English)"
  },
  "chat_id": 2
}
```

[["/notification-chat/chats/initiate/","POST"]][Table of contents](#toc)


# Retrieve Shared Post<a name='retrieve_shared_post'></a>

This API retrieves all the contents of a shared post. N.B:An Unregistered/Logged out user can call this API to retrieve post details.

**Endpoint:**`/post/share/?hash=542c2550-7f38-4c42-b059-c6d72e299d97`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
{
  "shared_by": {
    "id": 1,
    "first_name": "Opeyemi",
    "last_name": "Saliu",
    "middle_name": "Abdul-Azeez",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
    "qualification": "Bachelor of Engineering (Civil Engineering)"
  },
  "post": {
    "profile": {
      "id": 21,
      "first_name": "Bojowa Ventures Limited",
      "last_name": "",
      "middle_name": "",
      "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/b86858f7-c77e-4c5f-9796-14f27c855f7cDefault_company_image.png",
      "qualification": "Dealers in recycled wastes and compositions."
    },
    "body": "Technology isn’t just about gadgets and apps — it’s the invisible force shaping how we live, work, and connect. From cloud systems powering businesses to AI assisting in everyday tasks, it keeps pushing boundaries of speed, scale, and creativity.\n\nBut here’s the thing: technology is only as impactful as the minds behind it. The real breakthrough happens when curiosity meets code, when ideas turn into solutions.\n\nIn a world moving faster than ever, the question is no longer “What can technology do?” but “What will we choose to build with it?” 🚀",
    "pic1": "N/A",
    "pic2": "N/A",
    "pic3": "N/A",
    "video": "N/A",
    "parent": null,
    "like_count": 0,
    "comment_count": 0,
    "share_count": 2,
    "time_stamp": "2025-09-18T03:44:39.929867Z"
  }
}
```

[["/post/share/?hash=542c2550-7f38-4c42-b059-c6d72e299d97","GET"]][Table of contents](#toc)


# Lead Register<a name='lead_register'></a>

This API collects and stores the data of corporate leads that provide their information. N.B: interested_services options include hr_solutions,corporate_training,L&D and organizational_development. Also, leads are not allowed to register multiple times with the same email address. Also, there is an optional field package valid options which include basic,premium,inclusive.

**Endpoint:**`/user/lead/register/`

**Method:** `POST`

## Payload

``` json
{

"full_name":"*****"

"email_address":"*****"

"phone_number":"*****"

"interested_services":"*****"

"package":"*****"

}

```
## Response body

**status code:201**

``` json
{
  "full_name": "Opeyemi Abdul",
  "email_address": "bojvent2@yahoo.com",
  "phone_number": "08056430145",
  "interested_services": [
    "Technology",
    "L&D"
  ],
  "package": "basic"
}
```

[["/user/lead/register/","POST"]][Table of contents](#toc)


# Retrieve Corporate Leads<a name='retrieve_corporate_leads'></a>

This API retrieves all the data of corporate leads registered on the system. N.B:This API isonly accessible to users with Admin privileges.

**Endpoint:**`/user/lead/register/`

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
      "full_name": "Opeyemi Abdul",
      "email_address": "bojvent1@yahoo.com",
      "phone_number": "08056430145",
      "interested_services": [
        "Technology"
      ],
      "package": null
    },
    {
      "full_name": "Opeyemi Abdul",
      "email_address": "bojvent@yahoo.com",
      "phone_number": "08056430145",
      "interested_services": [
        "Technology",
        "L&D"
      ],
      "package": null
    },
    {
      "full_name": "Opeyemi Abdul",
      "email_address": "bojvent2@yahoo.com",
      "phone_number": "08056430145",
      "interested_services": [
        "Technology",
        "L&D"
      ],
      "package": "basic"
    }
  ]
}
```

[["/user/lead/register/","GET"]][Table of contents](#toc)


# Update Job Status<a name='update_job_status'></a>

This API updates a job status which can either be active,draft or closed. N.B:Only jobs posted by the logged in user can have their status updated.

**Endpoint:**`/job/status/update/`

**Method:** `PUT`

## Payload

``` json
{

"job":"*****"

"status":"*****"

}

```
## Response body

**status code:200**

``` json
{
  "id": 11,
  "title": "Backend Developer",
  "organization": "Sterling Technologies",
  "employment_type": "full_time",
  "work_type": "hybrid",
  "country": "Nigeria",
  "salary": "350,000NGN",
  "overview": "A skilled backend developer aith at least \n5 years of experience",
  "description": "As a Backend Developer, you will play a crucial role in designing, implementing, and optimizing the backbone of our digital services. You'll work closely with frontend developers, DevOps engineers, and product teams to deliver robust and high-performance applications. Responsibilities include developing RESTful APIs, ensuring data integrity and security, managing database schemas, and optimizing application performance. A strong understanding of backend frameworks, data structures, and software engineering principles is essential.",
  "experience_level": "senior",
  "time_stamp": "2025-10-30",
  "is_saved": false
}
```

[["/job/status/update/","PUT"]][Table of contents](#toc)


# Apply for Job<a name='apply_for_job'></a>

This API allows a user to apply for a Job. N.B: Job can only be applied to once.

**Endpoint:**`/job/apply/`

**Method:** `POST`

## Payload

``` json
{

"job":"*****"

}

```
## Response body

**status code:200**

``` json
{
  "application_status": "Success"
}
```

[["/job/apply/","POST"]][Table of contents](#toc)


# Retrieve Job Applications<a name='retrieve_job_applications'></a>

This API allows an Employer to retrieve all the applications for a particular job. N.B:A job_id query parameter is required for this request. Also. the user must be the poster of the job to be able to view it's applications.

**Endpoint:**`/job/application/?job_id=2`

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
      "id": 1,
      "applicant": {
        "id": 1,
        "first_name": "Opeyemi",
        "last_name": "Saliu",
        "middle_name": "Abdul-Azeez",
        "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
        "qualification": "Bachelor of Engineering (Civil Engineering)",
        "resume": "https://careernexus-storage1.s3.amazonaws.com/resumes/51b434ab-441f-4ab1-ab72-a58c91ac7172Resume_080525.pdf"
      }
    }
  ]
}
```

[["/job/application/?job_id=2","GET"]][Table of contents](#toc)


# Retrieve Applied Jobs<a name='retrieve_applied_jobs'></a>

This API retrieves all the jobs that a user has applied for.

**Endpoint:**`/job/apply/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 1,
    "job": {
      "id": 2,
      "title": "Backend Developer",
      "employment_type": "full_time",
      "salary": "350,000NGN",
      "country": "Nigeria",
      "organization": "Career Nexus Ltd",
      "posted_on": "2025-06-11"
    }
  },
  {
    "id": 2,
    "job": {
      "id": 10,
      "title": "Frontend Developer",
      "employment_type": "full_time",
      "salary": "150,000NGN",
      "country": "Nigeria",
      "organization": "TechExperts",
      "posted_on": "2025-10-30"
    }
  }
]
```

[["/job/apply/","GET"]][Table of contents](#toc)


# Retrieve Recent Applicants<a name='retrieve_recent_applicants'></a>

This API retrieves the 5 most recent job applications.

**Endpoint:**`/job/application/recent/`

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
    "applicant": "Opeyemi Saliu",
    "job_name": "Frontend Developer"
  }
]
```

[["/job/application/recent/","GET"]][Table of contents](#toc)


# Edit Job<a name='edit_job'></a>

This API allows a user to edit their draft jobs.

**Endpoint:**`/job/?job_id=11`

**Method:** `PUT`

## Payload

``` json
{

"title":"*****"

"organization":"*****"

"employment_type":"*****"

"work_type":"*****"

"country":"*****"

"salary":"*****"

"overview":"*****"

"description":"*****"

"experience_level":"*****"

"status (**optional)":"*****"

}

```
## Response body

**status code:206**

``` json
{
  "id": 11,
  "title": "Backend Developer",
  "organization": "Sterling Technologies",
  "employment_type": "full_time",
  "work_type": "remote",
  "country": "Nigeria",
  "salary": "350,000NGN",
  "overview": "A skilled backend developer aith at least \n5 years of experience",
  "description": "As a Backend Developer, you will play a crucial role in designing, implementing, and optimizing the backbone of our digital services. You'll work closely with frontend developers, DevOps engineers, and product teams to deliver robust and high-performance applications. Responsibilities include developing RESTful APIs, ensuring data integrity and security, managing database schemas, and optimizing application performance. A strong understanding of backend frameworks, data structures, and software engineering principles is essential.",
  "experience_level": "senior",
  "time_stamp": "2025-10-30",
  "is_saved": false
}
```

[["/job/?job_id=11","PUT"]][Table of contents](#toc)


# Add Organization Members<a name='add_organization_members'></a>

This API adds other users as members of a corporate account (Organization). N.B:other corporate accounts cannot be added as members of an organization.

**Endpoint:**`/user/organization-members/`

**Method:** `POST`

## Payload

``` json
{

"member":"*****"

}

```
## Response body

**status code:201**

``` json
{
  "member": {
    "id": 1,
    "name": "Opeyemi Abdul-Azeez Saliu",
    "profile_photo": "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/828bfe4c-48dc-47d7-82f9-46eabb70197dLaptop1.jpg",
    "extras": "Bachelor of Engineering (Civil Engineering)"
  }
}
```

[["/user/organization-members/","POST"]][Table of contents](#toc)


# Remove Organization Member<a name='remove_organization_member'></a>

This API removes a member from a corporate account (organization). N.B:The member should have been previously enrolled. Also, a member_id is required for this request.

**Endpoint:**`/user/organization-members/?member_id=1`

**Method:** `DELETE`

## Payload

``` json


```
## Response body

**status code:204**

[["/user/organization-members/?member_id=1","DELETE"]][Table of contents](#toc)


# Retrieve Invited Sessions<a name='retrieve_invited_sessions'></a>

This API retrieves all sessions a user has been invited to.

**Endpoint:**`/mentor/sessions/invited/`

**Method:** `GET`

## Payload

``` json


```
## Response body

**status code:200**

``` json
[
  {
    "id": 1,
    "session": {
      "id": 26,
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
      "session_type": "group",
      "session_at": {
        "date": "2025-11-11",
        "time": "16:35:00"
      },
      "discourse": "Career Coaching",
      "amount": "1USD",
      "rating": 0,
      "status": "PENDING",
      "is_paid": false
    }
  }
]
```

[["/mentor/sessions/invited/","GET"]][Table of contents](#toc)


# Unregistered Users Subscribe To Newsletter<a name='unregistered_users_subscribe_to_newsletter'></a>

This API allows unregistered users on the platform subscribe to Newsletter.

**Endpoint:**`/user/newsletter-subscribe/`

**Method:** `POST`

## Payload

``` json
{

"email":"*****",

}

```
## Response body

**status code:200**

``` json
{
  "status": "Subscribed Successfully"
}
```

[["/user/newsletter-subscribe/","POST"]][Table of contents](#toc)