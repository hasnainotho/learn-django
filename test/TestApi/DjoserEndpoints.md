"""
Djoser Authentication Endpoints

This module provides a set of RESTful endpoints for user authentication and management, powered by the Djoser library. The endpoints facilitate common authentication workflows, including:

- User registration (`/users/`): Allows new users to create an account.
- User login (`/token/login/`): Authenticates users and returns an authentication token.
- User logout (`/token/logout/`): Invalidates the user's authentication token.
- Password reset (`/users/reset_password/`): Initiates the password reset process by sending a reset email.
- Password reset confirmation (`/users/reset_password_confirm/`): Confirms and completes the password reset process.
- User activation (`/users/activation/`): Handles user account activation via email confirmation.
- Retrieve/update user profile (`/users/me/`): Allows authenticated users to view or update their profile information.
- Set password (`/users/set_password/`): Enables users to change their password while authenticated.
- Resend activation (`/users/resend_activation/`): Resends the account activation email.

All endpoints are designed to work with token-based authentication and support secure user management out of the box.
"""