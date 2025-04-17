# password.py
"""
Password utility functions for hashing and verifying user passwords.

This module uses Passlib with bcrypt to securely hash plain-text passwords
and verify them during authentication. Helps ensure that sensitive data
like passwords are never stored in plain text.

Functions:
- hash_password: Hashes a plain-text password.
- verify_password: Verifies a plain-text password against a hashed one.
"""

# Passlib is a powerful password hashing library for Python.
# CryptContext is a utility provided by Passlib to manage password hashing schemes, 
# allowing to abstract hashing/verification logic in a clean way.
from passlib.context import CryptContext

# Create a password hashing context with bcrypt algorithm 
# schemes=["bcrypt"] -> tells passlib to use bcrypt for all password hashing.
# deprecated="auto" -> ensures that if you switch algorithms later,
# Passlib can automatically mark old ones as deprecated and help migrate hashes.
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# Function that takes a plain-text password as input and returns a hashed version.
def get_hash_password(password: str) -> str:
    """ Hashes a plain text password. """
    return pwd_context.hash(password) # Uses the pwd_context to hash the input password

# Function that checks if a plain-text password matches a preiously hashed password.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against its hash.
    Parameters:
        -Plain_password: str -> the user input(e.g., from a login form).
        -hashed_password: str -> the hashed version stored in a database.
    Return type: bool ->  return True if they match, False otherwise
    """
    # Use the context's verify() method to check if the plain_password corresponds to the hashed_password.
    return pwd_context.verify(plain_password, hashed_password)
