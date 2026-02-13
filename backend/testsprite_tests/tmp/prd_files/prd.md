# ImageProcessing Backend - Product Requirements Document

## Overview
A FastAPI-based backend for an image processing platform. Users can register, authenticate, upload images to S3-compatible storage (MinIO), request async image transformations via Kafka, and manage their images through a REST API.

## Functional Requirements

### FR-1: User Registration
- Users register with username, email, and password
- Password is hashed with bcrypt before storage
- Returns a JWT access token upon successful registration
- Rejects duplicate usernames with 400 error

### FR-2: User Login
- Users authenticate with username and password
- Supports "remember me" functionality affecting cookie expiry
- Returns JWT token in response body AND sets httponly cookie
- Updates user's last_login timestamp
- Returns 401 for invalid credentials

### FR-3: User Logout
- Deletes the access_token cookie
- Returns confirmation message

### FR-4: Get Current User
- Authenticated endpoint requiring valid JWT
- Returns user profile: id, username, email, created_at, last_login
- Supports token from Authorization header or cookie

### FR-5: Image Upload
- Authenticated users can upload image files
- Images stored in S3/MinIO with unique UUID-based keys
- Creates ImageTask record in database with status "success"
- Returns image ID and URL

### FR-6: Request Image Transformation
- Authenticated users can request transformations on their images
- Sends transformation task to Kafka for async processing
- Returns confirmation message
- Returns 404 if image doesn't exist or doesn't belong to user

### FR-7: Get Image
- Authenticated users can retrieve image details by ID
- Returns image ID and URL
- Returns 404 if image doesn't exist or doesn't belong to user

### FR-8: Delete Image
- Authenticated users can delete their images
- Removes from S3 storage and database
- Returns 404 if image doesn't exist or doesn't belong to user

## Non-Functional Requirements

### NFR-1: Authentication
- JWT-based with configurable expiry (default 30min)
- HS256 algorithm
- Token accepted via Authorization header or httponly cookie

### NFR-2: Authorization
- Users can only access/modify their own images
- All image endpoints require authentication

### NFR-3: Data Persistence
- PostgreSQL database with SQLAlchemy ORM
- Cascade deletes for related records

## Tech Stack
- Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL
- JWT auth (python-jose), bcrypt (passlib)
- MinIO/S3 (boto3), Apache Kafka (confluent-kafka)
- Pydantic v2 for validation
