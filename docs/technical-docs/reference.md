---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Batool, Esma]

{: .no_toc }
## Reference documentation

{: .attention }
> This page collects internal functions, routes with their functions, and APIs (if any).
> 
> See [Uber](https://developer.uber.com/docs/drivers/references/api) or [PayPal](https://developer.paypal.com/api/rest/) for exemplary high-quality API reference documentation.
>
> You may delete this `attention` box.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## [Section / module]

### `function_definition()`

**Route:** `/route/`

**Methods:** `POST` `GET` `PATCH` `PUT` `DELETE`

**Purpose:** [Short explanation of what the function does and why]

**Sample output:**

[Show an image, string output, or similar illustration -- or write NONE if function generates no output]

---

# =========================================================
# Routes Documentation – WheelEats
# =========================================================
#
# ## Authentication
#
# ### home()
#
# **Route:** /
# **Methods:** GET
#
# **Purpose:**
# Entry point of the application.
# Redirects the user automatically to the start page (/index).
#
# **Sample output:**
# NONE
#
# ---------------------------------------------------------
#
# ### login()
#
# **Route:** /login
# **Methods:** GET, POST
#
# **Purpose:**
# Displays the login screen and authenticates users in demo mode.
# Logged-in users gain access to protected features such as
# adding restaurants and submitting reviews.
#
# **Sample output:**
# Login form (email and password)
#
# ---------------------------------------------------------
#
# ### register()
#
# **Route:** /register
# **Methods:** GET, POST
#
# **Purpose:**
# Allows new users to register.
# Registration is currently implemented as a demo
# without persistent data storage.
#
# **Sample output:**
# Registration form
#
# ---------------------------------------------------------
#
# ### logout()
#
# **Route:** /logout
# **Methods:** GET
#
# **Purpose:**
# Logs out the currently authenticated user
# and ends the session.
#
# **Sample output:**
# Redirect to login page with info message
#
# =========================================================
# ## Restaurants
# =========================================================
#
# ### index()
#
# **Route:** /index
# **Methods:** GET
#
# **Purpose:**
# Displays the main page of the application
# with a list of accessible restaurants.
#
# **Sample output:**
# Restaurant list overview
#
# ---------------------------------------------------------
#
# ### restaurant_detail(restaurant_id)
#
# **Route:** /restaurants/<int:restaurant_id>
# **Methods:** GET
#
# **Purpose:**
# Displays detailed information about a specific restaurant
# identified by its ID.
#
# **Sample output:**
# Restaurant detail view
#
# ---------------------------------------------------------
#
# ### restaurant_new()
#
# **Route:** /restaurants/new
# **Methods:** GET, POST
#
# **Purpose:**
# Allows authenticated users to submit a new restaurant.
# Unauthenticated users are redirected to the login page.
#
# **Sample output:**
# New restaurant submission form
#
# =========================================================
# ## Reviews
# =========================================================
#
# ### restaurant_review_create(restaurant_id)
#
# **Route:** /restaurants/<int:restaurant_id>/reviews
# **Methods:** POST
#
# **Purpose:**
# Allows authenticated users to submit a review
# for a restaurant. Reviews are currently handled
# in demo mode without database persistence.
#
# **Sample output:**
# Success message after submitting a review
#
# =========================================================
# ## Map
# =========================================================
#
# ### restaurant_map()
#
# **Route:** /map
# **Methods:** GET
#
# **Purpose:**
# Displays a map view of restaurants.
# Currently implemented as a placeholder.
#
# **Sample output:**
# Map view placeholder
#
# =========================================================
# ## Error Handling
# =========================================================
#
# ### http_not_found(e)
#
# **Route:** *
# **Methods:** GET
#
# **Purpose:**
# Handles requests to non-existing routes.
#
# **Sample output:**
# 404 error page
#
# ---------------------------------------------------------
#
# ### http_internal_server_error(e)
#
# **Route:** *
# **Methods:** GET
#
# **Purpose:**
# Handles internal server errors.
#
# **Sample output:**
# 500 error page
#
# =========================================================
