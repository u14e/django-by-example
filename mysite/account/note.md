Django provides the following views to deal with authentication:
- login : Handles a log in form and logs in a user
- logout : Logs out a user
- logout_then_login : Logs out a user and redirects him to the log-in page

Django provides the following views to handle password changes:
- password_change : Handles a form to change user password
- password_change_done : The success page shown to the user after
changing his password

Django also includes the following views to allow users to reset their password:
- password_reset : Allows the user to reset his password. It generates a
one-time use link with a token and sends it to the user's e-mail account.
- password_reset_done : Shows the user that the e-mail to reset his
password has been sent to his e-mail account.
- password_reset_confirm : Lets the user set a new password.
- password_reset_complete : The success page shown to the user after he
resets their password.